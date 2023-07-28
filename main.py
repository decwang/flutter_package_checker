#!/bin/env python

import os
import sys

import requests
import yaml
from lxml import html
from lxml import etree


def read_node_text(node, attrib, key):
    if node.attrib.get(attrib) == key:
        return node.text
    return None
#endfunc
def read_node_attrib_text(node, key):
    return node.attrib.get(key)
#endfunc
def is_node(node,attrib, key):
    if node.attrib.get(attrib) == key:
        return node
    return None
#endfunc
def convert_english_date(date):
    list = date.split(' ')
    month = convert_englist_month_to_int(list[0])
    day = fix_day(list[1])
    year = list[2]
    return year + "-" + month + "-" + day
#endfunc
def fix_day(day):
    str = day.replace(',', '')
    if len(str) < 2:
        str = "0" + str
    return str
#endfunc
def convert_englist_month_to_int(month):
    # 一月January ，二月february ，三月March ，四月April ，五月May ，六月June ，七月July ，八月August ，九月September ，十月October ，十一月November ，十二月December。
    if month == "Jan":
        return "01"
    if month == "Feb":
        return "02"
    if month == "Mar":
        return "03"
    if month == "Apr":
        return "04"
    if month == "May":
        return "05"
    if month == "Jun":
        return "06"
    if month == "Jul":
        return "07"
    if month == "Aug":
        return "08"
    if month == "Sep":
        return "09"
    if month == "Oct":
        return "10"
    if month == "Nov":
        return "11"
    if month == "Dec":
        return "12"
    return "--"
#endfunc
def get_version_list(package, currVersion, ignore_old):
    page = requests.get('https://pub.flutter-io.cn/packages/' + package + "/versions")
    tree = html.fromstring(page.content)
    #version_info = tree.xpath('/html/body/main/div/div[@class="detail-body"]/div[@class="detail-tabs"]/div[@clas="detail-container detail-body-main"]')
    #/div[@class="detail-tabs-content"]')
    #/section/table/tbody')
    all_tr = tree.xpath('/html/body/main/div[1]/div[3]/div/div[2]/div/section/table/tbody/tr')
    has_version = False
    for tr in all_tr:
        version = tr.attrib['data-version']
        version_info = "[package_version:" + version + "]"
        has_version = True
        for td in tr:
            # print(td)
            if is_node(td, "class", "sdk") is not None:
                sdk_version = read_node_text(td, "class", "sdk")
                if sdk_version is not None:
                    version_info = version_info + "[min_dart_sdk:" + td.text + "]"
                    continue
                #endif
            #endif
            if is_node(td, "class", "uploaded") is not None:
                for a in td:
                    upload_date = read_node_attrib_text(a, "title")
                    version_info = version_info + "[pub_date:" + convert_english_date(upload_date) + "]"                    
                    break
                continue
            #endif
        if version == currVersion:
            print_red(version_info)
            if ignore_old:
                break
        else:
            print(version_info)
    return has_version
#endfunc

def get_file_name():
    if len(sys.argv) > 1:
        return sys.argv[1]
    else:
        return os.getcwd() + "/pubspec.yaml"


def get_packages(file_name):
    try:
        yaml_dict = yaml.load(open(file_name), Loader=yaml.FullLoader)
        return yaml_dict['dependencies']
    except (OSError, KeyError) as e:
        print_red(file_name + " is not a pubspec.yaml file.")
        sys.exit(1)


def print_green(text):
    print('\033[94m' + text + '\033[0m')


def print_red(text):
    print('\033[91m' + text + '\033[0m')

def main():
    packages = get_packages(get_file_name())
    packages.pop('flutter')
    packages.pop('flutter_localizations')
    ignore_old = True
    no_data_package_list = []
    other_source_package_list = []
    for package, version in packages.items():
        if isinstance(version, str): 
            print_green(package + " check--"+ version + "---begin")
            version = version.replace('^', '')
            flag = False
            for i in range(3):
                flag = get_version_list(package,version, ignore_old)
                if flag:
                    break
            #endfor
            if not flag:
                no_data_package_list.append(package)
            print_green(package + " check--"+ version + "---end")                
            # break
        else:
            other_source_package_list.append(package)
    #endfor
    list_len = len(no_data_package_list)
    if list_len > 0:
        print_red("no version package has " + str(list_len))
        print_red(no_data_package_list)
    list_len = len(other_source_package_list)
    if list_len > 0:
        print_red("other source package has " + str(list_len))
        print_red(other_source_package_list)
#endfunc            
main()
