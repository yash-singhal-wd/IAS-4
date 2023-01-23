import ftplib
import os

ftpHost = input("Enter ftp host: ")
ftpPort = int(input("Enter port: "))
ftpUname = input("Enter the username: ")
ftpPass = input("Enter the password: ")

ftp = ftplib.FTP(timeout=30)
ftp.connect(ftpHost, ftpPort)

try:
    ftp.login(ftpUname, ftpPass)
except:
    print("Invalid credentials!")
    exit()

print("Connected...")

hostMessage = {"1":"", "2": "" , "3": "" , "4": "" , "5": ""}

while(True):    
    command = input("")
    tokens = command.split(" ")
    username = tokens[0]
    
    if(command=="WHO AM I?"):
        print(ftpUname)

    elif(username=="1" or username=="2" or username=="3" or username=="4" or username=="5"):
        message = ""
        for i in range(1, len(tokens)):
            message = message + " " + tokens[i]
        
        message = message + "\n"
        f = open("temp" + username + ".txt", "a")
        f.write(message)
        f.close()

        fp = open("temp" + username + ".txt", 'rb')
        generalName = "messageFile" + username + ".txt"

        ftp.storbinary('STOR %s' % os.path.basename(generalName), fp, 1024)
        fp.close()

    elif(command=="pull"):
        fileName = "messageFile" + ftpUname + ".txt"
        downloadedFile = "downloaded"+ ftpUname + ".txt"
        retcode = ftp.retrbinary("RETR " + fileName, open(downloadedFile, 'wb').write)
        f = open(downloadedFile, 'r')
        content = f.read()
        print(content)
        print()
        f.close()
        f = open(fileName, "w")
        f.close()
    
    else:
        ftp.quit()
        print("See you soon.")
    




    