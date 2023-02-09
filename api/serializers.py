from rest_framework.serializers import ModelSerializer, SlugRelatedField
from rest_framework.fields import SerializerMethodField

from helpdesk.models import Field, Node


class NodeSerializer(ModelSerializer):
    childs = SlugRelatedField(many=True, slug_field="id", read_only=True)

    class Meta:
        model = Node
        exclude = ("version", "original", "branch", "deleted", "creator", "parent")


class FieldSerializer(ModelSerializer):
    childs = SerializerMethodField()

    class Meta:
        model = Field
        exclude = ("version", "original", "branch", "deleted", "creator", "parent")
    
    def get_childs(self, obj, *args, **kwargs):
        return NodeSerializer(obj.childs.exclude(deleted=True), many=True, read_only=True).data
