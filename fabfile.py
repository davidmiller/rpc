"""
Fab commands for RPC
"""

from fabric.api import task, hosts, local, lcd,  cd, run
from fabric import operations

deadpan = "happenup@deadpansincerity.com"

@task
def make_docs():
    """
    Rebuild the documentation
    """
    with lcd("doc/"):
        local("make html")

@task
@hosts(deadpan)
def upload_docs():
    """
    Build, compress, upload and extract the latest docs
    """
    with lcd("doc/build/html"):
        local("rm -rf rpcdocs.tar.gz")
        local("tar zcvf rpcdocs.tar.gz *")
        operations.put("rpcdocs.tar.gz", "/home/happenup/webapps/rpcdocs/rpcdocs.tar.gz")
    with cd("/home/happenup/webapps/rpcdocs/"):
        run("tar zxvf rpcdocs.tar.gz")
