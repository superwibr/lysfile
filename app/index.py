from __future__ import print_function

# missing depend management
import sys
import subprocess
import pkg_resources

required = {'flask', 'bson'}
installed = {pkg.key for pkg in pkg_resources.working_set}
missing = required - installed

if missing:
    print(f'detected missing packages ({missing})\nInstalling them now..')
    python = sys.executable
    subprocess.check_call([python, '-m', 'pip', 'install', *missing], stdout=subprocess.DEVNULL)

# index.py
import time
from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def query_example():
    # if key doesn't exist, returns None
    language = request.args.get('path')

    return '''<h1>The path value is: {}</h1>'''.format(language)

if __name__ == "__main__":
    print('oh hello')
    #time.sleep(5)
    if sys.argv[1] == 'write':
        pass
    elif sys.argv[1] == 'read':
        pass
    else:
        app.run(host='127.0.0.1', port=5000)