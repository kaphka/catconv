import glob as g
import ujson
import os
import os.path as op
import re
import subprocess as sp
from subprocess import CalledProcessError
import time
import ocrolib
import gevent
from gevent.subprocess import Popen, PIPE, STDOUT


def crop(inpath, outpath, right=0, bottom=70):
    cropargs = '-{}-{}'.format(right,bottom)
    p = ['convert', inpath, '-crop', cropargs, outpath]
    return p

def binarize(path):
    return ['ocropus-nlbin', '-t', '0.5', '-z', '1.0', path]

def segment(path):
    return ['ocropus-gpageseg', '--maxcolseps', '0', '--usegauss', '-z', '1.0', path]

def predict(path, model_path, n_cpu=1):
    return ['ocropus-rpred', '-Q', str(n_cpu), '-m', model_path, path]

def create_dirs(path):
    """create all directories for a given file path"""
    directory = op.split(path)[0]
    if not op.isdir(directory):
        os.makedirs(directory)
    return directory

def echo(text):
    """create job that just prints text"""
    return ['echo', text]

def execute_queue(queue):
    t_start = time.time()
    subs = [Popen(job, stdout=PIPE) for job in queue]
    gevent.joinall(subs)
    duration = time.time() - t_start
    return {'output': subs, 'time': duration}

# TODO: delete
def execute_job(process):
    """executes a subprocess and returns a dict with information about the execution"""
    e = None
    t_start = time.time()
    try:
        output = sp.check_output(process,stderr=sp.STDOUT)
    except CalledProcessError as e:
        output = e
    duration = time.time() - t_start
    return {'output': output, 'time':duration, 'complete': e is None}

def execution_stats(executions):
    times = [execution['time'] for execution in executions if execution['complete']]
    not_completed = [execution for execution in executions if not execution['complete']]
    print(np.average(times), 's per job')
    print(len(not_completed),'not completed')


def convert_to_png(from_page, to_page):
    create_dirs(to_page["path"])
    crop_job = crop(from_page["path"], to_page["path"])
    return execute_job(crop_job)
