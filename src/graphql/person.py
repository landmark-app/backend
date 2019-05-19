from py2neo.ogm import GraphObject, Property
from py2neo.ogm import RelatedTo, RelatedFrom, Related


class Person(GraphObject):
    __primarykey__ = "key"

    key = Property()
    name = Property()
    rank = Property()
    score = Property()
    bio = Property()
    email = Property()
    phone = Property()

    # Set of friends. This is bi-directional relationship
    friends = Related("Person")

    # Set of Person whom the Person follows
    follows = RelatedTo("Person", "FOLLOWS")

    # Set of Person who follow the Person
    followed_by = RelatedFrom("Person", "FOLLOWED_BY")

    # Set of Landmarks visted by Person
    visited = RelatedTo("LandMark")

    # Set of Images posted by Person
    images_posted = RelatedTo("Image")

    # Set of Comments posted by Person
    comments_posted = RelatedTo("Comment")

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
            'rank': self.rank,
            'score': self.score,
            'bio': self.bio,
            'email': self.email,
            'phone': self.phone,
        }

    def update(self, **kwargs):
        self.add_or_update(**kwargs)

    # List interfaces
    def add_or_update_friends(self, friends):
        for friend in friends:
            self.friends.update(friend)

    def remove_friends(self, friends):
        for friend in friends:
            self.friends.remove(friend)

    def add_or_update_follows(self, follows):
        for follow in follows:
            self.follows.update(follow)

    def remove_follows(self, follows):
        for follow in follows:
            self.follows.remove(follow)

    def add_or_update_followed_by(self, followed_by):
        for follower in followed_by:
            self.followed_by.update(follower)

    def remove_followed_by(self, followed_by):
        for follower in followed_by:
            self.followed_by.remove(follower)

    def add_or_update_visited(self, visited):
        for visit in visited:
            self.visited.update(visit)

    def remove_visited(self, visited):
        for visit in visited:
            self.visited.remove(visit)

    def add_or_update_images_posted(self, images_posted):
        for image in images_posted:
            self.images_posted.update(image)

    def remove_images_posted(self, images_posted):
        for image in images_posted:
            self.images_posted.remove(image)

    def add_or_update_comments_posted(self, comments_posted):
        for comment in comments_posted:
            self.comments_posted.update(comment)

    def remove_comments_posted(self, comments_posted):
        for comment in comments_posted:
            self.comments_posted.remove(comment)

    # Object level interfaces
    def save(self, graph):
        graph.push(self)

    def delete(self, graph):
        graph.delete(self)
