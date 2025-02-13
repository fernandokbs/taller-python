import logging
import os
import sys
import argparse
import subprocess
import paramiko
from dotenv import load_dotenv
from jinja2 import Environment, FileSystemLoader
from executor import Executor

load_dotenv()

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")

parse = argparse.ArgumentParser()
parse.add_argument("--script_name", type=str, required=True)
parse.add_argument("--args", type=str)

args = parse.parse_args()
script_args = dict(item.split("=", 1) for item in args.args.split())

logging.info(f"Args {script_args}")

# subprocess.run("pwd && touch shell.txt", shell=True)

executor = Executor(args.script_name, script_args)
executor.run()