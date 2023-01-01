from ..database_engines.postgres import (
    PostgresHAInstance,
    PostgresSingleInstance,
)
from ...constants import NDB


def get_engine_type(module):
    engine_types = NDB.DatabaseTypes.ALL

    for type in engine_types:
        if type in module.params:
            return type, None

    return None, "Input doesn't conatains config for allowed engine types of databases"


def create_db_engine(module):
    engines = {"postgres": {"single": PostgresSingleInstance, "ha": PostgresHAInstance}}

    engine_type, err = get_engine_type(module)
    if err:
        return None, err

    db_architecture = module.params[engine_type].get("type")

    if engine_type in engines:
        if (
            db_architecture
            and isinstance(engines[engine_type], dict)
            and db_architecture in engines[engine_type]
        ):
            return engines[engine_type][db_architecture](module), None
        else:
            return (
                None,
                "Invalid database engine architecture: {0} given for {1}".format(
                    db_architecture, engine_type
                ),
            )
    else:
        return None, "Invalid database engine type: {0}".format(engine_type)
