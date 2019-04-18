#!/bin/bash

# create a temporary SSH config file
cat > "$1" <<ENDCFG
Host *
        ControlMaster auto
        ControlPath $2
ENDCFG

# open SSH tunnel:
ssh -F "$1" -f -N -l $3 $4