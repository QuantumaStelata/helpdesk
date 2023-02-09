from django.shortcuts import redirect, get_object_or_404
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView
from django.views.decorators.csrf import csrf_exempt
from django.http.response import HttpResponse
from django.utils.decorators import method_decorator

from .models import Field, Node
from .forms import FieldForm, NodeForm
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


class FieldCreateView(CreateView):
    model = Field
    form_class = FieldForm
    template_name = "form.html"

    def get_initial(self):
        initial = super().get_initial()

        if parent := self.request.GET.get("parent"):
            initial["parent"] = parent
        
        if branch := self.request.GET.get("branch"):
            initial["branch"] = branch
        
        initial["creator"] = self.request.user

        return initial
    
    def form_valid(self, form):
        form.save()
        return HttpResponse()
    
    def form_invalid(self, form):
        response =  super().form_invalid(form)
        response.status_code = 400
        return response


class FieldUpdateView(UpdateView):
    model = Field
    form_class = FieldForm
    template_name = "form.html"

    def form_valid(self, form):
        form.save()
        return HttpResponse()
    
    def form_invalid(self, form):
        response =  super().form_invalid(form)
        response.status_code = 400
        return response


@method_decorator(csrf_exempt, name='dispatch')
class FieldDeleteView(View):
    def post(self, request, pk, *args, **kwargs):
        field = get_object_or_404(Field, pk=pk)
        field.deleted = True
        field.save()

        return HttpResponse()


class NodeCreateView(CreateView):
    model = Node
    form_class = NodeForm
    template_name = "form.html"

    def get_initial(self):
        initial = super().get_initial()

        if parent := self.request.GET.get("parent"):
            initial["parent"] = parent
        
        if branch := self.request.GET.get("branch"):
            initial["branch"] = branch
        
        initial["creator"] = self.request.user

        return initial

    def form_valid(self, form):
        form.save()
        return HttpResponse()

    def form_invalid(self, form):
        response =  super().form_invalid(form)
        response.status_code = 400
        return response


class NodeUpdateView(UpdateView):
    model = Node
    form_class = NodeForm
    template_name = "form.html"

    def form_valid(self, form):
        form.save()
        return HttpResponse()
    
    def form_invalid(self, form):
        response =  super().form_invalid(form)
        response.status_code = 400
        return response


@method_decorator(csrf_exempt, name='dispatch')
class NodeDeleteView(View):
    def post(self, request, pk, *args, **kwargs):
        node = get_object_or_404(Node, pk=pk)
        node.deleted = True
        node.save()

        return HttpResponse()
