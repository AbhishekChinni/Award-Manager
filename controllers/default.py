#########################################################################
# Coding done by Madhuri,Neeharika,Abhishek
# 
#########################################################################
from gluon.sqlhtml import form_factory
import socket

#define the Login,Logout,Redirecting URL's here
CAS.login_url='https://login.iiit.ac.in/cas/login'
CAS.check_url='https://login.iiit.ac.in/cas/validate'
CAS.logout_url='https://login.iiit.ac.in/cas/logout'
CAS.my_url='http://127.0.0.1:8000/manager/default/login'
#if not logged in redirect to login page
if not session.token and not request.function=='login':
    redirect(URL(r=request, f='login'))
#--------Abhishek---------#
#define the session.login to distinguish between different users
#get the session.token
def login():   #function for login 
    session.login = 0 
    session.token = CAS.login(request)
    return dict()
def display_form():
   form=FORM('Your name:', INPUT(_name='name'), INPUT(_type='submit'))
   return dict(form=form)    
def check():
 form=db().select(db.Book.ALL)
 return dict(form=form)    
def logout():   #function for logout
    session.token=None
    CAS.logout()
    
def index():   #function returns the variables required for the first page of the student portal.
  """
  example action using the internationalization operator T and flash
  rendered by views/default/index.html or views/generic.html
  """
  name=session.token.split('@')[0]        #get the firstname.lastname from email
  first_name=name.split('.')[0]           #get the first name
  last_name=name.split('.')[1]            #get ethe last name
  test1 = db(db.auth_user.email == session.token).select()            #select the user whose email is the one logged in
  if(len(test1)==0):                                                  #if not already in database then store it for further use
        db.auth_user.insert(
        first_name=first_name,
        last_name=last_name,
        email=session.token)
  session.login = 0
  session.LOGGEDIN = 0
  users1 = db().select(db.Lpref.ALL)   
  users2 = db().select(db.Lpref.ALL)
  for i in users1:                   #This part of the code enables the consideration of the recently filled language preferences of the student. Therefore the students can change their language preferences , and the most recently filled ones are considered.
      for j in users2:
          if i.id > j.id:
              if i.E == j.E:
                  db(db.Lpref.id == j.id).delete()
  images=db().select(db.Book.ALL)
 #   return dict(message=T('Hello World'))
  award = db(db.Admin.id > 0).select().first()
  return dict(images=images,t=session.token,award=award)
def edit():
 if session.token=="neeharikak.v@students.iiit.ac.in":
   users = db().select(db.Book.ALL, orderby=db.Book.Name)
   return dict(users=users)
def drop():       #This function drops the student table and the UPBook table to re-enter the input incase the admin has entered the input wrong.
  db(db.User.id > 0).delete() 
  db(db.UPBook.id > 0).delete() 
  db(db.Admin.id > 0).delete()
  form2 = crud.create(db.Admin,
         next=URL("index"))
  award = db(db.Admin.id > 0).select().first()
  return dict(form2=form2,award=award)
def errorstu():  #This fuction redirects back to the upload (upload students list) page to enable the admin to append students to the list.
   if request.vars.csvfile != None:
        table = db[request.vars.table]
        file = request.vars.csvfile.file
        table.import_from_csv_file(file) #Import from the csv file
        award = db(db.Admin.id > 0).select().first()                                         
        #query = db.stlist.flag==""
        #db(query).update(flag="1")         
        for k in db(db.User.Award=="D1").select():
            k.Total=award.D1                                                        #The cost of D1 is given to the 'Total' field of the user table
            k.update_record()
        for k in db(db.User.Award=="D2").select():                                  #The cost of D2 is given to the 'Total' field of the user table
            k.Total=award.D2                                                        
            k.update_record()
        for k in db(db.User.Award=="D3").select():
            k.Total=award.D3                                                       #The cost of D3 is given to the 'Total' field of the user table
            k.update_record()
        for k in db(db.User.Award=="ML").select():
            k.Total=award.ML                                                       #The cost of ML is given to the 'Total' field of the user table
            k.update_record()
        #db(db.stlist.Award==k).update(total="1200")
        #response.flash = 'Students List uploaded'
        users1 = db().select(db.User.ALL, orderby=db.User.Name)
        users2 = db().select(db.User.ALL, orderby=db.User.Name)
        for i in users1:
         for j in users2:
           if i.id < j.id:
              if i.RollNo == j.RollNo:
                  db(db.User.id == i.id).update(Total=i.Total+j.Total)            #(removes duplicates)If a student gets more than one award , then the total amount will the sum of the cost of individual awards.
                  db(db.User.id == i.id).update(Award1=j.Award)
                  db(db.User.id == j.id).delete()  
 
        
   return dict()
def errorbook():#This fuction redirects back to the upload1 (upload book list) page to enable the admin to append books to the list.
   if request.vars.csvfile != None:
        table = db[request.vars.table]
        file = request.vars.csvfile.file
        table.import_from_csv_file(file)                                          #Import from the csv file
        response.flash = 'Books List uploaded'
   return dict()

def dropstu():#This fuction redirects back to the upload (upload students list) page after deleting the contents of the User table to enable the admin to re-enter the list.
   db(db.User.id > 0).delete() 
   if request.vars.csvfile != None:
        table = db[request.vars.table]
        file = request.vars.csvfile.file
        table.import_from_csv_file(file) #Import from the csv file
        award = db(db.Admin.id > 0).select().first()                                         
        #query = db.stlist.flag==""
        #db(query).update(flag="1")         
        for k in db(db.User.Award=="D1").select():
            k.Total=award.D1                                                         #The cost of D1 is given to the 'Total' field of the user table
            k.update_record()
        for k in db(db.User.Award=="D2").select():
            k.Total=award.D2                                                         #The cost of D2 is given to the 'Total' field of the user table
            k.update_record()
        for k in db(db.User.Award=="D3").select():
            k.Total=award.D3                                                        #The cost of D3 is given to the 'Total' field of the user table
            k.update_record()
        for k in db(db.User.Award=="ML").select():
            k.Total=award.ML                                                        #The cost of ML is given to the 'Total' field of the user table
            k.update_record()
        #db(db.stlist.Award==k).update(total="1200")
        #response.flash = 'Students List uploaded'
        users1 = db().select(db.User.ALL, orderby=db.User.Name)
        users2 = db().select(db.User.ALL, orderby=db.User.Name)
        for i in users1:
         for j in users2:
           if i.id < j.id:
              if i.RollNo == j.RollNo:
                  db(db.User.id == i.id).update(Total=i.Total+j.Total)            #If a student gets more than one award , then the total amount will the sum of the cost of individual awards.
                  db(db.User.id == i.id).update(Award1=j.Award)
                  db(db.User.id == j.id).delete()  
 
        
   return dict()
def dropbook():#This fuction redirects back to the upload1 (upload book list) page after deleting the contents of the Book table to enable the admin to re-enter the list.
   db(db.Book.id > 0).delete() 
   if request.vars.csvfile != None:
        table = db[request.vars.table]
        file = request.vars.csvfile.file
        table.import_from_csv_file(file)                                          #Import from the csv file
        response.flash = 'Books List uploaded'
   return dict()

def drop1m():
 if session.token=="neeharikak.v@students.iiit.ac.in":
  return dict() 
def error():
  return dict() 
def drop1(): #This function deletes the contents of all the tables , to start the entire process afresh for the next academic year.
  db(db.User.id > 0).delete() 
  
  db(db.UPBook.id > 0).delete() 
  
  db(db.Lpref.id>0).delete()
  db(db.prebook.id>0).delete()
  db(db.auth_user.id>0).delete()
  award = db(db.Admin.id > 0).select().first()#selects the first entry.
  db(db.Admin.id > 0).delete()
  return dict(award=award)
def label(): #This function returns the User and UPBook tables to print the labels for all the students.
 if session.token=="neeharikak.v@students.iiit.ac.in":
   users = users = db().select(db.User.ALL, orderby=db.User.Name)
   books = books = db().select(db.UPBook.ALL, orderby=db.UPBook.usd)
   return dict(users=users,books=books)
def admin():#This returns the variables required for the first page of the admin.
    award = db(db.Admin.id > 0).select().first()
    return dict(award=award)
def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    return dict(form=auth())
#@auth.requires_login()
def choose():  #Removes the duplicates and returns the variables to print the names of all the students with hyperlinks.
 if session.token=="neeharikak.v@students.iiit.ac.in":
  users1 = db().select(db.User.ALL, orderby=db.User.Name)
  users2 = db().select(db.User.ALL, orderby=db.User.Name)
  for i in users1:
      for j in users2:
          if i.id < j.id:
              if i.RollNo == j.RollNo:    
                  db(db.User.id == i.id).update(Total=i.Total+j.Total) #(removes duplicates)If a student gets more than one award , then the total amount will the sum of the cost of individual awards.
                  db(db.User.id == i.id).update(Award1=j.Award)
                  db(db.User.id == j.id).delete()
  users = db().select(db.User.ALL, orderby=db.User.Name)
  return dict(users=users)
def change():
   db(db.Book.id ==request.args(0)).update(Name=request.vars.t1,Cost=request.vars.t2,Copies=request.vars.t3,Type=request.vars.t4,Language=request.vars.t5)
   users = db().select(db.Book.ALL, orderby=db.Book.Name)
   return dict(users=users)
def bookdel():
   db(db.Book.id ==request.args(0)).delete()
   users = db().select(db.Book.ALL, orderby=db.Book.Name)
   return dict(users=users)
def nedit():#Allows the admin to edit the book list.
 Book = db.Book(request.args(0)) or redirect(URL('edit'))
 books = db(db.Book.id==request.args(0)).select()
# if request.vars.t1 != None:
 
  
 
 return dict(books=books)
 
def show():# This function returns the variables required to display the list of available books and the books selected by the admin for each student.
 User = db.User(request.args(0)) or redirect(URL('choose'))
 Books = db().select(db.Book.ALL, orderby=db.Book.Name)
 UPBooks = db(db.UPBook.usd==User.RollNo).select()
 upbooks1 = db(db.UPBook.usd==User.RollNo).select()
 upbooks = db(db.UPBook.usd==User.RollNo).select()
 Prebooks = db().select(db.prebook.ALL, orderby=db.prebook.Name)
 form = db().select(db.auth_user.ALL)
 for i in upbooks:
      for j in upbooks1:
          if i.id < j.id:
              if i.Bid == j.Bid:
                 db(db.UPBook.Bid == j.Bid).delete()
 langu = db().select(db.Lpref.ALL)
 lang = db().select(db.lang.ALL)
 return dict(User=User,UPBooks=UPBooks,Books=Books,langu=langu,lang=lang,Prebooks=Prebooks,form=form)

def preference():#This function creates a form in which student can fill in his language preferences.
  for rows in db(db.auth_user.email == session.token).select(db.auth_user.email):
   id1=rows.email
  db.Lpref.E.default=id1
  form1 = crud.create(db.Lpref,
         next=URL("index"))
  users1 = db().select(db.Lpref.ALL)
  users2 = db().select(db.Lpref.ALL)
  for i in users1:
      for j in users2:
          if i.id > j.id:       #This part of the code deletes all the previous language preferences and stores only the recent one. 
              if i.E == j.E:
                  db(db.Lpref.id == j.id).delete()
  return dict(form1=form1)
def total(): #This function returns the variables required for the output generation.
 if session.token=="neeharikak.v@students.iiit.ac.in":
   users = db().select(db.User.ALL, orderby=db.User.Name)
  # award = db().select(db.Admin.ALL).first()
   award = db(db.Admin.id > 0).select().first()
   return dict(users=users,award=award)
 
def Admin():
 if session.token=="neeharikak.v@students.iiit.ac.in":  #This function creates a form to fill the input i.e the academic year and the award money by the admin.
  form2 = crud.create(db.Admin,
         next=URL("index"))
  award = db(db.Admin.id > 0).select().first()
  return dict(form2=form2,award=award)
def submit():#Implements the functionality where the student's name disappers from the initial list of students once the allotment to that student is final.
 db(request.args(0) == db.User.id).update(flag = 1)
 users = db().select(db.User.ALL, orderby=db.User.Name)
 return dict(users=users)
def upload():#This function enables the admin to upload the csv file of students list
 if session.token=="neeharikak.v@students.iiit.ac.in":
    if request.vars.csvfile != None:
        table = db[request.vars.table]
        file = request.vars.csvfile.file
        table.import_from_csv_file(file) #Import from the csv file
        award = db(db.Admin.id > 0).select().first()                                         
        #query = db.stlist.flag==""
        #db(query).update(flag="1")         
        for k in db(db.User.Award=="D1").select():
            k.Total=award.D1                                                       #The cost of D1 is given to the 'Total'
            k.update_record()
        for k in db(db.User.Award=="D2").select():
            k.Total=award.D2                                                       #The cost of D2 is given to the 'Total'
            k.update_record()
        for k in db(db.User.Award=="D3").select():
            k.Total=award.D3                                                       #The cost of D3 is given to the 'Total'
            k.update_record()
        for k in db(db.User.Award=="ML").select():
            k.Total=award.ML                                                       #The cost of ML is given to the 'Total'
            k.update_record()
        #db(db.stlist.Award==k).update(total="1200")
        #response.flash = 'Students List uploaded'
    users1 = db().select(db.User.ALL, orderby=db.User.Name)
    users2 = db().select(db.User.ALL, orderby=db.User.Name)
    for i in users1:
         for j in users2:
           if i.id < j.id:
              if i.RollNo == j.RollNo:
                  db(db.User.id == i.id).update(Total=i.Total+j.Total)#(removes duplicates)If a student gets more than one award , then the total amount will the sum of the cost of individual awards.
                  db(db.User.id == i.id).update(Award1=j.Award)
                  db(db.User.id == j.id).delete()  
 
        
    return dict()
#@auth.requires_membership('Administrator')
def upload1():#This function enables the admin to upload the csv file of books list
 if session.token=="neeharikak.v@students.iiit.ac.in":
     if request.vars.csvfile != None:
        table = db[request.vars.table]
        file = request.vars.csvfile.file
        table.import_from_csv_file(file)                                          #Import from the csv file
        response.flash = 'Books List uploaded'
     return dict()
def update(): #This function inserts into the UPBook table when the admin selects a book to a student.              
  db.UPBook.insert(Stu_name=request.args(0),usd=request.args(1),Name=request.args(2),Language=request.args(3),Bid=request.args(7),Copies=request.args(8),Cost=request.args(5),Type=request.args(9)) 
  db(db.User.id ==request.args(4)).update(Uptotal=int(int(request.args(6))+int(request.args(5))))
  db(db.Book.id ==request.args(7)).update(Copies=int(int(request.args(8))-1))
  #db.UPBook.Stu_name.default = request.args(0)
  #db.UPBook.usd.default = request.args(1))
  #db.UPBook.Name.default=request.args(2)
  #db.UPBook.Language.default=request.args(3)
  #return dict(redirect(URL('show')))
  User = db.User(request.args(4)) or redirect(URL('choose'))
  upbooks1 = db(db.UPBook.usd==User.RollNo).select()
  upbooks = db(db.UPBook.usd==User.RollNo).select()
  Prebooks = db().select(db.prebook.ALL, orderby=db.prebook.Name)
  form = db().select(db.auth_user.ALL)
  for i in upbooks:
      for j in upbooks1:
          if i.id < j.id:
              if i.Bid == j.Bid:
                 
                  db(db.UPBook.id == j.id).delete()
  
  UPBooks = db(db.UPBook.usd==request.args(1)).select()
  langu = db().select(db.Lpref.ALL)
  lang = db().select(db.lang.ALL)
  Books = db().select(db.Book.ALL, orderby=db.Book.Name)
  return dict(User=User,UPBooks=UPBooks,Books=Books,lang=lang,langu=langu,Prebooks=Prebooks,form=form)
def delete():#This function deletes a entry from the UPBook table when the admin unselects a book for a particular student.
  db(db.UPBook.id == request.args(2)).delete()
  db(db.User.id ==request.args(0)).update(Uptotal=int(int(request.args(1))-int(request.args(6))))
  db(db.Book.id ==request.args(4)).update(Copies=int(int(request.args(3))))
  User = db.User(request.args(0)) or redirect(URL('choose'))
  UPBooks = db(db.UPBook.usd==request.args(5)).select()
  Books = db().select(db.Book.ALL, orderby=db.Book.Name)
  langu = db().select(db.Lpref.ALL)
  lang = db().select(db.lang.ALL)
  Prebooks = db().select(db.prebook.ALL, orderby=db.prebook.Name)
  form = db().select(db.auth_user.ALL)
  return dict(User=User,UPBooks=UPBooks,Books=Books,langu=langu,lang=lang,Prebooks=Prebooks,form=form)

def alloted():
 if session.token=="neeharikak.v@students.iiit.ac.in":
  users = db().select(db.User.ALL, orderby=db.User.Name)
  return dict(users=users)
  
def choose1():# This function returns the variables required to display the list of available books and the preferred books of each student.
 for rows in db(db.auth_user.email == session.token).select(db.auth_user.id):
  id1=rows.id
 prebooks = db(db.prebook.usd == id1).select()
 Books = db().select(db.Book.ALL, orderby=db.Book.Name)
 return dict(prebooks=prebooks,Books=Books)

def update1():#This function inserts into the prebook table when the student selects a book as his preference.  
  db.prebook.insert(usd=request.args(0),Name=request.args(1),Language=request.args(2),Bid=request.args(3),Stu_name=request.args(4),Type=request.args(6))
  db(db.prebook.Stu_name == 'static').delete()
 
  prebooks2 = db(db.prebook.usd ==request.args(0)).select()
  prebooks1 = db(db.prebook.usd ==request.args(0)).select()
  
  for i in prebooks2:
      for j in prebooks1:
          if i.id < j.id:                 #Ensures no multiple selection of the same book.
              if i.Bid == j.Bid:
                 
                  db(db.prebook.id == j.id).delete()
  prebooks = db(db.prebook.usd ==request.args(0)).select()
  Books = db().select(db.Book.ALL, orderby=db.Book.Name)
  return dict(prebooks=prebooks,Books=Books)
def delete1():#This function deletes a entry from the prebook table when the student unselects a book.
  db(db.prebook.id == request.args(1)).delete()
  
  prebooks = db(db.prebook.usd == request.args(0)).select()
  Books = db().select(db.Book.ALL, orderby=db.Book.Name)
  return dict(prebooks=prebooks,Books=Books)
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request,db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()


@auth.requires_signature()
def data():
    """
    http://..../[app]/default/data/tables
    http://..../[app]/default/data/create/[table]
    http://..../[app]/default/data/read/[table]/[id]
    http://..../[app]/default/data/update/[table]/[id]
    http://..../[app]/default/data/delete/[table]/[id]
    http://..../[app]/default/data/select/[table]
    http://..../[app]/default/data/search/[table]
    but URLs must be signed, i.e. linked with
      A('table',_href=URL('data/tables',user_signature=True))
    or with the signed load operator
      LOAD('default','data.load',args='tables',ajax=True,user_signature=True)
    """
    return dict(form=crud())
