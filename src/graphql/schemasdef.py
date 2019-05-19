import graphene


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


class VisitorInput(graphene.InputObjectType):
    landmark_name = graphene.String(required=True)
    visitor_key = graphene.String(required=True)
