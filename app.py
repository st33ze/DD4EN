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
  # if task is boss: await update.run() # Website data is updated 30 minutes before boss event.
  follow_up_task = await task.run()

















  # task = tasks.get_next()
  # await asyncio.sleep(task.get_seconds_to_start())
  # if task is update: await task.run()
  # elif task is boss: tasks.run_concurently(task, update)
  # else: task.run_concurently(task)




if __name__ == '__main__':
  asyncio.run(main())