# ProgramMonitor
## 背景
有些需要长期运行的程序，由于程序自身的有瘾，运行一段时间之后就异常退出了，需要有一个监视程序可以定期检查该程序是否还在正常运行，如果退出了就马上重新启动

## 用法
在使用之前要先配置好配置文件 ProgramMonitor.ini
按照如下的配置文件格式，先配置好轮询间隔，以及要监视的程序的名称和路径，然后启动程序即可

在程序启动之后再修改配置文件无效
```
[main]
# 要检查几个进程，因为此处指定了2个，所有后续要配置两个 program的 section
count=2
# 轮训间隔，单位秒，如果不配置，默认轮训间隔是60s
interval = 60

[program-1]
#进程名称
name=wiz.exe
#该程序所在的路径，最后可以带上斜杠 \， 也可以不带
path=C:\Program Files (x86)\WizNote\

[program-2]
#进程名称，后缀名可以省略，程序会自动加上
name=notepad
#如果该程序是系统程序，或者和当前脚本位于同一个目录下，则以下路径可以省略
#path=C:\Program Files (x86)\WizNote
```

