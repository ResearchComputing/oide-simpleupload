import os
import shutil
import tempfile
import tornado.web

from oide.lib.handlers.base import BaseHandler

import oide.settings as global_settings
import oidesupl.settings as app_settings



@tornado.web.stream_request_body
class SimpleUploadHandler(BaseHandler):

    @tornado.web.authenticated
    def post(self):
        import pdb; pdb.set_trace()
        fp = self.request.headers['Uploaddir']
        dest_path = os.path.join(fp,self.filename)
        self.fd.close()
        shutil.move(self.fd.name,dest_path)

    @tornado.web.authenticated
    def prepare(self):
        self.tmp_cache = ''
        self.stream_started = False
        self.request.connection.set_max_body_size(2*1024**3)
        fd_info = tempfile.mkstemp()
        self.fd = open(fd_info[1],'w')

    def data_received(self, data):
        self.tmp_cache += data
        pdata = self._process(data)
        self.fd.write(pdata)

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
                metadata = trimmed[:first_elem]
                self.filename = metadata[0].split(';')[-1].split('=')[-1][1:-1]
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
