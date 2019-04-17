#!/bin/bash

TARGET_ADDRESS=192.168.43.46 # the first script argument
HOST_PATH=/home/dinotumu/Documents/offloadProj/sbc/data/workloads/workload_1/10.png # the second script argument
TARGET_USER=root
TMP_DIR=$(mktemp -d)
SSH_CFG=$TMP_DIR/ssh-cfg
SSH_SOCKET=$TMP_DIR/ssh-socket
TARGET_PATH=/root/offloadProj/

# Create a temporary SSH config file:
cat > "$SSH_CFG" <<ENDCFG
Host *
        ControlMaster auto
        ControlPath $SSH_SOCKET
ENDCFG

# Open a SSH tunnel:
ssh -F "$SSH_CFG" -f -N -l $TARGET_USER $TARGET_ADDRESS

# Upload the file:
scp -F "$SSH_CFG" "$HOST_PATH" $TARGET_USER@$TARGET_ADDRESS:"$TARGET_PATH"

# Run SSH commands:
ssh -F "$SSH_CFG" $TARGET_USER@$TARGET_ADDRESS -T <<ENDSSH
# Do something with $TARGET_PATH here
ls -al $TARGET_PATH
rm offloadProj/10.png
ENDSSH

# Close the SSH tunnel:
ssh -F "$SSH_CFG" -S "$SSH_SOCKET" -O exit "$TARGET_ADDRESS"