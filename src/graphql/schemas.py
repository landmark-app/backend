import graphene
import json
from py2neo import Graph

# Internal imports
from imagego import Image
from landmarkgo import LandMark
from persongo import Person
from schemasdef import LandMarkSchema, LandMarkInput, PersonSchema,\
    PersonInput, VisitorInput, ImageSchema, ImageInput, LandMarkImageInput

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
        landmark = LandMark(name=landmark_data.name,
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


class LinkLandMarkVisitor(graphene.Mutation):

    class Arguments:
        visitor_data = VisitorInput(required=True)

    landmark = graphene.Field(LandMarkSchema)
    visitor = graphene.Field(PersonSchema)
    ok = graphene.Boolean()

    @staticmethod
    def mutate(self, info, visitor_data=None):
        landmark = LandMark.match(graph, visitor_data.landmark_name).first()
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
        landmark = LandMark.match(graph, visitor_data.landmark_name).first()
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


class LinkLandMarkImage(graphene.Mutation):

    class Arguments:
        landmark_image_data = LandMarkImageInput(required=True)

    landmark = graphene.Field(LandMarkSchema)
    image = graphene.Field(ImageSchema)
    ok = graphene.Boolean()

    @staticmethod
    def mutate(self, info, landmark_image_data=None):
        landmark = LandMark.match(graph,
                                  landmark_image_data.landmark_name).first()
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
                                  landmark_image_data.landmark_name).first()
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


class DeleteLandMark(graphene.Mutation):

    class Arguments:
        landmark_data = LandMarkInput(required=True)

    landmark = graphene.Field(LandMarkSchema)
    ok = graphene.Boolean()

    @staticmethod
    def mutate(self, info, landmark_data=None):
        landmark = LandMark.match(graph, landmark_data.name).first()
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
    # landmarks = graphene.List(LandMarkSchema, name=graphene.String())
    landmark = graphene.Field(LandMarkSchema, name=graphene.String())
    person = graphene.Field(PersonSchema, key=graphene.String())
    image = graphene.Field(ImageSchema, key=graphene.String())
    landmark_visitors = graphene.List(PersonSchema, name=graphene.String())
    person_visits = graphene.List(LandMarkSchema, key=graphene.String())
    landmark_images = graphene.List(ImageSchema, name=graphene.String())

    def resolve_landmark(self, info, name):
        landmark = LandMark.match(graph, name).first()
        # return [LandMarkSchema(**landmarks.as_dict())]
        return LandMarkSchema(**landmark.as_dict())

    def resolve_person(self, info, key):
        person = Person.match(graph, key).first()
        return PersonSchema(**person.as_dict())

    def resolve_image(self, info, key):
        image = Image.match(graph, key).first()
        return ImageSchema(**image.as_dict())

    def resolve_landmark_visitors(self, info, name):
        landmark = LandMark.match(graph, name).first()
        return [PersonSchema(**person.as_dict())
                for person in landmark.visitors]

    def resolve_person_visits(self, info, key):
        person = Person.match(graph, key).first()
        return [LandMarkSchema(**landmark.as_dict())
                for landmark in person.visited]

    def resolve_landmark_images(self, info, name):
        landmark = LandMark.match(graph, name).first()
        return [ImageSchema(**image.as_dict())
                for image in landmark.images]

    def resolve_image_landmarks(self, info, key):
        image = Image.match(graph, key).first()
        return [LandMarkSchema(**landmark.as_dict())
                for landmark in image.landmarks]


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


schema = graphene.Schema(query=Query,
                         mutation=Mutations,
                         auto_camelcase=False)

"""
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
                                  landmark_name: "GSB",
                                  image_key: "bbb111"})
            {
             landmark{
                      name,
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
                                  landmark_name: "SOL",
                                  image_key: "aaa111"})
            {
             landmark{
                      name,
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
                                  landmark_name: "SOL",
                                  image_key: "aaa222"})
            {
             landmark{
                      name,
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
                                  landmark_name: "SOL",
                                  image_key: "aaa222"})
            {
             landmark{
                      name,
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
"""

query_landmark_images = schema.execute(
    '''
    {
        landmark_images (name: "SOL"){
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
