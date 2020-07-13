from django.urls import path

from . import views

app_name = 'polls'
# urlpatterns = [
    # ex: /polls/
#     path('', views.index, name='index'),
    # ex: /polls/5/
    # the 'name' value as called by the {% url %} template tag
    # if we add specifics/, url becomes: http://127.0.0.1:8000/polls/specifics/1/ because {% url %} only look at 'name' arg
#     path('<int:question_id>/', views.detail, name='detail'),
    # ex: /polls/5/results/
#     path('<int:question_id>/results/', views.results, name='results'),
    # ex: /polls/5/vote/
#     path('<int:question_id>/vote/', views.vote, name='vote'),
# ]

"""
When somebody requests a page from your website – say, “/polls/34/”,
Django will load the mysite.urls Python module.
It finds the variable named urlpatterns and traverses the patterns in order.

After finding the match at 'polls/', it strips off the matching text ("polls/")
and sends the remaining text – "34/" – to the ‘polls.urls’ URLconf for further processing.

There it matches '<int:question_id>/', resulting in a call to the detail() view like so:
    detail(request=<HttpRequest object>, question_id=34)
"""

# Use Generic views               |

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    # changed from <int:quesiton_id> to <int:pk>
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote'), # did not change
]
