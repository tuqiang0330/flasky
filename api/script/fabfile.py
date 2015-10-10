#-*- encoding: utf-8 -*-
"""Fabric只支持Python2.5-2.7
"""

from os.path import join, dirname, realpath
from fabric.api import env, hosts, put, run

env.user = 'flasky'

hosts_test = ('localhost')
hosts_rel = (
    'localhost'
)

work_dir = '/home/flasky/api/'
script_dir = join(work_dir, 'script')


@hosts(hosts_test)
def start_test():
    run('bash %s' % join(script_dir, 'start.sh'))

@hosts(hosts_test)
def upload_test():
    backup_dir = '%s.bak' % script_dir
    run('rm -rf %s' % backup_dir)
    run('mv %s %s' % (script_dir, backup_dir))
    put(dirname(realpath(__file__)), work_dir)
    run('cp %s/config_test.py %s/config.py' % (script_dir, script_dir))
