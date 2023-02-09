from django.urls import path
from . import views

app_name = "helpdesk"


urlpatterns = [
   path("branch-list/", views.BranchListView.as_view(), name="branch-list"),
   path("branch-detail/", views.BranchDetailView.as_view(), name="branch-detail", kwargs={"branch_id": False}),
   path("branch-detail/<slug:branch_id>/", views.BranchDetailView.as_view(), name="branch-detail"),   
   path("branch-create/", views.BranchCreateView.as_view(), name="branch-create"),

   path("pull-list/", views.PullListView.as_view(), name="pull-list"),
   path("pull-detail/<slug:pull_id>/", views.PullDetailView.as_view(), name="pull-detail"),
   path("pull-create/<slug:branch_id>/", views.PullCreateView.as_view(), name="pull-create"),
   path("pull-merge/<slug:pull_id>/", views.PullMergeView.as_view(), name="pull-merge"),

   path("field-create/", views.FieldCreateView.as_view(), name="field-create"),
   path("field-update/<slug:pk>/", views.FieldUpdateView.as_view(), name="field-update"),
   path("field-delete/<slug:pk>/", views.FieldDeleteView.as_view(), name="field-delete"),
   path("node-create/", views.NodeCreateView.as_view(), name="node-create"),
   path("node-update/<slug:pk>/", views.NodeUpdateView.as_view(), name="node-update"),
   path("node-delete/<slug:pk>/", views.NodeDeleteView.as_view(), name="node-delete"),
]
