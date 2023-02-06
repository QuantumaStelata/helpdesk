from django.shortcuts import redirect, get_object_or_404
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, CreateView

from .models import Field, Node
from vcs import utils
from vcs.models import Branch, PullRequest


class BranchListView(ListView):
    template_name = "helpdesk/branch-list.html"
    model = Branch

    def get_queryset(self):
        return self.request.user.branchs.all() | self.request.user.contribute_branchs.all()


class BranchDetailView(TemplateView):
    template_name = "helpdesk/branch-detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        if branch_id := self.kwargs.get("branch_id"):
            context["branch"] = get_object_or_404(Branch, id=branch_id)
        else:
            context["branch"] = Branch(name="Main")

        return context


class BranchCreateView(CreateView):
    model = Branch
    fields = "__all__"
    template_name = "helpdesk/branch-create.html"

    def get_initial(self):
        initial = super().get_initial()
        initial["creator"] = self.request.user
        initial["contributors"] = self.request.user
        return initial
    
    def form_valid(self, form):
        branch = form.save()
        utils.create_branch(branch)
        return redirect("helpdesk:branch-detail", branch_id=branch.id)


class PullListView(ListView):
    template_name = "helpdesk/pull-list.html"
    model = PullRequest

    def get_queryset(self):
        return self.request.user.pullrequests.all()


class PullDetailView(DetailView):
    template_name = "helpdesk/pull-detail.html"
    model = PullRequest
    pk_url_kwarg = "pull_id"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        diffs = utils.pull_detail(context["object"])

        if diffs["fields"]:
            context["fields"] = Field.objects.filter(id__in=diffs["fields"])
        
        if diffs["nodes"]:
            context["nodes"] = Node.objects.filter(id__in=diffs["nodes"])

        context["fields_conflict"] = diffs["conflicts"]["fields"]
        context["nodes_conflict"] = diffs["conflicts"]["nodes"]

        return context


class PullCreateView(View):
    def get(self, request, branch_id, *args, **kwargs):
        branch = Branch.objects.get(id=branch_id)
        
        if not (pull := branch.pulls.filter(status=1).first()):
            pull = PullRequest.objects.create(
                branch=branch,
                creator=request.user
            )

        return redirect("helpdesk:pull-detail", pull_id=pull.id)


class PullMergeView(View):
    def get(self, request, pull_id, *args, **kwargs):
        pull = PullRequest.objects.get(id=pull_id)
        utils.pull_merge(pull)
        return redirect("helpdesk:pull-detail", pull_id=pull_id)
