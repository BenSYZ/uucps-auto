#!/bin/bash

module_info=$(pactl list modules|grep VTS)

if [ -n "$module_info" ];then
	pactl unload-module sink_name=VTS2
	pactl unload-module sink_name=VTS1_mute
fi
