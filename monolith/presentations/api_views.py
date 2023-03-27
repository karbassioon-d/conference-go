from django.http import JsonResponse
from common.json import ModelEncoder
from events.api_views import ConferenceDetailEncoder
from .models import Presentation
from events.models import Conference
import json
from django.views.decorators.http import require_http_methods


class PresentationDetailEncoder(ModelEncoder):
    model = Presentation
    properties = [
        "presenter_name",
        "company_name",
        "presenter_email",
        "title",
        "synopsis",
        "created",
        "conference",
    ]
    encoders = {
        "conference": ConferenceDetailEncoder()
    }

    def get_extra_data(self, o):
        return {"status": o.status.name}

class PresentationListEncoder(ModelEncoder):
    model = Presentation
    properties = ["title"]

    def get_extra_data(self, o):
        return {"status": o.status.name}

@require_http_methods(["GET", "POST"])
def api_list_presentations(request, conference_id):
    """
    Lists the presentation titles and the link to the
    presentation for the specified conference id.

    Returns a dictionary with a single key "presentations"
    which is a list of presentation titles and URLS. Each
    entry in the list is a dictionary that contains the
    title of the presentation, the name of its status, and
    the link to the presentation's information.

    {
        "presentations": [
            {
                "title": presentation's title,
                "status": presentation's status name
                "href": URL to the presentation,
            },
            ...
        ]
    }
    """
    if request.method == "GET":
        presentations = Presentation.objects.all()
        return JsonResponse(
            {"presentations": presentations},
            encoder=PresentationListEncoder,
        )
    else:
        #This is a post method that creates a presentation object
        #The presentation object requires the strings in the JSON body which can be found in the models.py
        #presentations also requires 2 models to be assigned, the foreign keys
        #The status model is assigned by the create function
        content = json.loads(request.body)
        #fetching the conference based on the id passed in the EARL
        conference = Conference.objects.get(id=conference_id)
        #That gets assigned to the content dictionary
        content["conference"] = conference
        #That dictioinary gets passed through to the Presentation.create() funciton
        #and puts it in our existing database
        presentation = Presentation.create(**content)
        return JsonResponse(
            presentation,
            encoder=PresentationDetailEncoder,
            safe=False,
        )

@require_http_methods(["DELETE", "GET", "PUT"])
def api_show_presentation(request, id):
    """
    Returns the details for the Presentation model specified
    by the id parameter.

    This should return a dictionary with the presenter's name,
    their company name, the presenter's email, the title of
    the presentation, the synopsis of the presentation, when
    the presentation record was created, its status name, and
    a dictionary that has the conference name and its URL

    {
        "presenter_name": the name of the presenter,
        "company_name": the name of the presenter's company,
        "presenter_email": the email address of the presenter,
        "title": the title of the presentation,
        "synopsis": the synopsis for the presentation,
        "created": the date/time when the record was created,
        "status": the name of the status for the presentation,
        "conference": {
            "name": the name of the conference,
            "href": the URL to the conference,
        }
    }
    """

    if request.method == "GET":
        presentation = Presentation.objects.get(id=id)
        return JsonResponse(
            presentation,
            encoder=PresentationDetailEncoder,
            safe=False,
        )
    elif request.method == "DELETE":
        count, _ = Presentation.objects.filter(id=id).delete()
        return JsonResponse({"deleted": count > 0})

    else:
        content = json.loads(request.body)
        # try:
        #     if "
        # except:

        Presentation.objects.filter(id=id).update(**content)

        presentation = Presentation.objects.get(id=id)
        return JsonResponse(
            presentation,
            encoder=PresentationDetailEncoder,
            safe=False,
        )