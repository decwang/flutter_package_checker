# Flutter Package Update Checker

##### Flutter Package Update Checker
用于检查pubspec中声明的版本号是否已经拖后最新版本太多,以及开源代码的编译时升降版本的快速获取.一个个查太难受了.
Easily check if new versions are available for packages you are using on your Flutter project (pubsec.yaml).

![](https://raw.githubusercontent.com/deworks/flutter_package_checker/master/screenshots/screenshot_1.png)

#### Todo
fix no data package get
multithreading
#### Required python packages

1. lxml (pip install lxml)
2. requests (pip install requests)
3. pyyaml (pip install pyyaml)

#### Setup & Usage

1. Clone the project.
2. Install required python packages
3. Run python script main.py from flutter directory or pass pubspec.yaml file full path as argument.
4. Done !
