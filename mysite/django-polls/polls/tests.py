from django.test import TestCase

import datetime
from django.utils import timezone
from django.urls import reverse

from polls.models import Question, Choice


"""
To run the test, put python manage.py test <testing python file's name> in the terminal.
eg. python manage.py test polls

"""


# Create your tests here.

"""
Testing function: was_published_recently in polls/models.py

    # Old logic: if the quesiton was published within the last day, it's published recently.
    # However, it will also be true when asking a question that will be posted in the future,
    # which is false (the question hasn't been posted yet).
    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

>>> import datetime
>>> from django.utils import timezone
>>> from polls.models import Question

>>> # create a Question instance with pub_date 30 days in the future
>>> future_question = Question(pub_date=timezone.now() + datetime.timedelta(days=30))

>>> # was it published recently?
>>> future_question.was_published_recently()
True

Which should be false

"""

class QuestionModelTests(TestCase):

    """
    What this testcase does is:
        1. manage.py test polls looked for tests in the polls application.
        2. It found a !subclass! of the django.test.TestCase class.
        3. It created a special database for the purpose of testing.
        4. It looked for test methods - !ones whose names begin with test!.
        5. In test_was_published_recently_with_future_question it created a Question instance
        whose pub_date field is 30 days in the future and using the assertIs() method,
        it discovered that its was_published_recently() returns True, though we wanted it to return False.
    """

    def test_was_published_recently_with_future_question(self):
        """
        was_published_recently() returns False for questions whose pub_date
        is in the future.
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)

        # Assert future question will return false, otherwise, there is a bug
        self.assertIs(future_question.was_published_recently(), False)

    # Some other tests
    def test_was_published_recently_with_old_question(self):
        """
        was_published_recently() returns False for questions whose pub_date
        is older than 1 day.
        """
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """
        was_published_recently() returns True for questions whose pub_date
        is within the last day.
        """
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)

"""
    Testing if index shows past and future question correctly.

"""


def create_question(question_text, days):
    """
    Create a question with the given `question_text` and published the
    given number of `days` offset to now (negative for questions published
    in the past, positive for questions that have yet to be published).
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)


class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        """
        If no questions exist, an appropriate message is displayed.
        """
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_past_question(self):
        """
        Questions with a pub_date in the past are displayed on the
        index page.
        """
        create_question(question_text="Past question.", days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question.>']
        )

    def test_future_question(self):
        """
        Questions with a pub_date in the future aren't displayed on
        the index page.
        """
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_future_question_and_past_question(self):
        """
        Even if both past and future questions exist, only past questions
        are displayed.
        """
        create_question(question_text="Past question.", days=-30)
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question.>']
        )

    def test_two_past_questions(self):
        """
        The questions index page may display multiple questions.
        """
        create_question(question_text="Past question 1.", days=-30)
        create_question(question_text="Past question 2.", days=-5)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question 2.>', '<Question: Past question 1.>']
        )

    def test_with_choices_question(self):
        q = create_question(question_text="Question with choices", days=-5)
        q.choice_set.create(choice_text='Choice 1', votes=0)
        q.choice_set.create(choice_text='Choice 2', votes=0)
        response = self.client.get(reverse('polls:index'))

        self.assertEqual(q.choice_set.count(), 2)
        self.assertQuerysetEqual(response.context['latest_question_list'],
        ['<Question: Question with choices>'])


    # # Test when exclude_no_choice = True
    # def test_without_choices_question(self):
    #     create_question(question_text="Question without choices", days=-5)
    #     response = self.client.get(reverse('polls:index'))
    #     self.assertQuerysetEqual(response.context['latest_question_list'], [])

"""
    Testing details can't be accessed by entering url directly.
"""

class QuestionDetailViewTests(TestCase):
    def test_future_question(self):
        """
        The detail view of a question with a pub_date in the future
        returns a 404 not found.
        """
        future_question = create_question(question_text='Future question.', days=5)
        url = reverse('polls:detail', args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        """
        The detail view of a question with a pub_date in the past
        displays the question's text.
        """
        past_question = create_question(question_text='Past Question.', days=-5)
        url = reverse('polls:detail', args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)
