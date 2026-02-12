class ChoiceMixin:
    @classmethod
    def choices(cls):
        return [(choice.name, choice.value) for choice in cls]

    @classmethod
    def names(cls):
        return [choice.name for choice in cls]

    @classmethod
    def values(cls):
        return [choice.value for choice in cls]

    @classmethod
    def from_value(cls, value: str):
        for choice in cls:
            if choice.value == value:
                return choice
