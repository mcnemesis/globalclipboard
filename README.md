globalclipboard
===============

Copy-Paste rules the World! The Uber-Geeks only need 1 Clipboard to rule them all - The Global-Clipboard!
Get it right here, or fork yourself one!

Motivation
-----------

Surely, ever copied something on your mobile device and wished you could paste it right then into a doc open on your laptop?

Or have you fired up multiple virtual machines (and had to hustle with clipboard sharing -- incompatible guest-additions, xclip hell, fifo tricks, ssh-paste-files, etc)

Oh, and what about sloppy work-arounds like emailing yourself the text, using multiple google-doc sessions, self-chating, etc just to share some text accross your many devices instantly? 

It's all not efficient and not as awesome too! Just think about it, I know u can!

I got fed up of doing things the _wrong_ way, and so I decided to shoot the zombies in the foot! 

This project is for you if *u just want only 1 clipboard to rule them all!*



How To
------

- Just install a clipboard client (check the list below for supported client-platforms)

- Do the simple one-time client configuration to link to a global-clipboard server you trust (there's in-built security, but u might want more).

- You only need a 1-time email-based activation for your account.

- Run you global-clipboard client and Rule the world! 

Once your device(s) are linked to the global-clipboard, anything you copy on any of them instantly becomes available on your clipboard(s) on all linked devices.

- Each client supports the ability to Turn-Off the service, once you want to save it for later.



Supported Clients
------------------

- **Python-Supporting Platforms (windows, mac, *nix):**

  Under the *clients* directory of this project, you will find a ready-to-use client for python-supporting platforms (reliably tested on Suse 11.4 for now).

  This awesome python client works, thanks to the cross-platform clipboard project pyperclip [Al Sweigart http://coffeeghost.net/src/pyperclip.py], and the remarkable HTTP-for-humans project python-requests [Kenneth Reitz https://github.com/kennethreitz/requests].

  You might want to check the included README for your client on how to setup and ejoy the service just the best way.


  
Available Global-Clipboard Servers / Hosts:
-------------------------------------------

- **You can Host your Own**

  Because of the delicate nature of placing one's clibboard on the wire (much as ther's in-bult security), you are free to setup your own global-clibboard server (instructions below), limited to and only accessible behind your firewall, within your LAN or VPN.

  Such a setup shouldn't be hard for anyone ready to follow the available docs or community guides (or even better, looking at the code). Find hints for doing this somewhere below...


- **Public Global-Clipboard**:

  You can point your client right at the globally-accessible Global-Clipboard service. 
  
  [This is gonna be ready for all of us to enjoy as soon as securing a reliable host for this is done - join in and make this real!]


Setting up Own Global Clipboard Server (e.g on LAN):
-----------------------------------------------------

- The globalclipboard server is built with Python using the awesome and minimal web-framework web.py [https://github.com/webpy/webpy]

- It also uses the Open-Source Postgresql as the database backend (a little tweak to the code should make it work with any db backend u fancy though)

- I recommend you run your server as a WSGI app [I've tested with an Apache container], but you could also just fire it up straight on the commandline like a good-ol' py, because web.py supports this!

- The server has little in terms of configuration, but you might want to change a few things in terms of logging (don't resist peeking at the server.py file)

- The server is just 1 file *only*, so reading and making changes to the code should be fun for those that want to sweat the technique ;-)


I might setup a google-group, or u can drop a request / ticket right here on github in case of anything.

This is just a sort o glorified weekend project, but am sure it gets the job done! And it's opensource, so feel free to mess with it, and fork!

Don't u forget this one truth: copy-paste runs the world [sometimes].
