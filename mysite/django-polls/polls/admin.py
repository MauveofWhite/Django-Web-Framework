from django.contrib import admin

# Register your models here.
from .models import Question, Choice

# Now it will show Polls app in the admin web.
# Django knows that a ForeignKey should be represented in the admin as a <select> box.
# So in each choice, there will be a select box for choosing questions to create a choice.

# Adding choices one-by-one is an inefficient way of adding Choice objects to the system.
# It’d be better if you could add a bunch of Choices directly when you create the Question object.
# StackedInline - each choice text and vote take one line.
# TabularInline - one choice (text and vote) take one line. (more compressed)
class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3
# This tells Django: “Choice objects are edited on the Question admin page. By default, provide enough fields for 3 choices.”
# For questions that already have choices, provide *additional* 3 fields for choices.

class QuestionAdmin(admin.ModelAdmin):
    # This particular change above makes the “Publication date” come before the “Question” field
    # fields = ['pub_date', 'question_text']

    # The first element of each tuple in fieldsets is the title of the fieldset.
    fieldsets = [
        (None,               {'fields': ['question_text']}),
        ('Date information', {'fields': ['pub_date']}),
    ]
    inlines = [ChoiceInline]

    # This line displays pub_date and was_published_recently on http://127.0.0.1:8000/admin/polls/question/
    list_display = ('question_text', 'pub_date', 'was_published_recently')

    # This line adds a filter based on the pub_date, including: Any date, Today, Past 7 days, This month, This year
    list_filter = ['pub_date']

    # This line adds the searching ability
    search_fields = ['question_text']

admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)
