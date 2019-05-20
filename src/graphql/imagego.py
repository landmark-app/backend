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
    posters = RelatedFrom("Person", "IMAGES_POSTED")

    # Set of Comments posted on the Image
    comments = RelatedFrom("Comment", "COMMENT_ON")

    # Set of Images of particular LandMark
    landmarks = RelatedTo("LandMark")

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
    def add_or_update_posters(self, posters):
        for poster in posters:
            self.posters.update(poster)

    def add_or_update_poster(self, poster):
        self.posters.update(poster)

    def remove_posters(self, posters):
        for poster in posters:
            self.posters.remove(poster)

    def remove_poster(self, poster):
        self.posters.remove(poster)

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

    def add_or_update_landmarks(self, landmarks):
        for landmark in landmarks:
            self.landmarks.update(landmark)

    def add_or_update_landmark(self, landmark):
        self.landmarks.update(landmark)

    def remove_landmarks(self, landmarks):
        for landmark in landmarks:
            self.landmarks.remove(landmark)

    def remove_landmark(self, landmark):
        self.landmarks.remove(landmark)

    # Object level interfaces
    def save(self, graph):
        graph.push(self)

    def delete(self, graph):
        graph.delete(self)


# To avoid cyclic dependency import error
from commentgo import Comment  # noqa: E402 F401
from landmarkgo import LandMark  # noqa: E402 F401
from persongo import Person  # noqa: E402 F401
