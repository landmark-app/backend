from py2neo.ogm import GraphObject, Property
from py2neo.ogm import RelatedTo, RelatedFrom


class Comment(GraphObject):
    __primarykey__ = "key"

    key = Property()
    text = Property()
    timestamp = Property()

    # Comment posted by a Person
    poster = RelatedFrom("Person", "COMMENT_POSTED")

    # Comment for a particular Image
    image = RelatedTo("Image")

    def add_or_update(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)

    def __init__(self, **kwargs):
        self.add_or_update(**kwargs)

    def as_dict(self):
        return {
            'key': self.key,
            'text': self.text,
            'timestamp': self.timestamp
        }

    def update(self, **kwargs):
        self.add_or_update(**kwargs)

    # List interfaces
    def add_or_update_poster(self, poster):
        self.poster.update(poster)

    def remove_poster(self, poster):
        self.poster.remove(poster)

    def add_or_update_image(self, image):
        self.image.update(image)

    def remove_image(self, image):
        self.image.remove(image)

    # Object level interfaces
    def save(self, graph):
        graph.push(self)

    def delete(self, graph):
        graph.delete(self)


# To avoid cyclic dependency import error
from imagego import Image  # noqa: E402 F401
from persongo import Person  # noqa: E402 F401
