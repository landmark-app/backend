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
    landmarks = graphene.Field(LandMarkSchema, name=graphene.String())

    def resolve_landmarks(self, info, name):
        landmark = LandMark.match(graph, name).first()
        # return [LandMarkSchema(**landmarks.as_dict())]
        return LandMarkSchema(**landmark.as_dict())


class CreateLandMark(graphene.Mutation):

    class Arguments:
        landmark_data = LandMarkInput(required=True)

    landmark = graphene.Field(LandMarkSchema)

    @staticmethod
    def mutate(self, info, landmark_data=None):
        print('Coming inside')
        landmark = LandMark(name=landmark_data.name,
                            description=landmark_data.description,
                            latitude=landmark_data.latitude,
                            longitude=landmark_data.longitude,
                            city=landmark_data.city,
                            state=landmark_data.state,
                            country=landmark_data.country,
                            continent=landmark_data.continent)
        landmark.save(graph)
        return CreateLandMark(landmark=landmark)


class Mutations(graphene.ObjectType):
    create_landmark = CreateLandMark.Field()


schema = graphene.Schema(query=Query,
                         mutation=Mutations,
                         auto_camelcase=False)

result = schema.execute(
    '''
    mutation createLandMark {
        create_landmark(landmark_data: {name: "SOL", description: "SAC",
        latitude: -72.0000, longitude: 140.1234, city: "NYC", state: "NY",
        country: "USA", continent: "NA"}) {
            landmark{
                     name,
                     description
            }
        }
    }
    '''
)

"""
result = schema.execute(
    '''
    mutation createLandMark {
        create_landmark(landmark_data: {name: "SOL", description: "SAC",
        latitude: -142.0010, longitude: 42.0001, city: "NYC", state: "NY",
        country: "USA", continent: "NA"}) {
            landmark{
                     name,
                     description,
                     latitude,
                     city,
                     state,
                     country,
                     continent
            }
        }
    }
    '''
)
"""

"""
result = schema.execute(
    '''
    {
        landmarks (name: "SOL"){
            name,
            description,
            city
        }
    }
    '''
)
"""


items = dict(result.data.items())
print(json.dumps(items, indent=4))
