import atexit
import os
import sys
import threading
import time

from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer
 
namePortDic = {
    "SV0": 8080,
    "SV1": 8081,
    "SV2": 8082,
    "SV3": 8083,
    "SV4": 8084,
}

portList = [8081, 8082, 8083, 8084]
portAssigned = ""
# main function
def main(portAssigned,):
    authorizer = DummyAuthorizer()
    authorizer.add_user('CL1', 'a', '.', perm='elradfmwMT')
    authorizer.add_user('CL2', 'b', '.', perm='elradfmwMT')
    authorizer.add_user('CL3', 'c', '.', perm='elradfmwMT')
    authorizer.add_user('CL4', 'd', '.', perm='elradfmwMT')
    authorizer.add_user('CL5', 'e', '.', perm='elradfmwMT')
    handler = FTPHandler
    handler.authorizer = authorizer
    handler.banner = "The server is ready!"
    address = ('127.0.0.1', portAssigned)
    server = FTPServer(address, handler)
    server.max_cons = 256
    server.max_cons_per_ip = 5
    server.serve_forever()

# helper function
def writeAddressResposne(counter, portNumber, clientName, operation):
    fp = open("./response/"+clientName+"_"+ str(operation) + "_" +counter, "w")
    message = "127.0.0.1 " + portNumber
    fp.write(message)
    fp.close()

def writeOfflineResponse(counter, clientName, operation):
    fp = open("./response/"+clientName+"_"+ str(operation) + "_" + counter, "w")
    message = "NO NO"
    fp.write(message)
    fp.close()

def exit_handler():
    if(portAssigned==8081):
        f = open("Add_online","w")
        f.write("NO")
        f.close()
    if(portAssigned==8082):
        f = open("Sub_online","w")
        f.write("NO")
        f.close()
    if(portAssigned==8083):
        f = open("Mul_online","w")
        f.write("NO")
        f.close()
    if(portAssigned==8084):
        f = open("Inc_online","w")
        f.write("NO")
        f.close()

atexit.register(exit_handler)

if __name__ == "__main__":
    n = len(sys.argv)
    if(n<=1):
        print("Exiting! No server name.")
        exit()
    
    serverName =  sys.argv[1]
    portAssigned = namePortDic[serverName]
    print("Port assigned:", portAssigned)

    #making directories
    dirs = ["add", "sub", "mul", "inc", "response"]
    if(portAssigned==8080):
        for dir in dirs:
            if not os.path.exists(dir):
                os.makedirs(dir)

    #making static port info file
    serverInfoFile = open("Ports_info", "w")
    message = "\n==========================\nServer port information: \n" + "Addition server: "+ str(portList[0]) + "\nSubtraction server: " + str(portList[1]) + "\nMultiplication server: " + str(portList[2]) + "\nIncrement server: " + str(portList[3]) + "\n==========================\n"
    serverInfoFile.write(message)
    serverInfoFile.close()

    #making online status files
    onlineStatusFiles = ["Add_online", "Sub_online", "Mul_online", "Inc_online"]
    if(portAssigned==8080):
        for fileName in onlineStatusFiles:
            f = open(fileName, "w")
            f.write("NO")
            f.close()

    if(portAssigned==8081):
        f = open("Add_online", "w")
        f.write("YES")
        f.close()
    if(portAssigned==8082):
        f = open("Sub_online", "w")
        f.write("YES")
        f.close()
    if(portAssigned==8083):
        f = open("Mul_online", "w")
        f.write("YES")
        f.close()
    if(portAssigned==8084):
        f = open("Inc_online", "w")
        f.write("YES")
        f.close()
    t1 = threading.Thread(target=main, args=(portAssigned,))
    t1.start()

    counter = 0

    while True:
        if(portAssigned==8080):
            # while True:
                files = [f for f in os.listdir('.') if os.path.isfile(f)]
                for f in files:
                    operation = f[7:8]
                    clientName = f[9:12]
                    if(operation=="1"):
                        isOnlineFile = open("Add_online","r")
                        onlineStatus = isOnlineFile.readlines()
                        isOnlineFile.close()
                        if(onlineStatus[0]=="YES"):
                            writeAddressResposne(str(counter), str(namePortDic["SV1"]), clientName, operation)
                        else:
                            writeOfflineResponse(str(counter), clientName, operation)
                        counter = counter+1
                        os.remove(f)
                    elif(operation=="2"):
                        isOnlineFile = open("Sub_online","r")
                        onlineStatus = isOnlineFile.readlines()
                        isOnlineFile.close()
                        if(onlineStatus[0]=="YES"):
                            writeAddressResposne(str(counter), str(namePortDic["SV2"]), clientName, operation)
                        else:
                            writeOfflineResponse(str(counter), clientName, operation)
                        counter = counter+1
                        os.remove(f)
                    elif(operation=="3"):
                        isOnlineFile = open("Mul_online","r")
                        onlineStatus = isOnlineFile.readlines()
                        isOnlineFile.close()
                        if(onlineStatus[0]=="YES"):
                            writeAddressResposne(str(counter), str(namePortDic["SV3"]), clientName, operation)
                        else:
                            writeOfflineResponse(str(counter), clientName, operation)
                        counter = counter+1
                        os.remove(f)
                    elif(operation=="4"):
                        isOnlineFile = open("Inc_online","r")
                        onlineStatus = isOnlineFile.readlines()
                        isOnlineFile.close()
                        if(onlineStatus[0]=="YES"):
                            writeAddressResposne(str(counter), str(namePortDic["SV4"]), clientName, operation)
                        else:
                            writeOfflineResponse(str(counter), clientName, operation)
                        counter = counter+1
                        os.remove(f)
        elif(portAssigned==8081):
            #add functionality
            while True:
                cwd = os.getcwd()
                isAddDir = cwd[-3:]
                if(isAddDir != "add"):
                    time.sleep(0.5)
                    os.chdir("add")
                    files = [f for f in os.listdir('.') if os.path.isfile(f)]
                    os.chdir("../")
                    for f in files:
                        os.chdir("add")
                        toAddFile = open(f, "r")
                        numberArray = toAddFile.readlines()[0].split()
                        message = str(numberArray[0]) + "+" + str(numberArray[1]) + "=" + str(int(numberArray[0])+int(numberArray[1]))
                        os.remove(f)
                        os.chdir("../")
                        responseFile = open("./response/"+"res_"+f+"_"+str(counter), "w")
                        counter = counter+1
                        responseFile.write(message)
                        responseFile.close()

        elif(portAssigned==8082):
            #sub functionality
            cwd = os.getcwd()
            isDir = cwd[-3:]
            if(isDir != "sub"):
                time.sleep(0.5)
                os.chdir("sub")
                files = [f for f in os.listdir('.') if os.path.isfile(f)]
                os.chdir("../")
                for f in files:
                    os.chdir("sub")
                    toAddFile = open(f, "r")
                    numberArray = toAddFile.readlines()[0].split()
                    message = str(numberArray[0]) + "-" + str(numberArray[1]) + "=" + str(int(numberArray[0])-int(numberArray[1]))
                    os.remove(f)
                    os.chdir("../")
                    responseFile = open("./response/"+"res_"+f+"_"+str(counter), "w")
                    counter = counter+1
                    responseFile.write(message)
                    responseFile.close()
        elif(portAssigned==8083):
            cwd = os.getcwd()
            isDir = cwd[-3:]
            if(isDir != "mul"):
                time.sleep(0.5)
                os.chdir("mul")
                files = [f for f in os.listdir('.') if os.path.isfile(f)]
                os.chdir("../")
                for f in files:
                    os.chdir("mul")
                    toAddFile = open(f, "r")
                    numberArray = toAddFile.readlines()[0].split()
                    message = str(numberArray[0]) + "*" + str(numberArray[1]) + "=" + str(int(numberArray[0])*int(numberArray[1]))
                    os.remove(f)
                    os.chdir("../")
                    responseFile = open("./response/"+"res_"+f+"_"+str(counter), "w")
                    counter = counter+1
                    responseFile.write(message)
                    responseFile.close()

        elif(portAssigned==8084):
            cwd = os.getcwd()
            isDir = cwd[-3:]
            if(isDir != "inc"):
                time.sleep(0.5)
                os.chdir("inc")
                files = [f for f in os.listdir('.') if os.path.isfile(f)]
                os.chdir("../")
                for f in files:
                    os.chdir("inc")
                    toAddFile = open(f, "r")
                    numberArray = toAddFile.readlines()[0].split()
                    message = str(numberArray[0]) + "++ = " + str(int(numberArray[0])+1)
                    os.remove(f)
                    os.chdir("../")
                    # print(os.getcwd())
                    responseFile = open("./response/"+"res_"+f+"_"+str(counter), "w")
                    counter = counter+1
                    responseFile.write(message)
                    responseFile.close()

