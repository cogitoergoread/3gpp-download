#!/bin/bash
# Get a set of 3GPP documents, latest version
for doc in 21.905 23.501 23.502 23.503 29.500 29.501 29.503 29.510 29.513 29.517 29.518 29.520 29.571 29.572 29.594 32.240 32.255 32.260 32.276 32.290 32.291 32.299 33.501
do
    echo Downloading $doc
    /mnt/f/gwork/repos/3gpp-download/3gpp.py $doc
done
