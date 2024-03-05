#called whenever pod just starts up
#puts all data in persistent disk

import os
import subprocess
for file in os.listdir('/usr/src/app/data/current'):
    src = os.path.join('/usr/src/app/data/current', file)
    dst = os.path.join('/usr/src/app', file)
    subprocess.run(["mv", src, dst])
    # os.rename(src, dst)
