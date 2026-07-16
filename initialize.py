import os
import sys
from constants import app_dir

sys.path.append(
    os.path.abspath(
        os.path.dirname(
            os.path.realpath(__file__)
        )
    )
)
if not os.path.exists(app_dir):
    os.makedirs(name=app_dir, exist_ok=True)
