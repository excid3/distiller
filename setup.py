import os
import shutil

path = "~/.gnome2/rhythmbox/plugins"

def install():
    folder = os.path.expanduser(os.path.expandvars(path))

    if not os.path.exists(folder):
        os.makedirs(folder)

    folder = os.path.join(folder, "Distiller")
    os.mkdir(folder)
    shutil.copy("__init__.py", folder)
    shutil.copy("Distiller.rb-plugin", folder)
    shutil.copy("README", folder)

    print "Distiller installed correctly!"

if __name__ == "__main__":
    install()

