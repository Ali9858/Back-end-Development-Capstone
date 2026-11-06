from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from concert.forms import LoginForm, SignUpForm
from concert.models import Concert, ConcertAttending


def index(request):
    return render(request, "index.html")


# Registration
def signup(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = User.objects.filter(username=username).first()

        if user:
            return render(
                request,
                "signup.html",
                {
                    "form": SignUpForm,
                    "message": "User already exists"
                }
            )

        user = User.objects.create(
            username=username,
            password=make_password(password)
        )

        login(request, user)
        return HttpResponseRedirect(reverse("index"))

    return render(request, "signup.html", {"form": SignUpForm})


# Songs
def songs(request):
    songs = {
        "songs": [
            {
                "id": 1,
                "title": "duis faucibus accumsan odio curabitur convallis",
                "lyrics": "Morbi non lectus. Aliquam sit amet diam in magna bibendum imperdiet. Nullam orci pede, venenatis non, sodales sed, tincidunt eu, felis."
            }
        ]
    }

    return render(
        request,
        "songs.html",
        {"songs": songs["songs"]}
    )


def photos(request):
    photos = [
        {
            "id": 1,
            "pic_url": "http://dummyimage.com/136x100.png/5fa2dd/ffffff",
            "event_country": "United States",
            "event_state": "District of Columbia",
            "event_city": "Washington",
            "event_date": "11/16/2022"
        }
    ]

    return render(
        request,
        "photos.html",
        {"photos": photos}
    )


# Login
def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        try:
            user = User.objects.get(username=username)

            if user.check_password(password):
                login(request, user)
                return HttpResponseRedirect(reverse("index"))

        except User.DoesNotExist:
            pass

        return render(
            request,
            "login.html",
            {
                "form": LoginForm,
                "message": "Invalid username or password"
            }
        )

    return render(request, "login.html", {"form": LoginForm})


# Logout
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("login"))


# Concerts
def concerts(request):
    if request.user.is_authenticated:
        lst_of_concert = []

        concert_objects = Concert.objects.all()

        for item in concert_objects:
            attendee = item.attendee.filter(
                user=request.user
            ).first()

            status = attendee.attending if attendee else "-"

            lst_of_concert.append({
                "concert": item,
                "status": status
            })

        return render(
            request,
            "concerts.html",
            {"concerts": lst_of_concert}
        )

    return HttpResponseRedirect(reverse("login"))


# Concert details
def concert_detail(request, id):
    if request.user.is_authenticated:
        obj = get_object_or_404(Concert, pk=id)

        attendee = obj.attendee.filter(
            user=request.user
        ).first()

        status = attendee.attending if attendee else "-"

        return render(
            request,
            "concert_detail.html",
            {
                "concert_details": obj,
                "status": status,
                "attending_choices":
                    ConcertAttending.AttendingChoices.choices
            }
        )

    return HttpResponseRedirect(reverse("login"))


# Update concert attendance
def concert_attendee(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            concert_id = request.POST.get("concert_id")
            attendee_status = request.POST.get("attendee_choice")

            concert_attendee_object = ConcertAttending.objects.filter(
                concert_id=concert_id,
                user=request.user
            ).first()

            if concert_attendee_object:
                concert_attendee_object.attending = attendee_status
                concert_attendee_object.save()
            else:
                ConcertAttending.objects.create(
                    concert_id=concert_id,
                    user=request.user,
                    attending=attendee_status
                )

        return HttpResponseRedirect(reverse("concerts"))

    return HttpResponseRedirect(reverse("login"))
