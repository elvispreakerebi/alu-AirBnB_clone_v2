#!/usr/bin/python3
"""Script that distributes an archive to web servers using paramiko"""

import os
import warnings
import paramiko
from paramiko import SSHClient
from scp import SCPClient

# Suppress all paramiko and cryptography related warnings
warnings.filterwarnings('ignore', category=Warning)

# Server configuration with provided values
WEB_01 = "18.206.168.44"
WEB_02 = "54.242.227.81"
SSH_USERNAME = "ubuntu"
SSH_KEY_PATH = "/Users/elviskerebi/.ssh/id_rsa"  # Use absolute path

def do_deploy(archive_path):
    """Distributes an archive to web servers using paramiko"""
    if not os.path.exists(archive_path):
        print(f"Error: Archive '{archive_path}' does not exist.")
        return False

    # Load private key
    try:
        key = paramiko.RSAKey.from_private_key_file(
            SSH_KEY_PATH,
            password=None  # Try without password first
        )
    except paramiko.ssh_exception.PasswordRequiredException:
        from getpass import getpass
        password = getpass('Enter SSH key password: ')
        try:
            key = paramiko.RSAKey.from_private_key_file(
                SSH_KEY_PATH,
                password=password
            )
        except Exception as e:
            print(f"Failed to load SSH key: {e}")
            return False

    file_name = os.path.basename(archive_path)
    file_noext = file_name.replace(".tgz", "")
    success = True

    try:
        for host in [WEB_01, WEB_02]:
            ssh = SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            
            try:
                # Connect with the loaded key
                ssh.connect(
                    hostname=host,
                    username=SSH_USERNAME,
                    pkey=key,
                    timeout=10
                )
                
                # Create SCP client
                with SCPClient(ssh.get_transport()) as scp:
                    # Upload the archive
                    scp.put(archive_path, f"/tmp/{file_name}")
                
                # Execute commands with sudo
                commands = [
                    f"sudo mkdir -p /data/web_static/releases/{file_noext}/",
                    f"sudo tar -xzf /tmp/{file_name} -C /data/web_static/releases/{file_noext}/",
                    f"sudo rm /tmp/{file_name}",
                    f"sudo mv /data/web_static/releases/{file_noext}/web_static/* /data/web_static/releases/{file_noext}/",
                    f"sudo rm -rf /data/web_static/releases/{file_noext}/web_static",
                    "sudo rm -rf /data/web_static/current",
                    f"sudo ln -s /data/web_static/releases/{file_noext}/ /data/web_static/current"
                ]
                
                for command in commands:
                    stdin, stdout, stderr = ssh.exec_command(command)
                    exit_status = stdout.channel.recv_exit_status()
                    if exit_status != 0:
                        error_msg = stderr.read().decode().strip()
                        raise Exception(f"Command '{command}' failed: {error_msg}")
                
                print(f"New version deployed to {host}!")
                
            except Exception as e:
                print(f"Error on {host}: {str(e)}")
                success = False
            
            finally:
                ssh.close()
        
        return success
        
    except Exception as e:
        print(f"An error occurred: {e}")
        return False

if __name__ == "__main__":
    archive_path = "versions/web_static_20250204145817.tgz"
    do_deploy(archive_path)
