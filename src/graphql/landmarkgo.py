from py2neo.ogm import GraphObject, Property
from py2neo.ogm import RelatedFrom


class LandMark(GraphObject):
    __primarykey__ = "key"

    key = Property()
    name = Property()
    description = Property()

    # Location information
    latitude = Property()
    longitude = Property()
    city = Property()
    state = Property()
    country = Property()
    continent = Property()

    # Set of people who visited the LandMark
    visitors = RelatedFrom("Person", "VISITED")

    # Set of images of LandMark
    images = RelatedFrom("Image", "IMAGES_OF")

    def add_or_update(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)

    def __init__(self, **kwargs):
        self.add_or_update(**kwargs)

    def as_dict(self):
        return {
            'key': self.key,
            'name': self.name,
            'description': self.description,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'city': self.city,
            'state': self.state,
            'country': self.country,
            'continent': self.continent
        }

    def update(self, **kwargs):
        self.add_or_update(**kwargs)

    # List interfaces
    def add_or_update_visitors(self, visitors):
        for visitor in visitors:
            self.visitors.update(visitor)

    def add_or_update_visitor(self, visitor):
        self.visitors.update(visitor)

    def remove_visitors(self, visitors):
        for visitor in visitors:
            self.visitors.remove(visitor)

    def remove_visitor(self, visitor):
        self.visitors.remove(visitor)

    def add_or_update_images(self, images):
        for image in images:
            self.images.update(image)

    def add_or_update_image(self, image):
        self.images.update(image)

    def remove_images(self, images):
        for image in images:
            self.images.remove(image)

    def remove_image(self, image):
        self.images.remove(image)

    # Object level interfaces
    def save(self, graph):
        graph.push(self)

    def delete(self, graph):
        graph.delete(self)


# To avoid cyclic dependency import error
from imagego import Image  # noqa: E402 F401
from persongo import Person  # noqa: E402 F401
