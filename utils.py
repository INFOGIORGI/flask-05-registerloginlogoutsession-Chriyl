def isEmpty(items: list[str]) -> bool:
    for item in items:
        if item == "":
            return True
    
    return False