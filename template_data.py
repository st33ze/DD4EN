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
  'description': 'World boss Ashava is going to appear soon!',
  'color': 0x1bb14d,
  'fields': [
  {
    'name': 'Time',
    'value': f'<t:{1687088832}:R>',
    'inline': True
  },
  {
    'name': 'Zone',
    'value': 'Kehjistan',
    'inline': True
  },
  {
    'name': 'Territory',
    'value': 'Seared Basin',
    'inline': True
  }],
  'thumbnail': {
    'url': 'attachment://avarice.jpg',
  },
  'footer': {
    'text': f'Next boss The Wandering Death is expected to spawn on Sunday 18:29'
  }
}
