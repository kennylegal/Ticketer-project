from typing import List
from django.http import HttpRequest, JsonResponse
from ninja.errors import HttpError
from ninja_jwt.authentication import JWTAuth
from ninja import Router
from .models import EventModel
from django.shortcuts import get_object_or_404
from .schema import (
    EventIn, EventOut
)

router = Router()

@router.get("", response=List[EventOut])
def listevents(request: HttpRequest):
    obj = EventModel.objects.all()
    return obj


@router.post("/", response=EventOut)
def eventCreate(request:HttpRequest, data: EventIn):
    return


@router.get("{event_id}", response=EventOut, auth=JWTAuth())
def getevent(request: HttpRequest, event_id: str):
    obj = __getEvent(id=event_id, request=request)
    if obj:
        return EventOut(
                id=obj.id,
                title=obj.title,
                description=obj.description,
                date=obj.date,
                image=obj.image.url if obj.image else None
            )
    return JsonResponse({"data": "Data does not exist"})


@router.get("user/my-event", response=List[EventOut], auth=JWTAuth())
def get_users_event(request: HttpRequest):
    events = __getUserEvent(request)
    return [ EventOut(
            id=obj.id,
            title=obj.title,
            description=obj.description,
            date=obj.date,
            image=obj.image.url if obj.image else None
        ) for obj in events
         ]


@router.delete("{event_id}", auth=JWTAuth())
def delete_event(request: HttpRequest, event_id:str):
    print(request.user)
    response = __getEvent(id=event_id, request=request)
    print(request.user)
    response.delete()
    return JsonResponse({"Detail": "Event deleted"}, status=204)


def __getEvent(request, id):
    user = request.user
    if not user.is_authenticated:
        raise HttpError(401, "USER IS NOT AUTHORIZED")
    qs = get_object_or_404(EventModel, id=int(id))
    if qs.user_id != user.id:
        raise HttpError(403, "YOU DO NOT HAVE PERMISSION TO VIEW THIS PAGE")
    return qs

def __getUserEvent(request: HttpRequest):
    user = request.user
    if not user.is_authenticated:
        raise HttpError(401, "USER IS NOT AUTHORIZED")
    qs = EventModel.objects.filter(user=user.id)
    if not qs.exists():
        raise JsonResponse({"data":"YOU DO NOT HAVE ANY EVENT CREATED YET"})
    return qs