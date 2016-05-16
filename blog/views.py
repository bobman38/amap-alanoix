from django.shortcuts import redirect, get_object_or_404, render
from django.contrib.auth.decorators import login_required
from django.views import generic
from datetime import datetime
from django.utils.text import slugify
# Create your views here.
from .models import *
from .forms import *

class IndexView(generic.ListView):
    model = Entry

class EntryDetail(generic.dates.DateDetailView):
    model = Entry
    date_field = "publication_date"
    month_format = "%m"
    slug_field = "slug"
    def get_context_data(self, **kwargs):
        context = super(EntryDetail, self).get_context_data(**kwargs)
        context['form'] = CommentForm()
        return context

@login_required
def add_comment(request, entry_id):
    comment = Comment(entry=Entry.objects.get(pk=entry_id), author=request.user)
    form = CommentForm(request.POST, instance=comment)
    if form.is_valid():
        form.save()
    return redirect(comment.entry.get_absolute_url())

class EntryCreate(generic.edit.CreateView):
    model = Entry
    fields = ['title', 'body']
    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.slug = slugify(form.instance.title)
        return super(EntryCreate, self).form_valid(form)
