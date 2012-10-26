globalclipboard
===============

Copy-Paste rules the World! So U need only 1 Clipboard to rule them all  - GlobalClipboard!

Motivation
-----------

Surely, ever copied something on your mobile device and wished you could paste it right then into a doc open on your laptop?
Or have you fired up multple virtual machines (and had to hustle with clipboard sharing -- incompatible guest-additions, xclip hell, fifo tricks, ssh-paste-files, etc)

Oh, and what about emailing yourself something, using google doc sessions, self-chating, etc just to share some text accross your
many devices instantly? It's all not efficient enough if you think of how many copy-paste operations you have to invoke. 

I got fed up of doing things the wrong way, and so I decided to solve this once and for all! So, in comes one clipboard to rule them all - GlobalClipboard.

How To
------

- Just install a clipboard client (check the list below for supported client-platforms)

- Perform a one-time client configuration to link to a global-clipboard server you trust (yes, I am well aware of how placing your
clipboard on the wire can be attractive to the evil dude next door, and am taking care of all that for u -- see below).

- You might have to activate your global-clipboard account by opening the activation link given in your e-mail (so no one should be able to
activate on your behalf easily). Activation is only necessary once on just one of the devices, next time it's all configure-n-play

- Rule the world! Once the client is running, just copy something on any of your connected devices, and it instally appears on the clipboard
of any of your other connected devices. 

Copy-once-paste-anywhere! And the rules of copying and pasting stay just the same as what your current device/ platform supports!
Apart from setting up the clients, all copy-paste with globalclipboard happens transparently from you, so u don't have to worry.

- Turn off the global-clipboard once u don't want to make the service [ check your client's options ]

Supported Clients
------------------

-- *Python-Supporting Platforms (windows, mac, *nix):*
  Under the *clients* directory of this project, you will find a read-to-use client for pythong-supporting platforms (though I've only tested this on a standard platform -- OpenSuse 11.4 ;-)
  
  You have to check the included README for that client, for how to setup the client on your platform, then install, configure, and enjoy!


Available Global-Clipboard Servers / Hosts:
-------------------------------------------

-- *You can Host your Own*
  Because of the delicate nature of placing one's clibboard on the wire (much as ther's security in-built in the app), it depends on what client you choose, and 
  what you are placing on the clipboard. But, no matter what, you are free to setup your own global-clibboard server (instructions below), limited to only your LAN for example.

-- *Public Global-Clipboard (on EC2)*:
  I've attempted to setup a freely available global-clipboard server on ec2, so that anyone can quickly try-out and use the service without much hustle, but I can't yet guarrantee that it'll
  be able to serve *real global traffic* before I push some more resources into this project. But this is opensource, and am sure some nice peeps might pick interest.

Setting up Own Global Clipboard Server (e.g on LAN):
-----------------------------------------------------

-- The globalclipboard server is built with Python using the awesome and minimal web-framework web.py
-- It also uses Postgresql as the database backend (but I guess a little change to the code should make it work with any db backend u fancy -- web.py takes care of this)
-- Because it's a web.py app, I would recommend you run this as a WSGI app in an Apache container, but you could also just fire it up straight on the commandline like any python program -- web.py is awesome!
-- The server has little in terms of configuration, but you might want to change a few things in terms of logging (look at the server.py file)
-- The server is just one file, so reading and making changes to the code should be a hustle for those that want to sweat the technique ;-)


I might setup a google-group, or u can drop a request / ticket right here on github in case of anything.

This is just a sort o glorified weekend(s) project, and it's opensource, so feel free to mess with it, and fork!

Recall, the world runs on Copy-N-Paste.


