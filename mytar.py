#! /usr/bin/env python3

import os
import sys


def tarFileMaker(files, fd):
    for f in files:
        openedFile = os.open(f, os.O_RDONLY)
        ibuf = read(openedFile, 100)
        while len(ibuf):
            os.write(fd, ibuf)
            ibuf = read(openedFile, 100)
        os.close(openedFile)
    
def findLenName(files, fd):
    for f in files:
        openedFile = os.open(f, os.O_RDONLY)
        ibuf = read(openedFile, 10)
        bytesRead = len(ibuf)
        while len(ibuf):
            ibuf = read(openedFile, 10)
            bytesRead += len(ibuf)
        os.write(fd, (f + "," + str(bytesRead) + ",").encode())
        os.close(openedFile)

def getNameSize(fd):
    tempStr = str(os.read(os.open(fd, os.O_RDONLY), 1000))
    if tempStr.find("b'") != -1:
        tempStr = tempStr[tempStr.find("b'") + 2:]
    return tempStr.split(",")
        
def getFileNames(fd, numBytes):
    name = read(fd, numBytes)
    return name.decode()

def initFolder():
    path = os.getcwd() + "/tar"
    if not os.path.exists(path):
        os.makedirs(path)
        
def createTarFile(fileName):
    path = os.path.join(os.getcwd() + "/tar", fileName)
    if os.path.isfile(path):
        os.remove(path)
        os.mknod(path)
    else:
        os.mknod(path)
    return path

def extract(nameBytes, fd):
    count = 0
    while count < len(nameBytes) - 1:
        temp = os.open(createTarFile(nameBytes[count]), os.O_RDWR)
        count += 1
        contents = os.read(fd, int(nameBytes[count]))
        os.write(temp, contents)
        count += 1

def createContainer():
    fdContain = os.open(createTarFile("container.txt"), os.O_RDWR)
    findLenName(files, fdContain)
    os.close(fdContain)
    
def createCompressed():
    compressed = os.open(createTarFile("compressed.txt"), os.O_RDWR)
    tarFileMaker(files, compressed)
    os.close(compressed)


files = sys.argv[1:]

containerFile = os.path.join(os.getcwd() + "/tar", "container.txt")
compressFile = os.path.join(os.getcwd() + "/tar", "compressed.txt")

if files[0] == 'c':
    files = files[1:]
    initFolder()
    createContainer()
    createCompressed()

elif files[0] == 'x':
    files = files[1:]
    lst = getNameSize(containerFile)
    extract(lst, os.open(compressFile, os.O_RDWR))

else:
    os.write(2, "Error mode not specified".encode())
    sys.exit(1)

        
