Are you writing a workhorse shell script in python?

Why not curses?

This class, using curses, lets a user select from a simple list of options. The return is a simple list of selected options, or False (for cancel).

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

If the user hits cancels, the routine returns a ```False``` - otherwise, you get a simple list:

```['.autofsck', '.autorelabel', 'bin/', 'boot/', 'cgroup/']```
