
[大学生网络党校](http://www.uucps.edu.cn/)网络课程不能快进，于是使用`selenium`自动录屏，以便自己学习。

录屏软件 `simplescreenrecorder`.

使用方法:

```
usage: uucps-auto-recording.py [-h] [-c SSR_CONFIG] [-o SAVE_RECORDING_PATH]

大学生网络党校课程自动录屏

optional arguments:
  -h, --help            show this help message and exit
  -c SSR_CONFIG, --ssr-config SSR_CONFIG
                        simplescreenrecorder 配置模板文件，默认~/.ssr/settings.conf
							真正的配置文件是 ./settings.conf，它是从模板中复制来的，修改了输出文件位置。
  -o SAVE_RECORDING_PATH, --save-recording-path SAVE_RECORDING_PATH
                        若要录屏，录屏文件夹位置
```


* `simplescreenrecorder` 的配置文件得自己配置一下，避免无声或录入环境音。
* `./login.conf`中修改 `<username>` 和 `<password>` 内容，不要有多余的空行，密码结尾不能是空格。
