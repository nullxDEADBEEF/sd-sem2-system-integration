from bottle import delete, error, get, hook, post, put, run, request, response
import json
import uuid

# Dont want a headache in Distributed Systems when integrating? use UUID4 :))
# Example: integrating two databases with clashing id's. Good luck mate...

items = [{"id": "3ad2ffc0-e40c-4c97-a59f-c65c46bf53d5", "name": "a", "last_name": "b"}]


@hook("after_request")
def _():
    response.content_type = "application/json"


@get("/")
def _():
    return "home"


@get("/items")
def _():
    # return {"id": "3ad2ffc0-e40c-4c97-a59f-c65c46bf53d5", "name": "a"}
    return json.dumps(items)


@get("/items/<item_id>")
def _(item_id):
    item = [item for item in items if item["id"] == item_id]
    if item:
        return json.dumps(item[0])
    response.status = 204
    return


@post("/items")
def _():
    item_id = str(uuid.uuid4())
    item_name = request.json.get("name")
    item = {"id": item_id, "name": item_name}
    items.append(item)
    print(type(item_id))
    response.status = 201
    return {"id": item_id}


@delete("/items/<item_id>")
def _(item_id):
    for index, item in enumerate(items):
        if item["id"] == item_id:
            items.pop(index)
            return {"info": "item deleted"}
    response.status = 204
    return
    # What is this? 204 doesnt return anything :^)
    # return json.dumps({"info": f"item with {item_id} not found"})


@put("/items/<item_id>")  # technically we want to patch here :D
def _(item_id):
    try:
        item = [item for item in items if item["id"] == item_id][0]
        for key in item.keys():
            if key in request.json.keys():
                item[key] = request.json.get(key)
        return json.dumps(item)
    except Exception as ex:
        print(ex)
        response.status = 204
        return


@error(404)
def _(error):
    response.content_type = "application/json"
    return json.dumps({"info": "page not found"})


run(host="127.0.0.1", port=5000, debug=True, reloader=True, server="paste")
