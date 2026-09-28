from flask import request

TRUE_VALUES = {"true", "1", "yes", "on"}
FALSE_VALUES = {"false", "0", "no", "off"}


def json_body():
    data = request.get_json(silent=True)
    return data if isinstance(data, dict) else None


def as_text(value, field, max_length):
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"Field '{field}' must be a non-empty string")

    text = value.strip()

    if len(text) > max_length:
        raise ValueError(f"Field '{field}' must be at most {max_length} characters")

    return text


def as_int(value, field, minimum=None, maximum=None):
    if isinstance(value, bool):
        raise ValueError(f"Field '{field}' must be an integer")

    if isinstance(value, int):
        number = value
    elif isinstance(value, float) and value.is_integer():
        number = int(value)
    elif isinstance(value, str) and value.strip().lstrip("-").isdigit():
        number = int(value.strip())
    else:
        raise ValueError(f"Field '{field}' must be an integer")

    if minimum is not None and number < minimum:
        raise ValueError(f"Field '{field}' must be >= {minimum}")

    if maximum is not None and number > maximum:
        raise ValueError(f"Field '{field}' must be <= {maximum}")

    return number


def as_bool(value, field="is_active"):
    if isinstance(value, bool):
        return value

    if isinstance(value, int):
        return bool(value)

    if isinstance(value, str):
        lowered = value.strip().lower()
        if lowered in TRUE_VALUES:
            return True
        if lowered in FALSE_VALUES:
            return False

    raise ValueError(f"Field '{field}' must be a boolean")
