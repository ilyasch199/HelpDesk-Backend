def TicketEntity(item) -> dict:
    return {
        "id":str(item["_id"]),
        "name_ticket": item["name_ticket"],
        "description_ticket": item["description_ticket"],
        "date_ticket": str(item["date_ticket"]),
        "assign_to": str(item["assign_to"]),
        "date_of_assignment": str(item["date_of_assignment"]),
        "status": str(item["status"]),
        "user_id": item["user_id"],
        "id_project": item["id_project"],
    }


def ticketsEntity(entity) -> list:
    return [TicketEntity(item) for item in entity]