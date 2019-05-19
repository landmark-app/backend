import graphene
import json
from py2neo import Graph

# Internal imports
from landmark import LandMark
from person import Person

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


class LandMarkSchema(graphene.ObjectType):
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
    name = graphene.String(required=True)
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


class Query(graphene.ObjectType):
    # landmarks = graphene.List(LandMarkSchema, name=graphene.String())
    landmark = graphene.Field(LandMarkSchema, name=graphene.String())
    person = graphene.Field(PersonSchema, key=graphene.String())

    def resolve_landmark(self, info, name):
        landmark = LandMark.match(graph, name).first()
        # return [LandMarkSchema(**landmarks.as_dict())]
        return LandMarkSchema(**landmark.as_dict())

    def resolve_person(self, info, key):
        person = Person.match(graph, key).first()
        return PersonSchema(**person.as_dict())


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


class Mutations(graphene.ObjectType):
    create_landmark = CreateLandMark.Field()
    delete_landmark = DeleteLandMark.Field()
    create_person = CreatePerson.Field()
    delete_person = DeletePerson.Field()


schema = graphene.Schema(query=Query,
                         mutation=Mutations,
                         auto_camelcase=False)

create_landmark = schema.execute(
    '''
    mutation createLandMark {
        create_landmark(landmark_data: {name: "SOL", description: "SAC",
        latitude: -142.0010, longitude: 42.0001, city: "NYC", state: "NY",
        country: "USA", continent: "NA"}) {
            landmark{
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

query_landmark = schema.execute(
    '''
    {
        landmark (name: "SOL"){
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


"""
delete_landmark = schema.execute(
    '''
    mutation deleteLandMark {
        delete_landmark(landmark_data: {name: "SOL"}) {
            landmark{
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
"""

items = dict(create_landmark.data.items())
print(json.dumps(items, indent=4))

items = dict(create_person.data.items())
print(json.dumps(items, indent=4))

items = dict(query_landmark.data.items())
print(json.dumps(items, indent=4))

items = dict(query_person.data.items())
print(json.dumps(items, indent=4))

"""
items = dict(delete_landmark.data.items())
print(json.dumps(items, indent=4))

items = dict(delete_person.data.items())
print(json.dumps(items, indent=4))
"""
