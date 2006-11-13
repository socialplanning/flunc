python ./ftest.py --help for details 


try: 

python ./ftest.py -t http://localhost:8080/p all 

(runs all tests listed in all.tsuite) 

or 

python ./ftest.py -c all create_user

(runs create_user.twill using all.conf) 



individual tests are contained in 
<test>.twill 

a suite of tests are contained in 
<suite>.tsuite 

suite configurations are contained in
<suite>.conf 





