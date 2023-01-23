from getpass import getpass
import ftplib
import os
import threading
import time

counter1 = 0
counter2 = 0

def clientRequestProcesor(ftp, ftpUname):
    while True:
        serverFiles = []
        serverFiles = ftp.nlst()
        toSearchFilename1 = "Todo_" + ftpUname
        toSearchFilename2 = "Rest_" + ftpUname
        for name in serverFiles:
            searchResult = name[0:6]
            if( searchResult == toSearchFilename1):
                retcode = ftp.retrbinary("RETR " + name, open(name + "_client", 'wb').write)

                file1 = open(name+"_client", 'r')
                allLines = file1.readlines()
                
                receiver = int(allLines[0])
                sender = int(allLines[1])
                operation = int(allLines[2])
                operator1 = int(allLines[3])
                operator2 = int(allLines[4])
                
                os.remove(name + "_client")
                
                result = 0
                resultMessage = ""
                op = ""
                if(operation==1):
                    result = operator1 + operator2
                    op = "+"
                elif(operation==2):
                    result = operator1 - operator2
                    op = "-"
                else:
                    result = operator1 * operator2
                    op = "*"

                resultMessage = "Message from "+ftpUname+":\n" + str(operator1) + op + str(operator2) + "=" + str(result)
                resultMessage = str(sender) + "\n" + str(receiver) + "\n" + resultMessage
                resultFilename = "Rest_"+str(sender)+"_"+str(receiver)+"_"+str(counter2)
                # global counter2
                # counter2 = counter2 + 1

                f = open(resultFilename, "w")
                f.write(resultMessage)
                f.close()

                fp = open(resultFilename, 'rb')
                serverFileName = resultFilename + "_server"
                ftp.storbinary('STOR %s' % os.path.basename(serverFileName), fp, 1024)
                ftp.delete(name)
                fp.close()
                os.remove(resultFilename)
            elif( searchResult == toSearchFilename2 ):
                ftp.retrbinary("RETR " + name, open(name + "_client", 'wb').write)
                
                file1 = open(name+"_client", 'r')
                allLines = file1.readlines()
                finalMessage = "\n" + allLines[2] + allLines[3]
                print(finalMessage)
                os.remove(name+"_client")
                ftp.delete(name)
        
        time.sleep(1)


if __name__ =="__main__":
    ftpHost = input("Enter ftp host: ")
    ftpPort = int(input("Enter port: "))
    ftpUname = input("Enter the username: ")
    ftpPass = getpass()

    ftp = ftplib.FTP(timeout=30)
    ftp.connect(ftpHost, ftpPort)

    try:
        ftp.login(ftpUname, ftpPass)
    except:
        print("Invalid credentials!")
        exit()

    print("\nConnected....")

    t1 = threading.Thread(target=clientRequestProcesor, args=(ftp,ftpUname))
    t1.start()
    
    while True:
        choice = int(input("\nSelect from following:\n1.Send messages \n2.Quit\n"))
        if(choice==2):
            break
        receiverClient = (input("Receiver client#: "))
        operation = int(input("Choose operation:\n1. Addition\n2. Subtract\n3. Multiply\n"))
        if( operation < 1 and operation >= 4 ):
            print("Invalid input. Try again!\n")
            continue
        operator1 = (input("First number: "))
        operator2 = (input("Second number: "))
        
        message = receiverClient + "\n" + ftpUname + "\n" + str(operation) + "\n" + operator1 + "\n" + operator2
        filename = "Todo_" + receiverClient + "_" + ftpUname + "_" + str(counter1)
        f = open(filename, "w")
        f.write(message)
        # global counter1 
        # counter1 = counter1+1
        f.close()

        fp = open(filename, 'rb')
        serverFileName = filename + "_server"

        ftp.storbinary('STOR %s' % os.path.basename(serverFileName), fp, 1024)
        fp.close()
        os.remove(filename)

print("Bye!")
ftp.quit()

