#!/usr/bin/env bash
sqlacodegen --noviews --noconstraints --outfile=models.py mysql+mysqlconnector://root:root@192.168.1.200:3306/yiguo?charset=utf8
