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
    self.assertEqual(embed.footer.text,
                     (f'Next boss {self.boss.incoming[1]["name"]} is expected to spawn on '
                     f'{self.boss.incoming[1]["time"].strftime("%A %H:%M")}'),
                     'Footer texts don\'t match')
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


class TestBossRun(unittest.IsolatedAsyncioTestCase):
  def setUp(self):
    self.boss = Boss()
  
  async def test_no_events(self):
    next_event = await self.boss.run()
    self.assertIsNone(next_event, 'There shouldn\'t be next event.')
  
  @unittest.skip('Skipping test_starting_event_no_msg_id')
  async def test_starting_event(self):
    self.boss.incoming = [
      templates.generate_boss_event(15),
      templates.generate_boss_event(300, location=False)
    ]
    next_event = await self.boss.run()
    self.assertEqual(next_event['type'], 'edit', 'Next incoming event should be of type edit.')
    self.assertEqual(len(self.boss.incoming), 2, 'There should be two events in the incoming array.')
  
  @unittest.skip('Skipping test_starting_event_no_next')
  async def test_starting_event_no_next(self):
    self.boss.incoming = [templates.generate_boss_event(15)]
    next_event = await self.boss.run()
    self.assertEqual(next_event['type'], 'edit', 'Next incoming event should be of type edit.')
    self.assertEqual(len(self.boss.incoming), 1, 'There should be one event in the incoming array.')
  
  @unittest.skip('Skipping test_starting_event_with_msg_id')
  async def test_starting_event_with_msg_id(self):
    self.boss.incoming = [templates.generate_boss_event(15)]
    next_event = await self.boss.run()
    message_id = self.boss.message_id
    self.assertIsNotNone(message_id, 'There should be a message id.')
    await asyncio.sleep(5)
    self.boss.incoming = [templates.generate_boss_event(15)]
    next_event = await self.boss.run()
    self.assertNotEqual(message_id, self.boss.message_id, 'Message IDs should be different.')
  
  @unittest.skip('Skipping test_incoming_event_with_msg_id')
  async def test_incoming_event_with_msg_id(self):
    self.boss.incoming = [templates.generate_boss_event(300)]
    self.boss.message_id = 12345
    next_event = await self.boss.run()
    self.assertEqual(self.boss.incoming[0], next_event, 'Event should stay the same.')
  
  @unittest.skip('Skipping test_incoming_event_without_msg_id')
  async def test_incoming_event_without_msg_id(self):
    self.boss.incoming = [templates.generate_boss_event(300)]
    next_event = await self.boss.run()
    self.assertEqual(self.boss.incoming[0], next_event, 'Event should stay the same.')

  @unittest.skip('Skipping test_edit_event')
  async def test_edit_event(self):
    self.boss.incoming = [templates.generate_boss_event(15)]
    await self.boss.run()
    await asyncio.sleep(5)
    self.boss.incoming = [
      templates.generate_boss_event(0, 'edit', False),
      templates.generate_boss_event(344)
    ]
    next_event = await self.boss.run()
    self.assertEqual(next_event, self.boss.incoming[0], 'Next event should be post type.')
  
  @unittest.skip('Skipping test_edit_event_no_next')
  async def test_edit_event_no_next(self):
    self.boss.incoming = [templates.generate_boss_event(0, 'edit', False)]
    next_event = await self.boss.run()
    self.assertIsNone(next_event, 'There shouldn\'t be next event.')
    



    

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
      Post message on discord, wait 5s and delete the message.
    '''
    from comunication import delete
    message_id = await self.post(self.embed, self.thumbnail)
    await asyncio.sleep(5)
    await delete(message_id)
  
  @unittest.skip('Skipping test_edit')
  async def test_edit(self):
    ''' 
      Post message on discord, wait 5s and edit the message.
    '''
    from comunication import edit
    message_id = await self.post(self.embed, self.thumbnail)
    await asyncio.sleep(5)
    self.embed.title = 'TEST'
    await edit(message_id, self.embed)

if __name__ == '__main__':
  unittest.main()