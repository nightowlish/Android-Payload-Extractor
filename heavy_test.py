import os
import time
import glob

for apk in glob.glob(r'tests\*'):
    if apk.startswith('!'):
        continue
    os.system(r'ctchr.py  extract {}'.format(os.path.abspath(apk)))
    time.sleep(120)