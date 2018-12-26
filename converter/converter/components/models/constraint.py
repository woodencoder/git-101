
class Constraint:

    def __init__(self, dictionary = {}):
        self.name = dictionary.get("name")
        self.kind = dictionary.get("kind")
        self.items = dictionary.get("items")
        self.reference_type = dictionary.get("reference_type")
        self.reference = dictionary.get("reference")
        self.expression = dictionary.get("expression")

        # Props
        self.has_value_edit = dictionary.get("has_value_edit", False)
        self.cascading_delete = dictionary.get("cascading_delete", False)
        self.full_cascading_delete = dictionary.get("full_cascading_delete", False)
