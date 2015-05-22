import os
import uuid
import string
import random
import tornado.web

from oide.lib.handlers.base import BaseHandler



@tornado.web.stream_body
class SimpleUploadHandler(BaseHandler):

    @tornado.web.authenticated
    def post(self):
        # open a file or a socket to stream the uploaded data to
        self.fp = open('file_{0}'.format(uuid.uuid1().hex), 'w')
        self.request.request_continue()
        self.read_bytes = 0
        self._read_chunk()

    def _read_chunk(self):
        # set the chunk size and read bytes from the stream
        chunk_length = min(10000,
            self.request.content_length - self.read_bytes)
        if chunk_length > 0:
            self.request.connection.stream.read_bytes(
                chunk_length, self._on_chunk)
        else:
            self.fp.close()
            self._on_uploaded()

    def _on_chunk(self, chunk):
        if chunk:
            # write chunk of data to disk
            self.fp.write(chunk)
            self.read_bytes += len(chunk)
        else:
            # no more incoming data, set correct content_length
            self.content_length = self.read_bytes
        self._read_chunk()

    def _on_uploaded(self):
        self.write("Uploaded!")
        self.finish()
