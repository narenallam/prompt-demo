from pydantic import BaseModel, ConfigDict

class Person(BaseModel):
    eid: int
    name: str
    age: int
    email: str
    fillTimer: bool

person = Person(eid="1234", name="John", age=30.1, email="john@example.com", fillTimer="on")
print(person.model_dump_json())