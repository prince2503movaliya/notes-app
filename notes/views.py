from urllib import request

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

import notes
from .models import Note
from django.db.models import Q
from django.core.paginator import Paginator
from django.views.decorators.http import require_POST
from django.contrib import messages

@login_required
def note_list(request):
    query = request.GET.get('q')
    sort = request.GET.get('sort')
    start_date = request.GET.get('start')
    end_date = request.GET.get('end')
    
    notes = Note.objects.filter(user=request.user, is_deleted=False)


    # 🔍 Search in title + content
    if query:
        notes = notes.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query)
        )
    
    # 📅 Date range filter
    if start_date:
        notes = notes.filter(created_at__date__gte=start_date)

    if end_date:
        notes = notes.filter(created_at__date__lte=end_date)

    # 🔃 Sorting
    if sort == 'new':
        notes = notes.order_by('-created_at')
    elif sort == 'old':
        notes = notes.order_by('created_at')

    pinned_notes = notes.filter(is_pinned=True).order_by('-created_at')
    other_notes = notes.filter(is_pinned=False).order_by('-created_at')

    paginator = Paginator(notes, 6)  
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'notes/list.html', {
         'pinned_notes': pinned_notes,
         'page_obj': page_obj
    })

@login_required
def note_detail(request, id):
    note = get_object_or_404(
        Note,
        id=id,
        user=request.user,
        is_deleted=False
    )
    return render(request, 'notes/detail.html', {'note': note})


@login_required
def note_create(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        image = request.FILES.get('image')
        file = request.FILES.get('file')

        Note.objects.create(
            user=request.user,
            title=title,
            content=content,
            image=image,
            file=file
        )

        messages.success(request, "Note created successfully")
        return redirect('note_list')

    return render(request, "notes/form.html", {
        "form_type": "Create",  
    })


@login_required
def note_update(request, id):
    note = get_object_or_404(
        Note,
        id=id,
        user=request.user,
        is_deleted=False
    )

    if request.method == 'POST':
        note.title = request.POST.get('title')
        note.content = request.POST.get('content')

        if request.FILES.get('image'):
            note.image = request.FILES.get('image')

        if request.FILES.get('file'):
             note.file = request.FILES.get('file')
             
        note.save()
        messages.success(request, "Note updated successfully", extra_tags="primary")
        return redirect('note_list')

    return render(request, "notes/form.html", {
        'note': note,
        "form_type": "Edit",   
    })


@login_required
def note_delete(request, id):
    note = get_object_or_404(Note, id=id, user=request.user)

    if request.method == 'POST':
        note.delete()
        messages.error(request, "Note deleted successfully")
        return redirect('note_list')

    return render(request, 'notes/delete.html', {'note': note})

@require_POST
def toggle_pin(request, id):
    note = get_object_or_404(Note, id=id, user=request.user)

    # 🔒 Check limit
    if not note.is_pinned:
        pinned_count = Note.objects.filter(user=request.user, is_pinned=True).count()

        if pinned_count >= 3:
            messages.error(request, "You can only pin up to 3 notes.")
            return redirect('note_list')

    # 🔁 Toggle
    note.is_pinned = not note.is_pinned
    note.save()

    if note.is_pinned:
        messages.warning(request, "Note pinned")
    else:
        messages.warning(request, "Note unpinned")

    return redirect('note_list')