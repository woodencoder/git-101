class Table:

    def __init__(self):
        self.name = None
        self.description = None

        self.fields = []
        self.constraints = []
        self.indices = []

        # Props
        self.add = False
        self.edit = False
        self.delete = False
        self.ht_table_flags = None
        self.access_level = None
