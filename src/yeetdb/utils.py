from pydantic import create_model, validator

def create_model_for_table(tablename, cols):

    def validate_length(cls, v, values, **kwargs):
        col_value = v
        col_length = lengths[kwargs["field"].name]
        assert col_length >= len(f"{col_value}")
        return col_value

    lengths = {}
    validators = {}
    fields = {}
    for key, value in cols.items():
        lengths[key] = value[1]
        validators[f"{key}_validator"] = validator(key, allow_reuse=True)(validate_length)
        if value[0] == "int":
            fields[key] = (int, ...)
        if value[0] == "str":
            fields[key] = (str, ...)

    table = create_model(
        tablename,
        **fields,
        __validators__=validators
    )
    return table
