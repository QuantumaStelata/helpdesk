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
]
