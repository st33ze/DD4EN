# Comunication module responsible for getting data from webpage and 
# sending processed data to the discord channel
from dotenv import dotenv_values
from discord import Webhook
import aiohttp
import asyncio

CONFIG = dotenv_values('.env')

async def send_request(session, url):
  try:
    async with session.get(url) as response:
      assert response.status == 200
      return await response.json()
  except AssertionError as e: print(f'Assertion Error occured. {e}')
  except Exception as e: print(f'Request exception occured: {e}')

async def get_data():
  ''' 
    Sends max 5 requests, time between each request doubles.
    Returns: data or None 
  '''
  tries = 5
  time_stamp = 30
  session = aiohttp.ClientSession()
  while tries > 0:
    tries -= 1
    data = await send_request(session, CONFIG['URL'])
    if not data and tries > 1: 
      await asyncio.sleep(time_stamp) 
      time_stamp *= 2
  await session.close()
  return data

async def post(embed, thumbnail=None):
  ''' 
  Sends embed message to discord channel.
  Returns: Message ID. 
  '''
  async with aiohttp.ClientSession() as session:
    webhook = Webhook.from_url(CONFIG['WEBHOOK_URL'], session=session)
    message = await webhook.send(file=thumbnail, wait=True, embed=embed)
    return message.id

async def delete(message_id):
  '''
    Deletes message by message_id from the discord channel.
  '''
  async with aiohttp.ClientSession() as session:
    webhook = Webhook.from_url(CONFIG['WEBHOOK_URL'], session=session)
    message = await webhook.fetch_message(message_id)
    await message.delete()

async def edit(message_id, embed):
  '''
    Edit message by message_id from the discord channel.
  '''
  async with aiohttp.ClientSession() as session:
    webhook = Webhook.from_url(CONFIG['WEBHOOK_URL'], session=session)
    message = await webhook.fetch_message(message_id)
    await message.edit(embed=embed)