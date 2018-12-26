class Table:

    def __init__(self, dictionary = {}):
        self.name = dictionary.get("name")
        self.description = dictionary.get("description")

        self.fields = []
        self.constraints = []
        self.indices = []

        # Props
        self.add = dictionary.get("add", False)
        self.edit = dictionary.get("edit", False)
        self.delete = dictionary.get("delete", False)

        self.ht_table_flags = dictionary.get("ht_table_flags")
        self.access_level = dictionary.get("access_level")



