from xmlrpclib import Server as XMLRPCServer

import urllib
import configuration

def cleanupTestProducts(): 
    scheme,uri = urllib.splittype(configuration._baseURL) 
    host,path = urllib.splithost(uri)
    authURL = "%s://%s:%s@%s%s" % (scheme,configuration.cleanup_user,configuration.cleanup_password,host,path)
    portal = XMLRPCServer(authURL)
    portal.projects.manage_delObjects([configuration.projname])
    portal.portal_memberdata.manage_delObjects([configuration.user])


if __name__ == '__main__': 
    cleanupTestProducts()
