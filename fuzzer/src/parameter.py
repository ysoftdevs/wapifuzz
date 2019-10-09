from typing import Union


class Parameter:
    def __init__(self, name: str, value: str, data_type: Union[str, None], data_format: Union[str, None], is_from_config: bool):
        self.name = name
        self.value = value
        self.data_type = data_type
        self.data_format = data_format
        self.is_from_config = is_from_config
