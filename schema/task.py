from pydantic import BaseModel, model_validator


class TaskSchema(BaseModel):
    id: int | None = None
    name: str | None = None
    pomodoro_count: int | None = None
    category_id: int
    user_id: int

    class Config:
        from_attributes = True

    @model_validator(mode="after")
    def check_name_or_pomodoro_count_is_not_none(self):
        if self.name is None and self.pomodoro_count is None:
            raise ValueError("name or pomodoro_count must be provided")
        return self


class TaskCreateSchema(BaseModel):
    name: str | None = None
    pomodoro_count: int | None = None
    category_id: int
