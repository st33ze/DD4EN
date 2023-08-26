from datetime import datetime, timedelta
import random

boss = {
  'names': ['Ashava', 'Avarice', 'The Wandering Death'],
  'locations': [
    {'territory': 'Seared Basin', 'zone': 'Kehjistan'},
    {'territory': 'The Crucible', 'zone': 'Fractured Peaks'},
    {'territory': 'Caen Adar', 'zone': 'Scosglen'},
    {'territory': 'Saraan Caldera', 'zone': 'Dry Stepps'},
    {'territory': 'Fields of Desecration', 'zone': 'Hawezar'},
  ]
}

def generate_boss_event(minutes, etype='post', location=True):
  event = {
    'type': etype,
    'name': random.choice(boss['names']),
    'time': datetime.now() + timedelta(minutes=minutes)
  }
  event['runtime'] = event['time'] - timedelta(minutes=29)
  if location: event.update(random.choice(boss['locations']))
  return event

def generate_boss_data(event_one, event_two):
  boss = {
    'expectedName': event_one['name'], 
    'nextExpectedName': event_two['name'],
    'expected': event_one['time'].timestamp(), 
    'nextExpected': event_two['time'].timestamp(),
  }
  for event in [event_one, event_two]:
    if 'territory' in event: 
      boss.update({'territory': event['territory'], 'zone': event['zone']})
  return {'boss': boss}


# fake_url =  'https://d4aarmory.io/api'
fake_url = 'https://httpstat.us/404'

d4armory_data = {
  'boss': {
    'name': 'Ashava', 
    'expectedName': 'The Wandering Death', 
    'nextExpectedName': 'The Wandering Death', 
    'timestamp': 1687088832, 
    'expected': 1687108347, 
    'nextExpected': 1688824754, 
    'territory': 'Seared Basin', 
    'zone': 'Kehjistan'
    }, 
  'helltide': {
    'timestamp': 1687101300, 
    'zone': 'kehj', 
    'refresh': 1687104000
    }, 
  'legion': {
    'timestamp': 1687100988, 
    'territory': 'Kor Dragan', 
    'zone': 'Fractured Peaks'
    }
}

embed_template = {
  'type': 'rich',
  'title': 'WORLD BOSS',
  # 'description': 'Ashava is going to appear soon!',
  'description': f'The Wandering Death is expected to spawn.',
  # 'color': 0x1bb14d,
  'fields': [
    {
      'name': 'Time',
      'value': f'<t:{1687088832}:R>',
      'inline': True
    }
  ],
  # 'fields': [
  # {
  #   'name': 'Time',
  #   'value': f'<t:{1687088832}:R>',
  #   'inline': True
  # },
  # {
  #   'name': 'Zone',
  #   'value': 'Kehjistan',
  #   'inline': True
  # },
  # {
  #   'name': 'Territory',
  #   'value': 'Seared Basin',
  #   'inline': True
  # }],
  'thumbnail': {
    'url': 'attachment://boss.png',
  },
  # 'footer': {
  #   'text': f'Next boss The Wandering Death is expected to spawn on Sunday 18:29'
  # }
}
