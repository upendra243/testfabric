from __future__ import with_statement
from fabric.api import *
from fabric.contrib.console import confirm

env.hosts = ['172.16.1.146']
env.user = 'upkushwaha'
git_url = 'https://github.com/upendra243/testfabric.git' 

def test():
    with settings(warn_only=True):
        result = local('./manage.py test', capture=True)
    if result.failed and not confirm("Tests failed. Continue anyway?"):
        abort("Aborting at user request.")

def commit():
    local("git add -p && git commit")

def push():
    local("git push")

def prepare_deploy():
    test()
    commit()
    push()

def deploy():
    code_dir = '~/testfabric/django/'
    with settings(warn_only=True):
        if run("test -d %s" % code_dir).failed:
            run("git clone %s  %s" % { git_url, code_dir})
    with cd(code_dir):
        run("git pull")
        run("touch app.wsgi")
