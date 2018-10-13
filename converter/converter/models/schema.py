class Schema:

    def __init__(self,
                 domains=[],
                 tables=[],
                 fulltext_engine='',
                 version='',
                 name='',
                 description=''):
        self.domains = domains
        self.tables = tables
        self.fulltext_engine = fulltext_engine
        self.version = version
        self.name = name
        self.description = description
