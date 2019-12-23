#modules
import smtplib
from sys import argv
from time import sleep

#define
def help():
    print('--wordlist_sm [senders mail]') #1
    print('--wordlist_rm [wordlist mail recipient]')
    print('--file_msg [file where the letter is stored]')
    print('--help [call the help menu]')
    quit()

def get_msg(file_msg):
    with open(file_msg,'rt') as file:
        msg = file.read().split('\n')
    if msg[0].split(':')[0] != 'From' or msg[1].split(':')[0] != 'Subject':
        print('The letter is incorrectly composed')
        quit()
    from_msg = msg[0].split(':')[1]
    sub_msg = msg[1].split(':')[1]
    list_text_msg = msg[2::]
    msg_text = ""
    for i in list_text_msg:
        msg_text = msg_text + i + '\n'
    msg = [from_msg,sub_msg,msg_text]
    return msg

def generator(string):
    for word in string:
        mail = word.replace('\n','')
        yield mail

def get_mails_sendner(wordlist):
    with open(wordlist,'rt') as file:
        mails_sendner = file.read().split('\n')
        emails = []
        for i in mails_sendner:
            emails.append(i.split(':'))
        del mails_sendner
        return emails

def type_email(email):
    email_spl = email.split('@')[1]
    if email_spl == 'yandex.ru':
        return 'yandex.ru'
    elif email_spl == 'mail.ru':
        return 'mail.ru'

def check_connect(email_login,password):
    if type_email(email_login) == 'yandex.ru':
        try:
            server = smtplib.SMTP_SSL('smtp.yandex.ru',465)
            server.login(email_login,password)
            return [True, 'yandex.ru']
        except:
            return [False]
    elif type_email(email_login) == 'mail.ru':
        try:
            server = smtplib.SMTP_SSL('smtp.mail.ru',465)
            server.login(email_login,password)
            return [True, 'mail.ru']
        except:
            return [False]

#if-else [argv]
if '--help' in argv or '-h' in argv:
    help()

if '--wordlist_sm' not in argv:
    print('--wordlist_sm specify a list of words with the mails \nto which the letter will be sent')
    quit()

if '--wordlist_rm' not in argv:
    print('--wordlist_rm specify a list of words with mail recipients')
    quit()

#scritp_var
wordlist_sm = argv[argv.index('--wordlist_sm') + 1]
wordlist_rm = argv[argv.index('--wordlist_rm') + 1]
msg_file = argv[argv.index('--file_msg') + 1]


msg_list = get_msg(msg_file)
msg = "From: " + msg_list[0] + "\n" + "Subject: " + msg_list[1] + "\n\n" + msg_list[2]

mails = get_mails_sendner(wordlist_sm)[:-1:]

mails_list = []

mails_yandex = []
mails_mail = []


count_yandex = 0
count_mail = 0

len_check_mail = 0
len_check_yandex = 0
#yandex/mail

for i in mails:
    if type_email(i[0]) == 'yandex.ru':
        mails_yandex.append(i)
    elif type_email(i[0]) == 'mail.ru':
        mails_mail.append(i)

yandex_len = len(mails_yandex)
mail_len = len(mails_mail)

with open(wordlist_rm,'rt',errors='ignore') as dict_mail_rec:
    for mail_rec in generator(dict_mail_rec):
        if len(mails_list) == 5:

            yandex_rec_mail = []
            mail_rec_mail = []

            for mail in mails_list:
                if type_email(mail) == 'yandex.ru':
                    yandex_rec_mail.append(mail)
                elif type_email(mail) == 'mail.ru':
                    mail_rec_mail.append(mail)
            #yandex
            while True:
                if count_yandex == yandex_len:
                    count_yandex = 0
                mail_checked = mails_yandex[count_yandex]
                if check_connect(mail_checked[0],mail_checked[1])[0]:
                    mail_yandex_sendner = mail_checked
                    count_yandex += 1
                    break
                print('checked ' + mail_yandex_sendner)
                if len_check_yandex == 10:
                    sleep(5)
                else:
                    sleep(1)

            #mail
            while True:
                if count_mail == mail_len:
                    count_mail = 0
                mail_checked = mails_mail[count_mail]
                if check_connect(mail_checked[0],mail_checked[1])[0]:
                    mail_mail_sendner = mail_checked
                    count_mail += 1
                    break
            #yandex_send
            if len(yandex_rec_mail) != 0:
                server = smtplib.SMTP_SSL('smtp.yandex.ru',465)
                server.login(mail_yandex_sendner[0],mail_yandex_sendner[1])
                for yandex_mail_rec in yandex_rec_mail:
                    server.sendmail(mail_yandex_sendner[0],yandex_mail_rec,msg)
                    print('send to ' + yandex_mail_rec)

            #mail_send
            if len(mail_rec_mail) != 0:
                server = smtplib.SMTP_SSL('smtp.mail.ru',465)
                server.login(mail_mail_sendner[0],mail_mail_sendner[1])
                for mail_mail_rec in mail_rec_mail:
                    server.sendmail(mail_mail_sendner[0],mail_mail_rec,msg)
                    print('send to ' + mail_mail_rec)
        else:
            mails_list.append(mail_rec)
            



