from fastapi import FastAPI
from homework05.tasks import Task, TaskList


app = FastAPI()
task_list = TaskList()


@app.get("/tasks")
async def all_tasks():
    return task_list.tasks


@app.get("/tasks/{task_id}")
async def task_by_id(task_id: int):
    return task_list.get_task_by_id(task_id)


@app.post("/tasks")
async def new_task(task: Task):
    task_list.add_new(task)
    return task_list.tasks


@app.put("/tasks/{task_id}")
async def upd_task(task_id: int, task: Task):
    if task_list.upd_task(task_id, task):
        return task_list.get_task_by_id(task_id)
    return {"message": "task not found"}


@app.delete("/tasks/{task_id}")
async def del_task(task_id: int):
    if task_list.del_by_id(task_id):
        return {"message": "task has been deleted successfully"}
    return {"message": "task not found"}
