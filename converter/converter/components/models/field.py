class Field():

    def __init__(self):
        self.name = None
        self.rname = None
        self.domain = None
        self.description = None

        # Props
        self.input = False
        self.edit = False
        self.show_in_grid = False
        self.show_in_details = False
        self.is_mean = False
        self.autocalculated = False
        self.required = False
