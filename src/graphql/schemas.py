import graphene
import json
from py2neo import Graph

# Internal imports
from imagego import Image
from landmarkgo import LandMark
from persongo import Person
from schemasdef import LandMarkSchema, LandMarkInput, PersonSchema,\
    PersonInput, VisitorInput, ImageSchema, ImageInput, LandMarkImageInput,\
    FriendsInput, FollowingInput, PersonImageInput

# Environment variables
"""
url = os.environ['NEO4J_URL']
username = os.environ['NEO4J_USERNAME']
password = os.environ['NEO4J_PASSWORD']
"""
url = "bolt://localhost:11007"
username = "neo4j"
password = "landmark"

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


class Query(graphene.ObjectType):
    landmark = graphene.Field(LandMarkSchema, key=graphene.String())
    person = graphene.Field(PersonSchema, key=graphene.String())
    image = graphene.Field(ImageSchema, key=graphene.String())

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

    def resolve_landmark(self, info, key):
        landmark = LandMark.match(graph, key).first()
        return LandMarkSchema(**landmark.as_dict())

    def resolve_person(self, info, key):
        person = Person.match(graph, key).first()
        return PersonSchema(**person.as_dict())

    def resolve_image(self, info, key):
        image = Image.match(graph, key).first()
        return ImageSchema(**image.as_dict())

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


class Mutations(graphene.ObjectType):
    create_landmark = CreateLandMark.Field()
    delete_landmark = DeleteLandMark.Field()

    create_person = CreatePerson.Field()
    delete_person = DeletePerson.Field()

    create_image = CreateImage.Field()
    delete_image = DeleteImage.Field()

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


schema = graphene.Schema(query=Query,
                         mutation=Mutations,
                         auto_camelcase=False)

"""
create_landmark = schema.execute(
    '''
    mutation createLandMark {
        create_landmark(landmark_data: {key: "111222", name: "SOL",
        description: "NY", latitude: -142.0010, longitude: 42.0001,
        city: "NYC", state: "NY", country: "USA", continent: "NA"}) {
            landmark{
                     key,
                     name,
                     description,
                     latitude,
                     longitude,
                     city,
                     state,
                     country,
                     continent
            },
            ok
        }
    }
    '''
)
items = dict(create_landmark.data.items())
print(json.dumps(items, indent=4))

create_landmark = schema.execute(
    '''
    mutation createLandMark {
        create_landmark(landmark_data: {key: "222333", name: "GSB",
        description: "SFO", latitude: -100.0010, longitude: 60.0001,
        city: "SFO", state: "CA", country: "USA", continent: "NA"}) {
            landmark{
                     key,
                     name,
                     description,
                     latitude,
                     longitude,
                     city,
                     state,
                     country,
                     continent
            },
            ok
        }
    }
    '''
)
items = dict(create_landmark.data.items())
print(json.dumps(items, indent=4))

create_person = schema.execute(
    '''
    mutation createPerson {
        create_person(person_data: {key: "111", name: "Shreyas", rank: 21,
        score: 121.90, bio: "test bio", email: "shreyas@gmail.com", phone:
        "+12222222"}){
            person{
                   key,
                   name,
                   rank,
                   score,
                   bio,
                   email,
                   phone
            },
            ok
        }
    }
    '''
)
items = dict(create_person.data.items())
print(json.dumps(items, indent=4))

create_person = schema.execute(
    '''
    mutation createPerson {
        create_person(person_data: {key: "222", name: "Rudy", rank: 11,
        score: 131.90, bio: "test bio", email: "rudy@gmail.com", phone:
        "+13333333"}){
            person{
                   key,
                   name,
                   rank,
                   score,
                   bio,
                   email,
                   phone
            },
            ok
        }
    }
    '''
)
items = dict(create_person.data.items())
print(json.dumps(items, indent=4))

create_person = schema.execute(
    '''
    mutation createPerson {
        create_person(person_data: {key: "333", name: "Michael", rank: 12,
        score: 131.90, bio: "test bio", email: "michael@gmail.com", phone:
        "+14444444"}){
            person{
                   key,
                   name,
                   rank,
                   score,
                   bio,
                   email,
                   phone
            },
            ok
        }
    }
    '''
)
items = dict(create_person.data.items())
print(json.dumps(items, indent=4))

create_person = schema.execute(
    '''
    mutation createPerson {
        create_person(person_data: {key: "444", name: "Erica", rank: 3,
        score: 131.90, bio: "test bio", email: "erica@gmail.com", phone:
        "+16666666"}){
            person{
                   key,
                   name,
                   rank,
                   score,
                   bio,
                   email,
                   phone
            },
            ok
        }
    }
    '''
)
items = dict(create_person.data.items())
print(json.dumps(items, indent=4))

link_landmark_visitor = schema.execute(
    '''
    mutation linkLandMarkVisitor {
        link_landmark_visitor(visitor_data: {landmark_key: "111222",
        visitor_key: "111"}){
            landmark{
                     key,
            },
            visitor{
                   key,
            },
            ok
        }
    }
    '''
)
items = dict(link_landmark_visitor.data.items())
print(json.dumps(items, indent=4))

link_landmark_visitor = schema.execute(
    '''
    mutation linkLandMarkVisitor {
        link_landmark_visitor(visitor_data: {landmark_key: "111222",
        visitor_key: "222"}){
            landmark{
                     key,
            },
            visitor{
                   key,
            },
            ok
        }
    }
    '''
)
items = dict(link_landmark_visitor.data.items())
print(json.dumps(items, indent=4))

link_landmark_visitor = schema.execute(
    '''
    mutation linkLandMarkVisitor {
        link_landmark_visitor(visitor_data: {landmark_key: "222333",
        visitor_key: "111"}){
            landmark{
                     key,
            },
            visitor{
                   key,
            },
            ok
        }
    }
    '''
)
items = dict(link_landmark_visitor.data.items())
print(json.dumps(items, indent=4))

delink_landmark_visitor = schema.execute(
    '''
    mutation delinkLandMarkVisitor {
        delink_landmark_visitor(visitor_data: {landmark_key: "111222",
        visitor_key: "111"}){
            landmark{
                     key,
            },
            visitor{
                   key,
            },
            ok
        }
    }
    '''
)
items = dict(delink_landmark_visitor.data.items())
print(json.dumps(items, indent=4))

query_landmark = schema.execute(
    '''
    {
        landmark (key: "111222"){
            key,
            name,
            description,
            latitude,
            longitude,
            city,
            state,
            country,
            continent
        }
    }
    '''
)
items = dict(query_landmark.data.items())
print(json.dumps(items, indent=4))

query_person = schema.execute(
    '''
    {
        person (key: "111"){
            key,
            name,
            rank,
            score,
            bio,
            email,
            phone
        }
    }
    '''
)
items = dict(query_person.data.items())
print(json.dumps(items, indent=4))

query_landmark_visitors = schema.execute(
    '''
    {
        landmark_visitors (key: "111222"){
            key,
            name,
            rank,
            score,
            bio,
            email,
            phone
        }
    }
    '''
)
items = dict(query_landmark_visitors.data.items())
print(json.dumps(items, indent=4))

query_person_visits = schema.execute(
    '''
    {
        person_visits (key: "111"){
            key,
            name,
            description,
            latitude,
            longitude,
            city,
            state,
            country,
            continent
        }
    }
    '''
)
items = dict(query_person_visits.data.items())
print(json.dumps(items, indent=4))

delete_landmark = schema.execute(
    '''
    mutation deleteLandMark {
        delete_landmark(landmark_data: {key: "111222"}) {
            landmark{
                     key,
                     name,
                     description,
                     latitude,
                     longitude,
                     city,
                     state,
                     country,
                     continent
            },
            ok
        }

    }
    '''
)
items = dict(delete_landmark.data.items())
print(json.dumps(items, indent=4))

delete_person = schema.execute(
    '''
    mutation deletePerson {
        delete_person(person_data: {key: "111"}) {
            person{
                   key,
                   name,
                   rank,
                   score,
                   bio,
                   email,
                   phone
            },
            ok
        }

    }
    '''
)
items = dict(delete_person.data.items())
print(json.dumps(items, indent=4))

create_image = schema.execute(
    '''
    mutation createImage {
        create_image(image_data: {key: "aaa111", url: "https://image",
        description: "SOL1", score: 80.4, private: false, timestamp:
        "2019-05-20T02:50:31+05:30"}){
            image{
                  key,
                  url,
                  description,
                  score,
                  private,
                  timestamp
            },
            ok
        }
    }
    '''
)
items = dict(create_image.data.items())
print(json.dumps(items, indent=4))

create_image = schema.execute(
    '''
    mutation createImage {
        create_image(image_data: {key: "aaa222", url: "https://image",
        description: "SOL2", score: 80.4, private: false, timestamp:
        "2019-05-20T06:50:31+05:30"}){
            image{
                  key,
                  url,
                  description,
                  score,
                  private,
                  timestamp
            },
            ok
        }
    }
    '''
)
items = dict(create_image.data.items())
print(json.dumps(items, indent=4))

create_image = schema.execute(
    '''
    mutation createImage {
        create_image(image_data: {key: "bbb111", url: "https://image",
        description: "GSB1", score: 80.4, private: false, timestamp:
        "2019-05-20T02:50:31+05:30"}){
            image{
                  key,
                  url,
                  description,
                  score,
                  private,
                  timestamp
            },
            ok
        }
    }
    '''
)
items = dict(create_image.data.items())
print(json.dumps(items, indent=4))

query_image = schema.execute(
    '''
    {
        image (key: "aaa111"){
            key,
            url,
            description,
            score,
            private,
            timestamp
        }
    }
    '''
)
items = dict(query_image.data.items())
print(json.dumps(items, indent=4))

delete_image = schema.execute(
    '''
    mutation deleteImage {
        delete_image(image_data: {key: "aaa111"}) {
            image{
                  key,
                  url,
                  description,
                  score,
                  private,
                  timestamp
            },
            ok
        }

    }
    '''
)
items = dict(delete_image.data.items())
print(json.dumps(items, indent=4))

link_landmark_image = schema.execute(
    '''
    mutation linkLandMarkImage {
        link_landmark_image(
            landmark_image_data: {
                                  landmark_key: "222333",
                                  image_key: "bbb111"})
            {
             landmark{
                      key,
             },
             image{
                   key,
             },
             ok
        }
    }
    '''
)
items = dict(link_landmark_image.data.items())
print(json.dumps(items, indent=4))

link_landmark_image = schema.execute(
    '''
    mutation linkLandMarkImage {
        link_landmark_image(
            landmark_image_data: {
                                  landmark_key: "111222",
                                  image_key: "aaa111"})
            {
             landmark{
                      key,
             },
             image{
                   key,
             },
             ok
        }
    }
    '''
)
items = dict(link_landmark_image.data.items())
print(json.dumps(items, indent=4))

link_landmark_image = schema.execute(
    '''
    mutation linkLandMarkImage {
        link_landmark_image(
            landmark_image_data: {
                                  landmark_key: "111222",
                                  image_key: "aaa222"})
            {
             landmark{
                      key,
             },
             image{
                   key,
             },
             ok
        }
    }
    '''
)
items = dict(link_landmark_image.data.items())
print(json.dumps(items, indent=4))

delink_landmark_image = schema.execute(
    '''
    mutation delinkLandMarkImage {
        delink_landmark_image(
            landmark_image_data: {
                                  landmark_key: "111222",
                                  image_key: "aaa222"})
            {
             landmark{
                      key,
             },
             image{
                   key,
             },
             ok
        }
    }
    '''
)
items = dict(delink_landmark_image.data.items())
print(json.dumps(items, indent=4))

query_landmark_images = schema.execute(
    '''
    {
        landmark_images (key: "111222"){
            key,
            url,
            description,
            score,
            private,
            timestamp
        }
    }
    '''
)
items = dict(query_landmark_images.data.items())
print(json.dumps(items, indent=4))

link_friends = schema.execute(
    '''
    mutation linkFriends {
        link_friends(
            friends_data: {
                           friend1_key: "111",
                           friend2_key: "222"})
            {
             friend1{
                     key,
             },
             friend2{
                     key,
             },
             ok
        }
    }
    '''
)
items = dict(link_friends.data.items())
print(json.dumps(items, indent=4))

delink_friends = schema.execute(
    '''
    mutation delinkFriends {
        delink_friends(
            friends_data: {
                           friend1_key: "111",
                           friend2_key: "222"})
            {
             friend1{
                     key,
             },
             friend2{
                     key,
             },
             ok
        }
    }
    '''
)
items = dict(delink_friends.data.items())
print(json.dumps(items, indent=4))

query_image_landmark = schema.execute(
    '''
    {
        image_landmark (key: "aaa111"){
            key,
        }
    }
    '''
)
items = dict(query_image_landmark.data.items())
print(json.dumps(items, indent=4))

query_friends = schema.execute(
    '''
    {
        friends (key: "111"){
            key,
        }
    }
    '''
)
items = dict(query_friends.data.items())
print(json.dumps(items, indent=4))

link_following = schema.execute(
    '''
    mutation linkFollowing {
        link_following(
            following_data: {
                             person_key: "444",
                             follower_key: "111"})
            {
             person{
                    key,
             },
             follower{
                      key,
             },
             ok
        }
    }
    '''
)
items = dict(link_following.data.items())
print(json.dumps(items, indent=4))

delink_following = schema.execute(
    '''
    mutation delinkFollowing {
        delink_following(
            following_data: {
                             person_key: "444",
                             follower_key: "111"})
            {
             person{
                    key,
             },
             follower{
                      key,
             },
             ok
        }
    }
    '''
)
items = dict(delink_following.data.items())
print(json.dumps(items, indent=4))

query_followers = schema.execute(
    '''
    {
        followers (key: "444"){
            key,
            name
        }
    }
    '''
)
items = dict(query_followers.data.items())
print(json.dumps(items, indent=4))

query_followings = schema.execute(
    '''
    {
        followings (key: "111"){
            key,
            name
        }
    }
    '''
)
items = dict(query_followings.data.items())
print(json.dumps(items, indent=4))

link_person_image = schema.execute(
    '''
    mutation linkPersonImage {
        link_person_image(
            person_image_data: {
                                person_key: "111",
                                image_key: "bbb111"})
            {
             person{
                    key,
             },
             image{
                   key,
             },
             ok
        }
    }
    '''
)
items = dict(link_person_image.data.items())
print(json.dumps(items, indent=4))

delink_person_image = schema.execute(
    '''
    mutation delinkPersonImage {
        delink_person_image(
            person_image_data: {
                                person_key: "111",
                                image_key: "bbb111"})
            {
             person{
                    key,
             },
             image{
                   key,
             },
             ok
        }
    }
    '''
)
items = dict(delink_person_image.data.items())
print(json.dumps(items, indent=4))

query_person_posted_images = schema.execute(
    '''
    {
        person_posted_images (key: "111"){
            key,
            url,
            description,
            score,
            private,
            timestamp
        }
    }
    '''
)
items = dict(query_person_posted_images.data.items())
print(json.dumps(items, indent=4))

query_image_poster = schema.execute(
    '''
    {
        image_poster (key: "bbb111"){
            key,
            name,
        }
    }
    '''
)
items = dict(query_image_poster.data.items())
print(json.dumps(items, indent=4))
"""
