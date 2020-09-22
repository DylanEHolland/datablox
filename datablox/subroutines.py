import os
import socket
import hashlib
from datetime import datetime

def extract_args(*args, **kwargs):
    output = {
        'hash': None,
        'parent': None,
        'arguments': {}
    }

    if len(args):
        if type(args[0]) == str:
            output['hash'] = args[0]

    if len(kwargs):
        data = dict(kwargs)
        if 'digest' in data:
            output['hash'] = data.get('digest')
            del(data['digest'])

        if 'parent' in data:
            output['parent'] = data.get('parent')
            del(data['parent'])
        
        output['arguments'] = data

    return output

def create_socket():
    return socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def mkdir_recursively(dirname):
    dirs = dirname.split("/")
    new_directory = ""
    built = False
    for directory in dirs:
        if len(directory) > 0:
            new_directory += "/%s" % directory
            if not os.path.exists(new_directory):
                try:
                    os.mkdir(new_directory)
                    built = True
                except PermissionError as err:
                    print(err)
                    return False

    if built:
        return True
    return None

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