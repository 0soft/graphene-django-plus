import json
from graphene_django.views import GraphQLView as _GraphQLView


def _get_key(key):
    try:
        int_key = int(key)
    except (TypeError, ValueError):
        return key
    else:
        return int_key


def _get_shallow_property(obj, prop):
    if isinstance(prop, int):
        return obj[prop]

    try:
        return obj.get(prop)
    except AttributeError:
        return None


def _obj_set(obj, path, value):
    if isinstance(path, int):
        path = [path]

    if not path:
        return obj

    if isinstance(path, str):
        new_path = [_get_key(part) for part in path.split(".")]
        return _obj_set(obj, new_path, value)

    current_path = path[0]
    current_value = _get_shallow_property(obj, current_path)

    if len(path) == 1:
        obj[current_path] = value

    if current_value is None:
        try:
            if isinstance(path[1], int):
                obj[current_path] = []
            else:
                obj[current_path] = {}
        except IndexError:
            pass

    return _obj_set(obj[current_path], path[1:], value)


class GraphQLView(_GraphQLView):
    """GraphQLView with file upload support.

    Based on:
        https://github.com/mirumee/saleor/blob/master/saleor/graphql/views.py
    """

    @staticmethod
    def get_graphql_params(request, data):
        query, variables, operation_name, id_ = _GraphQLView.get_graphql_params(
            request,
            data,
        )

        content_type = _GraphQLView.get_content_type(request)
        if content_type == 'multipart/form-data':
            operations = json.loads(data.get('operations', "{}"))
            files_map = json.loads(data.get('map', '{}'))
            for k, v in files_map.items():
                for f in v:
                    _obj_set(operations, f, k)
            query = operations.get("query")
            variables = operations.get("variables")

        return query, variables, operation_name, id_
