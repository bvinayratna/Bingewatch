from ssl import ALERT_DESCRIPTION_ACCESS_DENIED
from django.shortcuts import redirect, render
from pyparsing import srange
from .models import liked_songs, search_history, user, videos_watched
from sqlalchemy import create_engine
import requests
import pymysql
import pandas as pd
from django.conf import settings
from isodate import parse_duration
import requests
import pymsgbox
from django.conf import settings
from django.core.mail import send_mail


# Create your views here.
main_username = ""
def layout(request):
    return render(request, "app/layout.html")

def home(request):
    try:
        if request.session['username']:
            return render(request, "app/home.html")
    except:
        return redirect('login')

def login(request):
    if request.method=='POST':
        if request.POST.get('username') and request.POST.get('password'):
            
            try:
                User = user.objects.get(username=request.POST.get('username'))

            except:
                User=None
                User = user.objects.filter(username=request.POST.get('username'))
            if User:
                if User.password==request.POST.get('password'):
                    request.session['username']=User.username
                    return redirect('homepage')
                else: 
                    return redirect('login')
            else: 
                    return redirect('signup')
        else:
            return render(request, "app/login.html")
    else:
        return render(request, "app/login.html")

def signup(request):
    if request.method=='POST':
        if request.POST.get('username') and request.POST.get('password') and request.POST.get('fullname') and request.POST.get('email'):
            User=user()
            User.username=request.POST.get('username')
            User.password=request.POST.get('password')
            User.fullname=request.POST.get('fullname')
            User.email=request.POST.get('email')
            User.save()
            request.session['username']=User.username
            subject = 'Welcome to BINGEWATCH'
            message = f"<h1>Thanks for joining BINGEWATCH</h1><br/>Hi {User.username}, You're ready to start enjoying your favourite content in here.<br/><a to='http://127.0.0.1:8000/home/'>Start watching</a><br/><h3>Your Account Information: <br/>Email: {User.email}<br/>Distributor: BINGEWATCH<br/>We're here to help if you need it.<br/><strong>The BINGEWATCH team</strong></h3>"
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [User.email, ]
            send_mail( subject, message, email_from, recipient_list )
            return redirect('homepage')
    else:
         return render(request, "app/signup.html")

def logout(request):
    try:
        del request.session['username']
    except KeyError:
        pass
    return redirect('/')

def exportcsv(request):
    sqlEngine = create_engine('mysql+pymysql://ets:ets%40sdp2@127.0.0.1/ets', pool_recycle=3600)
    dbConnection = sqlEngine.connect()
    frame = pd.read_sql("select id, fullname, username, email from ets.app_user", dbConnection)
    print(frame)
    frame.to_csv('out.csv', index=False)
    dbConnection.close()
    return redirect('homepage')

def watch(request): 
    if request.session['username']:
        videos = []
        if request.method=='POST':
            search_url = 'https://www.googleapis.com/youtube/v3/search'
            video_url = 'https://www.googleapis.com/youtube/v3/videos'

            search_params = {
                'part': 'snippet',
                'q': request.POST['search'],
                'key': settings.YOUTUBE_DATA_API_KEY,
                'maxResults': 10,
                'type': 'video'
            }
            r = requests.get(search_url, params=search_params)
            if request.POST['search']:
                Search_history = search_history()
                Search_history.username = request.session['username']
                Search_history.search_query = search_params['q']
                Search_history.save()
            results = r.json()['items']
            print(results)
            video_ids = []
            for result in results:
                video_ids.append(result['id']['videoId'])
            
            if request.POST.get('submit')=='lucky':
                return redirect(f'https://www.youtube.com/watch?v={ video_ids[0] }')
            
            video_params = {
                'key': settings.YOUTUBE_DATA_API_KEY,
                'part': 'snippet, contentDetails',
                'id': ','.join(video_ids),
                'maxResults': 10
            }
            r = requests.get(video_url, params=video_params)
            results = r.json()['items']

            
            for result in results:
                video_data={
                    'title': result['snippet']['title'],
                    'id': result['id'],
                    'duration': parse_duration(result['contentDetails']['duration']),
                    'url': f'https://www.youtube.com/watch?v={ result["id"] }',
                    'thumbnail': result['snippet']['thumbnails']['high']['url'],
                }
                videos.append(video_data)
        context = {
            'videos': videos,
        }
        return render(request, "app/watch.html", context)
    '''except:
        return redirect('login')'''

def listen(request):
    try:
        if request.session['username']:

            track_ids=[]
            tracks=[]

            if request.method=='POST':


                url = "https://spotify23.p.rapidapi.com/search/"

                querystring = {"q": request.POST['search'],
                "type":"tracks",
                "offset":"0",
                "limit":"10",
                "numberOfTopResults":"10"}

                headers = {
                    "X-RapidAPI-Host": "spotify23.p.rapidapi.com",
                    "X-RapidAPI-Key": "496a72d3e7msh8ba8211fb1028c7p10e26ejsn8bad8a5d21b8",
                    #"X-RapidAPI-Key": "c23d11f8c0msh3027f0b2773f8d7p12e000jsn24118f54b6ed"
                }

                response = requests.request("GET", url, headers=headers, params=querystring)

                results = response.json()['tracks']['items']

                for result in results:
                    track_ids.append(result['data']['id'])

                for result in results:
                    track_data={
                        'title': result['data']['name'],
                        'track_id': result['data']['id'],
                        'album': result['data']['albumOfTrack']['name'],
                        'album_id': result['data']['albumOfTrack']['id'],
                        'thumbnail': result['data']['albumOfTrack']['coverArt']['sources'][0],
                        'artist': result['data']['artists']['items'][0]['profile']['name']
                    }
                    tracks.append(track_data)
            context={
                'tracks': tracks,
            }

            return render(request, "app/listen.html", context)
    except:
        redirect('login')

def play(request):
    try:
        if request.session['username']:
            return render(request, "app/play.html")
    except:
        redirect('login')