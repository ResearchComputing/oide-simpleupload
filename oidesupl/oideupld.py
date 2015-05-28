import sys
import getpass
import Pyro4
from oidesupl.services.upldwriter import UploadWriter

import oide.settings as global_settings
import oidesupl.settings as app_settings



def main():
    upload_writer=UploadWriter()

    user_dict = {'username':getpass.getuser()}

    upld_daemon=Pyro4.Daemon()
    ns=Pyro4.locateNS(
        host=global_settings.PYRO_NAMESERVER_HOST,
        port=global_settings.PYRO_NAMESERVER_PORT
    )
    uri=upld_daemon.register(upload_writer)
    ns.register(app_settings.PYRO_UPLDMODULE_URI%user_dict, uri)

    print "Upload daemon running for user: %(username)s."%user_dict
    upld_daemon.requestLoop()

if __name__ == "__main__":
    main()
