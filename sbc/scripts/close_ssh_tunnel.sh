#!/bin/bash

# close SSH tunnel
ssh -F "$1" -S "$2" -O exit "$3"