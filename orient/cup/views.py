import logging

from django.http import JsonResponse
from django.shortcuts import render
from django.template.context_processors import csrf
from django.utils.decorators import method_decorator
from django.views import generic
from django.views.decorators.csrf import csrf_protect

from .models import Organizer, Season
from .forms import OrganizerForm, SeasonForm

logger = logging.getLogger(__name__)


class IndexView(generic.TemplateView):
    template_name = 'cup/index.html'


class OrganizerView(generic.DetailView):
    model = Organizer

#    @method_decorator(csrf_protect)
    def render_to_response(self, context, **response_kwargs):
        organizer = {
            'pk': context['object'].pk,
            'first_name': context['object'].first_name,
            'last_name': context['object'].last_name,
            'username': context['object'].username,
            'web': context['object'].web,
            'phone': context['object'].phone,
            'desc': context['object'].desc,
            'csrf_token': str(csrf(self.request).get('csrf_token')),
        }

        return JsonResponse(organizer, safe=False)


class OrganizerUpdateView(generic.UpdateView):
    model = Organizer
    form_class = OrganizerForm

    def render_to_response(self, context, **response_kwargs):
        result = {
            'pk': context['object'].pk,
            'status': None
        }
        return JsonResponse(result, safe=False)


class OrganizerCreateView(generic.CreateView):
    model = Organizer
    form_class = OrganizerForm

    def render_to_response(self, context, **response_kwargs):
        context = super(OrganizerCreateView, self).render_to_response(context, **response_kwargs)
        result = {
            'pk': context.get('object', {}).get('pk'),
            'is_created': None
        }

        return JsonResponse(result, safe=False)
