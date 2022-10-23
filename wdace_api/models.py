from django.db import models

# Create your models here.

from neomodel import StructuredNode, StringProperty, IntegerProperty,UniqueIdProperty, RelationshipTo, FloatProperty, ArrayProperty



class Topic(StructuredNode):
    uid = UniqueIdProperty()
    name = StringProperty(unique_index=True, required=True)
    level = IntegerProperty(required=True)
    weight = FloatProperty(default=0.5)
    urls = ArrayProperty(StringProperty())

    #Relations
    hasTopic = RelationshipTo('Topic', 'HAS_TOPIC')
