from pydantic import BaseModel


class TODOCreateDTO(BaseModel):
    task_name: str
    task_description: str
