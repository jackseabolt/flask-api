from marshmallow import Schema, fields

class GetSchema(Schema): 
    pass

get_schema = GetSchema()

class PostSchema(Schema): 
    title = fields.Str(required=True)
    text = fields.Str(required=True)

post_schema = PostSchema()

