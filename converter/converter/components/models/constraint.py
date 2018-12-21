from enum import Enum


class ConstraintType(Enum):
    PRIMARY = 'PRIMARY'
    FOREIGN = 'FOREIGN'


class Constraint:

    def __init__(self, name, kind, reference, props):
        self.name = name
        self.kind = kind
        self.reference = reference
        self.props = props
