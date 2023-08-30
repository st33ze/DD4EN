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
  # Run update if the last update time is older than 30 minutes before boss event.
  if (task is boss and 
      boss.get_next()['type'] == 'post' and
      update.get_last_time() < boss.get_next()['runtime']):
      update.run()
      continue
  follow_up_task = await task.run()

















  # task = tasks.get_next()
  # await asyncio.sleep(task.get_seconds_to_start())
  # if task is update: await task.run()
  # elif task is boss: tasks.run_concurently(task, update)
  # else: task.run_concurently(task)




if __name__ == '__main__':
  asyncio.run(main())