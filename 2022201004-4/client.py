import ftplib
import os
import time
import sys
from getpass import getpass

n = len(sys.argv)
if(n<=1):
        print("Exiting! No server name.")
        exit()

ftpHost = "127.0.0.1"
ftpPort = 8080
ftpUname = sys.argv[1]
ftpPass = getpass("Enter password for " + ftpUname + ": ")

ftp = ftplib.FTP(timeout=30)
ftp.connect(ftpHost, ftpPort)
ftp.login(ftpUname, ftpPass)
print("\nLogin successful!")

counter = 0

while True:
    operation = int(input("\nSelect from options below:\n1. Addition\n2. Subtraction\n3. Multipication\n4. Increment\n5. Lookup\n"))

    if(operation==5):
        time.sleep(2)
        ftp.retrbinary("RETR " + "Ports_info", open("ports_info_client", 'wb').write)
        infoFile = open("ports_info_client", "r")
        infoArray = infoFile.readlines()
        for message in infoArray:
            print(message)
        os.remove("ports_info_client")
        continue
    
    uploadFilename = str(operation) + "_" + str(ftpUname) + "_" + str(counter)
    counter = counter + 1

    f = open(uploadFilename, "w")
    f.write("")
    f.close()

    fp = open(uploadFilename, 'rb')
    serverFileName = "server_" + uploadFilename
    if(ftp.pwd()!="/"):
        ftp.cwd("../")
        # print(ftp.pwd())
    ftp.storbinary('STOR %s' % os.path.basename(serverFileName), fp, 1024)

    fp.close()
    os.remove(uploadFilename)

    time.sleep(3)
    
    if(ftp.pwd()!="/response"):
        ftp.cwd("response")
    serverFiles = ftp.nlst()
    host = ""
    port = ""
    flag = 0

    serverFilenameToSearch = str(ftpUname) + "_" + str(operation)
    for eachFile in serverFiles:
        fileSearchResult = eachFile[0:5]
        if(fileSearchResult == serverFilenameToSearch):
            ftp.retrbinary("RETR " + eachFile, open(fileSearchResult + "_client", 'wb').write)
            
            f = open(fileSearchResult + "_client", "r")
            responseArray = f.readlines()
            f.close()

            os.remove(fileSearchResult+"_client")
            ftp.delete(eachFile)

            if(responseArray[0].split()[0]=="NO"):
                print("The server is offline. Choose again!")
                flag=1
            else:
                host = responseArray[0].split()[0]
                port = int(responseArray[0].split()[1])
    if(flag==1):
        continue
    print("\nConnecting to " + host + ":" + str(port))
    try:
        ftp = ftplib.FTP(timeout=30)
        ftp.connect(host, port)
        ftp.login(ftpUname, ftpPass)
    except:
        print("Some error connecting to the operation server. Try Again!")
        continue
    print("Connection to remote server successful!\n\n")
    
    
    operator1 = 0
    operator2 = 0
    if(operation==1 or operation==2 or operation==3):
        operator1 = int(input("First number: "))
        operator2 = int(input("Second number: "))
    else:
        operator1 = int(input("Input number: "))

    
    if(operation==1):
        ftp.cwd("add")
        message = str(operator1) + " " + str(operator2)
        filenameToUpload = ftpUname + "_" + str(counter) + "_client"
        counter = counter+1
        addFile = open(filenameToUpload, "w")
        addFile.write(message)
        addFile.close()

        addFile = open(filenameToUpload, 'rb')
        ftp.storbinary('STOR %s' % os.path.basename(filenameToUpload), addFile, 1024)
        addFile.close()
        os.remove(filenameToUpload)
        time.sleep(3)

        ftp.cwd("../response")
        fileStartName = "res_"+str(ftpUname)
        resArray = []
        filesArray = ftp.nlst()
        for eachfile in filesArray:
            if(eachfile[0:7]==fileStartName):
                ftp.retrbinary("RETR " + eachfile, open(ftpUname + "_client", 'wb').write)
                fTemp = open(ftpUname + "_client", "r")
                resultMessage = fTemp.readlines()
                ftp.delete(eachfile)
                os.remove(ftpUname + "_client")
                toPrintMessage = "Addition server says: " + resultMessage[0]
                resArray.append(toPrintMessage)
        for message in resArray:
            print(message)
        ftp.quit()
        ftp = ftplib.FTP(timeout=30)
        ftp.connect(ftpHost, ftpPort)
        ftp.login(ftpUname, ftpPass)

    if(operation==2):
        ftp.cwd("sub")
        message = str(operator1) + " " + str(operator2)
        filenameToUpload = ftpUname + "_" + str(counter) + "_client"
        counter = counter+1
        addFile = open(filenameToUpload, "w")
        addFile.write(message)
        addFile.close()

        addFile = open(filenameToUpload, 'rb')
        ftp.storbinary('STOR %s' % os.path.basename(filenameToUpload), addFile, 1024)
        addFile.close()
        os.remove(filenameToUpload)
        time.sleep(3)

        ftp.cwd("../response")
        fileStartName = "res_"+str(ftpUname)
        resArray = []
        filesArray = ftp.nlst()
        for eachfile in filesArray:
            # print(eachfile[0:7])
            if(eachfile[0:7]==fileStartName):
                ftp.retrbinary("RETR " + eachfile, open(ftpUname + "_client", 'wb').write)
                fTemp = open(ftpUname + "_client", "r")
                resultMessage = fTemp.readlines()
                ftp.delete(eachfile)
                os.remove(ftpUname + "_client")
                toPrintMessage = "Subtraction server says: " + resultMessage[0]
                resArray.append(toPrintMessage)
        for message in resArray:
            print(message)
        ftp.quit()
        ftp = ftplib.FTP(timeout=30)
        ftp.connect(ftpHost, ftpPort)
        ftp.login(ftpUname, ftpPass)

    if(operation==3):
        ftp.cwd("mul")
        message = str(operator1) + " " + str(operator2)
        filenameToUpload = ftpUname + "_" + str(counter) + "_client"
        counter = counter+1
        addFile = open(filenameToUpload, "w")
        addFile.write(message)
        addFile.close()

        addFile = open(filenameToUpload, 'rb')
        ftp.storbinary('STOR %s' % os.path.basename(filenameToUpload), addFile, 1024)
        addFile.close()
        os.remove(filenameToUpload)
        time.sleep(3)

        ftp.cwd("../response")
        fileStartName = "res_"+str(ftpUname)
        resArray = []
        filesArray = ftp.nlst()
        for eachfile in filesArray:
            print(eachfile[0:7])
            if(eachfile[0:7]==fileStartName):
                ftp.retrbinary("RETR " + eachfile, open(ftpUname + "_client", 'wb').write)
                fTemp = open(ftpUname + "_client", "r")
                resultMessage = fTemp.readlines()
                ftp.delete(eachfile)
                os.remove(ftpUname + "_client")
                toPrintMessage = "Multiplication server says: " + resultMessage[0]
                resArray.append(toPrintMessage)
        for message in resArray:
            print(message)
        ftp.quit()
        ftp = ftplib.FTP(timeout=30)
        ftp.connect(ftpHost, ftpPort)
        ftp.login(ftpUname, ftpPass)

    if(operation==4):
        ftp.cwd("inc")
        message = str(operator1) + " " + str(operator2)
        filenameToUpload = ftpUname + "_" + str(counter) + "_client"
        counter = counter+1
        addFile = open(filenameToUpload, "w")
        addFile.write(message)
        addFile.close()

        addFile = open(filenameToUpload, 'rb')
        ftp.storbinary('STOR %s' % os.path.basename(filenameToUpload), addFile, 1024)
        addFile.close()
        os.remove(filenameToUpload)
        time.sleep(3)

        ftp.cwd("../response")
        fileStartName = "res_"+str(ftpUname)
        resArray = []
        filesArray = ftp.nlst()
        for eachfile in filesArray:
            print(eachfile[0:7])
            if(eachfile[0:7]==fileStartName):
                ftp.retrbinary("RETR " + eachfile, open(ftpUname + "_client", 'wb').write)
                fTemp = open(ftpUname + "_client", "r")
                resultMessage = fTemp.readlines()
                ftp.delete(eachfile)
                os.remove(ftpUname + "_client")
                toPrintMessage = "Increment server says: " + resultMessage[0]
                resArray.append(toPrintMessage)
        for message in resArray:
            print(message)
        ftp.quit()
        ftp = ftplib.FTP(timeout=30)
        ftp.connect(ftpHost, ftpPort)
        ftp.login(ftpUname, ftpPass)

    if(operation==5):
        ftp.cwd("inc")
        message = str(operator1) + " " + str(operator2)
        filenameToUpload = ftpUname + "_" + str(counter) + "_client"
        counter = counter+1
        addFile = open(filenameToUpload, "w")
        addFile.write(message)
        addFile.close()

        addFile = open(filenameToUpload, 'rb')
        ftp.storbinary('STOR %s' % os.path.basename(filenameToUpload), addFile, 1024)
        addFile.close()
        os.remove(filenameToUpload)
        time.sleep(3)

        ftp.cwd("../response")
        fileStartName = "res_"+str(ftpUname)
        resArray = []
        filesArray = ftp.nlst()
        for eachfile in filesArray:
            print(eachfile[0:7])
            if(eachfile[0:7]==fileStartName):
                ftp.retrbinary("RETR " + eachfile, open(ftpUname + "_client", 'wb').write)
                fTemp = open(ftpUname + "_client", "r")
                resultMessage = fTemp.readlines()
                ftp.delete(eachfile)
                os.remove(ftpUname + "_client")
                toPrintMessage = "Increment server says: " + resultMessage[0]
                resArray.append(toPrintMessage)
        for message in resArray:
            print(message)
        ftp.quit()
        ftp = ftplib.FTP(timeout=30)
        ftp.connect(ftpHost, ftpPort)
        ftp.login(ftpUname, ftpPass)
# t_end = time.time() + 60 * 15
# while time.time() < t_end: