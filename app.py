from events import Tasks, Update, Boss
import asyncio

async def main():
  tasks = Tasks()
  boss = Boss()
  update = Update([boss], tasks)
  
  # Initial update.
  await update.run()
 
  # WHILE LOOP
  # while update.fails < update.MAX_FAILS:
  if not tasks.assigned: tasks.add(update)
  task = tasks.get_next()
  await asyncio.sleep(task.get_seconds_to_start())
  # Boss location is updated 30 minutes before the event.
  # Runs update before sending detailed boss notification.
  follow_up_task = await task.run(update) if task is boss else await task.run()

















  # task = tasks.get_next()
  # await asyncio.sleep(task.get_seconds_to_start())
  # if task is update: await task.run()
  # elif task is boss: tasks.run_concurently(task, update)
  # else: task.run_concurently(task)




if __name__ == '__main__':
  asyncio.run(main())