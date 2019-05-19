import graphene
import json
from py2neo import Graph

# Internal imports
from landmark import LandMark

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


class Query(graphene.ObjectType):
    # landmarks = graphene.List(LandMarkSchema, name=graphene.String())
    landmark = graphene.Field(LandMarkSchema, name=graphene.String())

    def resolve_landmark(self, info, name):
        landmark = LandMark.match(graph, name).first()
        # return [LandMarkSchema(**landmarks.as_dict())]
        return LandMarkSchema(**landmark.as_dict())


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


class Mutations(graphene.ObjectType):
    create_landmark = CreateLandMark.Field()
    delete_landmark = DeleteLandMark.Field()


schema = graphene.Schema(query=Query,
                         mutation=Mutations,
                         auto_camelcase=False)

result_create = schema.execute(
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

result_query = schema.execute(
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


result_delete = schema.execute(
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


items = dict(result_create.data.items())
print(json.dumps(items, indent=4))

items = dict(result_query.data.items())
print(json.dumps(items, indent=4))

items = dict(result_delete.data.items())
print(json.dumps(items, indent=4))
