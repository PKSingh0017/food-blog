from django.shortcuts import render, get_object_or_404, redirect, reverse
import json
from django.conf import settings
import os

BASE_DIR = settings.BASE_DIR
path_to_front_end_json = os.path.join(BASE_DIR, "core/front_end.json")

def edit_hero(request):
    front_end_variables = open(path_to_front_end_json, "r")
    FRONT_END_VARIABLES = json.load(front_end_variables)
    front_end_variables.close()
    FRONT_END_VARIABLES["Hero"] = {
        "title": request.POST.get('title'),
        "description": request.POST.get('description'),
        "button": request.POST.get('button'),
        "video_link": request.POST.get('video_link')
    }
    json_file = open(path_to_front_end_json, "w")
    json.dump(FRONT_END_VARIABLES, json_file)
    json_file.close()
    return redirect("home")


def edit_SocialMedia(request):
    front_end_variables = open(path_to_front_end_json, "r")
    FRONT_END_VARIABLES = json.load(front_end_variables)
    front_end_variables.close()
    FRONT_END_VARIABLES["SocialMedia"] = {
        "title": request.POST.get('title'),
        "description": request.POST.get('description'),
        "links": {
            "facebook": request.POST.get('links_facebook'),
            "linkedin": request.POST.get('links_linkedin'),
            "twitter": request.POST.get('links_twitter'),
            "instagram": request.POST.get('links_instagram'),
            "github": request.POST.get('links_github')
        }
    }
    json_file = open(path_to_front_end_json, "w")
    json.dump(FRONT_END_VARIABLES, json_file)
    json_file.close()
    return redirect("home")

def edit_Newsletter(request):
    front_end_variables = open(path_to_front_end_json, "r")
    FRONT_END_VARIABLES = json.load(front_end_variables)
    front_end_variables.close()
    FRONT_END_VARIABLES["Newsletter"] = {
        "title": request.POST.get('title'),
        "description": request.POST.get('description'),
        "button": request.POST.get('button'),
    }
    json_file = open(path_to_front_end_json, "w")
    json.dump(FRONT_END_VARIABLES, json_file)
    json_file.close()
    return redirect("home")

def edit_Contact(request):
    front_end_variables = open(path_to_front_end_json, "r")
    FRONT_END_VARIABLES = json.load(front_end_variables)
    front_end_variables.close()
    FRONT_END_VARIABLES["Contact"] = {
        "title": request.POST.get('title'),
        "description": request.POST.get('description'),
        "address": {
            "street": request.POST.get('address_street'),
            "city": request.POST.get('address_city'),
            "country": request.POST.get('address_country'),
            "pin": request.POST.get('address_pin'),
            "location_link": request.POST.get('location_link'),
        },
        "phone_number": request.POST.get('phone_number'),
        "email": request.POST.get('email')
    }
    json_file = open(path_to_front_end_json, "w")
    json.dump(FRONT_END_VARIABLES, json_file)
    json_file.close()
    return redirect("home")



def docs(request, doc_name):
    front_end_variables = open(path_to_front_end_json, "r")
    FRONT_END_VARIABLES = json.load(front_end_variables)
    front_end_variables.close()

    context = {
        "doc_object": FRONT_END_VARIABLES["Extras"][doc_name],
        "doc_object_name": doc_name,
        "title": FRONT_END_VARIABLES["Extras"][doc_name]["title"]
    }

    return render(request, 'store/extras.html', context)

def add_docs(request):

    front_end_variables = open(path_to_front_end_json, "r")
    FRONT_END_VARIABLES = json.load(front_end_variables)
    front_end_variables.close()
    new_doc_name = request.POST.get("doc_name")
    FRONT_END_VARIABLES["Extras"][new_doc_name] = {
        "name": request.POST.get("doc_name"),
        "title": request.POST.get("doc_title"),
        "content": request.POST.get("doc_content"),
    }


    json_file = open(path_to_front_end_json, "w")
    json.dump(FRONT_END_VARIABLES, json_file)
    json_file.close()
    return redirect("docs", name=new_doc_name)


def edit_docs(request, doc_name):

    front_end_variables = open(path_to_front_end_json, "r")
    FRONT_END_VARIABLES = json.load(front_end_variables)
    front_end_variables.close()

    FRONT_END_VARIABLES["Extras"][doc_name] = {
        "name": request.POST.get("doc_name"),
        "title": request.POST.get('doc_title'),
        "content": request.POST.get('doc_content'),
    }

    json_file = open(path_to_front_end_json, "w")
    json.dump(FRONT_END_VARIABLES, json_file)
    json_file.close()
    return redirect("docs", doc_name=doc_name)