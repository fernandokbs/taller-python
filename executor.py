from jinja2 import Environment, FileSystemLoader
import logging
import os
import sys
import argparse
import subprocess
import paramiko
from celery import Celery

app = Celery('tasks', broker='redis://localhost:6379/0')

@app.task
def exec_command(script):
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        client.connect(
            hostname="10.176.186.145",
            username="ubuntu",
            port="22"
        )

        client.exec_command(script)
    except Exception as e:
        print(f"Error al conectar: {e}")
    finally:
        client.close()

class Executor:
    def __init__(self, script_name, args):
        self.script_name = script_name
        self.args = args

    def run(self):
        template = self.get_template()
        self.execute(template)

    def execute(self, script):
        exec_command.delay(script)

    def get_template(self):
        env = Environment(loader=FileSystemLoader("scripts"))
        template = env.get_template(f"{self.script_name}.sh")
        return template.render(self.args)

