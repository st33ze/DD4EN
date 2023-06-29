from events import Tasks, Update, Boss
import asyncio

async def main():
  tasks = Tasks()
  boss = Boss()
  update = Update(tasks, [boss])
  
  # WHILE LOOP
  if not tasks.assigned: await update.run()


if __name__ == '__main__':
  asyncio.run(main())