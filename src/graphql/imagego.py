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

    # Image posted by a Person
    poster = RelatedFrom("Person", "IMAGES_POSTED")

    # Set of Comments posted on the Image
    comments = RelatedFrom("Comment", "COMMENT_ON")

    # Image of particular LandMark
    landmark = RelatedTo("LandMark")

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
    def add_or_update_poster(self, poster):
        self.poster.update(poster)

    def remove_poster(self, poster):
        self.poster.remove(poster)

    def add_or_update_comments(self, comments):
        for comment in comments:
            self.comments.update(comment)

    def add_or_update_comment(self, comment):
        self.comments.update(comment)

    def remove_comments(self, comments):
        for comment in comments:
            self.comments.remove(comment)

    def remove_comment(self, comment):
        self.comments.remove(comment)

    def add_or_update_landmark(self, landmark):
        self.landmark.update(landmark)

    def remove_landmark(self, landmark):
        self.landmark.remove(landmark)

    # Object level interfaces
    def save(self, graph):
        graph.push(self)

    def delete(self, graph):
        graph.delete(self)


# To avoid cyclic dependency import error
from .commentgo import Comment  # noqa: E402 F401
from .landmarkgo import LandMark  # noqa: E402 F401
from .persongo import Person  # noqa: E402 F401
