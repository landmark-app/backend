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
    followings = RelatedTo("Person", "FOLLOWINGS")

    # Set of Person who follow the Person
    followers = RelatedFrom("Person", "FOLLOWERS")

    # Set of Landmarks visted by Person
    visited = RelatedTo("LandMark")

    # Set of Images posted by Person
    posted_images = RelatedTo("Image")

    # Set of Comments posted by Person
    posted_comments = RelatedTo("Comment")

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

    def add_or_update_friend(self, friend):
        self.friends.update(friend)

    def remove_friends(self, friends):
        for friend in friends:
            self.friends.remove(friend)

    def remove_friend(self, friend):
        self.friends.remove(friend)

    def add_or_update_followings(self, followings):
        for following in followings:
            self.followings.update(following)

    def add_or_update_following(self, following):
        self.followings.update(following)

    def remove_followings(self, followings):
        for following in followings:
            self.followings.remove(following)

    def remove_following(self, following):
        self.followings.remove(following)

    def add_or_update_followers(self, followers):
        for follower in followers:
            self.followers.update(follower)

    def add_or_update_follower(self, follower):
        self.followers.update(follower)

    def remove_followers(self, followers):
        for follower in followers:
            self.followers.remove(follower)

    def remove_follower(self, follower):
        self.followers.remove(follower)

    def add_or_update_visited_landmarks(self, landmarks):
        for landmark in landmarks:
            self.visited.update(landmark)

    def add_or_update_visited_landmark(self, landmark):
        self.visited.update(landmark)

    def remove_visited_landmarks(self, landmarks):
        for landmark in landmarks:
            self.visited.remove(landmark)

    def remove_visited_landmark(self, landmark):
        self.visited.remove(landmark)

    def add_or_update_posted_images(self, images):
        for image in images:
            self.posted_images.update(image)

    def add_or_update_posted_image(self, image):
        self.posted_images.update(image)

    def remove_posted_images(self, images):
        for image in images:
            self.posted_images.remove(image)

    def remove_posted_image(self, image):
        self.posted_images.remove(image)

    def add_or_update_posted_comments(self, comments):
        for comment in comments:
            self.posted_comments.update(comment)

    def add_or_update_posted_comment(self, comment):
        self.posted_comments.update(comment)

    def remove_posted_comments(self, comments):
        for comment in comments:
            self.posted_comments.remove(comment)

    def remove_posted_comment(self, comment):
        self.posted_comments.remove(comment)

    # Object level interfaces
    def save(self, graph):
        graph.push(self)

    def delete(self, graph):
        graph.delete(self)


# To avoid cyclic dependency import error
from .commentgo import Comment  # noqa: E402 F401
from .imagego import Image  # noqa: E402 F401
from .landmarkgo import LandMark  # noqa: E402 F401
