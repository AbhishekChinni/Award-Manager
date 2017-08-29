Read the instructions carefully before executing the app:

If the app is to be run on a localhost then first install web2py from the site 'https://web2py.com/examples/default/download'
Follow the instructions given in the site for the installation of web2py your respective Operating system
After the installation copy the folder "manager" into the web2py/applications folder
click on the web2py.py exe file in the web2py folder to launch web2py and give a password to start the server
Change the URL to 127.0.0.1:8000/manager and click enter


For the app to be viewed on the server some changes in the code need to be done
In the web2py/applications/manager/controllers/default.py file change the
CAS.my_url='http://127.0.0.1:8000/manager/default/login' to CAS.my_url='http://your_server/manager/default/login'
