globalclipboard
===============

Copy-Paste rules the World! The Uber-Geeks only need 1 Clipboard to rule them all - The Global-Clipboard!
Get it right here, or fork yourself one!

NOTE: The entire project is currently GPL3 Licensed.

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

- Just install a clipboard client u trust and like (our client provides client-side Gnu-PG [En|De]cryption (PKI Cryptography) and is python-based)

- Do the simple one-time client configuration to link to a global-clipboard server u fancy (there's supposed to be in-built security in each client, so in terms of security, the client is all that matters).
    - might involve one-time registration of your account, something like:

    curl --form "email=myemail@domain.com" --form "password=password" http://global_clipboard_server/clip/register

- You only need a 1-time email-based activation for your account (activation link emailed to u)

- Run you global-clipboard client and Rule the world! 

Once your device(s) are linked to the global-clipboard, anything you copy on any of them instantly becomes available on your clipboard(s) on all linked devices.

- A client could support the ability to Turn-Off the service (or toggle it on/off) on demand.



Supported Clients
------------------

- **Python-Supporting Platforms (windows, mac, *nix):**

  Under the *clients* directory of this project, you will find a ready-to-use client for python-supporting platforms (reliably tested on OpenSuse 11.4,12.1 and 12.2 for now).

  This awesome python client works, thanks to the cross-platform clipboard project pyperclip [Al Sweigart http://coffeeghost.net/src/pyperclip.py], and the remarkable HTTP-for-humans project python-requests [Kenneth Reitz https://github.com/kennethreitz/requests].

  This client also utilizes GNU-pg via python-gnupg, for (d)encryption to ensure your clipboard contents are secure to and from the global-clipboard, and that they can *only* be read in their original form only on devices with your GNU-pg Private Key (at the server, we don't need to know your copy-paste contents at all!).

  You might want to check the included README for your client on how to setup and ejoy the service just the best way.

  NOTE : 
    - This client requires the python-gnupg Python package (check installation info here http://packages.python.org/python-gnupg/). 
    - It also assumes that the clibboard server sends back clipboard content encoded in base64 (which is the current server's default behaviour)
    - This client comes along with an Optional GUI Front-end called **GClip**, built using QT4 and PyQt4 (and currently tested on KDE4 platforms only)

  
Available Global-Clipboard Servers / Hosts:
-------------------------------------------

- **You can Host your Own**

  Because of the delicate nature of placing one's clibboard on the wire (much as ther's in-built security in the client say), you are free to setup your own trusted global-clibboard server (instructions below), limited to and only accessible behind your firewall, within your LAN or VPN.

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
