from asyncio import subprocess
import pandas as pd
from glob import glob
from tqdm import tqdm
import tarfile
import argparse
import os
import shutil
import sys

parser = argparse.ArgumentParser("Input which img folders are tar'd")
parser.add_argument(
    '--img_folder',
    type = str
)
args = parser.parse_args()

tar_name = f'{args.img_folder}.tar.gz'
#tar = tarfile.open(f'{os.path.abspath(args.data_dir)}/{tar_name}', "w:gz")
tar_path = f'tar_files/{args.img_folder}'

os.makedirs(tar_path, exist_ok=True)

tar = tarfile.open(f'{os.path.abspath(tar_path)}/{tar_name}', "w:gz")

path = f'imgs/{args.img_folder}/'
for i, val in enumerate(os.listdir(path)):
    if (os.path.isdir(val)):
        tar.add(f'imgs/{args.img_folder}/{val}', arcname=val)
        shutil.rmtree(f'imgs/{args.img_folder}/{val}')

tar.close()
