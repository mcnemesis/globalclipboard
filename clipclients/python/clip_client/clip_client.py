#!/usr/bin/env python

import json
import pyperclip
import os
import errno
import logging
import requests
from threading import Timer
import gnupg
import random

try:
    from cStringIO import StringIO
except:
    from StringIO import StringIO


def get_random_str(alphabet=None):
    al = list(alphabet or 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890_|{()-+!~\\/*&^%$#@')
    random.shuffle(al)
    p = ''.join(al[0:random.randrange(1,len(al)/2)])
    return p

def make_sure_path_exists(path):
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise BaseException('Path Doesn\'t Exist : %s' % path)

class ActionMode:
    EXIT = -1
    NONE = 0
    RECEIVE_SEND = 1
    SEND_ONLY = 2
    RECEIVE_ONLY= 3

class GClipClient:
    """
    Main Global Clipboard Client for Python

    Other Python-based Clients (like the GClip UI can subclass / import this)
    """
    VERSION = '1.1'
    DEFAULT_HOME = '~/.global_clip'
    CONF_FILE='%s/client.conf' % DEFAULT_HOME
    GPG_HOME = '%s/.gpg' % DEFAULT_HOME
    DEFAULT_KEYFILE = '%s/.keys' % DEFAULT_HOME
    DEFAULT_SESSION = '%s/.session' % DEFAULT_HOME


    _current_action_mode = ActionMode.NONE

    #----------- helpers --------------------

    @staticmethod
    def encrypt_file(in_s, out_s,email):
        gpg = gnupg.GPG(gnupghome=os.path.expanduser(GClipClient.GPG_HOME))
        unencrypted_string = in_s.read()
        encrypted_data = gpg.encrypt(unencrypted_string,email,always_trust=True)
        if encrypted_data.ok:
            encrypted_string = str(encrypted_data)
            out_s.write(encrypted_string)
        else:
            raise BaseException("Encrption Failed!\n\n%s" % encrypted_data.stderr)

    @staticmethod
    def decrypt_file(in_s, out_s, mypassword):
        gpg = gnupg.GPG(gnupghome=os.path.expanduser(GClipClient.GPG_HOME))
        encrypted_string = in_s.read()
        decrypted_data = gpg.decrypt(encrypted_string, passphrase=mypassword,always_trust=True)
        if decrypted_data.ok:
            out_s.write(decrypted_data.data)
        else:
            raise Exception("Decryption Failed!\n\n%s" % decrypted_data.stderr)

    def save_conf(self,conf):
        if conf:
            try:
                with open(os.path.expanduser(GClipClient.CONF_FILE),'w') as f:
                    f.write(json.dumps(conf, sort_keys=True, indent=4))
            except:
                logging.error("Failed to Save Configuration file")

    def save_session(self,conf,session_key):
        if session_key:
            try:
                with open(os.path.expanduser(conf['sessions']['session_file']),'w') as f:
                    f.write(session_key)
                logging.info("Saved Session Key")
            except:
                logging.error("Failed to write Session file")

    def get_session(self,conf):
        if conf is None:
            return None
        else:
            key = None
            try:
                with open(os.path.expanduser(conf['sessions']['session_file']),'r') as f:
                    key = f.readline()
            except:
                logging.error("Failed to read Session File")
            return key

    def credentials(self,conf):
        return conf['account']

    def create_save_gpgkeys(self,key_file,myemail,mypassphrase):
        file_path = os.path.expanduser(key_file)
        gpg_home = os.path.expanduser(GClipClient.GPG_HOME)
        os.system('rm -rf %s' % gpg_home)

        #use default gpg home
        gpg = gnupg.GPG(gnupghome=gpg_home)

        if not os.path.exists(file_path):
            #create key associated with configure email and passphrase
            input_data = gpg.gen_key_input(
                            name_email=myemail,
                            passphrase=mypassphrase)
            key = gpg.gen_key(input_data)
            ascii_armored_public_keys = gpg.export_keys(key)
            ascii_armored_private_keys = gpg.export_keys(key, True)
            #save the keys (public + private) to file
            with open(file_path, 'w') as f:
                    f.write(ascii_armored_public_keys)
                    f.write(ascii_armored_private_keys)

        #then import them into our keyring..
        key_data = open(file_path).read()

        #TODO:ensure key importing works fine
        import_result = gpg.import_keys(key_data)

        #hoping all is good...
        return True

    def get_encryptionconf(self,conf):
        econf = {
            'keyfile' : None,
        }


        creds = self.credentials(conf)

        if 'email' not in creds:
            raise BaseException("No Email Configured. Can't Use Encryption!")

        if 'password' not in creds:
            raise BaseException("No Password Configured. Can't Use Encryption!")

        if 'crypto' in conf:
            econf.update(conf.get('crypto',{}))

            from pprint import pprint

        key_file = econf.get('keyfile',None)

        if (econf['keyfile'] is None) or (os.path.exists(os.path.expanduser(key_file))):
            key_file = GClipClient.DEFAULT_KEYFILE
            if self.create_save_gpgkeys(key_file,creds['email'],creds['password']):
                econf['keyfile'] = key_file
            else:
                raise BaseException("[En|De]cryption Key File Creation Failed!")

        econf.update({'email' : creds['email'],'password' : creds['password']})

        return econf

    def encrypt_clip(self,text,econf):
        if econf['email'] is not None:
                in_s = StringIO(text)
                out_s = StringIO()
                self.encrypt_file(in_s,out_s,econf['email'])
                return out_s.getvalue()
        else:
            raise BaseException("No [En|De]cryption Email Configured Yet!")

    def decrypt_clip(self,text,econf):
        if econf['password'] is not None:
                in_s = StringIO(text)
                out_s = StringIO()
                self.decrypt_file(in_s,out_s,econf['password'])
                return out_s.getvalue()
        else:
            raise BaseException("No [En|De]cryption Password Configured Yet!")


    #-------------- End Helpers ----------------

    #-------------- Instance -------------------
    #default conf
    _conf = {
        "server" : {
            "url" : "http://localhost/clip"
        },

        "account" : {
            #this must actually be an email address. maybe use valid random emails from a service?
            "email" : get_random_str(alphabet='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890_'),
            "password" : get_random_str()
        },

        "clipboard" : {
            "intervals" : {
                "copy" : 10,
                "paste" : 10
            }
        },

        "sessions" : {
            "session_file" : DEFAULT_SESSION,
            "allow_reset" : "true"
        },

        "logging" : {
            "log_file" : "/tmp/global_clip.log"
        },
        "crypto" : {
            "keyfile" : DEFAULT_KEYFILE
        }
    }

    def __init__(self):
        make_sure_path_exists(os.path.dirname(os.path.expanduser(GClipClient.CONF_FILE)))
        self.__load_conf()
        self.__init_logs()
        self._current_action_mode = ActionMode.NONE


    def __load_conf(self):
        user_conf = None
        try:
            with open(os.path.expanduser(GClipClient.CONF_FILE),'r') as f:
                user_conf = json.loads(''.join(f.readlines()))
                if type(user_conf) is not dict:
                    raise BaseException("Invalid Conf!")
        except:
            print "Failed to Read Conf File"

        self._conf.update(user_conf if user_conf is not None else {})

        if user_conf is None:
            print "No valid User Configuration found, proceeding with defaults"
            self.save_conf(self._conf)
        else:
            self.save_conf(self._conf)#just incase user never defined some defaults...

    def __init_logs(self):
        print "Starting with Log : %s " % self._conf['logging']['log_file']
        logging.basicConfig(level=logging.INFO, filename=self._conf['logging']['log_file'])
        logging.info("Starting Global Clipboard Client [version %s]" % GClipClient.VERSION)

    def start(self,action_mode=ActionMode.RECEIVE_SEND):
        self._current_action_mode = ActionMode.NONE

        logging.info('Starting GlobalClip Client')

        if action_mode == ActionMode.RECEIVE_SEND:
            self.toggle_send_recieve()
        elif action_mode == ActionMode.RECEIVE_ONLY: 
            self.toggle_recieve_only()
        elif action_mode == ActionMode.SEND_ONLY: 
            self.toggle_send_only()
        elif action_mode == ActionMode.NONE: 
            self.toggle_stop_client()
        else:
            self.exit()
            return
        
        self._current_action_mode = action_mode
        self.local_clipboard = None
        self.session_key = self.get_session(self._conf)
        self.creds = self.credentials(self._conf)
        self.encryption_conf = self.get_encryptionconf(self._conf)

        self.run_clipclient()

    def run_clipclient(self):
        self.__run_clipclient()

    def toggle_stop_client(self):
        if self._current_action_mode == ActionMode.EXIT:
            warn = "GlobalClip Client is in EXIT mode. You have to call start() first, to toggle the Action Mode"
            logging.error(warn)
            print warn
        else:
            logging.info('Pausing GlobalClip Client')
            self._current_action_mode = ActionMode.NONE

    def toggle_send_only(self):
        if self._current_action_mode == ActionMode.EXIT:
            warn = "GlobalClip Client is in EXIT mode. You have to call start() first, to toggle the Action Mode"
            logging.error(warn)
            print warn
        else:
            logging.info('Toggle GlobalClip Client to SEND ONLY')
            self._current_action_mode = ActionMode.SEND_ONLY

    def toggle_recieve_only(self):
        if self._current_action_mode == ActionMode.EXIT:
            warn = "GlobalClip Client is in EXIT mode. You have to call start() first, to toggle the Action Mode"
            logging.error(warn)
            print warn
        else:
            logging.info('Toggle GlobalClip Client to RECEIVE ONLY')
            self._current_action_mode = ActionMode.RECEIVE_ONLY

    def toggle_send_recieve(self):
        if self._current_action_mode == ActionMode.EXIT:
            warn = "GlobalClip Client is in EXIT mode. You have to call start() first, to toggle the Action Mode"
            logging.error(warn)
            print warn
        else:
            logging.info('Toggle GlobalClip Client to SEND+RECEIVE')
            self._current_action_mode = ActionMode.RECEIVE_SEND

    def exit(self):
        if self._current_action_mode == ActionMode.EXIT:
            warn = "GlobalClip Client is already in EXIT mode."
            logging.error(warn)
            print warn
        else:
            logging.info('Exiting GlobalClip Client')
            self._current_action_mode = ActionMode.EXIT

    def __run_clipclient(self):
        """
        With consideration for the current global client state:
            Periodically check for new items on the local clipboard and paste them onto the global clip.
            Similarly, check for new items on the global clipboard and copy them onto the local clip
        """
        if self._current_action_mode == ActionMode.NONE:
            t = Timer(10,self.run_clipclient) 
            t.start()
        elif self._current_action_mode == ActionMode.EXIT:
            pass #we should now quit once no more timers are running
        else:
            t = None
            if  self.session_key is  None:
                #try to get a session...
                r = requests.request('post',"%s/session" % self._conf['server']['url'], data = {'email' : self.creds['email'] , 'password' : self.creds['password'] })
                rj = r.json
                if r.ok and rj['status'] == 200:
                    self.session_key = rj['payload']
                    self.save_session(self._conf,self.session_key)
                    logging.info('Obtained New Session Key')
                else:
                    logging.error('Failed to obtain New Session Key [%s]' % rj['payload'])

            if self.session_key is None:
                #try to login then...
                r = requests.request('post',"%s/register" % self._conf['server']['url'], data = {'email' : self.creds['email'] , 'password' : self.creds['password'] })
                rj = r.json
                if r.ok and rj['status'] == 200:
                    logging.info("Registration Successfull: %s" % rj['payload'])
                    #since's we've just registered... give user 1 min to complete registration before using clip client again
                    t = Timer(60,self.run_clipclient) 
                else:
                    logging.error("Registration Not Completed : %s" % rj['payload'])
                    #possibly, registration not complete yet or activation not yet done. delay for like 2 min now before trying again
                    t = Timer(120,self.run_clipclient) 
            else:
                #we have session key, so...
                #check if there's anything here on the clipboard that needs to be copied over...
                current_local_clip = pyperclip.paste()

                if (self._current_action_mode == ActionMode.RECEIVE_SEND ) or (self._current_action_mode == ActionMode.SEND_ONLY):
                    if self.local_clipboard != current_local_clip:
                        #there's new stuff on the local clip to copy over...
                        #First, secure the paste...
                        secure_local_clip = self.encrypt_clip(current_local_clip,self.encryption_conf)
                        #then send
                        r = requests.request('post',"%s/paste" % self._conf['server']['url'], data = {'session' : self.session_key , 'paste' : secure_local_clip })
                        rj = r.json
                        if r.ok and rj['status'] == 200:
                            logging.debug('Copying to Global Clipboard Successful : %s' % rj['payload'])
                            self.local_clipboard = current_local_clip
                            t = Timer(10,self.run_clipclient) 
                        else:
                            try:
                                print secure_local_clip
                                logging.error('Copying to Global Clipboard Failed : %s' % rj['payload'])
                            except Exception as e:
                                logging.error('Fatal Error while trying to Copy to Clipboard : %s' % e)
                            t = Timer(30,self.run_clipclient) 
                    else:
                        logging.debug("Local Clip : old")
                        t = Timer(10,self.run_clipclient) 

                if (self._current_action_mode == ActionMode.RECEIVE_SEND ) or (self._current_action_mode == ActionMode.RECEIVE_ONLY):
                    #get the remote / global clip contents if any...
                    r = requests.request('post',"%s/copy" % self._conf['server']['url'], data = {'session' : self.session_key })
                    rj = r.json
                    if r.ok and rj['status'] == 200:
                        secure_global_clipboard = rj['payload']
                        #we expect data to be sent encoded base64
                        secure_global_clipboard = secure_global_clipboard.decode('base64')
                        #First, decrypt the stuff...
                        global_clipboard = self.decrypt_clip(secure_global_clipboard,self.encryption_conf)
                        if global_clipboard != self.local_clipboard:
                            pyperclip.copy(global_clipboard)
                            self.local_clipboard = global_clipboard
                            logging.info("Found new Data on Global Clip from IP : %s" % (rj['source_ip'])) 
                            t = Timer(10,self.run_clipclient) 
                        else:
                            logging.debug("Global Clip : old")
                            t = Timer(10,self.run_clipclient) 
                    else:
                        try:
                            logging.error("Failed to Read Global Clip : %s " % rj['payload'])
                            t = Timer(30,self.run_clipclient) 
                        except Exception as e:
                            logging.error("Exception : %s" % e)

            if t:
                t.start() #schedule next run of the clip client...


if __name__ == '__main__':
    gclip_client = GClipClient()
    gclip_client.start()
