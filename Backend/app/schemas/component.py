from pydantic import BaseModel, ConfigDict

class ComponentBase (BaseModel):
    machine_id : int
    name : str
    component_type : str
    description : str | None = None


class ComponentCreate (ComponentBase):
    pass


class ComponentResponse (ComponentBase):
    id : int


    model_config = ConfigDict(from_attributes = True)



