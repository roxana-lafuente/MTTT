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
- MOSES (Install with "--with-mm" and "--install-scripts" flags)
- Cygwin (only on Windows)
- GTK 3.0 (only on Linux)
- On Linux you should link /bin/sh to /bin/bash and not to bin dash. To do that:
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


### Status
- Under development



### How to use
```
python main.py
```
