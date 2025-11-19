from fastapi import FastAPI
from space_data import space_data
from pydantic import BaseModel
app = FastAPI()

class SpaceItem(BaseModel):
    name: str
    type: str
    distance_light_years: int

@app.get("/")
def get_space_data(_id: int):
    if _id not in space_data:
        return {"Error": "Invalid param!"}
    return {"data" : space_data[_id]}

@app.post("/")
def add_space_data(data: SpaceItem):
    new_id = max(space_data.keys()) + 1
    space_data[new_id] = data.model_dump()

    return {"new_id": new_id, "data": space_data[new_id]}

@app.put("/edit/{_id}/{field}/{data}")
def change_data(_id: int, field: str, data: str|int):
    if _id not in space_data:
        return {"error": "wrong index!"}

    if field not in space_data[_id].keys():
        return {"error": "wrong field!"}

    original_value = space_data[_id][field]
    if isinstance(original_value, int):
        data = int(data)

    space_data[_id][field] = data

    return {"id": _id, "changed field": field, "new value": data}



if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
