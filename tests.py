import unittest
import asyncio
import templates
from datetime import timedelta
from events import Boss

class TestBoss(unittest.TestCase):
  def setUp(self):
    self.boss = Boss()
    self.restore_incoming()

  def restore_incoming(self):
    self.boss.incoming = [
      templates.generate_boss_event(155),
      templates.generate_boss_event(522, location=False)
    ]

  def test_embed(self):
    # No location in event.
    event = self.boss.incoming[1]
    embed = self.boss.create_embed(event)
    self.assertEqual(len(embed.fields), 1, 'No location in event: wrong field size.')
    # With location in event.
    event = self.boss.incoming[0]
    embed = self.boss.create_embed(event)
    self.assertEqual(len(embed.fields), 3, 'With location in event: wrong field size.')
    # With next expected boss.
    event = self.boss.incoming[0]
    embed = self.boss.create_embed(event)
    self.assertIsNotNone(embed.footer.text, 'With next expected boss: There should be a footer text.')
    # Without next expected boss.
    event = templates.generate_boss_event(55)
    self.boss.incoming = [event]
    embed = self.boss.create_embed(event)
    self.assertIsNone(embed.footer.text, 'Without next expected boss: There should not be a footer text.')
    # Edit event.
    event = templates.generate_boss_event(55, 'edit')
    embed = self.boss.create_embed(event)
    self.assertEqual(f'{event["name"]} is expected to spawn.', embed.description, 'Descriptions don\'t match.')
  
  def test_add_event(self):
    # New event between two existing events.
    new_event = templates.generate_boss_event(222)
    self.boss.add_event(new_event)
    self.assertIs(self.boss.incoming[1], new_event, 'New event should be between existing events.')
    # New event at the end of the array.
    self.restore_incoming()
    new_event = templates.generate_boss_event(666)
    self.boss.add_event(new_event)
    self.assertIs(self.boss.incoming[2], new_event, 'New event should be at the end of the array.')
    # Adding event to an empty array.
    self.boss.incoming = []
    new_event = templates.generate_boss_event(22)
    self.boss.add_event(new_event)
    self.assertIs(self.boss.incoming[0], new_event, 'New event should be at the beginning of the array.')

  def test_update(self):
    # Without data input.
    self.boss.update(data=None)
    self.assertEqual(len(self.boss.incoming), 2, 'Incoming events array shouldn\'t be changed.')
    # Data with old timers.
    event_one = templates.generate_boss_event(-350)
    event_two = templates.generate_boss_event(-5)
    data = templates.generate_boss_data(event_one, event_two) 
    self.boss.update(data)
    self.assertEqual(len(self.boss.incoming), 0, 'Incoming events array should be empty.')
    # Data with one relevant timer.
    event_one = templates.generate_boss_event(155)
    data = templates.generate_boss_data(event_one, event_two)
    self.boss.update(data)
    self.assertEqual(len(self.boss.incoming), 1, 'Incoming events array should have one event.')
    self.assertEqual(
      event_one['time'], 
      self.boss.incoming[0]['time'],
      'One relevant timer: timers don\'t match!')
    # Data with two relevant timers.
    event_two = templates.generate_boss_event(555)
    data = templates.generate_boss_data(event_one, event_two)
    self.boss.update(data)
    self.assertEqual(len(self.boss.incoming), 2, 'Incoming events array should have two events.')
    self.assertEqual(
      event_two['time'], 
      self.boss.incoming[1]['time'], 
      'Two relevant timers: Second timer doesn\'t match!')
    # Data with edit event between boss events.
    edit_event = templates.generate_boss_event(333, 'edit', False)
    self.boss.incoming = [edit_event]
    self.boss.update(data)
    self.assertIs(self.boss.incoming[1], edit_event, 'Edit event should be between two post events.')
    

    def test_run(self):
      # Initial message.
      pass

class TestBossAsync(unittest.IsolatedAsyncioTestCase):
  def setUp(self):
    self.boss = Boss()
    TestBoss.restore_incoming(self)
  
  

class TestCommunicatons(unittest.IsolatedAsyncioTestCase):
  def setUp(self):
    from comunication import post
    from discord import Embed, File
    template = templates.embed_template
    self.embed = Embed.from_dict(template)
    self.thumbnail = File('img/boss.png', filename='boss.png')
    self.post = post
  
  @unittest.skip('Skipping test_post')
  async def test_post(self):
    message_id = await self.post(self.embed, self.thumbnail)
    self.assertIsInstance(message_id, int)
  
  @unittest.skip('Skipping test_delete')
  async def test_delete(self):
    ''' 
      Posts message on discord, waits 5s and deletes the message.
    '''
    from comunication import delete
    message_id = await self.post(self.embed, self.thumbnail)
    await asyncio.sleep(5)
    await delete(message_id)

if __name__ == '__main__':
  unittest.main()