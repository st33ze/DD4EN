# Data process module.
from discord import Embed, File
from datetime import datetime, timedelta
from comunication import get_data, post, delete
from templates import d4armory_data


class Tasks():
  def __init__(self):
    self.assigned = []
    self.running =  set()
  
  def add(self, new):
    '''
      If there isn't this type of event in self.assigned adds the event. 
    '''
    if new in self.assigned: return
    for index, task in enumerate(self.assigned):
      if new.get_time() < task.get_time(): 
        self.assigned.insert(index, new)
        return
    self.assigned.append(new)
  
  def get_next(self):
    '''
      Returns the first item in self.assigned and removes it from the array.
    '''
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
    self.last_time = None
  
  async def run(self):
    data = await get_data()
    # data = d4armory_data
    # data = None
    if data:
      self.fails = 0
      for event in self.events: 
        event.update(data)
        if event.get_next(): self.tasks.add(event)
    else: self.fails += 1
    self.last_time = datetime.now()

  def get_seconds_to_start(self):
    return Update.INTERVAL * 3600
  
  def get_last_time(self):
    return self.last_time


class Boss(Event):
  def __init__(self):
    super().__init__()
    self.incoming = []
    self.message_id = None

  def add_event(self, new_event):
    for index, event in enumerate(self.incoming):
      if new_event['runtime'] < event['runtime']:
        self.incoming.insert(index, new_event)
        return
    self.incoming.append(new_event)
  
  def update(self, data):
    try:
      wb_data = data['boss']
      events = [
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
      self.incoming = []
      for event in events:
        if event['time'] > datetime.now():
          event['type'] = 'post'
          # Notify 29 minutes before the event starts.
          event['runtime'] = event['time'] - timedelta(minutes=29)
          self.add_event(event)
    except Exception as e: 
      # Make error log file??????????????
      # print(f'Exception during data unpacking: {e}')
      pass

  def get_next(self):
    if self.incoming: return self.incoming[0]
  
  def get_time(self):
    event = self.get_next()
    if event:
      # If there is no boss post, run post event immediately.
      if self.message_id == None: return datetime.now()
      return event['runtime']

  def get_seconds_to_start(self):
    time = self.get_time()
    return (time - datetime.now()).total_seconds()

  def create_embed(self, event):
    template = {
      'type': 'rich',
      'title': 'WORLD BOSS',
      'fields': [
        {
          'name': 'Time',
          'value': f'<t:{int(event["time"].timestamp())}:R>',
          'inline': True
        }
      ],
      'thumbnail': {'url': 'attachment://boss.png'}
    }
    if event['type'] == 'edit':
      template['description'] = f'{event["name"]} is expected to spawn.'
      template['fields'][0]['value'] = f'<t:{int(event["time"].timestamp())}:t>'
    elif event['type'] == 'post':
      template['description'] = f'{event["name"]} is going to appear soon!'
      template['color'] = 0x1bb14d
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
      # Add footer if there is next expected boss incoming.
      for inc_event in self.incoming:
        if inc_event is not event and inc_event['type'] == 'post':
          template['footer'] = {
            'text': (
              f'Next boss {inc_event["name"]} is expected to spawn on '
              f'{inc_event["time"].strftime("%A %H:%M")}'
            )
          }
    return Embed.from_dict(template)
  
  def create_edit_event(self, event):
    ''' 
      Get post event and create edit event.
      Return edit event object.
    '''
    return {
      'name': event['name'],
      'time': event['time'],
      'type': 'edit'
    }

  async def run(self):
    ''' 
      Post or edit boss event on discord.
      Return next boss event if exists.
    '''
    event = self.get_next()
    if not event: return
    if event['type'] == 'post':
      if event['time'] - datetime.now() < timedelta(minutes=29):
        if self.message_id:
          await delete(self.message_id)
          self.message_id = None
        embed = self.create_embed(event)
        self.message_id = await post(embed, File('img/boss.png', filename='boss.png'))
        self.incoming.pop(0)
        self.add_event({
          'type': 'edit',
          'runtime': datetime.now() + timedelta(minutes=30)
        })
      elif not self.message_id:
        embed = self.create_embed(self.create_edit_event(event))
        self.message_id = await post(embed, File('img/boss.png', filename='boss.png'))
    elif event['type'] == 'edit':
      self.incoming.pop(0)
      event = self.get_next()
      if not event: return
      embed = self.create_embed(self.create_edit_event())
      await edit(embed)
    return self.get_next()





        



    


