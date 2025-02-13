from jinja2 import Environment, FileSystemLoader
import logging
import os
import sys
import argparse
import subprocess
import paramiko

class Executor:
    def __init__(self, script_name, args):
        self.script_name = script_name
        self.args = args

    def run(self):
        template = self.get_template()
        self.execute(template)

    def execute(self, script):
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        client.connect(
            hostname=os.getenv('HOST'),
            username=os.getenv('REMOTE_USER'),
            port=os.getenv('PORT')
        )

        client.exec_command(script)

    def get_template(self):
        env = Environment(loader=FileSystemLoader("scripts"))
        template = env.get_template(f"{self.script_name}.sh")
        return template.render(self.args)

