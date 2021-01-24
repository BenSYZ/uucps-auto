# [大学生网络党校](http://www.uucps.edu.cn/)助手
网络课程不能快进，于是使用`selenium`自动录屏，以便学习。

## Requirement
* python packages
	+ `selenium`
	+ `argparse`
	+ `time`
	+ `os`
	+ `re`
	+ `pyvirtualdisplay`(optional 录屏虚拟桌面)

* `pactl` in `libpulse` 设置虚拟声卡
* `chromedriver` in `chromium`
* 录屏软件 `simplescreenrecorder`(optional)


## 使用方法:

```
usage: uucps-auto-recording.py [-h] [-o SAVE_RECORDING_PATH] [-v VIRTUAL_DISPLAY_WINDOW_SIZE] [-c SSR_CONFIG]

大学生网络党校课程自动录屏

optional arguments:
  -h, --help            show this help message and exit
  -o SAVE_RECORDING_PATH, --save-recording-path SAVE_RECORDING_PATH
                        录屏，录屏文件夹位置,缺省则在不录屏，后台运行，静音
  -v VIRTUAL_DISPLAY_WINDOW_SIZE, --virtual-display-window-size VIRTUAL_DISPLAY_WINDOW_SIZE
                        若要录屏，虚拟桌面尺寸<WIDTH>x<HEIGHT>，默认1024x768
  -c SSR_CONFIG, --ssr-config SSR_CONFIG
                        simplescreenrecorder 配置模板文件，缺省默认~/.ssr/settings.conf
```

* `./login.conf`中修改 `<username>` 和 `<password>` 内容，不要有多余的空行，密码结尾不能是空格。

* 静音是用`pactl load-module module-virtual-sink sink_name=VTS2`模拟，如果`ssr` 没有录到声音，手动修改一下`./uucps-auto-recording.py` 中的`line='audio_pulseaudio_source=VTS2.monitor'+'\n'`那行。

## 模式
* 后台运行，不录屏(chrome option`--headless`)
* 后台运行录屏(`pyvirtualdisplay`包)

## Tips
* 如果运行错误，`pyvirtualdisplay` 未能正确关闭: `killall Xvfb`
* `./remove_virtual_sink.sh` 清除由`./audio.sh`建立的virtual sink。

