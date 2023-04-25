from django.shortcuts import render
from .models import Task
from .forms import TaskForm
import openai
import os

openai.api_key = "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"

def index(request):
       if request.method == 'POST':
           form = TaskForm(request.POST)
           if form.is_valid():
               title = form.cleaned_data['title']
               prompt = f"Draft a task description for a to-do list item with the title '{title}':"
               response = openai.Completion.create(
                   engine="text-davinci-002",
                   prompt=prompt,
                   max_tokens=50,
                   n=1,
                   stop=None,
                   temperature=0.7,
               )
               description = response.choices[0].text.strip()
               task = Task(title=title, description=description)
               task.save()
               form = TaskForm()
       else:
           form = TaskForm()

       tasks = Task.objects.all()
       return render(request, 'todo_app/index.html', {'form': form, 'tasks': tasks})
