import web
from subprocess import Popen
import os
import getpass 
import sqlite3
import random
import hashlib
import xmlrpclib
import sys
from string import Template


urls = (
    '/','index',
    #'/(.*)', 'index'
    '/hauth','hauth'
)

app = web.application(urls, globals())



#harcmd_list=["\"c:\Program Files (x86)\CA\SCM\husrmgr.exe\"","-b cscr501",
#             "-eh .\common\harvest.eh","-cpw -ow"]

harcmd_list=["husrmgr.exe","-b cscr501",
             "-eh .\common\harvest.eh","-cpw -ow"]

tmpcmd=' '
valid_user=getpass.getuser()

not_allowed="ohh No, You can\'t change other\'s harvest password"
har_username_not_found="ohh No, Your harvest account doesn't exist"
succeed="Succeed to change your harvest password!"
fail="Oh God!Fail to change your harvest password!"
op_fail="Oh God!Fail to uppdate the flag of forcechange!Please remember the temp password to login!"

db_name="arc_har_user.db"
file_root=os.getcwd()

mail_eml=".\common\hpwd_change.eml"
mail_bodyroot=".\common\har_mail_body"
send_mailpy=".\sendmail.py"


def send_mail_har_usr(user, tmp_pwd,a_user):
    mail_tpl = mail_eml
    replace_tokens = {  'mail_to':a_user+'@arcserve.com',
                        'user':user,
                        'tmp_pwd':tmp_pwd,
                     }
    send_mail(mail_tpl, **replace_tokens)
    

def send_mail(mail_template,**replace_items):
    with open(mail_template,'r') as f:
        tmp_con = Template(f.read())
        msg = tmp_con.safe_substitute(**replace_items)  

    har_mailbody='%s_%s' %(mail_bodyroot,valid_user)
    mail_f = open(har_mailbody,'w')
    mail_f.write(msg)
    mail_f.close()
    sendm_cmd="type %s | python %s" %(har_mailbody,send_mailpy)
    os.system(sendm_cmd)
    os.remove(har_mailbody)




def user_auth(auth_tag):
    salt_key = 'bldwebauth'
    ori_info, hash_info = auth_tag.split('/')
    user, dummy = ori_info.split('-', 1)
    valid_user = user
    hash_result = hashlib.md5(ori_info + salt_key + "\n").hexdigest()
    if hash_result == hash_info:
        valid_user=valid_user
        return  valid_user
    else:
        return "current user=%s" %user  


class hauth:       
    def GET(name):
        return "hello auth!"
    
    def POST(name):
        #return "hello auth post!"  
        iall = web.input()
        if iall.has_key("auth_tag"):
            auth_user=user_auth(iall.auth_tag)
            pwd=random.randint(100000,999999)
            str_pwd=str(pwd)
            
            str_log='%s\log' %file_root
            str_db='%s\common\%s' %(file_root,db_name)            
            conn = sqlite3.connect(str_db)
            cur=conn.cursor()
            cur.execute("select username,realname from arc_har_usres")
            #return cur.fetchall() #to show all of the records in db
            
            for row in cur:                     
                if row[1].lower() == auth_user.lower():
                    #usrname='%s %s' %('-ousr',row[0])
                    opt_file='%s\%s_update.txt' %(str_log,row[0])
                    rule_f = open(opt_file,'w')
                    rule_f.write(row[0])
                    rule_f.write("\t")
                    rule_f.write(str_pwd)
                    rule_f.write("\t\t\t\t\t")
                    rule_f.close()
                    opt_log='-o %s\%s_husrmgr_%s_%s.log' %(str_log,row[0],auth_user,row[1])
                    resetcmd='%s %s %s' %(tmpcmd.join(harcmd_list),opt_file,opt_log)    
                    #resetcmd='%s %s %s' %(tmpcmd.join(harcmd_list),usrname,newpwd)
                    #return resetcmd #for test
                    ret = os.system(resetcmd)
                    if ret == 0:
                        send_mail_har_usr(row[0], str_pwd,row[1])
                        os.remove(opt_file)
                        return succeed
                    else:
                        return fail
            message='%s %s' %(har_username_not_found,auth_user)     
            return message
    
class index:  
    def GET(name):
        render = web.template.render('templates/')
        return render.index()
        #inputall =web.input(name=None,pwd=None)
        #name= inputall.name
       #pwd= inputall.pwd
        #print name ,pwd
        return "hello world get!"
    def POST(name):
        i = web.input()
        if i.has_key("auth_tag"):
            return i.auth_tag      

if __name__ == "__main__":
    app.run()
