import unittest

class TestBoss(unittest.TestCase):
  def setUp(self):
    from events import Boss
    # from discord import Embed
    from datetime import datetime, timedelta
    self.datetime = datetime
    self. timedelta = timedelta
    self.boss = Boss()
    self.boss.incoming = [
      {
        'name': 'Ashava',
        'time': datetime.now() + timedelta(minutes=188),
        'zone': 'Kehjistan',
        'territory': 'Seared Basin'
      },
      {
        'name': 'The Wandering Death',
        'time': datetime.now() + timedelta(minutes=299)
      }
    ]

  def test_embed_without_location(self):
    event = self.boss.incoming[1]
    embed = self.boss.create_embed(event)
    self.assertEqual(len(embed.fields), 1, 'Wrong fields size in embed object.')
  
  def test_embed_with_location(self):
    event = self.boss.incoming[0]
    embed = self.boss.create_embed(event)
    self.assertEqual(len(embed.fields), 3, 'Wrong fields size in embed object.')

  def test_embed_without_next_expected(self):
    self.boss.incoming[0]['time'] = self.datetime.now() - self.timedelta(minutes=55)
    event = self.boss.incoming[0]
    embed = self.boss.create_embed(event)
    self.assertIsNone(embed.footer.text, 'There should not be a footer text')

  def test_embed_with_next_expected(self):
    event = self.boss.incoming[0]
    embed = self.boss.create_embed(event)
    self.assertIsNotNone(embed.footer.text, 'There should be a footer text')
  
class TestCommunicatons(unittest.IsolatedAsyncioTestCase):
  def setUp(self):
    from comunication import post
    from discord import Embed, File
    from template_data import embed_template
    template = embed_template
    self.embed = Embed.from_dict(template)
    self.thumbnail = File('img/avarice.jpg', filename='avarice.jpg')
    self.post = post
  
  @unittest.skip('Skipping test_post')
  async def test_post(self):
    message_id = await self.post(self.embed, self.thumbnail)
    self.assertIsInstance(message_id, int)

if __name__ == '__main__':
  unittest.main()