#!/usr/bin/python3
"""Fabric configuration file that imports and exposes the do_pack and do_deploy tasks."""

from fabric import Connection, Config, task
from datetime import datetime
import os
from os import environ
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get host servers from environment variables
WEB_01 = environ.get('WEB_01')
WEB_02 = environ.get('WEB_02')
HOSTS = [host for host in [WEB_01, WEB_02] if host]

# Get SSH configuration from environment variables
SSH_USERNAME = environ.get('SSH_USERNAME', 'ubuntu')
SSH_KEY_PATH = environ.get('SSH_KEY_PATH')

# Validate configuration
if not HOSTS:
    raise ValueError("No web servers configured. Please set WEB_01 and/or WEB_02 environment variables.")
if not SSH_KEY_PATH:
    raise ValueError("SSH key path not provided. Please set SSH_KEY_PATH environment variable.")

def do_pack():
    """Generates a .tgz archive from the contents of the web_static folder."""
    try:
        # Get the current working directory
        current_dir = os.path.dirname(os.path.abspath(__file__))
        web_static_path = os.path.join(current_dir, 'web_static')
        versions_path = os.path.join(current_dir, 'versions')

        # Check if web_static directory exists
        if not os.path.isdir(web_static_path):
            print(f"Error: {web_static_path} directory not found")
            return None

        # Ensure the 'versions' directory exists
        if not os.path.exists(versions_path):
            os.makedirs(versions_path)

        # Generate timestamped archive name
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        archive_name = os.path.join(versions_path, f"web_static_{timestamp}.tgz")

        # Create the archive using local connection
        print(f"Packing web_static to {archive_name}")
        c = Connection('localhost')
        result = c.local(f"cd {current_dir} && tar -czvf {archive_name} web_static/")

        # Check if archive was created successfully
        if result.ok and os.path.exists(archive_name):
            return archive_name
        return None

    except Exception as e:
        print(f"Error: {e}")
        return None

from fabric import task

@task
def deploy(c, archive_path="versions/web_static_20250204145817.tgz"):
    """Deploy web static files to servers
    
    Args:
        c: Connection object
        archive_path: Path to the archive file
    
    Returns:
        True if successful, False otherwise
    """
    if not os.path.exists(archive_path):
        return False

    try:
        # Get filename without extension and full filename
        file_name = os.path.basename(archive_path)
        folder_name = file_name.replace('.tgz', '')

        for host in HOSTS:
            # Create a connection with SSH configuration
            config = Config(overrides={'load_ssh_config': True})
            conn = Connection(
                host=host,
                user=SSH_USERNAME,
                connect_kwargs={
                    'key_filename': os.path.expanduser(SSH_KEY_PATH)
                },
                config=config
            )

            # Upload archive to /tmp/
            conn.put(archive_path, '/tmp/')

            # Create target directory
            conn.run(f'mkdir -p /data/web_static/releases/{folder_name}/')

            # Extract archive
            conn.run(f'tar -xzf /tmp/{file_name} -C /data/web_static/releases/{folder_name}/')

            # Remove archive
            conn.run(f'rm /tmp/{file_name}')

            # Move extracted files to proper location
            conn.run(f'mv /data/web_static/releases/{folder_name}/web_static/* '
                f'/data/web_static/releases/{folder_name}/')

            # Remove now-empty web_static directory
            conn.run(f'rm -rf /data/web_static/releases/{folder_name}/web_static')

            # Remove current symbolic link
            conn.run('rm -rf /data/web_static/current')

            # Create new symbolic link
            conn.run(f'ln -s /data/web_static/releases/{folder_name}/ /data/web_static/current')

            print(f'New version deployed to {host}!')
        return True

    except Exception as e:
        print(f'Error: {e}')
        return False
    """Distributes an archive to web servers.
    
    Args:
        archive_path: Path to the archive file
    
    Returns:
        True if successful, False otherwise
    """
    if not os.path.exists(archive_path):
        return False

    try:
        # Get filename without extension and full filename
        file_name = os.path.basename(archive_path)
        folder_name = file_name.replace('.tgz', '')

        for host in HOSTS:
            # Create a connection with SSH configuration
            config = Config(overrides={'load_ssh_config': True})
            c = Connection(
                host=host,
                user=SSH_USERNAME,
                connect_kwargs={
                    'key_filename': os.path.expanduser(SSH_KEY_PATH)
                },
                config=config
            )

            # Upload archive to /tmp/
            c.put(archive_path, '/tmp/')

            # Create target directory
            c.run(f'mkdir -p /data/web_static/releases/{folder_name}/')

            # Extract archive
            c.run(f'tar -xzf /tmp/{file_name} -C /data/web_static/releases/{folder_name}/')

            # Remove archive
            c.run(f'rm /tmp/{file_name}')

            # Move extracted files to proper location
            c.run(f'mv /data/web_static/releases/{folder_name}/web_static/* '
                f'/data/web_static/releases/{folder_name}/')

            # Remove now-empty web_static directory
            c.run(f'rm -rf /data/web_static/releases/{folder_name}/web_static')

            # Remove current symbolic link
            c.run('rm -rf /data/web_static/current')

            # Create new symbolic link
            c.run(f'ln -s /data/web_static/releases/{folder_name}/ /data/web_static/current')

            print(f'New version deployed to {host}!')
        return True

    except Exception as e:
        print(f'Error: {e}')
        return False