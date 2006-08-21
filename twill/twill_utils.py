import sys 
import twill
from twill.namespaces import get_twill_glocals

def executeTwillScriptsInSession(twillFiles): 
  """ run a list of twill scripts in a single 
      session.
  """ 
  for testFile in twillFiles: 
    twill.execute_file(testFile,no_reset=1)

def defineTwillVars(varDict):
  """Make the name-value bindings in varDict 
     available in the twill namespace for 
     use in twill scripts
  """
  twillGlobals,twillLocals = get_twill_glocals()
  twillLocals.update(varDict)


if __name__ == '__main__':
  if len(sys.argv) < 2: 
    print "usage:", sys.argv[0], "<twillScript> [twillScript...]"
    sys.exit(0)

  twill.parse.debug_print_commands(True)
  executeTwillScriptsInSession(sys.argv[1:])

