import json
import random
import string
import crypt
import os
import web

urls = (
  '/', 'hello',
  '/register', 'register',
  '/activate/(.+)', 'activate',
  '/session', 'session',
  '/paste', 'paste',
  '/copy', 'copy',
)

#------------- STATIC --------------
EMAIL_ROOT = 'globalclip.org'
ACTIVATION_EMAIL = 'activation@%s' % EMAIL_ROOT
SERVER_HOST = os.environ.get('SERVER_NAME','localhost')
BASE_URI = '/clip'
SALT = '!](A7>(90OD(IN!.\\.3G^DKCZ)C;C:5,PV)>G;A%VCAB1[(Q2H39_U]ZTNXM5HCSY^:W@GGP8JYG9,%CEEWJZQU:KK&Q5M)^O,;H'

#------------- GLOBALS -------------
db = web.database(dbn='SCHEMA', user='USER', pw='PASS', db='DB')

#------------- utils ---------------

def j_e(msg,status='401 Invalid',**kwargs):
    d = {'payload' : msg,'status':401}
    d.update(kwargs)
    web.status = status
    return json.dumps(d)

def j_s(msg,status='200 OK',**kwargs):
    d = {'payload' : msg, 'status':200}
    d.update(kwargs)
    web.status = status
    return json.dumps(d)

def is_registered(email):
    return len(db.select(['accounts'],where=web.db.reparam("email=$e",dict(e=email)),limit=1)) > 0

def is_activated(email):
    return len(db.select(['accounts'],where=web.db.reparam("email=$e AND isactive=$i",dict(e=email,i=True)),limit=1)) > 0

def crypt_password(passwd):
    """ return a hashed and salted password using the in-built crypt package"""
    return crypt.crypt(passwd,SALT)

def is_authentic_account(email,password):
    crypt_passwd = db.select(['accounts'],what='password',where=web.db.reparam("email=$e",dict(e=email)),limit=1)
    if password is None:
        return False
    if len(crypt_passwd) > 0:
        crypt_passwd = crypt_passwd[0].password
        return True if crypt.crypt(password,crypt_passwd) == crypt_passwd else False
    else:
        return False

def has_active_session(email,ip):
    ac = db.select(['accounts'],what="id",where=web.db.reparam("email=$e",dict(e=email)),limit=1)
    if len(ac) > 0:
        ac = ac[0].id
        return len(db.select(['account_sessions'],what="id",where=web.db.reparam("owner=$o AND source_ip=$i",dict(o=ac,i=ip)),limit=1)) > 0
    else:
        return False

def create_session_key(email,ip):
    ac = db.select(['accounts'],what="id",where=web.db.reparam("email=$e",dict(e=email)),limit=1)
    if len(ac) > 0:
        ac = ac[0].id
        ses_key = random_string(20)
        new_id = db.insert('account_sessions',seqname='account_sessions_id_seq',source_ip=ip,owner=ac,session_key=ses_key)
        return ses_key if new_id else None
    else:
        return None

def get_active_session_key(email,ip):
    ac = db.select(['accounts'],what="id",where=web.db.reparam("email=$e",dict(e=email)),limit=1)
    if len(ac) > 0:
        ac = ac[0].id
        res = db.select(['account_sessions'],what="session_key",where=web.db.reparam("owner=$o AND source_ip=$i",dict(o=ac,i=ip)),limit=1)
        return res[0].session_key if len(res) > 0 else None
    else:
        return None

def get_or_create_session_key(email,ip):
    if not has_active_session(email,ip):
        ses = create_session_key(email,ip)
        return ses
    else:
        return get_active_session_key(email,ip)


def save_registration(email,password,key):
    new_id = db.insert('accounts',seqname='accounts_id_seq',email=email,password=crypt_password(password),activation_key=key)
    return True if new_id else False

def make_activation_uri(key):
    return "http://%s/%s/activate/%s" % (SERVER_HOST,BASE_URI,key)

def send_activation_key(email,key):
    if is_valid_email(email):
        link = make_activation_uri(key)
        web.sendmail(
                ACTIVATION_EMAIL,
                email, 
                'GlobalClipboard Activation', 
                "Visit this URI to activate your global clipboard : %s" %  link
                )
        web.debug("Activation Link Sent : %s" % link)
        return True
    else:
        return False

def get_activation_key(email):
    """ get the activation key assigned to this email if it exists"""
    res = db.select(['accounts'],what="activation_key",where=web.db.reparam("email=$e",dict(e=email)),limit=1)
    if len(res) > 0:
        return res[0].activation_key
    else:
        return None

def send_activation_key_reminder(email):
    """ remind the owner of this email about their account activation key"""
    send_activation_key(email,get_activation_key(email))

def random_string(size):
    return ''.join(random.choice(string.ascii_uppercase + string.digits + '_') for x in range(size))

def activation_key_exists(key):
    return len(db.select(['accounts'],where=web.db.reparam("activation_key=$a",dict(a=key)),limit=1)) > 0

def activate_account(key):
    """ activate the account with this key, then clear the activation key """
    return (db.update('accounts',where=web.db.reparam("activation_key=$a",dict(a=key)),isactive=True,activation_key=None)) > 0


def make_activation_key(email,password):
    """currently, just generates a randon string, and ensure's there are no collisions in the db"""
    key = random_string(100)
    while activation_key_exists(key):
        key = random_string(100)
    return key

def is_valid_email(email):
    """ validates the syntax of this email"""
    from lepl.apps.rfc3696 import Email as EmailValidator
    is_valid = EmailValidator()
    return is_valid(email)


def new_registration(email,password):
    activation_key = make_activation_key(email,password)
    if save_registration(email,password,activation_key):
        if send_activation_key(email,activation_key):
            return True
        else:
            web.debug("Failed to Send Activation to Email (%s)" % email)
            return False
    else:
        web.debug("Failed to Save Registration to DB")
        return False

def is_valid_session(key,ip):
    return len(db.select(['account_sessions'],where=web.db.reparam("session_key=$s AND source_ip = $i",dict(s=key,i=ip)),limit=1)) > 0

def get_session_email(session_key,ip):
    res = db.select(['account_sessions'],what="owner",where=web.db.reparam("session_key=$s AND source_ip = $i",dict(s=session_key,i=ip)),limit=1)
    if len(res) > 0:
        id = res[0].owner
        ac = db.select(['accounts'],what="email",where=web.db.reparam("id=$i",dict(i=id)),limit=1)
        if len(ac) > 0:
            return ac[0].email
        else:
            return None
    else:
        return None

def get_mail_to_account_id(email):
        ac = db.select(['accounts'],what="id",where=web.db.reparam("email=$e",dict(e=email)),limit=1)
        if len(ac) > 0:
            return ac[0].id
        else:
            return None

def save_paste(email,ip,paste):
    id = get_mail_to_account_id(email)
    if id:
        safe_paste = paste.encode('base64')
        new_id = db.insert('clipboard_write',seqname='clipboard_write_id_seq',source_ip=ip,owner=id,clipboard=safe_paste)
        return True if new_id else False
    else:
        return False

def clipboard_has_data(email):
    ac = get_mail_to_account_id(email)
    if ac:
        #we should fetch latest item copied onto clipboard from any of this user's machines
        q = db.select(['clipboard_write'],where=web.db.reparam("owner=$o",dict(o=ac)),limit=1,order='created desc')
        #web.debug(repr(q.query))
        return len(q) > 0
    else:
        return False

def delete_paste_id(id):
    res = db.delete('clipboard_write',where=web.db.reparam("id=$i",dict(i=id)))
    return True if res else False


def pop_paste(email):
    ac = get_mail_to_account_id(email)
    if ac:
        res = db.select(['clipboard_write'],what="clipboard,created,id,source_ip",where=web.db.reparam("owner=$o",dict(o=ac)),limit=1,order='created DESC')
        if len(res) > 0:
            res = res[0]
            d = { 'clipboard' : res.clipboard, 'created' : res.created , 'source_ip' : res.source_ip}
            #delete_paste_id(res.id)
            return d
        else:
            return None
    else:
        return None


#~~~~~~~~~~~~~~ VIEWS ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class hello:
    """ say hello and introduce guests to the global clipboard"""
    def POST(self):
        return j_e("Not Supported")
    def GET(self):
        return "Welcome to the 1 & ONLY, GLOBAL CLIPBOARD.\n\nStart by getting a globalclip client << here >>"

class register:
    """ Register New Accounts, send them activation links or remind them of their registration"""
    def GET(self):
        return j_e("Registration only supported via POST")
    def POST(self):
        params = web.input(email=None,password=None)

        if not is_valid_email(params.email):
            return j_e("Email is Invalid!")

        if is_registered(params.email):
            if is_activated(params.email):
                return j_e("Already Registered and Activated :-)")
            else:
                send_activation_key_reminder(params.email)
                return j_e("Already Registered [Activation Pending]. Check your Email Inbox")
        else:
            if new_registration(params.email,params.password):
                return j_s("Registration Complete. Check you Email Inbox")
            else:
                return j_e("Registration Failed. Try Again")

class activate:
    def POST(self):
        return j_e("Not Supported")
    def GET(self,key):
        if key:
            if activation_key_exists(key):
                if activate_account(key):
                    return "Congs! Your Global Clipboard account has been activated :-) Go Copy and Paste the World!"
                else:
                    web.ctx.status = '401 Invalid'
                    return "Sorry, activation of your account has failed. Please Try Again later."
            else:
                web.ctx.status = '401 Invalid'
                return "Sorry, but this Activation Link is not Valid!"
        else:
            web.ctx.status = '401 Invalid'
            return "Please use the Activation Link that was emailed to you. Thanks"

class session:
    def GET(self):
        return j_e("Not Supported")
    def POST(self):
        params = web.input(email=None,password=None)
        if is_authentic_account(params.email,params.password):
            if is_activated(params.email):
                session_key = get_or_create_session_key(params.email,web.ctx.ip)
                if session_key:
                    web.debug("Session Key Sent for (%s,%s) : %s" % (params.email,web.ctx.ip,session_key))
                    return j_s("%s" % session_key,extra="Session Key Included")
                else:
                    web.debug("Failed to Create Session Key for (%s,%s)" % (params.email,web.ctx.ip))
                    return j_s("Failed to Create / Get an Active Session for you. Try Again Later")
            else:
                return j_e("This Account is Not Activated Yet")
        else:
            return j_e("These Credentials are Invalid!")


class paste:
    def GET(self):
        return j_e("Not Supported")
    def POST(self):
        params = web.input(paste=None,session=None,_unicode=False) #because the paste might be binary data

        session_key = params.session
        if not session_key:
            return j_e("Invalid Paste Request : Session Key is Required")

        if params.paste:
            if is_valid_session(session_key,web.ctx.ip):
                if save_paste(get_session_email(session_key,web.ctx.ip),web.ctx.ip,params.paste):
                    web.debug("PASTE (%s @ %s)" % (session_key,web.ctx.ip))
                    return j_s("Paste Successful")
                else:
                    web.debug("** FAILED **  PASTE (%s)" % (session_key))
                    return j_e("Failed  to Paste!")
            else:
                return j_e("This Session Key is Invalid")
        else:
            return j_e("No Data to Paste!")

class copy:
    def GET(self):
        return j_e("Not Supported")
    def POST(self):
        params = web.input(session=None)

        session_key = params.session
        if not session_key:
            return j_e("Invalid Copy Request : Session Key is Required")

        if is_valid_session(session_key,web.ctx.ip):
            email = get_session_email(session_key,web.ctx.ip)
            if clipboard_has_data(email):
                copy = pop_paste(email)
                safe_copy = copy.get('clipboard',None)
                if safe_copy is not None:
                    safe_copy = str(safe_copy)
                if copy is not None:
                    web.debug("COPY (%s @ %s)" % (session_key, web.ctx.ip))
                    return j_s(safe_copy,created=copy.get('created',None).strftime('%Y-%m-%d %H:%M:%S %z'), source_ip = copy.get('source_ip',None))
                else:
                    web.debug("** FAILED **  COPY (%s @ %s)" % (session_key,web.ctx.ip))
                    return j_e("Failed  to Copy!")
            else:
                return j_e("There's No Data on the Global Clipboard")
        else:
            return j_e("This Session Key is Invalid")

application = web.application(urls, globals()).wsgifunc()
