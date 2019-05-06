import subprocess
from threading import Thread
from ActiveMQtoMySql import main


Result1 = Thread(target = main)
Result1.start()

print("Working")
