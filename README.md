# TTT: Translators' Training Tool



## Machine translation made easy for human translators!
TTT is an under development post-editing suite which aims to improve the translators experience with machine translation tools such as moses. It provides the user with a graphical user interface to:

- Work with the moses machine translation pipeline.
- Apply metrics such as BLEU.
- Post-edit the obtained machine translation.



### Authors
- Paula Estrella
- Roxana Lafuente
- Miguel Lemos



### Features
- Portable (Windows / Linux)



### Dependencies

#### Source code

##### On Linux
- MOSES (Install with "--with-mm" and "--install-scripts" flags)
- GTK 3.0
- Also, you should link /bin/sh to /bin/bash and not to bin dash. To do that:
	- Check the link:
	```
	ls -l /bin/sh
	```
	- If /bin/sh is a link to /bin/dash, change it to /bin/bash.
	```
	sudo mv /bin/sh /bin/sh.orig
	sudo ln -s /bin/bash /bin/sh
	```
This is necessary to use the redirection commands used by MOSES commands.

##### On Windows
- MOSES (Install with "--with-mm" and "--install-scripts" flags)
- Cygwin (only on Windows)
	- gi (python-gi)
	- gobject (python-gobject)
	- GTK 3.0 ()



#### Binaries (portable)
More details on this soon!



### Status
- Under development



### How to use

#### Source code

##### On Linux
Simply install all dependencies and run:
```
python main.py
```
######How to install the dependencies on ubuntu:

```sudo apt-get install python gobject```  to install GTK 3.0

```sudo apt-get install gir1.2-webkit-3.0``` to instal WebKit 3.0

```sudo python main.py``` to install pip, if needed to

##### On Windows

Run LXDE or any other X window environment from CygWin. From inside LXDE or your favorite one run:

```
python main.py
```

#### Binaries (portable)
More details on this soon!
