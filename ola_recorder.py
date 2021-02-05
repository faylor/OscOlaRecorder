import subprocess
import enum import Enum

class RunType(Enum):
    PLAY = 2
    RECORD = 3
    OTHER = 4

class OlaRecorder:


    def __init__(self, name, age):
        self.play_process = None
        self.record_process = None

    def play(self, y):
        self.kill_all()
        self.process = subprocess.Popen(["ola_recorder", "-p", y, "-i 0"], stdout=subprocess.PIPE)

    def record(self, x):
        self.kill_all()
        self.process = subprocess.Popen(['ola_recorder', '-r', x, '-u 1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20'], stdout=subprocess.PIPE)

    def kill_all(self):
        self.kill_play()
        self.kill_record()

    def kill_play(self):
        if self.play_process is not None:
            self.play_process.kill()
            self.play_process = None
    
    def kill_record(self):
        if self.play_process is not None:
            self.record_process.kill()
            self.record_process = None