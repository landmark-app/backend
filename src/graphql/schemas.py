import graphene
import os
from py2neo import Graph

# Internal imports
from .commentgo import Comment
from .imagego import Image
from .landmarkgo import LandMark
from .persongo import Person
from .schemasdef import LandMarkSchema, LandMarkInput, PersonSchema,\
    PersonInput, VisitorInput, ImageSchema, ImageInput, LandMarkImageInput,\
    FriendsInput, FollowingInput, PersonImageInput, CommentSchema,\
    CommentInput, PersonCommentInput, ImageCommentInput

# Environment variables
url = os.environ['NEO4J_URL']
username = os.environ['NEO4J_USERNAME']
password = os.environ['NEO4J_PASSWORD']

"""
url = "bolt://localhost:11007"
username = "neo4j"
password = "landmark"
"""

# Global variables
graph = Graph(url, auth=(username, password))


class CreateLandMark(graphene.Mutation):

    class Arguments:
        landmark_data = LandMarkInput(required=True)

    landmark = graphene.Field(LandMarkSchema)
    ok = graphene.Boolean()

    @staticmethod
    def mutate(self, info, landmark_data=None):
        landmark = LandMark(key=landmark_data.key,
                            name=landmark_data.name,
                            description=landmark_data.description,
                            latitude=landmark_data.latitude,
                            longitude=landmark_data.longitude,
                            city=landmark_data.city,
                            state=landmark_data.state,
                            country=landmark_data.country,
                            continent=landmark_data.continent)
        landmark.save(graph)
        ok = True

        return CreateLandMark(landmark=landmark, ok=ok)


class CreatePerson(graphene.Mutation):

    class Arguments:
        person_data = PersonInput(required=True)

    person = graphene.Field(PersonSchema)
    ok = graphene.Boolean()

    @staticmethod
    def mutate(self, info, person_data=None):
        person = Person(key=person_data.key,
                        name=person_data.name,
                        rank=person_data.rank,
                        score=person_data.score,
                        bio=person_data.bio,
                        email=person_data.email,
                        phone=person_data.phone)
        person.save(graph)
        ok = True

        return CreatePerson(person=person, ok=ok)


class CreateImage(graphene.Mutation):

    class Arguments:
        image_data = ImageInput(required=True)

    image = graphene.Field(ImageSchema)
    ok = graphene.Boolean()

    @staticmethod
    def mutate(self, info, image_data=None):
        image = Image(key=image_data.key,
                      url=image_data.url,
                      description=image_data.description,
                      score=image_data.score,
                      private=image_data.private,
                      timestamp=image_data.timestamp)
        image.save(graph)
        ok = True

        return CreateImage(image=image, ok=ok)


class CreateComment(graphene.Mutation):

    class Arguments:
        comment_data = CommentInput(required=True)

    comment = graphene.Field(CommentSchema)
    ok = graphene.Boolean()

    @staticmethod
    def mutate(self, info, comment_data=None):
        comment = Comment(key=comment_data.key,
                          text=comment_data.text,
                          timestamp=comment_data.timestamp)
        comment.save(graph)
        ok = True

        return CreateComment(comment=comment, ok=ok)


# Relationship between landmark and its visitor
class LinkLandMarkVisitor(graphene.Mutation):

    class Arguments:
        visitor_data = VisitorInput(required=True)

    landmark = graphene.Field(LandMarkSchema)
    visitor = graphene.Field(PersonSchema)
    ok = graphene.Boolean()

    @staticmethod
    def mutate(self, info, visitor_data=None):
        landmark = LandMark.match(graph, visitor_data.landmark_key).first()
        visitor = Person.match(graph, visitor_data.visitor_key).first()

        if not landmark or not visitor:
            ok = False
            return LinkLandMarkVisitor(landmark=None, visitor=None, ok=ok)

        landmark.add_or_update_visitor(visitor)
        landmark.save(graph)

        visitor.add_or_update_visited_landmark(landmark)
        visitor.save(graph)
        ok = True

        return LinkLandMarkVisitor(landmark=landmark, visitor=visitor, ok=ok)


class DelinkLandMarkVisitor(graphene.Mutation):

    class Arguments:
        visitor_data = VisitorInput(required=True)

    landmark = graphene.Field(LandMarkSchema)
    visitor = graphene.Field(PersonSchema)
    ok = graphene.Boolean()

    @staticmethod
    def mutate(self, info, visitor_data=None):
        landmark = LandMark.match(graph, visitor_data.landmark_key).first()
        visitor = Person.match(graph, visitor_data.visitor_key).first()

        if not landmark or not visitor:
            ok = False
            return LinkLandMarkVisitor(landmark=None, visitor=None, ok=ok)

        landmark.remove_visitor(visitor)
        landmark.save(graph)

        visitor.remove_visited_landmark(landmark)
        visitor.save(graph)
        ok = True

        return DelinkLandMarkVisitor(landmark=landmark, visitor=visitor, ok=ok)


# Relationship between landmark and its image
class LinkLandMarkImage(graphene.Mutation):

    class Arguments:
        landmark_image_data = LandMarkImageInput(required=True)

    landmark = graphene.Field(LandMarkSchema)
    image = graphene.Field(ImageSchema)
    ok = graphene.Boolean()

    @staticmethod
    def mutate(self, info, landmark_image_data=None):
        landmark = LandMark.match(graph,
                                  landmark_image_data.landmark_key).first()
        image = Image.match(graph, landmark_image_data.image_key).first()

        if not landmark or not image:
            ok = False
            return LinkLandMarkImage(landmark=None, image=None, ok=ok)

        landmark.add_or_update_image(image)
        landmark.save(graph)

        image.add_or_update_landmark(landmark)
        image.save(graph)
        ok = True

        return LinkLandMarkImage(landmark=landmark, image=image, ok=ok)


class DelinkLandMarkImage(graphene.Mutation):

    class Arguments:
        landmark_image_data = LandMarkImageInput(required=True)

    landmark = graphene.Field(LandMarkSchema)
    image = graphene.Field(ImageSchema)
    ok = graphene.Boolean()

    @staticmethod
    def mutate(self, info, landmark_image_data=None):
        landmark = LandMark.match(graph,
                                  landmark_image_data.landmark_key).first()
        image = Image.match(graph, landmark_image_data.image_key).first()

        if not landmark or not image:
            ok = False
            return LinkLandMarkImage(landmark=None, image=None, ok=ok)

        landmark.remove_image(image)
        landmark.save(graph)

        image.remove_landmark(landmark)
        image.save(graph)
        ok = True

        return DelinkLandMarkImage(landmark=landmark, image=image, ok=ok)


# Establish friendship
class LinkFriends(graphene.Mutation):

    class Arguments:
        friends_data = FriendsInput(required=True)

    friend1 = graphene.Field(PersonSchema)
    friend2 = graphene.Field(PersonSchema)
    ok = graphene.Boolean()

    @staticmethod
    def mutate(self, info, friends_data=None):
        friend1 = Person.match(graph, friends_data.friend1_key).first()
        friend2 = Person.match(graph, friends_data.friend2_key).first()

        if not friend1 or not friend2:
            ok = False
            return LinkFriends(friend1=None, friend2=None, ok=ok)

        friend1.add_or_update_friend(friend2)
        friend1.save(graph)

        friend2.add_or_update_friend(friend1)
        friend2.save(graph)
        ok = True

        return LinkFriends(friend1=friend1, friend2=friend2, ok=ok)


class DelinkFriends(graphene.Mutation):

    class Arguments:
        friends_data = FriendsInput(required=True)

    friend1 = graphene.Field(PersonSchema)
    friend2 = graphene.Field(PersonSchema)
    ok = graphene.Boolean()

    @staticmethod
    def mutate(self, info, friends_data=None):
        friend1 = Person.match(graph, friends_data.friend1_key).first()
        friend2 = Person.match(graph, friends_data.friend2_key).first()

        if not friend1 or not friend2:
            ok = False
            return LinkFriends(friend1=None, friend2=None, ok=ok)

        friend1.remove_friend(friend2)
        friend1.save(graph)

        friend2.remove_friend(friend1)
        friend2.save(graph)
        ok = True

        return DelinkFriends(friend1=friend1, friend2=friend2, ok=ok)


# Establish following
class LinkFollowing(graphene.Mutation):

    class Arguments:
        following_data = FollowingInput(required=True)

    person = graphene.Field(PersonSchema)
    follower = graphene.Field(PersonSchema)
    ok = graphene.Boolean()

    @staticmethod
    def mutate(self, info, following_data=None):
        person = Person.match(graph, following_data.person_key).first()
        follower = Person.match(graph, following_data.follower_key).first()

        if not person or not follower:
            ok = False
            return LinkFollowing(person=None, follower=None, ok=ok)

        person.add_or_update_follower(follower)
        person.save(graph)

        follower.add_or_update_following(person)
        follower.save(graph)
        ok = True

        return LinkFollowing(person=person, follower=follower, ok=ok)


class DelinkFollowing(graphene.Mutation):

    class Arguments:
        following_data = FollowingInput(required=True)

    person = graphene.Field(PersonSchema)
    follower = graphene.Field(PersonSchema)
    ok = graphene.Boolean()

    @staticmethod
    def mutate(self, info, following_data=None):
        person = Person.match(graph, following_data.person_key).first()
        follower = Person.match(graph, following_data.follower_key).first()

        if not person or not follower:
            ok = False
            return LinkFollowing(person=None, follower=None, ok=ok)

        person.remove_follower(follower)
        person.save(graph)

        follower.remove_following(person)
        follower.save(graph)
        ok = True

        return DelinkFollowing(person=person, follower=follower, ok=ok)


# Relationship between person and image posted
class LinkPersonImage(graphene.Mutation):

    class Arguments:
        person_image_data = PersonImageInput(required=True)

    person = graphene.Field(PersonSchema)
    image = graphene.Field(ImageSchema)
    ok = graphene.Boolean()

    @staticmethod
    def mutate(self, info, person_image_data=None):
        person = Person.match(graph, person_image_data.person_key).first()
        image = Image.match(graph, person_image_data.image_key).first()

        if not person or not image:
            ok = False
            return LinkPersonImage(person=None, image=None, ok=ok)

        person.add_or_update_posted_image(image)
        person.save(graph)

        image.add_or_update_poster(person)
        image.save(graph)
        ok = True

        return LinkPersonImage(person=person, image=image, ok=ok)


class DelinkPersonImage(graphene.Mutation):

    class Arguments:
        person_image_data = PersonImageInput(required=True)

    person = graphene.Field(PersonSchema)
    image = graphene.Field(ImageSchema)
    ok = graphene.Boolean()

    @staticmethod
    def mutate(self, info, person_image_data=None):
        person = Person.match(graph, person_image_data.person_key).first()
        image = Image.match(graph, person_image_data.image_key).first()

        if not person or not image:
            ok = False
            return LinkPersonImage(person=None, image=None, ok=ok)

        person.remove_posted_image(image)
        person.save(graph)

        image.remove_poster(person)
        image.save(graph)
        ok = True

        return LinkPersonImage(person=person, image=image, ok=ok)


# Relationship between person and comment posted
class LinkPersonComment(graphene.Mutation):

    class Arguments:
        person_comment_data = PersonCommentInput(required=True)

    person = graphene.Field(PersonSchema)
    comment = graphene.Field(CommentSchema)
    ok = graphene.Boolean()

    @staticmethod
    def mutate(self, info, person_comment_data=None):
        person = Person.match(graph, person_comment_data.person_key).first()
        comment = Comment.match(graph, person_comment_data.comment_key).first()

        if not person or not comment:
            ok = False
            return LinkPersonComment(person=None, comment=None, ok=ok)

        person.add_or_update_posted_comment(comment)
        person.save(graph)

        comment.add_or_update_poster(person)
        comment.save(graph)
        ok = True

        return LinkPersonComment(person=person, comment=comment, ok=ok)


class DelinkPersonComment(graphene.Mutation):

    class Arguments:
        person_comment_data = PersonCommentInput(required=True)

    person = graphene.Field(PersonSchema)
    comment = graphene.Field(CommentSchema)
    ok = graphene.Boolean()

    @staticmethod
    def mutate(self, info, person_comment_data=None):
        person = Person.match(graph, person_comment_data.person_key).first()
        comment = Comment.match(graph, person_comment_data.comment_key).first()

        if not person or not comment:
            ok = False
            return LinkPersonComment(person=None, comment=None, ok=ok)

        person.remove_posted_comment(comment)
        person.save(graph)

        comment.remove_poster(person)
        comment.save(graph)
        ok = True

        return DelinkPersonComment(person=person, comment=comment, ok=ok)


# Relationship between image and comment
class LinkImageComment(graphene.Mutation):

    class Arguments:
        image_comment_data = ImageCommentInput(required=True)

    image = graphene.Field(PersonSchema)
    comment = graphene.Field(CommentSchema)
    ok = graphene.Boolean()

    @staticmethod
    def mutate(self, info, image_comment_data=None):
        image = Image.match(graph, image_comment_data.image_key).first()
        comment = Comment.match(graph, image_comment_data.comment_key).first()

        if not image or not comment:
            ok = False
            return LinkImageComment(image=None, comment=None, ok=ok)

        image.add_or_update_comment(comment)
        image.save(graph)

        comment.add_or_update_image(image)
        comment.save(graph)
        ok = True

        return LinkImageComment(image=image, comment=comment, ok=ok)


class DelinkImageComment(graphene.Mutation):

    class Arguments:
        image_comment_data = ImageCommentInput(required=True)

    image = graphene.Field(PersonSchema)
    comment = graphene.Field(CommentSchema)
    ok = graphene.Boolean()

    @staticmethod
    def mutate(self, info, image_comment_data=None):
        image = Image.match(graph, image_comment_data.image_key).first()
        comment = Comment.match(graph, image_comment_data.comment_key).first()

        if not image or not comment:
            ok = False
            return DelinkImageComment(image=None, comment=None, ok=ok)

        image.remove_comment(comment)
        image.save(graph)

        comment.remove_image(image)
        comment.save(graph)
        ok = True

        return DelinkImageComment(image=image, comment=comment, ok=ok)


class DeleteLandMark(graphene.Mutation):

    class Arguments:
        landmark_data = LandMarkInput(required=True)

    landmark = graphene.Field(LandMarkSchema)
    ok = graphene.Boolean()

    @staticmethod
    def mutate(self, info, landmark_data=None):
        landmark = LandMark.match(graph, landmark_data.key).first()
        landmark.delete(graph)
        ok = True

        return DeleteLandMark(landmark=landmark, ok=ok)


class DeletePerson(graphene.Mutation):

    class Arguments:
        person_data = PersonInput(required=True)

    person = graphene.Field(PersonSchema)
    ok = graphene.Boolean()

    @staticmethod
    def mutate(self, info, person_data=None):
        person = Person.match(graph, person_data.key).first()
        person.delete(graph)
        ok = True

        return DeletePerson(person=person, ok=ok)


class DeleteImage(graphene.Mutation):

    class Arguments:
        image_data = ImageInput(required=True)

    image = graphene.Field(ImageSchema)
    ok = graphene.Boolean()

    @staticmethod
    def mutate(self, info, image_data=None):
        image = Image.match(graph, image_data.key).first()
        image.delete(graph)
        ok = True

        return DeleteImage(image=image, ok=ok)


class DeleteComment(graphene.Mutation):

    class Arguments:
        comment_data = CommentInput(required=True)

    comment = graphene.Field(CommentSchema)
    ok = graphene.Boolean()

    @staticmethod
    def mutate(self, info, comment_data=None):
        comment = Comment.match(graph, comment_data.key).first()
        comment.delete(graph)
        ok = True

        return DeleteComment(comment=comment, ok=ok)


class Query(graphene.ObjectType):
    landmark = graphene.Field(LandMarkSchema, key=graphene.String())
    person = graphene.Field(PersonSchema, key=graphene.String())
    image = graphene.Field(ImageSchema, key=graphene.String())
    comment = graphene.Field(CommentSchema, key=graphene.String())

    # Query to fetch all visitors to a particular landmark
    landmark_visitors = graphene.List(PersonSchema, key=graphene.String())

    # Query to fetch all landmark visits of a person
    person_visits = graphene.List(LandMarkSchema, key=graphene.String())

    # Query to fetch all images of a particular landmark
    landmark_images = graphene.List(ImageSchema, key=graphene.String())

    # Query to fetch landmark in a particular image
    image_landmark = graphene.List(LandMarkSchema, key=graphene.String())

    # Query to fetch all friends of a person
    friends = graphene.List(PersonSchema, key=graphene.String())

    # Query to fetch all followers of a person
    followers = graphene.List(PersonSchema, key=graphene.String())

    # Query to fetch all followers of a person
    followings = graphene.List(PersonSchema, key=graphene.String())

    # Query to fetch all images posted by a person
    person_posted_images = graphene.List(ImageSchema, key=graphene.String())

    # Query to fetch poster of a particular image
    image_poster = graphene.List(PersonSchema, key=graphene.String())

    # Query to fetch all comments posted by a person
    person_posted_comments = graphene.List(CommentSchema,
                                           key=graphene.String())

    # Query to fetch poster of a particular comment
    comment_poster = graphene.List(PersonSchema, key=graphene.String())

    # Query to fetch comments posted on a particular image
    image_comments = graphene.List(CommentSchema, key=graphene.String())

    # Query to fetch image associated with a particular comment
    comment_image = graphene.List(ImageSchema, key=graphene.String())

    def resolve_landmark(self, info, key):
        landmark = LandMark.match(graph, key).first()
        return LandMarkSchema(**landmark.as_dict())

    def resolve_person(self, info, key):
        person = Person.match(graph, key).first()
        return PersonSchema(**person.as_dict())

    def resolve_image(self, info, key):
        image = Image.match(graph, key).first()
        return ImageSchema(**image.as_dict())

    def resolve_comment(self, info, key):
        comment = Comment.match(graph, key).first()
        return CommentSchema(**comment.as_dict())

    def resolve_landmark_visitors(self, info, key):
        landmark = LandMark.match(graph, key).first()
        return [PersonSchema(**person.as_dict())
                for person in landmark.visitors]

    def resolve_person_visits(self, info, key):
        person = Person.match(graph, key).first()
        return [LandMarkSchema(**landmark.as_dict())
                for landmark in person.visited]

    def resolve_landmark_images(self, info, key):
        landmark = LandMark.match(graph, key).first()
        return [ImageSchema(**image.as_dict())
                for image in landmark.images]

    def resolve_image_landmark(self, info, key):
        image = Image.match(graph, key).first()
        return [LandMarkSchema(**landmark.as_dict())
                for landmark in image.landmark]

    def resolve_friends(self, info, key):
        person = Person.match(graph, key).first()
        return [PersonSchema(**friend.as_dict())
                for friend in person.friends]

    def resolve_followers(self, info, key):
        person = Person.match(graph, key).first()
        return [PersonSchema(**follower.as_dict())
                for follower in person.followers]

    def resolve_followings(self, info, key):
        person = Person.match(graph, key).first()
        return [PersonSchema(**following.as_dict())
                for following in person.followings]

    def resolve_person_posted_images(self, info, key):
        person = Person.match(graph, key).first()
        return [ImageSchema(**image.as_dict())
                for image in person.posted_images]

    def resolve_image_poster(self, info, key):
        image = Image.match(graph, key).first()
        return [PersonSchema(**person.as_dict())
                for person in image.poster]

    def resolve_person_posted_comments(self, info, key):
        person = Person.match(graph, key).first()
        return [CommentSchema(**comment.as_dict())
                for comment in person.posted_comments]

    def resolve_comment_poster(self, info, key):
        comment = Comment.match(graph, key).first()
        return [PersonSchema(**person.as_dict())
                for person in comment.poster]

    def resolve_image_comments(self, info, key):
        image = Image.match(graph, key).first()
        return [CommentSchema(**comment.as_dict())
                for comment in image.comments]

    def resolve_comment_image(self, info, key):
        comment = Comment.match(graph, key).first()
        return [ImageSchema(**image.as_dict())
                for image in comment.image]


class Mutations(graphene.ObjectType):
    create_landmark = CreateLandMark.Field()
    delete_landmark = DeleteLandMark.Field()

    create_person = CreatePerson.Field()
    delete_person = DeletePerson.Field()

    create_image = CreateImage.Field()
    delete_image = DeleteImage.Field()

    create_comment = CreateComment.Field()
    delete_comment = DeleteComment.Field()

    link_landmark_visitor = LinkLandMarkVisitor.Field()
    delink_landmark_visitor = DelinkLandMarkVisitor.Field()

    link_landmark_image = LinkLandMarkImage.Field()
    delink_landmark_image = DelinkLandMarkImage.Field()

    link_friends = LinkFriends.Field()
    delink_friends = DelinkFriends.Field()

    link_following = LinkFollowing.Field()
    delink_following = DelinkFollowing.Field()

    link_person_image = LinkPersonImage.Field()
    delink_person_image = DelinkPersonImage.Field()

    link_person_comment = LinkPersonComment.Field()
    delink_person_comment = DelinkPersonComment.Field()

    link_image_comment = LinkImageComment.Field()
    delink_image_comment = DelinkImageComment.Field()


schema = graphene.Schema(query=Query,
                         mutation=Mutations,
                         auto_camelcase=False)
