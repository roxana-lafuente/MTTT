@ECHO OFF
REM -- Automates cygwin installation
REM -- Source: https://github.com/rtwolf/auto-cygwin-install
REM -- Based on: https://gist.github.com/wjrogers/1016065

SETLOCAL

REM -- Change to the directory of the executing batch file
CD %~dp0

REM -- Configure our paths
SET SITE=http://cygwin.mirrors.pair.com/
SET LOCALDIR=%CD%
SET ROOTDIR=C:/cygwin

REM -- These are the packages we will install (in addition to the default packages)
SET PACKAGES=mintty,wget,ctags,diffutils,git,git-completion,git-svn,stgit,mercurial,make,boost,automake,libtool,cmake,gcc-g++,python,girepository-WebKit3.0,git,subversion,openssh,tcl,zlib0,zlib-devel,libbz2_devel,unzip,libexpat-devel,libcrypt-devel,xorg-server,xinit,xlaunch,libgtk3-devel,python-gi,libwebkitgtk3,libwebkitgtk3.0_0,libwebkitgtk1,libwebkitgtk1.0_0,libwebkitgtk3.0-devel,libwebkitgtk1.0-devel,lxde-common,xorg-server,xinit,xlaunch
REM -- These are necessary for apt-cyg install, do not change. Any duplicates will be ignored.
SET PACKAGES=%PACKAGES%,wget,tar,gawk,bzip2,subversion

REM -- Do it!
ECHO *** INSTALLING DEFAULT PACKAGES
setup --quiet-mode --no-desktop --download --local-install --no-verify -s %SITE% -l "%LOCALDIR%" -R "%ROOTDIR%"
ECHO.
ECHO.
ECHO *** INSTALLING CUSTOM PACKAGES
setup -q -d -D -L -X -s %SITE% -l "%LOCALDIR%" -R "%ROOTDIR%" -P %PACKAGES%

REM -- Show what we did
ECHO.
ECHO.
ECHO cygwin installation updated
ECHO  - %PACKAGES%
ECHO.


PAUSE
EXIT /B 0
