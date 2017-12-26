# mws_autoSetHost
基于ping.chinaz.com的自动改host脚本，不输入参数的情况下默认改steam社区的host。需要以管理员权限运行。

从ping.chinaz.com获取ip后通过ping得到访问速度最快的ip，如果host文件已经包含该域名会自动修改该项，否则直接在host文件最后加上。

修改steam社区host：

python mws_autoSetHost.py

ps:需要给steam的快捷方式设置 -community="https://steamcommunity.com" 才能够直接在客户端里访问社区。

修改xxxx的host:

python mws_autoSetHost.py xxxxxx
