from pydantic import BaseModel
from typing import Optional


class Task(BaseModel):
    header: str
    description: str
    done: Optional[bool] = False


class TaskList:

    def __init__(self):
        self.tasks_created: int = 0
        self.tasks: list[dict[str, int | Task]] = []

    def add_new(self, task: Task):
        self.tasks_created += 1
        self.tasks.append(
            {
                "task_id": self.tasks_created,
                "task": task
            }
        )

    def get_index_by_id(self, id_to_find: int):
        """
        :param id_to_find: task_id of desired task
        :return: tasks[] index or None

        Uses binary search since all task since all ids are sorted
        """
        start = 0
        stop = len(self.tasks) - 1
        while start < stop:
            pivot = (start + stop) // 2
            if self.tasks[pivot]["task_id"] == id_to_find:
                return pivot
            if self.tasks[pivot]["task_id"] > id_to_find:
                stop = pivot - 1
            else:
                start = pivot + 1

        if start == stop:
            if self.tasks[start]["task_id"] == id_to_find:
                return start
        return None

    def get_task_by_id(self, id_to_find: int):
        if self.get_index_by_id(id_to_find) is not None:
            return self.tasks[self.get_index_by_id(id_to_find)]
        return None

    def del_by_id(self, id_to_del: int):
        index_to_del = self.get_index_by_id(id_to_del)
        if index_to_del is not None:
            del self.tasks[index_to_del]
            return 1
        return None

    def upd_task(self, id_to_upd: int, updt_task: Task):
        if self.get_index_by_id(id_to_upd) is not None:
            self.tasks[self.get_index_by_id(id_to_upd)]["task"] = updt_task
            return 1
        return None
