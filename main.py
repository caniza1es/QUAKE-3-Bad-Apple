from pymem import Pymem
import os
import time
import sys
import keyboard
from playsound import playsound
import threading

pm = Pymem("quake3.exe")

class Console:
    def __init__(self,size):
        self.size = size
        self.base = pm.allocate(self.size)
        self.print_function = 0x41CB80
        self.execute_function = 0x41BCE0
    def printf(self,str):
        #size = len(str.encode('utf-8'))
        pm.write_string(self.base,str)
        pm.start_thread(self.print_function,self.base)
        #pm.write_bytes(self.base,bytes([0]*size),size)
    def exec(self,str):
        size = len(str.encode('utf-8'))
        pm.write_string(self.base,str)
        pm.start_thread(self.execute_function,self.base)
        pm.write_bytes(self.base,bytes([0]*size),size)



shell = Console(15000)

processed_folder_path = 'processed'


files = os.listdir(processed_folder_path)
while not keyboard.is_pressed("p"):
    pass

def play_sound(file_path):
    playsound(file_path)

# Path to your MP3 file
mp3_file_path = 'badderapple.mp3'

# Create a thread to play the sound
sound_thread = threading.Thread(target=play_sound, args=(mp3_file_path,))

# Start the thread
sound_thread.start()


for file in files:
    file_path = os.path.join(processed_folder_path, file)
    with open(file_path, 'r') as f:
        content = f.read()
        try:
            shell.printf(content)
            time.sleep(0.09655)
        except:
            print(file_path)
            sys.exit()
