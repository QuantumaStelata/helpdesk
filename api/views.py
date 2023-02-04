from django.shortcuts import redirect
from django.conf import settings

from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response

from helpdesk.models import Field, Node
from .serializers import FieldSerializer, NodeSerializer


class FieldViewSet(ModelViewSet):
    queryset = Field.objects.all()
    serializer_class = FieldSerializer
    http_method_names = ['get']

    def list(self, request, *args, **kwargs):
        branch_id = request.GET.get("branch_id")

        if start_field := Field.objects.filter(is_start=True, branch_id=branch_id).first():
            return redirect("api:field-detail", pk=start_field.id)

        return Response({}, status=404)


class NodeViewSet(ModelViewSet):
    queryset = Node.objects.all()
    serializer_class = NodeSerializer
    http_method_names = ['get']
