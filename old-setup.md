```
Tutorial: Setting Up Q4D on Unraid 6.12.10 and Ultra.cc

Steps on the Seedbox:

1. **Check OS Version**

   lsb_release -a

   - For Debian 10, extract and copy the contents of `mosq_bin_deb10.tar.z` into `/home/USERNAME/bin`.
   - For Debian 11, extract and copy the contents of `mosq_bin.tar.z` into `/home/USERNAME/bin`.
   - Open a new terminal or reload bash and enter:

     mosquitto -h
     
     It should display the version and help screen.

2. **Clone Q4D Repository**

   git clone https://github.com/weaselBuddha/Queue4Download.git ~/.Q4D
   mv ~/.Q4D/Q4D/* ~/.Q4D/
   rmdir ~/.Q4D/Q4D
   rm -rf ~/.Q4D/.git


3. **Configure Mosquitto**

   cd /home/USERNAME/.Q4D

   cat << EOF > mosquitto.conf
   listener 1883 0.0.0.0
   persistence_file mosquitto.db
   log_dest syslog
   log_type error
   connection_messages true
   log_timestamp true
   allow_anonymous false
   password_file /home/USERNAME/.Q4D/mosquitto_pws
   EOF


4. **Set Mosquitto Password**

   ~/bin/mosquitto_passwd -c ~/.Q4D/mosquitto_pws USERNAME

   Enter your password.

5. **Edit Q4Ddefines.sh**

   nano ~/.Q4D/Q4Ddefines.sh

   Change:

   readonly PUBLISHER="/usr/bin/mosquitto_pub"
   readonly SUBSCRIBER="/usr/bin/mosquitto_sub"

   To:

   readonly PUBLISHER="/home/USERNAME/bin/mosquitto_pub"
   readonly SUBSCRIBER="/home/USERNAME/bin/mosquitto_sub"


6. **Create Mosquitto Service**

   nano ~/.config/systemd/user/mosquitto.service

   Paste the following content:

   [Unit]
   Description=mosquitto daemon
   Wants=network-online.target
   After=network-online.target

   [Service]
   Type=simple
   ExecStart=/home/USERNAME/bin/mosquitto -c /home/USERNAME/.Q4D/mosquitto.conf
   Restart=always

   [Install]
   WantedBy=multi-user.target


   Save and exit, then run:

   systemctl --user daemon-reload
   systemctl --user start mosquitto.service
   systemctl --user enable mosquitto.service


   To check if Mosquitto is running properly:

   systemctl --user status mosquitto.service


7. **Edit Q4Dconfig.sh**

   nano ~/.Q4D/Q4Dconfig.sh

   - Change the host address:

     readonly BUS_HOST="your.mosquitto.ip_addr"

   - Set Mosquitto credentials:

     readonly USER="mosquitto_user"
     readonly PW="mqtt_password"


   - Configure torrent client:
     Example for rTorrent:

     readonly TORRENT_CLIENT=RTCONTROL
     readonly ACTIVE_TORRENT_FOLDER=~/.session


     Example for qBittorrent:

     readonly TORRENT_CLIENT=QBITTORRENT
     readonly ACTIVE_TORRENT_FOLDER=~/.local/share/qBittorrent/BT_backup


   - Enable labeling:

     LABELLING=true
     readonly _LABEL_TOOL='~/.Q4D/qbitLabeller.py ${Event[$HASH_INDEX]} ${Event[$LABEL_INDEX]}'


8. **Edit Types.config**

   nano ~/.Q4D/Types.config

   Example configuration:

   LABEL IS Music A ""
   LABEL IS Books B ""
   LABEL IS Movies M ""
   LABEL IS Software P ""
   LABEL IS TV S ""


9. **Create Q4D Label Daemon Service**

   nano ~/.config/systemd/user/q4d-labeld.service

   Paste the following content:

   [Unit]
   Description=Q4D Label Daemon
   Wants=network-online.target
   After=network-online.target

   [Service]
   Type=simple
   ExecStart=bash -xv /home/USERNAME/.Q4D/LabelD.sh
   Restart=always

   [Install]
   WantedBy=multi-user.target


   Save and exit, then run:

   systemctl --user daemon-reload
   systemctl --user start q4d-labeld.service
   systemctl --user enable q4d-labeld.service


   This completes the server-side setup.




Steps on Unraid:

1. **install mosquitto in unraid**

   wget -P /boot/extras https://download.salixos.org/x86_64/extra-15.0/salix/misc/mosquitto-2.0.14-x86_64-1salix15.0.txz
   installpkg /boot/extras/mosquitto-2.0.14-x86_64-1salix15.0.txz
 
   to test run mosquitto -h

1. **Create a Share for Q4D**

   - Create a share, e.g., `/mnt/user/scripts`.

2. **Clone Q4D Repository**

   git clone https://github.com/weaselBuddha/Queue4Download.git /mnt/user/scripts/.Q4D
   mv /mnt/user/scripts/.Q4D/Q4D/* /mnt/user/scripts/.Q4D/
   rmdir /mnt/user/scripts/.Q4D/Q4D
   rm -rf /mnt/user/scripts/.Q4D/.git
   
   Delete unnecessary scripts:

   rm /mnt/user/scripts/.Q4D/Queue4Download.sh /mnt/user/scripts/.Q4D/LabelD.sh


3. ** Add your host as trusted, and get Q4Dconfig.sh from seedbox and copy it to unraid **

   scp yourUser@YourIP:~/.Q4D/Q4Dconfig.sh /mnt/user/scripts/.Q4D


4. **Edit Q4Dconfig.sh**

   nano /mnt/user/scripts/.Q4D/Q4Dconfig.sh

   Change:

   readonly Q4D_PATH=~/.Q4D/

   To:

   readonly Q4D_PATH=/mnt/user/scripts/.Q4D/


5. **Edit Q4Dclient.sh**

   nano /mnt/user/scripts/.Q4D/Q4Dclient.sh


   Add SSH credentials or set up SSH keys:

   readonly CREDS='user:password'

   Add your seedbox IP:

   readonly HOST="seedbox_ip"


   Configure the directory mapping:
   (this is how mine looks)

   declare -Ag TypeCodes=\
   (
       [A]="/mnt/user/data/torrents/Music"
       [B]="/mnt/user/data/torrents/Books"
       [M]="/mnt/user/data/torrents/Movies"
       [P]="/mnt/user/data/torrents/Software"
       [S]="/mnt/user/data/torrents/TV"
       [V]="/mnt/user/data/torrents"
       [ERR]="/mnt/user/data/torrents/ERR"
   )


6. **Edit LFTPtransfer.sh**

   nano /mnt/user/scripts/.Q4D/LFTPtransfer.sh

   Change:

   source ~/.Q4D/Q4Dconfig.sh
   source ~/.Q4D/Q4Ddefines.sh
   source ~/.Q4D/Q4Dclient.sh

   To:

   source /mnt/user/scripts/.Q4D/Q4Dconfig.sh
   source /mnt/user/scripts/.Q4D/Q4Ddefines.sh
   source /mnt/user/scripts/.Q4D/Q4Dclient.sh


7. **Edit ProcessEvent.sh**

   nano /mnt/user/scripts/.Q4D/ProcessEvent.sh

   Change:

   exec 2>&1 >>~/Events.log
   source ~/.Q4D/Q4Dconfig.sh
   source ~/.Q4D/Q4Ddefines.sh
   source ~/.Q4D/Q4Dclient.sh

   To:

   exec 2>&1 >>/mnt/user/scripts/Events.log
   source /mnt/user/scripts/.Q4D/Q4Dconfig.sh
   source /mnt/user/scripts/.Q4D/Q4Ddefines.sh
   source /mnt/user/scripts/.Q4D/Q4Dclient.sh


8. **Create a User Script for ProcessEvent.sh**
     Paste:

   #!/bin/bash
   screen -S Q4D -X quit ; sleep 1 ; screen -dmS Q4D bash -xv /mnt/user/scripts/.Q4D/ProcessEvent.sh


   Save and set it to run at array start. it runs the ProcessEvent.sh as a screen session,
   im sure there are better solutions but this works aswell.

9. **Testing**
   -  Check execute permissions
    Server: chmod 755 ~/.Q4D/*.sh
    unraid: chmod 755 /mnt/user/scripts/.Q4D/*.sh


   - on server try downloading a torrent using this command:
    ~/.Q4D/Queue4Download.sh "TorrentName" Hash Category Tracker "FullPath"

    example:
    ~/.Q4D/Queue4Download.sh "linuxmint-21.3-cinnamon-64bit.iso" 5aa5483aee76df2eae84ca4109adbc0d0702ab46 Software udp://tracker.opentrackr.org:1337/announce "/home/USERNAME/files/torrents/Software/linuxmint-21.3-cinnamon-64bit.iso"


this should start the download of the iso on unraid and mark the torrent as QUEUED and than DONE in your torrent client.


This completes the setup of Q4D on Unraid and Ultra.cc.
```
