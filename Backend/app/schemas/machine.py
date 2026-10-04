import pydantic
from pydantic import BaseModel, ConfigDict

class MachineBase(BaseModel):
    name : str
    machine_type : str
    serial_number : str | None = None
    description : str | None = None


class MachineCreate(MachineBase):
    pass

class MachineResponse (MachineBase):
    id : int

    model_config = ConfigDict (from_attributes = True)

