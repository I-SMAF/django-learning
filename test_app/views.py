from django.shortcuts import render
from django.views import View
from .models import *


class TestView(View):
    def get(self, request):
        return render(request, 'test.html',
                      {
                          'persons': Person.objects.have_pets(False),
                          'pets': Pet.objects.have_friends(True)

                      }
                      )
