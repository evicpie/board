from django.shortcuts import render, redirect, HttpResponse
from .forms import RegisterForm
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password
from django.contrib.auth import get_user_model
from django.contrib import auth
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.core.mail import EmailMessage
from .tokens import account_activation_token
from django.utils.encoding import force_bytes, force_text

def register(request):

    if request.method == 'POST':
        user_form = RegisterForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.is_active = False
            new_user.save()
            current_site = get_current_site(request)
            # localhost:8000
            message = render_to_string('registration/user_active_email.html',                         {
                'user': new_user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(new_user.pk)).encode().decode(),
                'token': account_activation_token.make_token(new_user),
            })
            mail_subject = "[SOT] 회원가입 인증 메일입니다."
            user_email = new_user.email
            email = EmailMessage(mail_subject, message, to=[user_email])
            email.send()
            return HttpResponse(
                """
                <div style="font-size: 40px; width: 100%; height:100%; display:flex; text-align:center;
                justify-content: center; align-items: center;">
                입력하신 이메일<span>로 인증 링크가 전송되었습니다.</span>
                <a href="http://127.0.0.1:8000/">메인으로</a>
                </div>
                """
            )
            return render(request, 'registration/register_done.html', {'new_user':new_user})
    else:
        user_form = RegisterForm()

    return render(request, 'registration/register.html',{'form':user_form})

def activate(request, uid64, token):

    uid = force_text(urlsafe_base64_decode(uid64))
    user = User.objects.get(pk=uid)

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        auth.login(request, user)
        context = {'uid64':uid64, 'token':token}
        return render(request, 'registration/register_done.html', context)
    else:
        return HttpResponse('비정상적인 접근입니다.')
