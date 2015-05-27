import os
import shutil
import tempfile



class UploadWriter():

    def __init__(self):
        self.open_fds = {} #{'filepath':file_descriptor}

    def open_fd(self,tmp_uuid):
        try:
            fd = self.open_fds[tmp_uuid]
            fd.close()
        except KeyError:
            pass

        self.open_fds[tmp_uuid] = tempfile.mkstemp()

    def close_fd(self,tmp_uuid,filepath):
        try:
            fd = self.open_fds[tmp_uuid]
            fd.close()
            shutil.move(fd[1],filepath)
            del self.open_fds[tmp_uuid]
        except KeyError:
            pass

    def write_to_fd(self,tmp_uuid,data):
        fd = self.open_fds[tmp_uuid]
        fd.write(data)
