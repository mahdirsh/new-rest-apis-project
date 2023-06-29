from marshmallow import Schema, fields


class PlainItemSchema(Schema):  # when we want to include a nested item within a store
    # id : beacuse we generated the field ourselves it's never gonna come in a request 
    # (we only want to use it for returning data) not going to get used for validation
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)  # if this field is required and must be in the JSON payload
    price = fields.Float(required=True)
    

class PlainStoreSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)


class PlainTagSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()




class ItemUpdateSchema(Schema):
    name = fields.Str()               # not required beacuse the user may send us name or price or both or neither
    price = fields.Float()
    store_id = fields.Int()


class ItemSchema(PlainItemSchema):
    store_id = fields.Int(required=True, load_only=True)
    store = fields.Nested(PlainStoreSchema(), dump_only=True)  # only be used when returning data to the client and not when receiving data from them
    tags = fields.List(fields.Nested(PlainTagSchema()), dump_only=True)


class StoreSchema(PlainStoreSchema):
    items = fields.List(fields.Nested(PlainItemSchema()), dump_only=True)
    tags = fields.List(fields.Nested(PlainTagSchema()), dump_only=True) 


class TagSchema(PlainTagSchema):
    store_id = fields.Int(load_only=True)
    store = fields.Nested(PlainStoreSchema(), dump_only=True)
    items = fields.List(fields.Nested(PlainItemSchema()), dump_only=True)


class TagAndItemSchema(Schema):
    message = fields.Str()
    item = fields.Nested(ItemSchema)
    tag = fields.Nested(TagSchema)


class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True)
    password = fields.Str(required=True)   # load_only=True >>> make sure that the password is never being sent to the client


class UserRegisterSchema(UserSchema):
    emal = fields.Str(required=True)