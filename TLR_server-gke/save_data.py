#this file is called whenever the pod is about to restart
#It saves all needed data to the persistent disk
#path to save: /usr/src/app/data/current
#if the server is crashing and files are still needed, put them in data/current

import os
import subprocess
for file in os.listdir('/usr/src/app'):
    if file.endswith('_motion_data.txt') or file.endswith('_hr_data.txt') or file.endswith('_labels.txt') or file.endswith('_times.txt') or file == 'updates.txt':
        if file == 'undefined_motion_data.txt': continue
        src = os.path.join('/usr/src/app', file)
        dst = os.path.join('/usr/src/app/data/current', file)
        subprocess.run(["mv", src, dst])

