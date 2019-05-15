from py2neo.ogm import GraphObject, Property
from py2neo.ogm import RelatedTo, RelatedFrom


class Comment(GraphObject):

    text = Property()
    timestamp = Property()

    # Set of Comments posted by a Person
    comments = RelatedFrom("Person", "COMMENT_POSTED")

    # Set of Comments for a particular Image
    comment_on = RelatedTo("Image")

    def add_or_update(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)

    def __init__(self, **kwargs):
        self.add_or_update(**kwargs)

    def as_dict(self):
        return {
            'id': self._GraphObject__ogm.node._Entity__remote._id,
            'text': self.text,
            'timestamp': self.timestamp
        }

    def update(self, **kwargs):
        self.add_or_update(**kwargs)

    def add_or_update_comments(self, comments):
        for comment in comments:
            self.comments.update(comment)

    def remove_comments(self, comments):
        for comment in comments:
            self.comments.remove(comment)

    def add_or_update_comment_on(self, comment_on):
        for comment in comment_on:
            self.comment_on.update(comment)

    def remove_comment_on(self, comment_on):
        for comment in comment_on:
            self.comment_on.remove(comment)

    # Object level interfaces
    def fetch(self, graph):
        _id = self._GraphObject__ogm.node._Entity__remote._id
        return self.select(graph, _id).first()

    def fetch_by_id(self, graph, _id):
        return self.select(graph, _id).first()

    def save(self, graph):
        graph.push(self)

    def delete(self, graph):
        graph.delete(self)
