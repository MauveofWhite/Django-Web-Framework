from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, Http404, HttpResponseRedirect
from .models import Question, Choice
from django.template import loader
from django.urls import reverse
from django.utils import timezone

from django.shortcuts import render, get_object_or_404

# import generic views
from django.views import generic

""" A URLconf maps URL patterns to views. """

"""
Respectively, ListView and DetailView abstract the concepts of “display a list of objects” and
“display a detail page for a particular type of object.”

Each generic view needs to know what model it will be acting upon. This is provided using the model attribute.

The DetailView generic view expects the primary key value captured from the URL to be called "pk",
so we’ve changed question_id to pk for the generic views.
"""

# def index(request):
#     latest_question_list = Question.objects.order_by('-pub_date')[:5]
#     template = loader.get_template("polls/index.html")
#     context = {
#         "latest_question_list" : latest_question_list,
#     }
#     return HttpResponse(template.render(context, request))

# Shortcut for template render
# If we only use this shortcut, we don't need to import loader and HttpResponse.
# def index(request):
    # latest_question_list = Question.objects.order_by('-pub_date')[:5]
    # context = {"latest_question_list" : latest_question_list,}
    # return render(request, "polls/index.html", context)

    # Change above to generic views:

"""
For DetailView the question variable is provided automatically – since we’re using a Django model (Question),
Django is able to determine an appropriate name for the context variable. However, for ListView,
the automatically generated context variable is !question_list! (since it's list view). To override this we
provide the context_object_name attribute, specifying that we want to use latest_question_list instead.
"""

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        # """Return the last five published questions.
        # This will also return questions that will be published in the future, which needs to be fixed."""
        # return Question.objects.order_by('-pub_date')[:5]

        # Fixed:

        """
        Return the last five published questions (not including those set to be
        published in the future).

        ** Additional Feature: hides questions with no choices. Can be turned off.

        Question.objects.filter(pub_date__lte=timezone.now()) returns a queryset
        containing Questions whose pub_date is less than or equal to - that is, earlier than or equal to - timezone.now.
        """

        exclude_no_choice = False

        if exclude_no_choice:
            return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date').exclude(choice=None)[:5]
        else:
            return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]

# def detail(request, question_id):
    # try:
    #     question = Question.objects.get(pk=question_id)
    # except:
    #     raise Http404("Question does not exist.")
    # # Can be replaced to: get_object_or_404(object, query). See following code:
    # question = get_object_or_404(Question, pk=question_id)
    # return render(request, "polls/detail.html", {"question":question})

    # Change above to generic views:

class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet. Otherwise, user can access future questions
        by guessing the url right.

        Now, by entering questions by url, the web will display 404.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())

"""
By default, the DetailView generic view uses a template called <app name>/<model name>_detail.html.
In our case, it would be "polls/question_detail.html".
The 'template_name' attribute tells Django to use a specific template name instead of the
autogenerated default template name.

We also specify the template_name for the results list view – this ensures that
the results view and the detail view have a !different appearance when rendered!, even though
they’re both a DetailView behind the scenes.
"""

# def results(request, question_id):
    # question = get_object_or_404(Question, pk=question_id)
    # return render(request, 'polls/results.html', {'question': question})

    # Change above to generic views:

class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        # request.POST is a dictionary-like object that lets you access submitted data by key name.
        # In this case, request.POST['choice'] returns the ID of the selected choice, as a string.
        # request.POST values are always strings.
        # Note that Django also provides request.GET for accessing GET data in the same way – but
        # we’re explicitly using request.POST in our code, to ensure that data is only altered via a POST call.
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        # It's for user who does not pick any choice and hit vote button directly.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        # server-data modification
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.

        # This function helps avoid having to hardcode a URL in the view function.
        # It is given the name of the view that we want to pass control to and the variable
        # portion of the URL pattern that points to that view. In this case, using the URLconf
        # we set up in Tutorial 3, this reverse() call will return a string like:
        # '/polls/3/results/'
        # where the 3 is the value of question.id. This redirected URL will then call
        # the 'results' view to display the final page.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
