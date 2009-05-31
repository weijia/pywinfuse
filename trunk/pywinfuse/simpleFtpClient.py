import ftplib
import re

import re

'''
total 24418
drwxrwsr-x   5 ftp-usr  pdmaint     1536 Mar 20 09:48 .
dr-xr-srwt 105 ftp-usr  pdmaint     1536 Mar 21 14:32 ..
-rw-r--r--   1 ftp-usr  pdmaint     5305 Mar 20 09:48 INDEX
'''
#b = re.compile('([drwxs\-]+)[\t ]+([0-9]+)[\t ]+([^\t ]+)[\t ]+([^\t ]+)[\t ]+([0-9]+)[\t ]+([a-zA-Z])+[\t ]+([0-9])+[\t ]+([a-zA-Z0-9\:])+[\t ]+(.+)')
dirPattern = re.compile('[\t ]*'+'([^\t ]+)[\t ]+'*8+'([^\t ]+)')


class simpleFtpClient:
    def __init__(self, server, user = "anonymous", passwd = "ftplib-example-2"):
        self.ftp = ftplib.FTP(server)
        self.ftp.set_debuglevel(0)
        print user, passwd
        self.user = user
        self.passwd = passwd
        self.loginFlag = False
        self.lastDirList = []
        self.pwd = '/'
    def gotoDir(self, dirPath):
        self.pwd = dirPath
        self.ftp.cwd(dirPath)
        
    def dirCallback(self, line):
        #print line
        o = []
        m = dirPattern.match(line)
        if m == None:
            print 'no dir in this line'
        else:
            for i in range(0, 10):
                o.append(m.group(i))
            self.lastDirList.append(o)

    def login(self):
        if self.loginFlag:
            #Check if we lost connection
            self.gotoDir(self.pwd)
            return
        self.ftp.login(self.user, self.passwd)
        self.gotoDir(self.pwd)
        self.loginFlag = True
        
    def get(self, filePath, targetFile):
        self.login()
        #Change all '\\' to '/'
        filePath.replace('\\','/')
        #Change current dir
        dirName, filename = filePath.rsplit('/',1)
        dirName += '/'
        self.gotoDir(dirName)
        self.ftp.retrbinary("RETR " + filename, targetFile.write)

    def getDir(self, dirName):
        self.pwd = dirName
        self.login()
        self.lastDirList = []
        self.ftp.dir(self.dirCallback)
        return self.lastDirList


def main():
    hi = simpleFtpClient('localhost', 'wwj','wwj')
    i = hi.getDir('/')
    for m in i:
      print m
    import uuid
    cached = 'd:/tmp'+'/'+str(uuid.uuid4())
    wf = open(cached, 'wb')
    hi.get('/BPP_spel.log', wf)
    wf.close()
    
if __name__ == '__main__':
    main()
