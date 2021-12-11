from django.shortcuts import render

from django.http import (
    Http404,
    HttpResponseRedirect
)

from .models import Parse
from django import forms
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import serializers, status
from rest_framework.decorators import api_view


class ParseForm(forms.ModelForm):
    raw_url = forms.URLField(widget=forms.URLInput(
        attrs={
            "class": "form-control form-control-lg",
            "placeholder": "masukin link dimari",
            "style": "text-align: center;"}
    ))

    class Meta:
        model = Parse
        fields = ('raw_url',)

class Downloader(serializers.ModelSerializer):
    class Meta:
        model = Parse
        fields = ('raw_url',)


def home(request):
    template = 'index.html'
    context = {}
    context['form'] = ParseForm()
    if request.method == 'GET':
        return render(request, template, context)
    elif request.method == 'POST':
        used_form = ParseForm(request.POST)
        # If URL is valid
        if used_form.is_valid():
            downloadable_object = used_form.save()
            context['downloadable_url'] = downloadable_object.downloadable_url
            context['raw_url'] = downloadable_object.raw_url
            context['social_media_source'] = downloadable_object.social_media_source
            return render(request, template, context)
        # Else
        context['errors'] = used_form.errors
        return render(request, template, context)


def downloadable_parse_url(request, downloadable_url):
    try:
        parsed_url = Parse.objects.get(downloadable_url=downloadable_url)
        parsed_url.times_followed += 1
        parsed_url.save()
        return HttpResponseRedirect(parsed_url.raw_url)
    except:
        raise Http404('This link is broken')


class DiDownloadinAPI(APIView):
    def post(self, request):
        context = {}
        used_form = Downloader(data=request.data, many=False)
        if used_form.is_valid():
            downloadable_object = used_form.save()
            context['raw_url'] = downloadable_object.raw_url
            context['downloadable_url'] = downloadable_object.downloadable_url
            context['social_media_source'] = downloadable_object.social_media_source
            return Response(context, status=status.HTTP_201_CREATED)
        context['errors'] = used_form.errors
        return Response(context, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, url):
        return Response({
            'Message': 'GET method is allowed, but doesn\'t return anything except this message of how to usage this API, use POST method instead to get downloadable media links',
            'Usage': {
                "Method": "POST",
                "Media Type": "application/json",
                "Body": {
                    "raw_url": "enter your URL here"
                },
                "Return": {
                        "raw_url": "your entered URL",
                        "downloadable_url": "shorted URL",
                        "social_media_source": "download link from social media"
                }
            }
        })