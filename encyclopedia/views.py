from django.shortcuts import render
from markdown2 import Markdown
from . import util
from django import forms
from django.urls import reverse
from django.http import HttpResponseRedirect


class entry_form(forms.Form):
    title = forms.CharField(label="Title", widget=forms.TextInput(
        attrs={'class': 'form-control'}))
    description = forms.CharField(
        label="Description", widget=forms.Textarea(attrs={'class': 'form-control'}))
    edit = forms.BooleanField(
        initial=False, widget=forms.HiddenInput, required=False)


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entry(request, entry):
    markdown = Markdown()
    entry_page = util.get_entry(entry)
    if entry_page is None:
        return render(request, "encyclopedia/noExisting.html", {
            "entry_title": entry,
        })
    else:
        return render(request, "encyclopedia/entry.html", {
            "entry": markdown.convert(entry_page),
            "entry_title": entry.capitalize(),
        })


# def search(request):
#     query = request.GET.get('q', '')
#     if(util.get_entry(query) is not None):
#         return HttpResponseRedirect(reverse("entry", kwargs={'entry': query}))
#     else:
#         sub_entries = []
#         for entry in util.list_entries():
#             if search.upper() in entry.upper():
#                 sub_entries.append(entry)
#         return render(request, "encyclopedia/index.html", {
#             "sub_entries": sub_entries,
#             "search": True,
#             "value": query,
#         })


def new_entry(request):
    return render(request, "encyclopedia/new_entry.html", {
        "form": entry_form,
    })
