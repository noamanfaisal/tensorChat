import subprocess
import time

class StreamdownStreamer:
    def __init__(self):
        self.proc = subprocess.Popen(["sd"], stdin=subprocess.PIPE, text=True)

    def write_chunk(self, chunk: str):
        if self.proc.stdin:
            self.proc.stdin.write(chunk)
            self.proc.stdin.flush()
    
    def close(self):
        if self.proc.stdin:
            self.proc.stdin.close()
        self.proc.wait()
    
    def cancel(self):
        self.proc.terminate()
        self.proc.wait()

