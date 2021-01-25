#!/bin/bash

module_info=$(pactl list modules|grep VTS2)
if [ -z "$module_info" ];then
	pactl load-module module-virtual-sink sink_name=VTS2
fi
module_info=$(pactl list modules|grep VTS1_mute)
if [ -z "$module_info" ];then
	pactl load-module module-virtual-sink sink_name=VTS1_mute
fi


sink_input=$(pactl list sink-inputs |grep -E "Input|application.name"|grep Chromium -B 1 |grep -v Chromium |sed -n 's/Sink Input \#\(.*\)/\1/p')
if [ -n "$sink_input" ]; then
	pactl move-sink-input $sink_input VTS2
fi

sink_input_VTS2=$(pactl list sink-inputs |grep -E "Input|VTS2"|grep VTS2 -B 1|grep -v VTS2|sed -n 's/Sink Input \#\(.*\)/\1/p')
pactl move-sink-input $sink_input_VTS2 VTS1_mute
pactl set-sink-mute VTS2 0
pactl set-sink-mute VTS1_mute 1

sources_output=$(pactl list source-outputs |grep -E "Source Output|application.name" |grep SimpleScreenRecorder -B 1 |grep -v SimpleScreenRecorder |sed -n 's/Source Output #\(.*\)/\1/p')

if [ -n "$sources_output" ];then
	pactl move-source-output $sources_output VTS2.monitor
fi
