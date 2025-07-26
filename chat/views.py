# chat/views.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import get_user_model
from .models import Group, PrivateMessage, GroupMessage

User = get_user_model()

# ---------- GROUP ----------


@login_required
def group_list(request):
    groups = Group.objects.all()
    return render(request, 'chat/group_list.html', {'groups': groups})


@login_required
def group_chat(request, group_name):
    group = get_object_or_404(Group, name=group_name)
    messages = group.messages.select_related('author').order_by('sent_at')
    return render(request, 'chat/group_ws.html', {'group': group, 'msgs': messages})

# ---------- PRIVATE ----------


@login_required
def private_chat(request, username):
    other = get_object_or_404(User, username=username)
    messages = (PrivateMessage.objects
                .filter(sender__in=[request.user, other],
                        receiver__in=[request.user, other])
                .select_related('sender', 'receiver')
                .order_by('sent_at'))
    return render(request, 'chat/private_ws.html',
                  {'other': other, 'msgs': messages})
