#!/bin/bash
cd /home/pi/python
/usr/bin/python3.10 info_screen.py &
/usr/bin/perl autosleep.pl &
DISPLAY=:0 xhost +SI:localuser:root
DISPLAY=:0 xhost +SI:localuser:motion
