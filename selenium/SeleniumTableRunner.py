"""

Some utilities for running selenium tests generated 
by the Selenium IDE (html tables) via Selenium-remote-control 
in python

Requires the Selenium remote control package (Selenium RC) 
available from http://www.openqa.org/selenium/

"""


import sys
import selenium 
from HTMLParser import HTMLParser


class SeleniumTableParser(HTMLParser): 
  """
    This class parses a Selenium HTML table of commands into 
    a list of 3 element lists corresponding to the rows of 
    the HTML Table given to parseTable(tableData)
    
    Each 3 element list represents a Selenese command:  
      The first element is the Selenese command name 
      The second element is the Selenese target
      The third element is the value 
  """
 

  def __init__(self):
    self.table = []
    self.curRow = []
    self.inTableData = False 
    self.inTableHead = False 
    HTMLParser.__init__(self)


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
    elif tag == "thead":
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

def runSeleniumTable(tester,tableOfCommands): 
  """
    run the Selenium test given as a list of 
    3 element lists [command,target,value] using 
    the selenium object given
 
    returns True if the test succeeds, False otherwise
  """

  for command in tableOfCommands:
    try: 
      result = tester.do_command(command[0],command[1:])
      if (result != 'OK'):
        print 'Test Failed during command (' , str(command) , '), result was ', result
        tester.stop()
        return False 
    except Exception,data: 
        print 'Test Failed during command (' , str(command) , '): exception reason (' , data , ')'
        tester.stop()
        return False 

  return True 


def redirectOpenCommands(commands,baseURL):
  """
    prepend the target of all Selenese 'open' commands with the 
    baseURL given 
  """
  for cmd in commands:
    if cmd[0] == 'open':
      cmd[1] = baseURL + cmd[1]
   

def commandLineMain(): 
  """
   example and main routine called if this script is executed from 
   the command line. 
  """ 
  if len(sys.argv) < 3:
    print "Usage: ", sys.argv[0] , '<baseURL> <testFile> [testFile 2] ...'
    sys.exit(0)


  baseURL = sys.argv[1] 
  testFiles = sys.argv[2:] 

  tester = selenium.selenium('localhost',4444, \
                           '*firefox /usr/lib/firefox/firefox-bin',
                           baseURL)


  tp = SeleniumTableParser()

  tester.start()
  for testFile in testFiles:
    cmdTable = tp.parseTable(open(testFile).read())
    redirectOpenCommands(cmdTable,baseURL)
    print 'Running [' , testFile , ']'
 
    if (runSeleniumTable(tester,cmdTable)): 
      print 'Test [' , testFile , '] Succeeded'

  tester.stop()

if __name__ == "__main__":
  commandLineMain()