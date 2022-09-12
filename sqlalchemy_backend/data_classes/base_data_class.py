from pandas import Series


class BaseDataClass:

    def to_dict(self):
        return {
            key: self.to_dict_value(value) for key, value in
            self.__dict__.items()
        }

    @classmethod
    def to_dict_value(cls, value):
        if hasattr(value, 'to_dict'):
            return value.to_dict()
        if isinstance(value, list):
            if value:
                if hasattr(value[0], 'to_dict'):
                    return [v.to_dict() for v in value]
        return value

    def __repr__(self):
        return self.to_json()

    def to_json(self):
        return Series(self.to_dict()).to_json(indent=2)

    def empty(self):
        return all(self.is_value_empty(value) for key, value in self.__dict__.items())

    @classmethod
    def is_value_empty(cls, value):
        if hasattr(value, 'empty'):
            return value.empty
        return value is None

    @classmethod
    def from_dict(cls, obj_dict: dict):
        return cls(**obj_dict)

    @classmethod
    def from_kwargs(cls, **kwargs):
        return cls.from_dict(kwargs)

    @classmethod
    def from_dict_values(cls, **dict_values):
        obj = cls()
        for key, value in dict_values.items():
            if hasattr(obj, key):
                setattr(obj, key, value)
        return obj
