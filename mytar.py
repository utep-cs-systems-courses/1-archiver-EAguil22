# Enrique Aguilar mytar file
#! /usr/bin/env python3

import os
import sys

progName = sys.argv[0]
files = sys.argv[1:]

if progName == 'c':
    tarC(files)
    
if progName == 'x':
    tarX(files)

    
else:
    print("invalid mode")

def tarC(files):
    if len(files):
        for fname in files:
            os.write(2, f"copying file: {fname}\n".encode())
            
            file_path = os.path.join('/dev/mt0', dest) #path is now /dev/mt0/dest
            if not os.path.exists(file_path):
                # create file
                fd = os.open(file_path, os.O_RDONLY | os.O_CREAT)
                printFromFd(fd)
            else:
                fd = os.open(file_path, os.O_RDONLY)
                printFromFd(fd)
                

def tarX(files):

    while len(files):
        try:
            fdExtract = files.pop()
            fdDest = files.pop()
            try:
                os.lseek(fdExtract, 0, os.SEEK_END)
            except:
                err(f"seek to end of {fdExtract} failed")
            
            writeFromFd(fdExtract, fdDest)
        except:
            err(f"can't obtain file to extract or destination")
       

def writeFromFd(xfd, dest):
    numReads = 1
    while True:
        try:
            ibuf = os.read(0, 100)
        except:
            err("can't read from stdin")
        if not len(ibuf): break
        numReads += 1
        for ofd in xfd:
            obuf = bytes(ibuf)
            try:
                while len(obuf):
                    numBytes = os.write(xfd, obuf)
                    obuf = obuf[numBytes:]
            except:
                err(f"failed write to {dest}")
                

def printFromFd(ifd):
    numReads = 1
    while True:
        ibuf = os.read(ifd, 100)
        if not len(ibuf): break
        numReads += 1
        os.write(1, ibuf)
    os.close(ifd)
    os.write(2, f"EOF on {numReads}th call to read()\n".encode())

def err(msg):
    os.write(2, f"{progName}: {msg}\n".encode())
    sys.exit(1)
