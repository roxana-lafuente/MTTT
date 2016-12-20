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

##### About Linux
- You should link /bin/sh to /bin/bash and not to bin dash. To do that:
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


##### On Ubuntu
	- MOSES (Install with "--with-mm" and "--install-scripts" flags)
	- To install its dependencies run

		```
		python ubuntu_install.py
		```

##### On Windows using Cygwin
	- MOSES (Install with "--with-mm" and "--install-scripts" flags)
	- To install Cygwin and its dependencies run
		
		```
		python cygwin_install.py
		```
##### On Windows
- MOSES (Install with "--with-mm" and "--install-scripts" flags)
- the following installer is recommended:
	[https://sourceforge.net/projects/pygobjectwin32/files/pygi-aio-3.18.2_rev10-setup_84c21bc2679ff32e73de38cbaa6ef6d30c628ae5.exe/download](https://sourceforge.net/projects/pygobjectwin32/files/pygi-aio-3.18.2_rev10-setup_84c21bc2679ff32e73de38cbaa6ef6d30c628ae5.exe/download)

	- visual installation guide:

	![Screenshot](./installation/windows_guide/GTK.png)

	![Screenshot](./installation/windows_guide/Webkit.png)





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
##### On Windows

Run LXDE or any other X window environment from CygWin. From inside LXDE or your favorite one run:

```
python main.py
```

#### Binaries (portable)
More details on this soon!
