import sys

from twill import set_output, set_errout

# custom stream for handling indenting
class IndentedStream(object):
    def __init__(self, output_pred=None, fstream=None):
        if fstream is None:
            self.fstream = sys.stdout
        self.pred = output_pred
        self.indentation = 0
        self.nspaces = 4
    def write(self, s):
        if not self.pred(s): return
        spacing = ' ' * self.nspaces * self.indentation
        # one newline
        msg = s.strip() + '\n'
        self.fstream.write(spacing + msg)
    def indent(self):
        self.indentation += 1
    def outdent(self):
        self.indentation -= 1
        if self.indentation < 0:
            self.indentation = 0

# this controls what messages to allow through
def output_pred(msg):
    return msg.strip()

def make_log_fn(output_stream, prepend_string, pred):
    def log_fn(msg):
        if pred(msg):
            output_stream.write(prepend_string + msg)
    return log_fn

# this is where all output will go
output_stream = IndentedStream(output_pred=output_pred)

# flunc uses these for output
log_error = make_log_fn(output_stream, '[X] ', output_pred)
log_warn = make_log_fn(output_stream, '[!] ', output_pred)
log_info = make_log_fn(output_stream, '[*] ', output_pred)

# and these hook in flunc's output
set_output(output_stream)
set_errout(output_stream)
