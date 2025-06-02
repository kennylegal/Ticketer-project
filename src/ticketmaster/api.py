from ninja import Router
from ninja_extra import NinjaExtraAPI
from ninja_jwt.controller import NinjaJWTDefaultController
from ninja_jwt.authentication import JWTAuth
from django.http import HttpResponse
from event.api import router as event_router


api = NinjaExtraAPI()
api.register_controllers(NinjaJWTDefaultController)
api.add_router("events/", event_router)


@api.get("", auth=JWTAuth())
def home(request):
    return HttpResponse("Hello, this is taiwo")