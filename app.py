from comunication import get_data
import asyncio






async def main():
  data = await get_data()
  print(data)

if __name__ == '__main__':
  asyncio.run(main())