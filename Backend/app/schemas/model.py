from pydantic import BaseModel, ConfigDict


class ModelBase(BaseModel):
    component_id: int
    name: str
    version: str
    file_path: str
    description: str | None = None


class ModelCreate(ModelBase):
    pass


class ModelResponse(ModelBase):
    id: int

    model_config = ConfigDict(from_attributes=True)