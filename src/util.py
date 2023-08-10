def list_to_str(items):
    if len(items) == 0:
        return "`empty`"

    def append(item):
        return "`" + str(item) + "`"

    result = ""
    for i in items[:-1]:
        result += append(i) + ", "

    return result + append(items[-1])
