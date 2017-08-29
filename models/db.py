# -*- coding: utf-8 -*-

#########################################################################
## This scaffolding model makes your app work on Google App Engine too
## File is released under public domain and you can use without limitations
#########################################################################

## if SSL/HTTPS is properly configured and you want all HTTP requests to
## be redirected to HTTPS, uncomment the line below:
# request.requires_https()

if not request.env.web2py_runtime_gae:
    ## if NOT running on Google App Engine use SQLite or other DB
    db = DAL('sqlite://storage.sqlite')
else:
    ## connect to Google BigTable (optional 'google:datastore://namespace')
    db = DAL('google:datastore')
    ## store sessions and tickets there
    session.connect(request, response, db = db)
    ## or store session in Memcache, Redis, etc.
    ## from gluon.contrib.memdb import MEMDB
    ## from google.appengine.api.memcache import Client
    ## session.connect(request, response, db = MEMDB(Client()))

## by default give a view/generic.extension to all actions from localhost
## none otherwise. a pattern can be 'controller/function.extension'
response.generic_patterns = ['*'] if request.is_local else []
## (optional) optimize handling of static files
# response.optimize_css = 'concat,minify,inline'
# response.optimize_js = 'concat,minify,inline'

#########################################################################
## Here is sample code if you need for
## - email capabilities
## - authentication (registration, login, logout, ... )
## - authorization (role based authorization)
## - services (xml, csv, json, xmlrpc, jsonrpc, amf, rss)
## - old style crud actions
## (more options discussed in gluon/tools.py)
#########################################################################

from gluon.tools import *
auth=Auth(globals(),db)                      # authentication/authorization
auth.settings.hmac_key='sha512:f5cbda62-70b3-4b5e-bb7b-c65c6d95e1cc'

## create all tables needed by auth if not custom tables
auth.settings.extra_fields['auth_user']=[Field('cnt','integer',default = '0')]
auth.define_tables()
crud=Crud(globals(),db)                      # for CRUD helpers using auth
service=Service(globals())


## create all tables needed by auth if not custom tables

auth.define_tables()

## configure email

#########################################################################
## Define your tables below (or better in another model file) for example
##
## >>> db.define_table('mytable',Field('myfield','string'))
##
## Fields can be 'string','text','password','integer','double','boolean'
##       'date','time','datetime','blob','upload', 'reference TABLENAME'
## There is an implicit 'id integer autoincrement' field
## Consult manual for more options, validators, etc.
##
## More API examples for controllers:
##
## >>> db.mytable.insert(myfield='value')
## >>> rows=db(db.mytable.myfield=='value').select(db.mytable.ALL)
## >>> for row in rows: print row.id, row.myfield
#########################################################################
db.define_table('Book',      # Table to store the book list which is uploaded by the admin .
    Field('Name','text'),
    Field('Language','string'),
    Field('Cost','integer'),
    Field('Copies','integer'),
    Field('Type','integer'))

db.define_table('UPBook',   # Table to store the books alloted to each student by the admin.
    Field('stu_id'),
    Field('Stu_name','string'),
    Field('Name','text'),
    Field('Language','string'),
    Field('usd'),
    Field('Bid','integer'),
    Field('Copies'),
    Field('Cost'),
    Field('Type','integer'))  
db.define_table('prebook',   #Table to store the book preferences of each student which are filled when logged into the portal.
    Field('Stu_name','string'),
    Field('Name','text'),
    Field('Language','string'),
    Field('usd'),
    Field('Bid','integer'),
    Field('Type','integer'))
db.define_table('User',       #Table to stote the awardees list which is uploaded by the admin
    Field('SlNo','integer'),
    Field('RollNo','string'),
    Field('Name','string'),
    Field('Email','string'),
    Field('Award','string'),
    Field('year','string'),
    Field('Award1','string'),
    Field('flag','integer',default="0"), #this attribute decides whether the allotment of books for a particular student is final or not ,if it is final then (flag becomes "1")   
    Field('Uptotal','integer',default="0"),#updated total which is automatically incremented/decremented by the cost of the books selected/unselected
    Field('Total','integer',default="0"))
db.define_table('lang',   #Table which has the list of languages,from which the student has to choose two as his preferences. 
    Field('Name','string'),
    format='%(Name)s')
db.define_table('Admin',  #Table(implemented as a form) to store the input such as year and award money from the admin. 
    Field('year','string'),#year = academic year for which awards are being given.
    Field('D1','integer'), #to be filled with the award money associated with this particular award.
    Field('D2','integer'),
    Field('D3','integer'),
    Field('ML','integer'))  
db.define_table('Lpref',  # Table to store the language preferences of the student when logged into the portal.
    Field('E','string'),
    Field('First','reference lang'),
    Field('Second','reference lang'))
db.Lpref.E.writable = db.Lpref.E.readable = False
#db.auth_user.cnt.readable = False
db.Lpref.First.requires = IS_IN_DB(db, db.lang.id,'%(Name)s')   #Displays a drop down box
db.Lpref.Second.requires = IS_IN_DB(db, db.lang.id,'%(Name)s')
db.Admin.year.requires = IS_NOT_EMPTY() #year cannot be empty,the admin has to input the academic year for which the awards are being given     given(ex:2011-2012)
db.Admin.D1.requires = IS_NOT_EMPTY() #D1 amount cannot be empty
db.Admin.D2.requires = IS_NOT_EMPTY() #D2 amount cannot be empty
db.Admin.D3.requires = IS_NOT_EMPTY()  #D3 amount  cannot be empty
db.Admin.ML.requires = IS_NOT_EMPTY()  #ML amount cannot be empty
