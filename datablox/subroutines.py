import os
import socket
import hashlib
from datetime import datetime

def create_socket():
    return socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def mkdir_recursively(dirname):
    dirs = dirname.split("/")
    new_directory = ""
    for directory in dirs:
        if len(directory) > 0:
            new_directory += "/%s" % directory
            if not os.path.exists(new_directory):
                os.mkdir(new_directory)

def read_file(filename):
    buffer = False
    with open(filename, 'r') as fp:
        buffer = fp.read()
        fp.close()

    return buffer

def write_file(filename, data):
    with open(filename, 'w') as fp:
        fp.write(data)
        fp.close()

    return True

def hash_digest(data):
    hasher = hashlib.new("md5")
    hasher.update(data)

    return hasher.hexdigest()

def datetime_from_string(date_time_str):
    return datetime.strptime(date_time_str, '%Y-%m-%d %H:%M:%S.%f')