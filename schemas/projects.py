def ProjectEntity(item) -> dict:
    return {
        "id":str(item["_id"]),
        "name_project": item["name_project"],
        "description_project": item["description_project"],
        "status": (item["status"]),
        "id_ticket": (item["id_ticket"]),
    }

def ProjectsEntity(entity) -> list:
    return [ProjectEntity(item) for item in entity]