@echo off
set arg1=%1
set arg2=%2
set arg3=%3
set arg4=%4
set drivers=number of drivers in the championship:
set suppliers=number of engine suppliers:
set images=number of images:
set sizes=size of all images:
echo %drivers% %1% > stat.txt
echo %suppliers% %2% >> stat.txt
echo %images% %3% >> stat.txt
echo %sizes% %4% >> stat.txt