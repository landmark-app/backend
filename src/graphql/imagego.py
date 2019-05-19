from py2neo.ogm import GraphObject, Property
from py2neo.ogm import RelatedTo, RelatedFrom


class Image(GraphObject):
    __primarykey__ = "key"

    key = Property()
    url = Property()
    description = Property()
    score = Property()
    private = Property()
    timestamp = Property()

    # Set of Images posted by a Person
    posted_by = RelatedFrom("Person", "IMAGES_POSTED")

    # Set of Comments posted on the Image
    comments = RelatedFrom("Comment", "COMMENT_ON")

    # Set of Images of particular LandMark
    images_of = RelatedTo("LandMark")

    def add_or_update(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)

    def __init__(self, **kwargs):
        self.add_or_update(**kwargs)

    def as_dict(self):
        return {
            'key': self.key,
            'url': self.url,
            'description': self.description,
            'score': self.score,
            'private': self.private,
            'timestamp': self.timestamp
        }

    def update(self, **kwargs):
        self.add_or_update(**kwargs)

    # List interfaces
    def add_or_update_posted_by(self, posted_by):
        for poster in posted_by:
            self.posted_by.update(poster)

    def remove_posted_by(self, posted_by):
        for poster in posted_by:
            self.posted_by.remove(poster)

    def add_or_update_comments(self, comments):
        for comment in comments:
            self.comments.update(comment)

    def remove_comments(self, comments):
        for comment in comments:
            self.comments.remove(comment)

    def add_or_update_images_of(self, images_of):
        for image in images_of:
            self.images_of.update(image)

    def remove_images_of(self, images_of):
        for image in images_of:
            self.images_of.remove(image)

    # Object level interfaces
    def fetch(self, graph):
        return self.select(graph, self.key).first()

    def fetch_by_key(self, graph, key):
        return self.select(graph, key).first()

    def save(self, graph):
        graph.push(self)

    def delete(self, graph):
        graph.delete(self)
