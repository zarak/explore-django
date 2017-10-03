from django.http import HttpResponse
from .models import Question

# How do I import Question here
def index(request):
    question_list = Question.objects.all()
    first_question = question_list[0]
    output = f'{first_question.id} {first_question.question_text} {first_question.pub_date}'
    return HttpResponse(output)
