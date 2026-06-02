from pydantic import BaseModel, ConfigDict, EmailStr


class UserSchema(BaseModel):
    id: int | None = None
    nome: str
    sobrenome: str
    email: EmailStr
    admin: int | None = 0
    model_config: ConfigDict = ConfigDict(from_attributes=True)

class CreateUserSchema(UserSchema):
    senha: str

