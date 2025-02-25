from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Conversation, Message
from .forms import MessageForm
from accounts.models import CustomUser  # Assuming 'core' is your user model app


@login_required
def conversation_list(request):
    conversations = Conversation.objects.filter(user=request.user) | Conversation.objects.filter(botanist=request.user)

    if not conversations.exists():  # If there are no conversations
        botanists = CustomUser.objects.filter(role="botanist").exclude(id=request.user.id)
    else:
        botanists = None  # No need to show botanists if there are conversations

    return render(request, "messaging/conversation_list.html", {"conversations": conversations, "botanists": botanists})


@login_required
def conversation_detail(request, conversation_id):
    conversation = get_object_or_404(Conversation, id=conversation_id)
    messages = conversation.messages.all()
    form = MessageForm()
    return render(request, "messaging/conversation_detail.html", {"conversation": conversation, "messages": messages, "form": form})

@login_required
def send_message(request, conversation_id):
    conversation = get_object_or_404(Conversation, id=conversation_id)

    if request.method == "POST":
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.conversation = conversation
            message.save()
            return redirect("messaging:conversation_detail", conversation_id=conversation.id)
    
    return redirect("messaging:conversation_detail", conversation_id=conversation.id)
