# !/usr/bin/python3

import os
lst = ['git pull', 'git add -A', 'git commit -m "Modified"', 'git push']
for i in lst:
    os.system(i)
