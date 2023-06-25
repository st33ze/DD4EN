# Data process module.
from discord import Embed, File
from template_data import d4armory_data

class Data(Embed):
  def __init__(self, event_name):
    super().__init__(type='rich')
    self.name = event_name
    self.init_wb()

  def update_wb(self, data):
    try:
      # Exctract world boss data.
      wb_data = data['boss']
      self.incoming = {
        'name': wb_data['name'],
        'time': wb_data['timestamp'],
        'territory': wb_data['territory'],
        'zone': wb_data['zone']
      }
      self.expected = {
        'name': wb_data['expectedName'],
        'time': wb_data['expected']
      }
      self.nextExpected = {
        'name': wb_data['nextExpectedName'],
        'time': wb_data['nextExpected']
      }
    except Exception as e: print(f'Exception during data unpacking: {e}')

  def init_wb(self):
    self.incoming = None
    self.expected = None
    self.nextExpected = None  
# world_boss = Data('wb')
# world_boss.update_wb(d4armory_data)
# print(world_boss.incoming, world_boss.expected, world_boss.nextExpected)
