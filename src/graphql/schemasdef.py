import datetime
import graphene
from neotime import DateTime


class CustomGrapheneDateTime(graphene.DateTime):
    @staticmethod
    def serialize(date):
        if isinstance(date, DateTime):
            date = datetime.datetime(date.year, date.month, date.day,
                                     date.hour, date.minute, int(date.second),
                                     int(date.second * 1000000 % 1000000),
                                     tzinfo=date.tzinfo)
        return graphene.DateTime.serialize(date)


class LandMarkSchema(graphene.ObjectType):
    key = graphene.String()
    name = graphene.String()
    description = graphene.String()

    # Location information
    latitude = graphene.Float()
    longitude = graphene.Float()
    city = graphene.String()
    state = graphene.String()
    country = graphene.String()
    continent = graphene.String()


class LandMarkInput(graphene.InputObjectType):
    key = graphene.String(required=True)
    name = graphene.String()
    description = graphene.String()

    # Location information
    latitude = graphene.Float()
    longitude = graphene.Float()
    city = graphene.String()
    state = graphene.String()
    country = graphene.String()
    continent = graphene.String()


class PersonSchema(graphene.ObjectType):
    key = graphene.String()
    name = graphene.String()
    rank = graphene.Int()
    score = graphene.Float()
    bio = graphene.String()
    email = graphene.String()
    phone = graphene.String()


class PersonInput(graphene.InputObjectType):
    key = graphene.String(required=True)
    name = graphene.String()
    rank = graphene.Int()
    score = graphene.Float()
    bio = graphene.String()
    email = graphene.String()
    phone = graphene.String()


class ImageSchema(graphene.ObjectType):
    key = graphene.String()
    url = graphene.String()
    description = graphene.String()
    score = graphene.Float()
    private = graphene.Boolean()
    timestamp = CustomGrapheneDateTime()


class ImageInput(graphene.InputObjectType):
    key = graphene.String(required=True)
    url = graphene.String()
    description = graphene.String()
    score = graphene.Float()
    private = graphene.Boolean()
    timestamp = CustomGrapheneDateTime()


class CommentSchema(graphene.ObjectType):
    # key = graphene.String()
    text = graphene.String()
    timestamp = CustomGrapheneDateTime()


class CommentQuerySchema(graphene.ObjectType):
    key = graphene.Int()
    text = graphene.String()
    timestamp = CustomGrapheneDateTime()


class CommentInput(graphene.InputObjectType):
    # key = graphene.String(required=True)
    text = graphene.String()
    timestamp = CustomGrapheneDateTime()


class CommentDeleteInput(graphene.InputObjectType):
    key = graphene.Int()


# LandMark Person relationship
class VisitorInput(graphene.InputObjectType):
    landmark_key = graphene.String(required=True)
    visitor_key = graphene.String(required=True)


# LandMark Image relationship
class LandMarkImageInput(graphene.InputObjectType):
    landmark_key = graphene.String(required=True)
    image_key = graphene.String(required=True)


# Friend relationship
class FriendsInput(graphene.InputObjectType):
    friend1_key = graphene.String(required=True)
    friend2_key = graphene.String(required=True)


# Following relationship
class FollowingInput(graphene.InputObjectType):
    person_key = graphene.String(required=True)
    follower_key = graphene.String(required=True)


# Person Image relationship
class PersonImageInput(graphene.InputObjectType):
    person_key = graphene.String(required=True)
    image_key = graphene.String(required=True)


# Person Comment relationship
class PersonCommentInput(graphene.InputObjectType):
    person_key = graphene.String(required=True)
    comment_key = graphene.Int(required=True)


# Person Comment relationship
class ImageCommentInput(graphene.InputObjectType):
    image_key = graphene.String(required=True)
    comment_key = graphene.Int(required=True)
