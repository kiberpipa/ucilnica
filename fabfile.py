from os.path import basename

from fabric.api import env, run, cd, put, sudo

class NotTested(Exception):
    """docstring for NotTested"""
    print "\n This isn't tested. Do not use it. \n"
    pass

raise NotTested

def list_dir(dir_=None):
    """docstring for list_dir"""
    dir_ = dir_ or env.cwd
    string_ = sudo("for i in %s*; do echo $i; done" % dir_)
    files = string_.replace("\r","").split("\n")
    return files

def _mv_homes_to_opt():
    """docstring for mv_homes_to_opt"""
    with cd("/home/"):
        #rel = [basename(abs) for abs in list_dir()]
        homes = list_dir()
    sudo("mkdir -p /opt/home/")
    sudo("rsync -a %s /opt/home/" % homes)

def put_and_backup(local_path, remote_path, use_sudo=False):
    """docstring for put_and_backup"""
    sudo("cp {0} {0}_backup~".format(remote_path))
    put(local_path, remote_path, use_sudo)


def upgrade():
    """docstring for upgrade"""
    sudo("apt-get update")
    sudo("apt-get upgrade -y")

def install_packages(list_):
    """docstring for install_packages"""
    string_ = " ".join(list_)
    sudo("apt-get install -y %s " % string_)

def install_ldap_pam():
    """docstring for install_ldap_pam"""

    for file in ["common-account", "common-auth", "common-password"]:
        put_and_backup("etc/pam.d/%s" % file, "/etc/pam.d/", True)

def install_ldap():
    """docstring for install_ldap"""

    deps = ["libpam-ldap", "libnss-ldap", "nss-updatedb", "libnss-db"]

    install_packages(deps)

    for file in ["pam_ldap.conf", "ldap.conf", "libnss-ldap.conf", "nsswitch.conf"]:
        put_and_backup("etc/%s" % file, "/etc/", True)
    sudo("ln -s /etc/ldap.conf /etc/ldap/ldap.conf")
    sudo("ln -s /etc/libnss-ldap.conf /etc/ldap/libnss-ldap.conf")


def install_automounter():
    """docstring for install_nfs_magic"""

    deps = ["autofs", "portmap", "nfs-common"]

    install_packages(deps)

    for file in ["auto.master", "auto.nfs"]:
        put_and_backup("etc/%s" % file, "/etc/", True)

    sudo("service autofs restart")

def install_classroom():
    """docstring for install_classroom"""
    upgrade()
    install_ldap_pam()
    install_ldap()
    install_automounter()
