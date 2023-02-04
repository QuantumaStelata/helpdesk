from rest_framework.serializers import ModelSerializer
from rest_framework.fields import SerializerMethodField

from helpdesk.models import Field, Node


class FieldSerializer(ModelSerializer):
    # child_nodes = SerializerMethodField()

    class Meta:
        model = Field
        exclude = ("version", "original", "branch")
    
    # def get_child_nodes(self, obj):
    #     return NodeSerializer(obj.child_nodes.filter(is_active=True, deleted=False), many=True).data


class NodeSerializer(ModelSerializer):
    class Meta:
        model = Node
        exclude = ("version", "original", "branch")
