from comunication import get_data
from data import Data
import asyncio






async def main():
  tasks = []
  world_boss = Data('wb')
  while True:
    




  # world_boss.update_wb(await get_data())
  # print(world_boss.incoming, world_boss.expected, world_boss.nextExpected)

if __name__ == '__main__':
  asyncio.run(main())