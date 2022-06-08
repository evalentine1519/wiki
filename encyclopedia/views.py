from django.shortcuts import render, redirect

import markdown2 as md

from . import util

from django import forms

from random import getrandbits

class SearchBox(forms.Form):
    query = forms.CharField(label="searchquery")


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def test(request, title):
    return render(request, "encyclopedia/test.html", {
        "entries": util.list_entries(),
        "title": title,

    })

def entry(request, title):
    x = type(util.get_entry(title))
    if issubclass(x, str):
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "entry": md.markdown(util.get_entry(title)),
            "content": util.get_entry(title)
        })
    else:
        return render(request, "encyclopedia/error.html", {
            #"title": title,
            "error": f"<h1>Error: {title} was not found.</h1>"
        })

def search(request):
    query = request.GET['q']


    if util.get_entry(query):
        return render(request, "encyclopedia/entry.html", {
            "entry": md.markdown(util.get_entry(query)),
            "title": query
        })
    else:
        all_articles = util.list_entries()
        matched_articles = []

        for article in all_articles:
            #print(query)
            #print(article)
            if query.lower() in article.lower():
                matched_articles.append(article)

        if matched_articles == []:
            print("No results found")
            return render(request, "encyclopedia/search.html", {
                "exists": False,
                "title": query
            })
        else:
            print("results found")
            print(matched_articles)
            return render(request, "encyclopedia/search.html", {
                "exists": True,
                "entries": matched_articles,
                "title": query
            })

#Generates a random number, mods it with the length of the list of all articles, returns a page
#with the index of the result
def random(request):
    art_list = util.list_entries()
    art = art_list[(getrandbits(10) % len(art_list))]

    #print(art_list)
    #print(art)

    #return render(request, "encyclopedia/entry.html", {
    #    "title": art,
    #    "entry": md.markdown(util.get_entry(art))
    #})

    return redirect('entry', title=art)

def new(request):
    if request.method == "POST":
        content = request.POST['content']
        title = request.POST['title']

        if len(title) > 0:
            articles = util.list_entries()
            test_title = title.lower()

            for i in range(len(articles)):
                articles[i] = articles[i].lower()

            if test_title not in articles:
                util.save_entry(title, content)
                return redirect('entry', title=title)
            else:
                return render(request, "encyclopedia/new.html", {
                    "title": "New Entry",
                    "entry_title": title,
                    "content": content,
                    "error": "<h1>Error: An article with this title already exists.</h1>"
                })
        else:
            return render(request, "encyclopedia/new.html", {
                "title": "New Entry",
                "entry_title": title,
                "content": content,
                "error": "<h1>Error: You must submit a name for your entry.</h1>"
            })

    return render(request, "encyclopedia/new.html", {
        "title": "New Entry",
    #    "entry_title": "test2"
    #    "content": "Please enter the markdown content for the page you wish to create."
    })

def edit(request):
    if request.method == 'GET':
        entry_title = request.GET['title']
        entry_content = request.GET['content']

    if request.method == "POST":
        entry_title = request.POST['title']
        entry_content = request.POST['content']
        util.save_entry(entry_title, entry_content)
        return redirect('entry', title=entry_title)
    return render(request, "encyclopedia/edit.html", {
        "title": entry_title,
        "content": entry_content
    })