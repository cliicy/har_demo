1. access http://www.sqliteexpert.com/download.html to download the freeware of SQLite Expert Personal 5.x or SQLite Expert Personal 3  to install to your machine
2. open \\pk-buildrequest\c$\cliicy.har.userpwd\common\arc_har_user.db to add new username and new real name or update the existing username and real name.
3. exit SQLite Expert Personal and the DB will be saved automatically
4.restart apache server.


1. run python to check whether the version of python is above 3. web.py just can work very well on python 2.xxx 
2. cd C:\cliicy.har.userpwd\tools\web.py-0.36
3. python setup.py install
4. cd C:\cliicy.har.userpwd
5. python harpwd_reset.py 8888
6. if some new harvest-users are coming, please remember to add the new ones to common\arc_har_user.db
7. update \templates\index.html to get a new web gui
8. start /b python harpwd_reset.py 8888 >harpwdreset.log

