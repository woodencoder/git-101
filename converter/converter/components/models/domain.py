class Domain:

    def __init__(self, dictionary = {}):

        self.name = dictionary.get("name")
        self.description = dictionary.get("description")
        self.type = dictionary.get("type")
        self.align = dictionary.get("align")
        self.width = dictionary.get("width")
        self.precision = dictionary.get("precision")
        
        # Props
        self.show_null = dictionary.get("show_null", False)
        self.summable = dictionary.get("summable", False)
        self.case_sensitive = dictionary.get("case_sensitive", False)
        self.show_lead_nulls = dictionary.get("show_lead_nulls", False)
        self.thousands_separator = dictionary.get("thousands_separator", False)
        self.char_length = dictionary.get("char_length")
        self.length = dictionary.get("length")
        self.scale = dictionary.get("scale")
