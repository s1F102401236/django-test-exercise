from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
from django.utils.timezone import make_aware
from django.utils.dateparse import parse_datetime
from todo.models import Task
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django import forms
from .models import Post, Comment
from .models import Task

# Create your views here.


def index(request):
    if request.method == 'POST':
        title = request.POST['title']
        due_at_raw = request.POST.get('due_at')
        parsed_due_at = parse_datetime(due_at_raw) if due_at_raw else None

        if parsed_due_at is not None:
            # tzinfoがない場合だけmake_awareを呼ぶ
            due_at = make_aware(parsed_due_at) if parsed_due_at.tzinfo is None else parsed_due_at
        else:
            due_at = None

        task = Task(title=title, due_at=due_at)

        # 画像があればセット
        if 'image' in request.FILES:
            task.image = request.FILES['image']

        task.save()
        return redirect('todo:index')

    # GET処理
    if request.GET.get('order') == 'due':
        tasks = Task.objects.order_by('due_at')
    else:
        tasks = Task.objects.order_by('-posted_at')

    context = {
        'tasks': tasks
    }
    return render(request, 'todo/index.html', context)

def detail(request, task_id):
    try:
        task = Task.objects.get(pk=task_id)
    except Task.DoesNotExist:
        raise Http404("Task does not exist")

    context = {
        'task': task,
    }
    return render(request, 'todo/detail.html', context)


def delete(request, task_id):
    try:
        task=Task.objects.get(pk=task_id)
    except Task.DoesNotExist:
        raise Http404('Task does not exist')
    task.delete()
    return redirect(index)
    
 
def update(request,task_id):
    try:
        task=Task.objects.get(pk=task_id)
    except Task.DoesNotExist:
        raise Http404('Task does not exist')
    if request.method=='POST':
        task.title=request.POST['title']
        task.due_at=make_aware(parse_datetime(request.POST['due_at']))
        task.save()
        return redirect(detail,task_id)

    context={
        'task':task
    }
    return render(request,'todo/edit.html',context)

# コメントフォームをここで定義
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']

# 記事詳細とコメント投稿処理
@login_required
def task_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = post.comments.all()

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('task_detail', post_id=post.id)
    else:
        form = CommentForm()

    return render(request, 'blog/task_detail.html', {
        'post': post,
        'comments': comments,
        'form': form
    })


def close(request, task_id):
    try:
        task = Task.objects.get(pk=task_id)
    except Task.DoesNotExist:
        raise Http404("Task does not exist")
    task.completed = True
    task.save()
    return redirect('todo:index')

def add_like(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    task.likes_count += 1
    task.save()
    return redirect('todo:task_detail', pk=task.id)
