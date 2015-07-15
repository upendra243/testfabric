from __future__ import with_statement
from fabric.api import *
from fabric.contrib.console import confirm

env.hosts = ['172.16.1.146']
env.user = 'upkushwaha'
git_url = 'https://github.com/upendra243/testfabric.git' 
code_dir = '~/testfabric/django/'
env.path = code_dir

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

def prepare_server():
   sudo('apt-get install aptitude -y')
   sudo('aptitude install -y python-setuptools')
   sudo('easy_install pip')
   sudo('pip install virtualenv')
   sudo('aptitude install -y apache2')
   sudo('aptitude install -y libapache2-mod-wsgi')
   # we want rid of the defult apache config
   sudo('cd /etc/apache2/sites-available/; a2dissite default;')
   run('mkdir -p $(path); cd $(path); virtualenv .;')

def deploy_apache():
    prepare_server()
    restart_webserver()


def deploy():
    with settings(warn_only=True):
        if run("test -d %s" % code_dir).failed:
            run("git clone %s  %s" % { git_url, code_dir})
    with cd(code_dir):
        run("git pull")
        run("touch app.wsgi")

def restart_webserver():
    "Restart the web server"
    sudo('/etc/init.d/apache2 restart')
