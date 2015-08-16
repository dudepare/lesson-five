from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import CreateView, RedirectView, DetailView, UpdateView
from django.core.urlresolvers import reverse

from .forms import EntryForm, ProjectForm, ClientForm
from .models import Client, Entry, Project

class RootRedirectView(RedirectView):
    permanent = False

    def get_redirect_url(self):
        return reverse('client-list')

class ClientCreateView(CreateView):
    model = Client
    template_name = 'clients.html'
    form_class = ClientForm

    def get_success_url(self):
        return reverse('client-list')

    def get_context_data(self, **kwargs):
        context = super(ClientCreateView, self).get_context_data(**kwargs)
        # you still need to set the context client_list so your template could read the data
        context['client_list'] = self.model.objects.all()
        return context

class ClientUpdateView(UpdateView):
    model = Client
    template_name = 'client_detail.html'
    form_class = ClientForm

    def get_success_url(self):
        return reverse('client-list')

class EntriesCreateView(CreateView):
    model = Entry
    template_name = 'entries.html'
    form_class = EntryForm 

    def get_success_url(self):
        return reverse('entry-list')

    def get_context_data(self, **kwargs):
        context = super(EntriesCreateView, self).get_context_data(**kwargs)
        context['entry_list'] = self.model.objects.all()
        return context

class ProjectsCreateView(CreateView):
    model = Project
    template_name = 'projects.html'
    form_class = ProjectForm

    def get_success_url(self):
        return reverse('project-list')

    def get_context_data(self, **kwargs):
        context = super(ProjectsCreateView, self).get_context_data(**kwargs)
        context['project_list'] = self.model.objects.all()
        return context


class ProjectUpdateView(UpdateView):
    model = Project
    template_name = 'project_detail.html'
    form_class = ProjectForm

    def get_success_url(self):
        return reverse('project-list')
