#!/usr/bin/python3
"""Fabric script that creates and distributes an archive to web servers"""

import os
import time
import tarfile
from datetime import datetime
from fabric import Connection, Config
import paramiko
from paramiko import SSHClient
from scp import SCPClient

# Server configuration
WEB_01 = "18.206.168.44"
WEB_02 = "54.242.227.81"
SSH_USERNAME = "ubuntu"
SSH_KEY_PATH = "/Users/elviskerebi/.ssh/id_rsa"

def do_pack():
    """
    Generates a .tgz archive from the contents of web_static folder
    """
    try:
        # Create versions directory if it doesn't exist
        if not os.path.exists("versions"):
            os.makedirs("versions")

        # Create archive name using timestamp
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        archive_path = f"versions/web_static_{timestamp}.tgz"

        # Create tar archive
        print(f"Packing web_static to {archive_path}")
        with tarfile.open(archive_path, "w:gz") as tar:
            tar.add("web_static", arcname="web_static")

        # Get archive size
        archive_size = os.path.getsize(archive_path)
        print(f"web_static packed: {archive_path} -> {archive_size}Bytes")

        return archive_path
    except Exception as e:
        print(f"An error occurred while packing: {e}")
        return None

def do_deploy(archive_path):
    """Distributes an archive to web servers using paramiko"""
    if not os.path.exists(archive_path):
        print(f"Error: Archive '{archive_path}' does not exist.")
        return False

    try:
        key = paramiko.RSAKey.from_private_key_file(SSH_KEY_PATH)
        file_name = os.path.basename(archive_path)
        file_noext = file_name.replace(".tgz", "")
        success = True

        for host in [WEB_01, WEB_02]:
            ssh = SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            
            try:
                ssh.connect(
                    hostname=host,
                    username=SSH_USERNAME,
                    pkey=key,
                    timeout=10
                )
                
                with SCPClient(ssh.get_transport()) as scp:
                    scp.put(archive_path, f"/tmp/{file_name}")
                
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

def deploy():
    """
    Creates and distributes an archive to web servers
    """
    # Create archive
    archive_path = do_pack()
    if not archive_path:
        return False
    
    # Deploy archive
    return do_deploy(archive_path)

if __name__ == "__main__":
    deploy()