import pyttsx3
import SpeechRecognition as sr
import datetime
import wikipedia
import smtplib
import webbrowser as wb
import os
import mysql.connector as con
import pyautogui
import pyjokes

new=pyttsx3.init()
mydb=con.connect(
    host="localhost",
    user="root",
    passwd="<Your password>",
    database="<Database name>" #here the name is rem_data
)
cur=mydb.cursor()
sql1="insert into rem_data(data) values(%s)"
cur.execute("create table if not exists rem_data(item_no int not null auto_increment,data varchar(255) not null, primary key(item_no))")

def speak(audio):
    new.say(audio)
    new.runAndWait()

def time():
    time=datetime.datetime.now().time()
    speak("The current time is:")
    speak(time)

def date():
    year=int(datetime.datetime.now().year)
    month=int(datetime.datetime.now().month)
    day=int(datetime.datetime.now().day)
    speak("The current date is:")
    speak(day)
    speak(month)
    speak(year)

def wish():
    hour=datetime.datetime.now().hour
    if hour>=6 and hour<12:
        speak("Good Morning")
    elif hour>=12 and hour<4:
        speak("Good Afternoon")
    elif hour>=4 and hour<9:
        speak("Good Evening")
    else:
        speak("Good Night")
    speak("Welcome Back!")
    speak("I am at your service. How can i help you?")

def takeCommand():
    r=sr.Recognizer()
    with sr.Microphone as source:
        print("Listening...")
        r.pause_threshold=1
        audio=r.listen(source)

    try:
        print("Recognizing...")
        query=r.recognize_google(audio, language="en-in")
        print(query)

    except Exception as e:
        print(e)
        speak("Can you please repeat?")

    return query

def sendEmail(to, content):
    server=smtplib.SMTP('smtp.gmail.com', port=5874,)
    server.ehlo()
    server.starttls()
    server.login("*Your email id*",'Password')
    server.sendmail('your email id', to,content)
    server.close()

def takess():
    img=pyautogui.screenshot()
    img.save("*path of the file where you want to save the file*")

def joke():
    speak(pyjokes.get_joke())

if __name__ == "__main__":
    wish()
    while True:
        query=takeCommand().lower()

        if "time" in query:
            time()
        elif "date" in query:
            date()
        elif "Wikipedia" or "wiki" in query:
            speak("Searching...")
            query=query.replace("wikipedia","")
            result=wikipedia.summary(query, sentences=2)
            print(result)
            speak(result)
        elif "send email" or "send mail" in query:
            try:
                speak("What should the email say?")
                content= takeCommand()
                to="*reciever's mail id*"
                sendEmail(to,content)
                speak("Email sent sucessfully!")

            except Exception as e:
                print(e)
                speak("Unable to send email")
        elif "search on google" or "search online" in query:
            speak("What should I search?")
            chromepath='C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s'
            search=takeCommand().lower()
            wb.get(chromepath).open_new_tab(search+'.com')
        elif "logout" in query:
            os.system("shutdown -l")
        elif "shutdown" in query:
            os.system("shutdown /s /t 1")
        elif "restart" in query:
            os.system("shutdown /r /t 1 ")
        elif "play songs" in query:
            songs_dir="*songs folder location*"
            songs=os.listdir(songs_dir)
            os.startfile(os.path.join(songs_dir, songs[0] ))
        elif "remember that" in query:
            speak("What should I remember? ")
            data=takeCommand()
            cur.execute(sql1, data)
        elif "you to remember" in query:
            speak("select * from rem_data")
        elif "screenshot" in query:
            takess()
            speak("Screenshot taken!")
        elif "joke" in query:
            joke()
        elif "bye" or "offline" in query:
            quit()

