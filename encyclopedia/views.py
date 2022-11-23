from django.shortcuts import render
from . import util
from random import choice
import markdown2

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, entry_title):
    """
    Will render an entry using the title of the entry to find it. 
    If the title isn't an existing entry, it will render an error.
    """
    content = util.get_entry(entry_title)
    if not content:
        return render(request, "encyclopedia/error.html",{
            "error": "The requested entry does not exist!"
        })
    return render(request, "encyclopedia/entry.html", {
        "entry_title": entry_title,
        "content": markdown2.markdown(content.strip())
    })

def search(request):
    """
    Will attempt to find a match for the search result.
    If none is found, it will return related pages by checking whether the query is a substring of any title of any entry. 
    Otherwise, will return an error page.
    """      
    if request.method == "POST":
        entries = util.list_entries()
        partial_matches = []
        query = request.POST.get("q","")
        for entry in entries:        
            if query == entry:
                return entry(request, entry)
            if query in entry:
                partial_matches.append(entry)   
        if not partial_matches:
            return render(request, "encyclopedia/error.html", {
                "error": "No results found, please try again or go back to the homepage."
            })
        return render(request, "encyclopedia/search-results.html",{
            "entries": partial_matches
        })

def random(request):
    """
    Selects a random item from the entries list and passes it to the entry view.
    """
    return entry(request, choice(util.list_entries()))

def add(request):
    """
    If it's a POST request the entry information is added to DB.
    Then the user is redirected to the new entry.
    Otherwise, render the form to submit the new entry info.
    """
    if request.method == "POST":       
        title = request.POST.get("title")
        content = request.POST.get("content")
        util.save_entry(title, content)
        return entry(request, title)
    return render(request, "encyclopedia/add.html")

def edit(request):
    """
    If it's a POST request, we save the entry information using the original title.
    The save function will override the old data with the new one.
    Then the user is redirected to the new entry. 
    """
    if request.method == "POST":
        title = request.POST.get("title")
        new_content = request.POST.get("content")
        util.save_entry(title, new_content)
        return entry(request, title)
    title = request.GET.get("title")
    return render(request, "encyclopedia/edit.html", {
        "title": title,
        "content": util.get_entry(title).strip()
    })