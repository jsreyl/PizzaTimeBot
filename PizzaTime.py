import sys #For getting command line arguments
import subprocess # For running bash commands
import requests # For posting requests to telegram
import datetime # For measuring performance

#GLOBAL
TOKEN = "1372388727:AAFHvMlZcpY4_9FsrXcjtc-aA9YXdCPXdgY" #Bot Token
MASTER_ID = "1375865756" # Juan Rey's Telegram personal ID
# MASTER_ID= "881381200"

def get_usr_info()->str:
    url=f"https://api.telegram.org/bot{TOKEN}/getUpdates"
    dict_=requests.post(url).json()
    # print(dict_)
    #Get the latest result from user input
    chat_id=dict_['result'][len(dict_['result'])-1]['message']['from']['id']
    print(chat_id)
    return chat_id

def send_message(msg:str="Pizza Time!", chat_id:str=MASTER_ID):
    #https://api.telegram.org/bot$token/sendMessage?chat_id=$chat&text=Pizza+Time
    send_url=f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    data={'chat_id':chat_id,'text':msg}
    dict_=requests.post(send_url,data).json()
    # print(dict_)

def send_image(img_path:str,chat_id:str=MASTER_ID):
    send_url=f"https://api.telegram.org/bot{TOKEN}/sendPhoto"
    data={'chat_id':chat_id}
    files={'photo':open(img_path,'rb')}
    requests.post(send_url,files=files,data=data)

def run(command:str):
    p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,  text=True)
    stdout = []
    while True:
        line = p.stdout.readline()
        stdout.append(line)
        print(line)
        if line == '' and p.poll() != None:
            break
    return ''.join(stdout)


if __name__ == "__main__":
    #chat_id=get_usr_info();
    try:
        if len(sys.argv)>1:
            command=sys.argv[1]
            start=datetime.datetime.now()
            start_string=start.strftime("%d")+'-'+start.strftime("%m")+'-'+start.strftime("%Y")+' '+start.strftime("%I")+':'+start.strftime("%M")+':'+start.strftime("%S")
            print(f"Starting process {command} at {start_string}")
            send_message(msg=f"Starting process {command} at {start_string}")
            # result_text=run(command)
            # send_message(msg=result_text)
            result=subprocess.run(command, shell=True, capture_output=True, text=True)
            finish=datetime.datetime.now()
            finish_string=finish.strftime("%d")+'-'+finish.strftime("%m")+'-'+finish.strftime("%Y")+' '+finish.strftime("%I")+':'+finish.strftime("%M")+':'+finish.strftime("%S")
            delta=finish-start
            if result.stdout !='':
                text=f"Pizza Time! Running {command} finished at {finish_string} (that's delta={delta.total_seconds()}s)!\n"
                text2=f"You know I'm something of a scientist myself\n"
                print(text+result.stdout+text2)
                send_message(msg=text+result.stdout+text2)
                send_image(sys.path[0]+"/images/toby_scientist.png")
            if result.stderr != '':
                text=f"Uh oh, error generated running {command}, exited at {finish_string} (that's delta={delta.total_seconds()}s)\n"
                text2=f"You'll get your rent when you fix this damn code\n"
                print(text+result.stderr)
                send_message(msg=text+result.stderr+text2)
                send_image(sys.path[0]+"/images/toby_cry.jpg")
    except Exception as e:
        send_message(msg="Uh oh, that's a bad pizza. Error running my python script.")
        send_image(sys.path[0]+"/images/toby_scream.jpg")
        pass
