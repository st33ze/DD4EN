# Data process module.
from discord import Embed, File
from datetime import datetime, timedelta
from comunication import get_data
from template_data import d4armory_data


class Tasks():
  def __init__(self):
    self.assigned = []
    self.running =  set()
  
  def add(self, new):
    if not new.time: return
    for index, task in enumerate(self.assigned):
      if new == task: return
      if new.time < task.time: 
        self.assigned.insert(index, new)
        return
    self.assigned.append(new)


class Event():
  def __init__(self):
    self.time = None

  def get_timer(self):
    return self.time


class Update(Event):
  def __init__(self, tasks, events):
    super().__init__()
    self.tasks = tasks
    self.events = events
  
  async def run(self):
    # data = await get_data()
    data = d4armory_data
    if data: 
      for event in self.events: 
        event.update(data)
        self.tasks.add(event)

class Boss(Event):
  def __init__(self):
    super().__init__()
    self.incoming = []

  def update(self, data):
    try:
      wb_data = data['boss']
      extracted = [
        {
          'name': wb_data['expectedName'],
          'time': datetime.fromtimestamp(wb_data['expected'])
        },
        {
          'name': wb_data['nextExpectedName'],
          'time': datetime.fromtimestamp(wb_data['nextExpected'])
        }
      ]
      for boss in extracted:
        if boss['time'] > datetime.now(): self.incoming.append(boss)
      # Notify 30 minutes before the event.
      self.time = self.incoming[0]['time'] - timedelta(minutes=30)
    except Exception as e: print(f'Exception during data unpacking: {e}')