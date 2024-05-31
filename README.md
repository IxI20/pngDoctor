# pngDoctor
Python script for CTF's to check integrity of PNG blocks

Usage
========================================================================
to use the script please store Damaged png in the same Folder/Directory,
add the file name as an arguement without file path when running the
python file.

For a demonstration use test.png in this repository using this command
python pngDoc.py test.png

Uses
========================================================================
This script simply checks PNG signature, IHDR and IEND blocks for the
correct hex values and replaces them if they are incorrect

this script will not restore a PNG if bytes have been added to the file,
only if they have been replaced. This script also does not interact or
check the CRC (Cyclic Redundancy Check).


