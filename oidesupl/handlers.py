import os
import uuid
import string
import random
import tornado.web

from oide.lib.handlers.base import BaseHandler



@tornado.web.stream_request_body
class SimpleUploadHandler(BaseHandler):

    @tornado.web.authenticated
    def post(self):
        self.fp.close()

    @tornado.web.authenticated
    def prepare(self):
        self.stream_started = False
        self.request.connection.set_max_body_size(2*1024**3)
        self.fp = open('/tmp/file_{0}'.format(uuid.uuid1().hex), 'w')

    def data_received(self, data):
        pdata = self._process(data)
        self.fp.write(pdata)

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
