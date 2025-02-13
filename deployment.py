import logging
import os
import sys
import argparse
import subprocess
import paramiko
from dotenv import load_dotenv
from jinja2 import Environment, FileSystemLoader

load_dotenv()

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")

parse = argparse.ArgumentParser()
parse.add_argument("--script_name", type=str, required=True)
parse.add_argument("--args", type=str)

args = parse.parse_args()
script_args = dict(item.split("=", 1) for item in args.args.split())

logging.info(f"Args {script_args}")

# subprocess.run("pwd && touch shell.txt", shell=True)

env = Environment(loader=FileSystemLoader("scripts"))
template = env.get_template(f"{args.script_name}.sh")
config_content = template.render(script_args)

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

client.connect(
    hostname=os.getenv('HOST'),
    username=os.getenv('REMOTE_USER'),
    port=os.getenv('PORT')
)

client.exec_command(config_content)