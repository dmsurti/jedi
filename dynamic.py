"""
For dynamic completion.
"""
import parsing
import evaluate

# This is something like the sys.path, but only for searching params. It means
# that this is the order in which Jedi searches params.
search_param_modules = ['.']


class ParamListener(object):
    """
    This listener is used to get the params for a function.
    """
    def __init__(self):
        self.param_possibilities = []

    def execute(self, params):
        self.param_possibilities.append(params)


def search_params(param):
    def get_params_for_module(module):
        try:
            possible_stmts = current_module.used_names[func_name]
        except KeyError:
            return []

        for stmt in possible_stmts:
            evaluate.follow_statement(stmt)

        result = []
        for params in listener.param_possibilities:
            for p in params:
                if str(p) == param_name:
                    result += evaluate.follow_statement(p.parent)
        #print listener.param_possibilities, param, result

        return result

    func = param.get_parent_until(parsing.Function)

    # add the listener
    listener = ParamListener()
    func.listeners.add(listener)

    func_name = str(func.name)

    # get the param name
    if param.assignment_details:
        arr = param.assignment_details[0][1]
    else:
        arr = param.get_assignment_calls()
    param_name = str(arr[0][0].name)

    current_module = param.get_parent_until()

    result = get_params_for_module(current_module)

    # TODO check other modules
    # cleanup: remove the listener
    func.listeners.remove(listener)

    return result
