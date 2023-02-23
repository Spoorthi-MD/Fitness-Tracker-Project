from django.shortcuts import render, redirect
from workout.forms import Exercise_add_Form
from workout.models import Exercise_add, Exercise_list
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login as loginUser, logout
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail, EmailMessage
from fitness_tracker import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags


# Create your views here.

@login_required(login_url='login')
def home(request):
    if request.user.is_authenticated:
        user = request.user
        form = Exercise_add_Form()
        exer = Exercise_add.objects.filter(user=user).order_by('id')

        return render(request, 'index.html', context={'form': form, 'exer': exer, })


def login(request):
    if request.method == 'GET':
        form1 = AuthenticationForm()
        context = {"form": form1}
        return render(request, 'login.html', context=context)
    else:
        form = AuthenticationForm(data=request.POST)
        print(form.is_valid())
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)

            if user is not None:
                loginUser(request, user)
                return redirect('home')
        else:
            context = {"form": form}
            return render(request, 'login.html', context=context)

def signup(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 == password2:
            if User.objects.filter(email=email).exists():   # user to check Exists details in data base to entered details by user
                messages.info(request, "Email Id Exists...!!! Try Another...")
                return redirect('signup')

            else:
                user = User.objects.create_user(username=username, email=email, password=password2)
                user.save()

                # Email Generation Block

                subject = 'Jaguar Fitness'
                content = f'Hiii {username} Thank you for registering Jaguar Fitness'
                email_from = settings.EMAIL_HOST_USER
                recipient_list = [email,]
                email = EmailMessage(
                                subject,
                                content,
                                email_from,
                                recipient_list,
                                    )

                email.send()

                messages.info(request, "User Successfully Created")
                return redirect('signup')

        else:
            messages.info(request, "Password Not Match...!!!")
            return redirect('signup')

    else:
        return render(request, 'signup.html')

@login_required(login_url='login')
def add_exercise(request):
    if request.user.is_authenticated:
        user = request.user
        print(user)
        form = Exercise_add_Form(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            exercise = form.save(commit=False)
            exercise.user = user
            exercise.save()
            print(exercise)
            return redirect("home")
        else:
            return render(request, 'index.html', context={'form': form, })


def delete_exercise(request, id):
    print(id)
    Exercise_add.objects.get(pk=id).delete()
    return redirect('home')


def change_exercise(request, id, status):
    exer = Exercise_add.objects.get(pk=id)
    exer.status = status
    exer.save()
    return redirect('home')

def signout(request):
    logout(request)
    return redirect('login')


#====================================================================================

# log in Block
def extend_index(request):
    if request.method == "POST":
        #email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']

        if username == 'admin' and password == 'admin1234':
            user = auth.authenticate(username=username,
                                     password=password)  # used Check the DB information and the entered data by the User

            if user is not None:  # if the deatails exists in db then returns Not None
                auth.login(request, user)
                # messages.info(request, "Successfully Logged In...")
                return redirect("admin-index")
            else:
                messages.info(request, "Sorry...!!! your not Admin")
                return redirect('extend-admin-index')
        else:
            messages.info(request, "Sorry...!!! your not Admin")
            return redirect('extend-admin-index')
    else:
        return render(request, 'extend-admin-index.html')



@login_required(login_url='extend_index')
def index(request):

    exr = Exercise_list.objects.all()
    paginator = Paginator(exr, 5)   #
    page_number = request.GET.get('page')   #
    exr = paginator.get_page(page_number)   #
    context = {'exr': exr, }
    return render(request, 'admin-index.html', context=context)

@login_required(login_url='extend_index')
def ADD(request):
    if request.method == 'POST':
        Id = request.POST.get('Id')
        exercise = request.POST.get('exercise')

        exr = Exercise_list(sl_no=Id, Exercise=exercise,)
        exr.save()
        return redirect('admin-index')
    return render(request, 'admin-index.html')


def Edit(request):

    exr = Exercise_list.objects.all()
    context = {'exr': exr, }
    return redirect(request, 'admin-index.html', context)


def Update(request, id):

    if request.method == 'POST':
        Id = request.POST.get('Id')
        exercise = request.POST.get('exercise')

        exr = Exercise_list(
            id=id,
            sl_no=Id,
            Exercise=exercise,
        )
        exr.save()
        return redirect('admin-index')
    return redirect(request, 'admin-index.html')


def Delete(request, id):

    exr = Exercise_list.objects.filter(id=id)
    exr.delete()
    # context = {'exr': exr, }

    return redirect('admin-index')


def email(request):
    exr = Exercise_add.objects.filter(user=request.user)
    email_from = settings.EMAIL_HOST_USER
    recipient_list = request.user.email
    html_content = render_to_string('email.html', {'username': request.user.username, 'exr': exr, })
    c_text = strip_tags(html_content)
    send1 = EmailMultiAlternatives(
        "Exercise List",
        c_text,
        email_from,
        [recipient_list, ],
    )
    send1.attach_alternative(html_content, 'text/html')
    send1.send()
    return redirect('/')









