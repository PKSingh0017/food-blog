import os
import json
from django.conf import settings

BASE_DIR = settings.BASE_DIR

path_to_front_end_json = os.path.join(BASE_DIR, "core/front_end.json")

def front_end_variables(request):
    front_end_variables = open(path_to_front_end_json, "r")
    FRONT_END_VARIABLES = json.load(front_end_variables)
    front_end_variables.close()
    context = FRONT_END_VARIABLES
    return context