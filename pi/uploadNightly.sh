#!/bin/bash
set -e
tar czvf currentData.tgz currentData
./dropbox_uploader.sh upload currentData.tgz "Power/PV/currentData.tgz"

