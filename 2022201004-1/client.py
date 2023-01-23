import ftplib

def getFtpFilenames(ftpHost, ftpPort, ftpUname, ftpPass, remoteWorkingDirectory=""):
    ftp = ftplib.FTP(timeout=30)
    ftp.connect(ftpHost, ftpPort)
    try:
        ftp.login(ftpUname, ftpPass)
    except:
        print("Invalid credentials!")
        exit()

    if not (remoteWorkingDirectory == None or remoteWorkingDirectory.strip() == ""):
        _ = ftp.cwd(remoteWorkingDirectory)
    fnames = []
    try:
        ftp.dir(fnames.append)
    except ftplib.error_perm as resp:
        if str(resp) == "550 No files found":
            fnames = []
        else:
            raise
    ftp.quit()

    return fnames


ftpHost = input("Enter ftp host: ")
ftpPort = int(input("Enter port: "))
ftpUname = input("Enter the username: ")
ftpPass = input("Enter the password: ")

fileNames = getFtpFilenames(ftpHost, ftpPort, ftpUname, ftpPass )

for item in fileNames:
    print(item)


targetFilepath = input("Enter the file you want to download: ")
localFilepath = targetFilepath + "-copy"

ftp = ftplib.FTP(timeout=30)
ftp.connect(ftpHost, ftpPort)
ftp.login(ftpUname, ftpPass)

try:
    retcode = ftp.retrbinary("RETR " + targetFilepath, open(localFilepath, 'wb').write)
except:
    print("Wrong filename entered!")
    exit()

ftp.quit()


if retcode.startswith("226"):
    print("Downloaded successfully")
else :
    print("Some error occured.")
