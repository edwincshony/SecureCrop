from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Conversation, Message
from .forms import MessageForm
from accounts.models import CustomUser
from notifications.models import Notification
from django.urls import reverse
from django.contrib import messages

@login_required
def conversation_list(request):
    # Fetch all users except the current user
    users = CustomUser.objects.exclude(id=request.user.id).order_by('username')
    
    # Filter users based on role selection
    selected_role = request.GET.get('role', 'all')
    if selected_role != 'all':
        users = users.filter(role=selected_role)

    # Fetch all conversations the user is part of
    conversations = Conversation.objects.filter(participants=request.user)

    context = {
        'conversations': conversations,
        'users': users,
        'selected_role': selected_role,
    }
    return render(request, "messaging/conversation_list.html", context)

@login_required
def start_conversation(request, user_id):
    target_user = get_object_or_404(CustomUser, id=user_id)
    current_user = request.user

    if current_user == target_user:
        messages.error(request, "You cannot start a conversation with yourself.")
        return redirect('messaging:conversation_list')

    # Try to get an existing conversation between the two users
    conversation = Conversation.objects.filter(participants=current_user).filter(participants=target_user).first()
    
    # Create a new conversation if none exists
    if not conversation:
        conversation = Conversation.objects.create()
        conversation.participants.add(current_user, target_user)

    return redirect('messaging:conversation_detail', conversation_id=conversation.id)


@login_required
def conversation_detail(request, conversation_id):
    conversation = get_object_or_404(Conversation, id=conversation_id)

    # Ensure only participants can view the conversation
    if request.user not in conversation.participants.all():
        messages.error(request, "You don’t have permission to view this conversation.")
        return redirect('messaging:conversation_list')

    messages_list = conversation.messages.all()
    print("Messages in this conversation:", messages_list)  # Debug print

    form = MessageForm()

    # Mark messages as read for all messages not sent by the current user
    conversation.messages.filter(~Q(sender=request.user), is_read=False).update(is_read=True)

    context = {
        "conversation": conversation,
        "messages": messages_list,
        "form": form,
    }
    return render(request, "messaging/conversation_detail.html", context)


@login_required
def send_message(request, conversation_id):
    conversation = get_object_or_404(Conversation, id=conversation_id)

    # Check if the user is part of the conversation
    if request.user not in conversation.participants.all():
        messages.error(request, "You are not part of this conversation.")
        return redirect("messaging:conversation_list")

    if request.method == "POST":
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.conversation = conversation
            message.save()  # 🔥 Saves message to DB
            
            # Debugging
            print(f"✅ Message saved: {message.text} from {message.sender.username}")

            return redirect("messaging:conversation_detail", conversation_id=conversation.id)
        else:
            print("❌ Form errors:", form.errors)  # Debugging
            messages.error(request, "Message sending failed.")
    
    return redirect("messaging:conversation_detail", conversation_id=conversation.id)





