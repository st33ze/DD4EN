# Data process module.
from discord import Embed, File
from datetime import datetime, timedelta
from comunication import get_data, post
from template_data import d4armory_data


class Tasks():
  def __init__(self):
    self.assigned = []
    self.running =  set()
  
  def add(self, new):
    if new in self.assigned: return
    for index, task in enumerate(self.assigned):
      if new.get_time() < task.get_time(): 
        self.assigned.insert(index, new)
        return
    self.assigned.append(new)
  
  def get_next(self):
    if self.assigned:
      task = self.assigned[0]
      self.assigned.pop(0)
      return task


class Event():
  def __init__(self):
    self.time = None

  def get_time(self):
    if self.time and self.time > datetime.now():
      return self.time
  
  def get_time_left(self):
    time_left = abs(datetime.now() - self.time).total_seconds()
    # (self.time - datetime.now()).total_seconds()
    return time_left

  def set_time(self, time):
    self.time = time


class Update(Event):
  MAX_FAILS = 5
  INTERVAL = 8 # hours

  def __init__(self, events, tasks):
    super().__init__()
    self.events = events
    self.tasks = tasks
    self.fails = 0
  
  async def run(self):
    # data = await get_data()
    data = d4armory_data
    # data = None
    if data:
      self.fails = 0 
      for event in self.events: 
        event.update(data)
        if event.get_next(): self.tasks.add(event)
    else: self.fails += 1

  def get_seconds_to_start(self):
    return Update.INTERVAL * 3600

class Boss(Event):
  THUMBNAIL = File('img/avarice.jpg', filename='avarice.jpg')
  
  def __init__(self):
    super().__init__()
    self.incoming = []

  def update(self, data):
    try:
      wb_data = data['boss']
      self.incoming = [
        {
          'name': wb_data['expectedName'],
          'time': datetime.fromtimestamp(wb_data['expected']),
          'zone': wb_data['zone'],
          'territory': wb_data['territory']
        },
        {
          'name': wb_data['nextExpectedName'],
          'time': datetime.fromtimestamp(wb_data['nextExpected'])
        }
      ]
    except Exception as e: print(f'Exception during data unpacking: {e}')

  def get_next(self):
    for boss in self.incoming:
      if boss['time'] > datetime.now(): return boss

  def get_time(self):
    ''' 
      Returns start time minus 30 minutes to notify.
    '''
    event = self.get_next()
    if event: return (event['time'] - timedelta(minutes=30))

  def get_seconds_to_start(self):
    return (self.get_time() - datetime.now()).total_seconds()
  
  def create_embed(self, event):
    template = {
      'type': 'rich',
      'title': 'WORLD BOSS',
      'description': f'World boss {event["name"]} is going to appear soon!',
      'color': 0x1bb14d,
      'fields': [
      {
          'name': 'Time',
          'value': f'<t:{event["time"].timestamp()}:R>',
          'inline': True
      }
      ],
      'thumbnail': {
      'url': 'attachment://avarice.jpg',
      }
    }
    if 'zone' in event: 
      template['fields'] += [
        {
          'name': 'Zone',
          'value': f'{event["zone"]}',
          'inline': True
        },
        {
          'name': 'Territory',
          'value': f'{event["territory"]}',
          'inline': True
        }
      ]
    if all(event['time'] > datetime.now() for event in self.incoming):
      template['footer'] = {
        'text': f'''Next boss {self.incoming[1]["name"]} is expected to spawn on\
                {self.incoming[1]['time'].strftime("%A %H:%M")}'''
      }
    return Embed.from_dict(template)
  
  async def run(self):
    event = self.get_next()
    if not event: return
    embed = self.create_embed(event)
    message_id = await post(embed, Boss.THUMBNAIL)
    


