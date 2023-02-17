from django.shortcuts import redirect

from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from helpdesk.models import Field, Node
from .serializers import FieldSerializer, NodeSerializer


class FieldViewSet(ModelViewSet):
    queryset = Field.objects.all()
    serializer_class = FieldSerializer
    http_method_names = ['get']
    permission_classes = [IsAuthenticated]

    def get_queryset(self):    
        queryset = super().get_queryset().exclude(deleted=True)

        if branch_id := self.request.GET.get("branch_id"):
            queryset = queryset.filter(branch_id=branch_id)

        return queryset

    def list(self, request, *args, **kwargs):
        if start_field := self.get_queryset().filter(is_start=True).first():
            return redirect("api:field-detail", pk=start_field.id)

        return Response({}, status=404)


class NodeViewSet(ModelViewSet):
    queryset = Node.objects.all()
    serializer_class = NodeSerializer
    http_method_names = ['get']
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return super().get_queryset().exclude(deleted=True)
