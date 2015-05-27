import os
import sys



class UploadWriter():

    def __init__(self):
        self.open_fd = {} #{'filepath':file_descriptor}

    def open_fd(self,filepath):
        try:
            fd = self.open_fd[filepath]
            fd.close()
        except KeyError:
            pass

        self.open_fd[filepath] = open(filepath,'w')

    def close_fd(self,filepath):
        try:
            fd = self.open_fd[filepath]
            fd.close()
        except KeyError:
            pass

    def write_to_fd(self,filepath,data):
        fd = self.open_fd[filepath]
        fd.write(data)
