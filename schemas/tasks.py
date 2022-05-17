def TaskEntity(item) -> dict:
    return {
        "id":str(item["_id"]),
        "name_task": item["name_task"],
        "description_task": item["description_task"],
        "status": str(item["status"]),
        "id_project": item["id_project"],
    }


def TasksEntity(entity) -> list:
    return [TaskEntity(item) for item in entity]