#!/usr/bin/python3

# Edit this tool to reflect your qBittorrent settings (host, port, user, pw)

# Changes to Q4Dconfig.sh

#LABELLING=true
#readonly _LABEL_TOOL='~/.Q4D/qbitTagger.py ${Event[$HASH_INDEX]} ${Event[$LABEL_INDEX]}'

import sys
# Dependency: pip install qbittorrent-api
import qbittorrentapi

# Configuration variables for qBittorrent WebUI
host = 'your.qbittorrent.host'  # Replace with your qBittorrent host URL
port = 443  # Replace with your qBittorrent WebUI port
username = 'your_username'  # Replace with your qBittorrent username
password = 'your_password'  # Replace with your qBittorrent password

# Command-line arguments
torrent_hash = sys.argv[1]
tag = sys.argv[2]

print(f"Setting tag of {torrent_hash} to '{tag}'")

# Instantiate a Client using the appropriate WebUI configuration
qbt_client = qbittorrentapi.Client(
    host=host,
    port=port,
    username=username,
    password=password
)

try:
    # Authenticate to the qBittorrent WebUI
    qbt_client.auth_log_in()

    # Remove the 'QUEUED' tag from the specified torrent
    qbt_client.torrents_remove_tags(torrent_hashes=torrent_hash, tags='QUEUED')
    print(f"Tag 'QUEUED' removed successfully from torrent {torrent_hash}")

    # Add the new tag to the specified torrent
    qbt_client.torrents_add_tags(torrent_hashes=torrent_hash, tags=tag)
    print(f"Tag '{tag}' set successfully for torrent {torrent_hash}")

except qbittorrentapi.LoginFailed as e:
    print(f"Failed to authenticate: {e}")
except Exception as e:
    print(f"An error occurred: {e}")
