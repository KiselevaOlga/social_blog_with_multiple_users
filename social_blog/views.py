from django.views.generic import TemplateView


class HomePage(TemplateView):
    template_name = 'home_page.html'


class TestPage(TemplateView):
    template_name = 'test.html'


class ThanksPage(TemplateView):
    template_name = 'thanks.html'
