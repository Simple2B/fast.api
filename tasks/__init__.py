# flake8: noqa F401

import os
import sys

sys.path.append(os.getcwd())

from .shell import shell
from .superuser import create_superuser
from .example import time
from .init_db import init_db
