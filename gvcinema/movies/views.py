import json
from datetime import datetime
from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from django.http.response import JsonResponse
from django.views.generic.base import View
from django.conf import settings
from _gvcinema_system.utilities.messages import message
# Forms
from .forms import SearchByName as FSearchByName, SaveJsonFile as FSaveJsonFile
# Models
from gvcinema.models import Movie

class Index(View):
    template_name   = "movies/pages/index.html"
    context         = {}

    def get(self, request, *args, **kwargs):
        try:
            self.context["page_title"]      = "GV Cinema - Movies"
            self.context["content_title"]   = "Movie Listings GVCinema"
            self.context["form_search"]     = FSearchByName
        except Exception as error:
            error                   = error if settings.DEBUG else "Internal server error code #IDXGT"
            self.context["error"]   = error
            self.template_name      = "public/error.html"
        finally:
            return render(
                request,
                self.template_name,
                self.context 
            )

class List(View):
    template_name   = "movies/sections/list.html"
    context         = {}

    def get(self, request, *args, **kwargs):
        try:
            self.context["section_title"]   = "Popular Movies This Month"
            # Get movies
            movies                          = Movie.objects.all()

            if request.GET and "name" in request.GET:
                name                            = request.GET.get("name")
                # Get movies
                movies                          = Movie.objects.filter(name__icontains=name)
                self.context["section_title"]   = f"Show { movies.count() } movies"

            self.context["media_url"]       = settings.MEDIA_URL
            self.context["movies"]          = movies
        except Exception as error:
            error                   = error if settings.DEBUG else "Internal server error code #LSGT"
            self.context["error"]   = error
            self.template_name      = "public/error.html"
        finally:
            return render(
                request,
                self.template_name,
                self.context 
            )
       
class Details(View):
    template_name   = "movies/sections/details.html"
    context         = {}

    def get(self, request, *args, **kwargs):
        try:
            # Get movie
            movie   = Movie.objects.get(
                external_id = kwargs.get("mov_exid")
            )

            self.context["media_url"]   = settings.MEDIA_URL
            self.context["movie"]       = movie
        except Exception as error:
            error                   = error if settings.DEBUG else "Internal server error code #DTXGT"
            self.context["error"]   = error
            self.template_name      = "public/error.html"
        finally:
            return render(
                request,
                self.template_name,
                self.context 
            )

class Search(View):
    template_name   = "movies/sections/formSearch.html"
    context         = {}

    def get(self, request, *args, **kwargs):
        try:
            self.context["form_search"] = FSearchByName
        except Exception as error:
            error                   = error if settings.DEBUG else "Internal server error code #DTXGT"
            self.context["error"]   = error
            self.template_name      = "public/error.html"
        finally:
            return render(
                request,
                self.template_name,
                self.context 
            )
        
    def post(self, request, *args, **kwargs):
        try:
            form_search = FSearchByName(
                request.POST or None,
                request.FILES or None
            )

            if form_search.is_valid():
                response    = message(
                    code        = 1,
                    messages    = {
                        "message"   : [f"Success at {datetime.now()}"]
                    },
                    data        = form_search.cleaned_data.get("name")
                )
            else:
                errors      = form_search.errors
                response    = message(
                    code        = 0,
                    messages    = errors
                )
        except Exception as error:
            error   = error if settings.DEBUG else "Inter server error code #SBNPT"
            response    = message(
                code        = 1,
                messages    = {
                    "message"   : error
                }
            ) 
        finally:
            return JsonResponse(
                response
            )

class BackendSave(View):
    template_name   = "movies/pages/backendSave.html"
    context         = {}

    def get(self, request, *args, **kwargs):
        self.context["form_create"]     = FSaveJsonFile
        self.context["page_title"]      = "BE Save"
        self.context["content_title"]   = "Save to Backend"
        
        return render(
            request,
            self.template_name,
            self.context
        )
    
    def post(self, request, *args, **kwargs):
        form_create = FSaveJsonFile(request.POST or None)
        if form_create.is_valid():
            data        = form_create.save()
            response    = message(
                code        = 1,
                messages    = {
                    "message"   : [f"Success at {datetime.now()}"]
                }
            )
        else:
            response    = message(
                code        = 0,
                messages    = form_create.errors
            )

        return JsonResponse(
            response
        )
    
