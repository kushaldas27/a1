#!/bin/bash
userid=$(whoami)
architecture=$(uname -m)
kernel=$(uname -r)
hostname=$(uname -n)
echo "Hello $userid, you are using a $architecture machine running kernel version $kernel on $hostname"
