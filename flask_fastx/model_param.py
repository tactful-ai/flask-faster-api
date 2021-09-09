def prepare_param(params):
    """Prepare the parameter"""
    if hasattr(params, '__annotations__'):
        params = params.__annotations__
        for param in params:
            print("param1", params[param])
            params[param] = prepare_param(params[param])
            print("param2", params[param])
    return params
