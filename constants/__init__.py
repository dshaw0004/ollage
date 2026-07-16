import os
from pathlib import Path

# get home path
HOME = Path.home()

# folder to store this agent related infomations
app_dir = os.path.join(HOME, '.ol-agent')
