import random
from re import S
from django.shortcuts import render, redirect
from markdown2 import Markdown
from . import util
from django import forms
from django.urls import reverse
from django.http import HttpResponseRedirect, request


class SearchForm(forms.Form):
    title = forms.CharField(label='', widget=forms.TextInput(attrs={
        "class": "search",
        "placeholder": "Search"
    }))


markdown = Markdown()


class entry_form(forms.Form):
    title = forms.CharField(label="Title", widget=forms.TextInput(
        attrs={'class': 'form-control'}))
    description = forms.CharField(
        label="Description", widget=forms.Textarea(attrs={'class': 'form-control'}))
    edit = forms.BooleanField(
        initial=False, widget=forms.HiddenInput, required=False)


class edit_form(forms.Form):
    entry = forms.CharField(label="", widget=forms.Textarea(
        attrs={'class': 'form-control', "placeholder": "Edit Page Content"}))


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "search_form": SearchForm(),
    })


def entry(request, entry):
    entry_page = util.get_entry(entry)
    if entry_page is None:
        return render(request, "encyclopedia/noExisting.html", {
            "entry_title": entry,
            "search_form": SearchForm(),
        })
    else:
        return render(request, "encyclopedia/entry.html", {
            "entry": markdown.convert(entry_page),
            "entry_title": entry,
            "search_form": SearchForm(),
        })


def search(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            entry = util.get_entry(title)
            print('search: ', title)
            if entry:
                return redirect(reverse('entry', args=[title]))
            else:
                related_search = util.related_search(title)
                return render(request, "encyclopedia/search.html", {
                    "search_form": SearchForm(),
                    "related_search": related_search,
                    "title": title,
                })


def new_entry(request):
    if request.method == 'GET':
        return render(request, "encyclopedia/new_entry.html", {
            "form": entry_form,
            "search_form": SearchForm(),
        })
    elif request.method == 'POST':
        form = entry_form(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            description = form.cleaned_data['description']
        else:
            return render(request, "encyclopedia/new_entry.html", {
                "form": entry_form,
                "search_form": SearchForm(),
            })

        if util.get_entry(title):
            return render(request, "encyclopedia/exist.html", {
                "form": entry_form,
                "search_form": SearchForm(),
                'title': title,
            })
        else:
            util.save_entry(title, description)
            return redirect(reverse('entry', args=[title]))


def edit(request, title):
    if request.method == 'GET':
        getentry = util.get_entry(title)
        return render(request, "encyclopedia/edit_page.html", {
            "edit": edit_form(initial={'entry': getentry}),
            "title": title,
        })
    elif request.method == 'POST':
        form = edit_form(request.POST)
        if form.is_valid():
            entry = form.cleaned_data['entry']
            util.save_entry(title, entry)
            return redirect(reverse("entry", args=[title]))
        else:
            return render(request, "encyclopedia/edit.html", {
                "title": title,
                "edit": form,
                "search_form": SearchForm(),
            })


def random_page(request):
    entries = util.list_entries()
    selected = random.choice(entries)
    return HttpResponseRedirect(reverse('entry', args=[selected]))
