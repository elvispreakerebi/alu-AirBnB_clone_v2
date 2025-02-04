#!/usr/bin/python3
"""Fabric configuration file that imports and exposes the do_pack task."""

from fabric.api import local
from datetime import datetime
import os

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

        # Create the archive
        print(f"Packing web_static to {archive_name}")
        result = local(f"cd {current_dir} && tar -czvf {archive_name} web_static/")

        # Check if archive was created successfully
        if result.succeeded and os.path.exists(archive_name):
            return archive_name
        return None

    except Exception as e:
        print(f"Error: {e}")
        return None