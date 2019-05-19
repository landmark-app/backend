import graphene
import json
from py2neo import Graph

# Internal imports
from landmarkgo import LandMark
from persongo import Person
from schemasdef import LandMarkSchema, LandMarkInput, PersonSchema,\
    PersonInput, VisitorInput

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


class Query(graphene.ObjectType):
    # landmarks = graphene.List(LandMarkSchema, name=graphene.String())
    landmark = graphene.Field(LandMarkSchema, name=graphene.String())
    person = graphene.Field(PersonSchema, key=graphene.String())
    landmark_visitors = graphene.List(PersonSchema, name=graphene.String())
    person_visits = graphene.List(LandMarkSchema, key=graphene.String())

    def resolve_landmark(self, info, name):
        landmark = LandMark.match(graph, name).first()
        # return [LandMarkSchema(**landmarks.as_dict())]
        return LandMarkSchema(**landmark.as_dict())

    def resolve_person(self, info, key):
        person = Person.match(graph, key).first()
        return PersonSchema(**person.as_dict())

    def resolve_landmark_visitors(self, info, name):
        landmark = LandMark.match(graph, name).first()
        return [PersonSchema(**person.as_dict())
                for person in landmark.visitors]

    def resolve_person_visits(self, info, key):
        person = Person.match(graph, key).first()
        return [LandMarkSchema(**landmark.as_dict())
                for landmark in person.visited]


class Mutations(graphene.ObjectType):
    create_landmark = CreateLandMark.Field()
    delete_landmark = DeleteLandMark.Field()
    create_person = CreatePerson.Field()
    delete_person = DeletePerson.Field()
    link_landmark_visitor = LinkLandMarkVisitor.Field()
    delink_landmark_visitor = DelinkLandMarkVisitor.Field()


schema = graphene.Schema(query=Query,
                         mutation=Mutations,
                         auto_camelcase=False)

create_landmark = schema.execute(
    '''
    mutation createLandMark {
        create_landmark(landmark_data: {name: "SOL", description: "NY",
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
items = dict(create_landmark.data.items())
print(json.dumps(items, indent=4))

create_landmark = schema.execute(
    '''
    mutation createLandMark {
        create_landmark(landmark_data: {name: "GSB", description: "SFO",
        latitude: -100.0010, longitude: 60.0001, city: "SFO", state: "CA",
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

link_landmark_visitor = schema.execute(
    '''
    mutation linkLandMarkVisitor {
        link_landmark_visitor(visitor_data: {landmark_name: "SOL", visitor_key:
        "111"}){
            landmark{
                     name,
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
        link_landmark_visitor(visitor_data: {landmark_name: "GSB", visitor_key:
        "222"}){
            landmark{
                     name,
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
        link_landmark_visitor(visitor_data: {landmark_name: "GSB", visitor_key:
        "111"}){
            landmark{
                     name,
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

"""
delink_landmark_visitor = schema.execute(
    '''
    mutation delinkLandMarkVisitor {
        delink_landmark_visitor(visitor_data: {landmark_name: "SOL",
        visitor_key: "111"}){
            landmark{
                     name,
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
"""

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
        landmark_visitors (name: "SOL"){
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
"""
