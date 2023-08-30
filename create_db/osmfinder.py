import osmium


class AddressHandler(osmium.SimpleHandler):
    def __init__(self, filter, find_return_format):
        super(AddressHandler, self).__init__()
        self.filter = filter
        self.find_return_format = find_return_format
        self.elements = []

    def node(self, n):
        if self.filter(n):
            self.elements.append(self.find_return_format(n))
        
    def way(self, w):
        if self.filter(w):
            self.elements.append(self.find_return_format(w))

    def relation(self, r):
        if self.filter(r):
            self.elements.append(self.find_return_format(r))
