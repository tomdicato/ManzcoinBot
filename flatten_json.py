def flatten_json(nested_json, exclude=[""]):
    """Flatten json object with nested keys into a single level.
    Args:
        nested_json: A nested json object.
        exclude: Keys to exclude from output.
    Returns:
        The flattened json object if successful, None otherwise.
    """
    out = {}

    def flatten(x, name="", exclude=exclude):
        if type(x) is dict:
            for a in x:
                if a not in exclude:
                    flatten(x[a], name + a + "_")
        elif type(x) is list:
            i = 0
            for a in x:
                flatten(a, name + str(i) + "_")
                i += 1
        else:
            out[name[:-1]] = x

    flatten(nested_json)
    return out