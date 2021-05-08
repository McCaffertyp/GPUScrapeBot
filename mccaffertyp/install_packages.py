import sys
import subprocess


def install():
    try:
        subprocess.check_call([sys.executable, '-m', 'pip3', 'install', 'selenium'])
        subprocess.check_call([sys.executable, '-m', 'pip3', 'install', 'pynput'])
    except subprocess.CalledProcessError:
        print("Error running install command `pip3 install <package>`")
