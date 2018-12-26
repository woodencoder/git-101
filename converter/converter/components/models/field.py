class Field():

    def __init__(self, dictionary = {}):
        self.name = dictionary.get("name")
        self.rname = dictionary.get("rname")
        self.domain = dictionary.get("domain")
        self.description = dictionary.get("description")

        # Props
        self.input = dictionary.get("input", False)
        self.edit = dictionary.get("edit", False)
        self.show_in_grid = dictionary.get("show_in_grid", False)
        self.show_in_details = dictionary.get("show_in_details", False)
        self.is_mean = dictionary.get("is_mean", False)
        self.autocalculated = dictionary.get("autocalculated", False)
        self.required = dictionary.get("required", False)
