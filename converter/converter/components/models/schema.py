class Schema:

    # def __init__(self):
    #     self.fulltext_engine = None
    #     self.version = None
    #     self.name = None
    #     self.description = None
    #     self.domains = []
    #     self.tables = []


    # def __init__(self, metadata = []):
    #     self.fulltext_engine = None
    #     self.version = None
    #     self.name = None
    #     self.description = None
    #     self.domains = []
    #     self.tables = []

    def __init__(self, metadata = {}):
        self.fulltext_engine = metadata.get("fulltext_engine")
        self.version = metadata.get("version")
        self.name = metadata.get("name")
        self.description = metadata.get("description")
        self.domains = []
        self.tables = []