"""
Some utilities for running selenium tests generated 
by the Selenium IDE (html tables) via Selenium-remote-control 
in python

Requires the Selenium remote control package (Selenium RC) 
available from http://www.openqa.org/selenium/

in particular this expects the selenium module found
in that package to be available.

To hanlde starting the selenium server, selenium-server.jar
should be alongside this module and some java should be in
PATH
"""

import os 
import platform
import selenium
import signal 
import subprocess
import sys
import time

from HTMLParser import HTMLParser

class SeleniumTableSuiteParser(HTMLParser): 
    """
    This class parses a Selenium HTML suite table and
    extracts the list of filenames of selenium tests
    contained inside the HTML table given to
    parseTable(tableData)
    """

    def __init__(self): 
        HTMLParser.__init__(self)
        self.inTableData = False
        self.inTableHead = False

    def handle_starttag(self,tag,attrs): 
        if tag == 'td':
            self.inTableData = True; 
        elif tag == 'thead':
            self.inTableHead = True
        elif tag == 'a' and self.inTableData and not self.inTableHead:
            for attr in attrs:
                if (attr[0] == 'href' and len(attr[1]) > 0):
                    self.files.append(attr[1])
            
    def handle_endtag(self,tag): 
        if tag == 'td':
            self.inTableData = False 
        elif tag == 'thead':
            self.inTableHead = False

    def parseTable(self,tableData): 
        """
        Parses the Selenium Suite HTML table data given and extracts
        the filenames referenced in the rows 
        """
        self.files = []
        self.feed(tableData)
        return self.files
        
class SeleniumTableTestParser(HTMLParser): 
    """
    This class parses a Selenium HTML test table of commands into 
    a list of 3 element lists corresponding to the rows of 
    the HTML Table given to parseTable(tableData)
    
    Each 3 element list represents a Selenese command:  
      The first element is the Selenese command name 
      The second element is the Selenese target
      The third element is the value 
    """
 

    def __init__(self):
        HTMLParser.__init__(self)
        self.table = []
        self.curRow = []
        self.inTableData = False 
        self.inTableHead = False 



    def rowCompleted(self): 
        if not self.inTableHead:
            while (len(self.curRow) < 3):
                self.curRow.append('')

            self.table.append(self.curRow)
            self.curRow = []

    def handle_starttag(self,tag,attrs): 
        if tag == 'td':
            self.inTableData = True; 
        elif tag == 'thead':
            self.inTableHead = True

    def handle_data(self,data): 
        if self.inTableData and not self.inTableHead: 
            self.curRow.append(data)

    def handle_endtag(self,tag): 
        if tag == 'tr':
            self.rowCompleted()
        elif tag == 'td':
            self.inTableData = False 
        elif tag == 'thead':
            self.inTableHead = False

    def parseTable(self,tableData): 
        """
        parses the selenium HTML table representation of 
        a Selenium test given by the string tableData and 
        returns a list of 3 element lists as described 
        in the class comment. 
        """
        self.table = []
        self.curRow = []
        self.feed(tableData)
        return self.table

def runSeleniumCommands(tester,commandList):
    """
    run the Selenium test given as a list of 
    3 element lists [command,target,value] using 
    the selenium object given by tester

    returns True if the test succeeds, False otherwise
    """

    for command in commandList:
        try: 
            result = tester.do_command(command[0],command[1:])
            if (result != 'OK'):
                print 'Test Failed during command (' , str(command) , '), result was ', result
                return False 
        except Exception,data: 
            print 'Test Failed during command (' , str(command) , '): exception reason (' , data , ')'
            return False 

    return True 

def runSeleniumTestFile(tester,filename,baseURL=None):
    """
    runs the HTML selenium test contained in the
    filename given.
    returns True if the test succeeds, False otherwise
    """
    parser = SeleniumTableTestParser()
    commands = parser.parseTable(open(filename).read())
    if (baseURL != None):
        redirectSeleniumOpenCommands(commands,baseURL)
    else:
        print "Running with absolute URLs"
    return runSeleniumCommands(tester,commands)

  
def runSeleniumSuite(tester,filename,baseURL=None):
    """
    runs the HTML selenium test suite contained in
    the filename given. returns True if all tests
    succeed, False if any test fails. 
    """
    print "Running Selenium Suite",filename
    parser = SeleniumTableSuiteParser()
    files = parser.parseTable(open(filename).read())
    basePath = os.path.dirname(filename)
    
    succeeded = True    
    for testFilename in files:
        fullFilename = testFilename
        if not os.path.isabs(fullFilename):
            fullFilename = os.path.join(basePath,testFilename)
            
        print "Running test" , fullFilename
        if runSeleniumTestFile(tester,fullFilename,baseURL) == False:
            succeeded = False
    return succeeded

def redirectSeleniumOpenCommands(commands,baseURL):
    """
    prepend the target of all Selenese 'open' commands with the 
    baseURL given. commands is a list of 3 element lists [command,target,value],
    each representing a selenium command 
    """
    print "Redirecting to",baseURL
    for cmd in commands:
        if cmd[0] == 'open':
            cmd[1] = baseURL + cmd[1]
   
def startSeleniumServer(port=4444,display=':0'):
    """
    attempt to run the selenium rc server as a subprocess
    XXX this probably only works under unix
    """
    print "Starting Selenium Server on port", port 
    serverJar = os.path.dirname(__file__) + "/selenium-server.jar"
    print "using",serverJar
    p1 = subprocess.Popen("java -jar %s -port %s" % (serverJar,str(port)),
                          shell=True)
    time.sleep(1)
    return p1

def stopSeleniumServer(process):
    """
    attempt to kill the selenium rc server subprocess,
    process - the Popen object returned by startSeleniumServer
    """
    print "Killing Selenium Server"
    if (platform.system() == 'Windows'):
        import win32api
        handle = win32api.OpenProcess(1, 0, process.pid)
        win32api.TerminateProcess(handle, 0)
    else:
        os.kill(process.pid,signal.SIGKILL)

def commandLineMain(): 
  """
   example and main routine called if this script is executed from 
   the command line.
  """ 
  if len(sys.argv) != 3:
    print "Usage: ", sys.argv[0] , '<baseURL> <testSuite>'
    sys.exit(0)


  baseURL = sys.argv[1] 
  testSuiteFileName = sys.argv[2] 

  server = startSeleniumServer()

  tester = selenium.selenium('localhost',4444, 
                             '*firefox /usr/lib/firefox/firefox-bin',baseURL)


  tester.start()

  try:
      passed = runSeleniumSuite(tester,testSuiteFileName,baseURL=baseURL)
      if (passed == True):
          print "Passed all tests"
      else:
          print "Tests failed"
  finally:
      tester.stop()
      stopSeleniumServer(server)

if __name__ == "__main__":
  commandLineMain()
