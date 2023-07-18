import os
import time
from tqdm import tqdm
from typing import Tuple
import click
import subprocess

from datetime import date, datetime

#-------------------------------global vars-----------------------------------#

FORMAT = "%Y-%m-%d %H:%M:%S"
FILE = "timecard.csv"
DIR = click.get_app_dir("Workhours")
FILE_PATH = os.path.join(DIR, FILE)


#--------------------------------functions------------------------------------#
