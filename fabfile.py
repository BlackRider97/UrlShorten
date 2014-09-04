from fabric.operations import local
from fabric.state import env
from fabric.api import require
from fabric.contrib import *

def setup_localhost():
    """Configures fabric to run on Local servers"""
    env.hosts = ["localhost"]
    env.app_directory="."
    env.virtualenv_root = "%s/venv" % env.app_directory
    env.activate = "source %s/bin/activate" % env.virtualenv_root
    env.role = "local"
    global run
    run = local
    filename = "%s/conf/%s-config.yaml" % (env.app_directory, env.role)
    remotefile = "%s/conf/config.yaml" % env.app_directory
    run("virtualenv %s %s" % ("--clear --system-site-packages", env.virtualenv_root))
    run("cp %s %s" % (filename,remotefile))
    cmd = "bash %s/bin/runinvenv.sh %s %s/bin/bootstrap.py" % (env.app_directory, env.virtualenv_root, env.app_directory)
    run(cmd)

def production():
    """Configures fabric to run on Production servers"""
    env.hosts = ['rajneesh@X.X.X.X'] #private IP to production server
    env.app_directory = "~/UrlShorten"
    env.virtualenv_root = "%s/venv" % env.app_directory
    env.activate = "source %s/bin/activate" % env.virtualenv_root
    env.role = "production"
  
def staging():
    """Configures fabric to run on Staging servers"""
    env.hosts = ['rajneesh@X.X.X.X'] #private IP to staging server
    env.app_directory = "~/UrlShorten"
    env.virtualenv_root = "%s/venv" % env.app_directory
    env.activate = "source %s/bin/activate" % env.virtualenv_root
    env.role = "staging"
    
def create_virtualenv():
    """Creates a virtualenvironment"""
    require("virtualenv_root", provided_by=("staging", "production", "local"))
    args = "--clear --system-site-packages"
    run("sudo virtualenv %s %s" % (args, env.virtualenv_root))

def deploy_app():
    """Deploys the application using rsync, and reinstall the requirements in the configured virtualenv"""
    require("app_directory", provided_by=("staging", "production", "local"))
    project.rsync_project(local_dir="urlshorten requirements bin conf", remote_dir=env.app_directory, exclude=["*~", "*.pyc"])
    filename = "conf/%s-config.yaml" % env.role
    remotefile = "%s/conf/config.yaml" % env.app_directory
    project.put(local_path=filename, remote_path=remotefile)
    cmd = "sudo %s/bin/runinvenv.sh %s %s/bin/bootstrap.py" % (env.app_directory, env.virtualenv_root, env.app_directory)
    run(cmd)

def reload_app():
    """Uses supervisorctl to restart the application"""
    require("app_directory", provided_by=("staging", "production", "local"))
    run("sudo supervisorctl restart urlshorten:*")

def deploy():
    deploy_app()

def restart():
    reload_app()

def all():
    deploy()

        
