#!/usr/bin/env bash
# Sets up web servers for web_static deployment (macOS compatible)

# Exit on any error
set -e

# Ensure script is NOT run with sudo
if [ "$(id -u)" == "0" ]; then
    echo "Do NOT run this script with sudo!"
    exit 1
fi

# Define base directory inside alu-AirBnB_clone_v2
BASE_DIR="$(pwd)/data/web_static"

# Install Nginx if not installed (using Homebrew)
if ! command -v nginx &> /dev/null; then
    echo "Installing Nginx..."
    brew install nginx
fi

# Create required directories
mkdir -p "$BASE_DIR/releases/test/"
mkdir -p "$BASE_DIR/shared/"

# Create a fake HTML file for testing
echo "<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>" > "$BASE_DIR/releases/test/index.html"

# Remove existing symbolic link and create a new one
rm -rf "$BASE_DIR/current"
ln -s "$BASE_DIR/releases/test/" "$BASE_DIR/current"

# Get current macOS user and group
CURRENT_USER=$(whoami)
CURRENT_GROUP=$(id -gn)

# Change ownership to the current macOS user and group
chown -R "$CURRENT_USER:$CURRENT_GROUP" "$(pwd)/data"

# Ensure Nginx config exists
NGINX_CONF="/usr/local/etc/nginx/nginx.conf"

if [ ! -f "$NGINX_CONF" ]; then
    echo "Creating default Nginx configuration..."
    echo "worker_processes  1;

    events {
        worker_connections  1024;
    }

    http {
        include       mime.types;
        default_type  application/octet-stream;

        sendfile        on;
        keepalive_timeout  65;

        server {
            listen       8080;
            server_name  localhost;

            location / {
                root   html;
                index  index.html index.htm;
            }
        }
    }" > "$NGINX_CONF"
fi

# Backup nginx configuration
cp "$NGINX_CONF" "$NGINX_CONF.backup"

# Add location block if not already in the config
if ! grep -q "location /hbnb_static" "$NGINX_CONF"; then
    echo "Updating Nginx configuration..."
    sed -i '' -e "/http {/a\\
        location /hbnb_static {\\
            alias $BASE_DIR/current/;\\
        }" "$NGINX_CONF"
fi

# Restart Nginx
brew services restart nginx

echo "Setup completed successfully!"
exit 0
