Are you writing a workhorse shell script in python? Why not curses?

This class, using curses, lets a user select from a simple list of options. The return is a simple list of selected options, or False (for cancel). And, for the OCD in all of us, it preserves terminal window contents after exiting.

![picker example](http://pp19dd.com/wp-content/uploads/2013/11/picker3.png "picker example")


### Usage example:

```python
from picker import *
    
opts = Picker(
    title = 'Select files to delete',
    options = [
        ".autofsck", ".autorelabel", "bin/", "boot/", 
        "cgroup/", "dev/", "etc/", "home/", "installimage.conf",
        "installimage.debug", "lib/", "lib64/", "lost+found/",
        "media/", "mnt/", "opt/", "proc/", "root/",
        "sbin/", "selinux/", "srv/", "sys/",
        "tmp/", "usr/", "var/"
    ]
).getSelected()

if opts == False:
    print "Aborted!"
else:
    print opts
```

If the user hits cancel, the routine returns a ```False``` - otherwise, you get a simple list:

```['.autofsck', '.autorelabel', 'bin/', 'boot/', 'cgroup/']```

The return, being a simple list, allows for a fairly readable logic:

```python
if "cgroup/" in opts:
	print "cgroup is done for!"
```


### What's missing:

Pretty much everything, but, this little routine is uncommonly handy in its current form. Elsewise:

* Ability to resize window.
* Page up/down keys.
* Select / unselect all.

### License / Usage Rights:

This code is available for use under CC0 (Creative Commons 0 - universal).  You can copy, modify, distribute and perform the work, even for commercial purposes, all without asking permission.  For more information, see LICENSE.md or https://creativecommons.org/publicdomain/zero/1.0/
