def serializedict(a) -> dict:
    return {**{i: str(a[i]) for i in a if i == '_id'}, **{i: a[i] for i in a if i != '_id'}}


def serializelist(entity) -> list:
    return [serializedict(a) for a in entity]
