python ./ftest.py --help for details 


try: 

python ./ftest.py all 

(runs all tests listed in all.tsuite against localhost:8080/portal) 

or 

python ./ftest.py -t http://localhost:8080/p -c all create_user

(runs create_user.twill using all.conf) 

or 

python ./ftest.py -c all create_user create_project destroy_project destroy_user

(specify an ad hoc suite creating and tearing down a user and project
 on default host) 



individual tests are contained in 
<test>.twill 

a suite of tests are contained in 
<suite>.tsuite 

suite configurations are contained in
<suite>.conf 





