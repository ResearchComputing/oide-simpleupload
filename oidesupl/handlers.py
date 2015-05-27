import os
import uuid
import string
import random
import tornado.web
import Pyro4

from oide.lib.handlers.base import BaseHandler
from oide.lib.mixins.fs_mixin import FSMixin

import oide.settings as global_settings
import oidesupl.settings as app_settings



@tornado.web.stream_request_body
class SimpleUploadHandler(BaseHandler,FSMixin):

    def initialize(self):
        pyro_uri = app_settings.PYRO_UPLDMODULE_URI%{'username':self.current_user}
        self.upld_writer = Pyro4.Proxy('PYRONAME:%s@%s:%d'%(
            pyro_uri,
            global_settings.PYRO_NAMESERVER_HOST,
            global_settings.PYRO_NAMESERVER_PORT
            )
        )

    @tornado.web.authenticated
    def post(self):
        fp = self.get_argument('uploadDir')
        fn = self.get_argument('filename')
        dest_path = os.path.join(fp,fn)
        self.upld_writer.close_fd(self.tmp_uuid,dest_path)

    @tornado.web.authenticated
    def prepare(self):
        self.stream_started = False
        self.tmp_uuid = uuid.uuid1().hex
        self.request.connection.set_max_body_size(2*1024**3)
        self.upld_writer.open_fd(self.tmp_uuid)

    def data_received(self, data):
        pdata = self._process(data)
        self.upld_writer.write_to_fd(self.tmp_uuid,pdata)

    def _process(self, data):
        trimmed = data.splitlines()
        tmp = data.splitlines(True)

        if not self.stream_started:
            self.boundary = trimmed[0].strip()
            tmp = tmp[1:]
            trimmed = trimmed[1:]
            self.stream_started = True

            try:
                first_elem = trimmed[:5].index("")
                tmp = tmp[first_elem + 1:]
                trimmed = trimmed[first_elem + 1:]
            except ValueError:
                pass

        try:
            last_elem = trimmed.index(self.boundary + "--")
            self.stream_started = False
            return "".join(tmp[:last_elem - 1])
        except ValueError:
            return "".join(tmp)
