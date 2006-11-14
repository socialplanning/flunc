
you should be able to setup.py develop into a working env, 
after that: 


ftest --help for details 


by default ftest will search ./ftests/ to find tests. you can 
change this with the -p (--path) option 


ftest all 

[runs all tests listed in all.tsuite against localhost:8080/portal]

ftest -t http://localhost:8080/some_portal all 
[runs all tests listed in all.tsuite against localhost:8080/some_portal]

or 

ftest -t http://localhost:8080/p -c all create_user

(runs create_user.twill using all.conf) 

or 

ftest -c all create_user create_project destroy_project destroy_user

(specify an ad hoc suite creating and tearing down a user and project
 on default host) 


individual tests are contained in 
<test>.twill 

a suite of tests are contained in 
<suite>.tsuite 

suite configurations are contained in
<suite>.conf 





