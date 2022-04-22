import os, datetime, csv, re

log_path = "/var/log/SuppyBot"
if not os.path.exists(log_path):
    os.mkdir(log_path)
if not os.path.exists(log_path+"/sent"):
    os.mkdir(log_path+"/sent")
if not os.path.exists(log_path+"/received"):
    os.mkdir(log_path+"/received")

def logMessagesReceived(contact, messages, isgroup):
    now = datetime.datetime.now()
    date = str(now.day)+"/"+str(now.month)+"/"+str(now.year)[-2:]
    if not os.path.exists(log_path+"/received/"+contact+"_in.log"):
        with open(log_path+"/received/"+contact+"_in.log", 'w+') as new_logfile:
            if isgroup:
                new_logfile.write("name,message,time_received,date\n")
            else:
                new_logfile.write("message,time_received,date\n")
    with open(log_path+"/received/"+contact+"_in.log", 'a') as logfile:
        for message in messages:
            if isgroup:
                logfile.write('"'+contact+'",')
            logfile.write('"'+','.join(message)+'"'+","+date+"\n")

def logMessageSent(contact,message,isgroup):
    now = datetime.datetime.now()
    date = str(now.day)+"/"+str(now.month)+"/"+str(now.year)[-2:]
    time = str(now.hour)+":"+str(now.minute)
    if not os.path.exists(log_path+"/sent/"+contact+"_out.log"):
        with open(log_path+"/sent/"+contact+"_out.log", 'w+') as new_logfile:
            if isgroup:
                new_logfile.write("name,message,time_sent,date\n")
            else:
                new_logfile.write("message,time_sent,date\n")
    with open(log_path+"/sent/"+contact+"_out.log", 'a') as logfile:
        if isinstance(message, str):
            logfile.write('"'+message+'",'+time+","+date+"\n")
        elif isinstance(message, list):
            for line in message:
                logfile.write('"'+line+'",'+time+","+date+"\n")

def removeAlias(phone_number):
    with open("../configs/aliases.csv", "w+") as aliases_file:
        csv_reader = csv.reader(aliases_file, delimiter=",")
        for line in csv_reader:
            if line[-1] == phone_number:
                return line[0]


def setAlias(alias, phone_number):
    if not os.path.exists("../configs/aliases.csv"):
        with open("../configs/aliases.csv", 'w+') as aliases_file:
            aliases_file.write("alias,phone_number\n")
    elif not getAlias(phone_number=phone_number):
        with open("../configs/aliases.csv", "a") as aliases_file:
            aliases_file.write(alias + "," + phone_number + "\n")
    else:
        with open("../configs/aliases.csv", "r+") as aliases_file:
            lines = aliases_file.readlines()
            aliases_file.seek(0)
            for line in lines:
                if re.match(r"^.*,"+phone_number+"\n", line):
                    aliases_file.write(alias.capitalize()+","+phone_number+"\n")
                else:
                    aliases_file.write(line)
            aliases_file.truncate()




def getAlias(phone_number):
    with open("../configs/aliases.csv") as aliases_file:
        csv_reader = csv.reader(aliases_file, delimiter=",")
        for line in csv_reader:
            if line[-1] == phone_number:
                return line[0]
