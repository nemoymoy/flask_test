import pydantic
from errors import HttpError

class BaseUserRequest(pydantic.BaseModel):
    login: str
    password: str

    @pydantic.field_validator('password')
    @classmethod
    def secure_password(cls, v: str):
        if len(v) < 8:
            raise ValueError('password must be at least 8 characters long')
        return v

class CreateUserRequest(BaseUserRequest):
    pass

class UpdateUserRequest(BaseUserRequest):
    login: str | None = None
    password: str | None = None

def validate(schema: type[CreateUserRequest | UpdateUserRequest], json_data: dict):
    try:
        schema_instance = schema(**json_data)
        return schema_instance.model_dump(exclude_unset=True)
    except pydantic.ValidationError as e:
        errors = e.errors()
        for error in errors:
            error.pop('ctx', None)
        raise HttpError(400, errors)
