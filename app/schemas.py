from pydantic import BaseModel, ConfigDict


class ItemBase(BaseModel):
    title: str
    description: str | None = None
    model_config = ConfigDict(from_attributes=True)


class ItemCreate(ItemBase):
    pass


class Item(ItemBase):
    id: int
