#!/bin/bash
# vi: ts=4:sw=4:et
# Associate Array, type code -> destination directory


# LFTP Throttle, (optional)
# this would download 5 files at a time, with 5 Segments

readonly SEGMENTS=5
readonly THREADS=5

# LFTP Login  Your ssh username for the Seedbox, keep the :xyz for some reason it needs any password, even if ssh keys are already configured
readonly CREDS='YOUR_USERNAME:xyz'

# Your Server
readonly HOST="YOUR_SEEDBOX_IP"

# Type Code to Destination Directory Map: [CODE]="DIRECTORY"
# Don't Remove ERR as last entry

declare -Ag TypeCodes=\
(
        [A]="/data/torrents/Music"
        [B]="/data/torrents/Books"
        [M]="/data/torrents/Movies"
        [P]="/data/torrents/Software"
        [S]="/data/torrents/TV"
        [V]="/data/torrents"
        [ERR]="/data/torrents/ERR"
)

# Event Indexes
readonly FILENAME=0
readonly HASH=1
readonly TYPE=2
