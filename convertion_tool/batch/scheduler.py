import schedule
import time
from pydub import AudioSegment
from ..models import db, File, Task, Status

def job():


schedule.every(30).seconds.do(job)

while True:
    schedule.run_pending()
    time.sleep(1)