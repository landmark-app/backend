import graphene
from graphene.types import datetime
import json
import os
from py2neo import Graph

# Internal imports
from comment import Comment
from image import Image
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
    _id = graphene.ID()
    name = graphene.String()
    description = graphene.String()

    # Location information
    latitude = graphene.Float()
    longitude = graphene.Float()
    city = graphene.String()
    state = graphene.String()
    country = graphene.String()
    continent = graphene.String()

    # Set of people who visited the LandMark
    # visitors = graphene.List(lambda: PersonSchema)

    # Set of images of LandMark
    # images = graphene.List(lambda: ImageSchema)


class PersonSchema(graphene.ObjectType):
    key = graphene.ID()
    name = graphene.String()
    rank = graphene.Int()
    score = graphene.Float()
    bio = graphene.String()
    email = graphene.String()
    phone = graphene.String()

    # Set of friends. This is bi-directional relationship
    friends = graphene.List(lambda: PersonSchema)

    # Set of Person whom the Person follows
    follows = graphene.List(lambda: PersonSchema)

    # Set of Person who follow the Person
    followed_by = graphene.List(lambda: PersonSchema)

    # Set of Landmarks visted by Person
    visited = graphene.List(lambda: LandMarkSchema)

    # Set of Images posted by Person
    images_posted = graphene.List(lambda: ImageSchema)

    # Set of Comments posted by Person
    comments_posted = graphene.List(lambda: CommentSchema)


class ImageSchema(graphene.ObjectType):
    key = graphene.ID()
    url = graphene.String()
    description = graphene.String()
    score = graphene.Float()
    private = graphene.Boolean()
    timestamp = datetime.DateTime()

    # Set of Images posted by a Person
    posted_by = graphene.List(lambda: PersonSchema)

    # Set of Comments posted on the Image
    comments = graphene.List(lambda: CommentSchema)

    # Set of Images of particular LandMark
    images_of = graphene.List(lambda: ImageSchema)


class CommentSchema(graphene.ObjectType):
    _id = graphene.ID()
    text = graphene.String()
    timestamp = datetime.DateTime()

    # Set of Comments posted by a Person
    comments = graphene.List(lambda: PersonSchema)

    # Set of Comments for a particular Image
    comment_on = graphene.List(lambda: ImageSchema)


# Query Schemas
class Query(graphene.ObjectType):
    landmark = graphene.Field(lambda: LandMarkSchema, _id=graphene.ID())

    def resolve_landmark(self, info, _id):
        landmark = LandMark().fetch_by_id(graph, _id)
        return LandMarkSchema(**landmark.as_dict())


class CreateLandMark(graphene.Mutation):

    class Arguments:
        name = graphene.String(required=True)
        description = graphene.String(required=True)

        # Location information
        latitude = graphene.Float()
        longitude = graphene.Float()
        city = graphene.String()
        state = graphene.String()
        country = graphene.String()
        continent = graphene.String()

    success = graphene.Boolean()
    landmark = graphene.Field(lambda: LandMarkSchema)

    def mutate(self, info, **kwargs):
        print('Inside mutate')
        landmark = LandMark(**kwargs)
        landmark.save(graph)

        return CreateLandMark(landmark=landmark, success=True)


class Mutations(graphene.ObjectType):
    create_landmark = CreateLandMark.Field()


schema = graphene.Schema(query=Query, mutation=Mutations, auto_camelcase=False)

if __name__ == "__main__":
    result = schema.execute(
        '''
        mutation createLandMark {
            create_landmark(name: 'SOL',
                            description: 'NY'){
                landmark {
                    _id,
                    name,
                    description
                }
                ok
            }
        }
        '''
    )

    # items = dict(result.data.items())
    # print(json.dumps(items, indent=4))
    print(result.data)
