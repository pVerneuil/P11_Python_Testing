from email import message
import json
from pathlib import Path
import datetime

from flask import Flask,render_template,request,redirect,flash,url_for

current_path = Path(__file__).absolute().parent
PATH_CLUBS = current_path / "data/clubs.json"
PATH_COMPETITIONS = current_path / "data/competitions.json"

def loadClubs():
    with open(PATH_CLUBS) as c:
        listOfClubs = json.load(c)['clubs']
        return listOfClubs


def loadCompetitions():
    with open(PATH_COMPETITIONS) as comps:
        listOfCompetitions = json.load(comps)['competitions']
        date_format = "%Y-%m-%d %H:%M:%S"
        for competition in listOfCompetitions:
            competition['date'] = datetime.datetime.strptime(competition["date"], date_format)
            if competition['date'] < datetime.datetime.now():
                competition['is_over'] = True
            else:
                competition['is_over'] = False
        return listOfCompetitions


app = Flask(__name__)
app.secret_key = 'something_special'

competitions = loadCompetitions()
clubs = loadClubs()
"""
track how many places are already reserved by clubs in each competition.
reserved_place ={'competition1_name': {
                        'club1_name': place booked,
                        'club2_name': place booked, ...
                                    },
                'competition2_name': {
                        'club1_name': place booked,
                        'club2_name': place booked, ...
                                    }, ...
                }
"""
reserved_places = {competition['name']:{club['name']:0 for club in clubs} for competition in competitions }


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/showSummary',methods=['POST'])
def showSummary():
    try :
        club = [club for club in clubs if club['email'] == request.form['email']][0]
        return render_template('welcome.html',club=club,competitions=competitions)
    except IndexError:
        return render_template('index.html', message="Email does not match any accounts"), 400
    except:
        return render_template('index.html', message="Something went wrong..."), 400


@app.route('/book/<competition>/<club>')
def book(competition,club):
    foundClub = [c for c in clubs if c['name'] == club][0]
    foundCompetition = [c for c in competitions if c['name'] == competition][0]
    if foundCompetition['is_over']:
        message = 'This competition already took place. '
        return render_template('booking.html',club=foundClub,competition=foundCompetition, message=message, is_over=True),400
    elif foundClub and foundCompetition:
        return render_template('booking.html',club=foundClub,competition=foundCompetition, is_over=False)
    else:
        flash("Something went wrong-please try again")
        return render_template('welcome.html', club=club, competitions=competitions),400


@app.route('/purchasePlaces',methods=['POST'])
def purchasePlaces():
    competition = [c for c in competitions if c['name'] == request.form['competition']][0]
    club = [c for c in clubs if c['name'] == request.form['club']][0]
    placesRequired = int(request.form['places'])
    if competition['is_over']: 
        flash('This competition already took place. You can not book place for it. ')
        return render_template('welcome.html', club=club, competitions=competitions),400
    else:
        if placesRequired<=12 and placesRequired+reserved_places[competition['name']][club['name']]<= 12 :
            
            if int(club['points'])<placesRequired:
                message = f"You do not have enough points to perfom this action ( you have {club['points']} point(s))"
                return render_template('booking.html',club=club,competition=competition, message=message), 400
            else :
                competition['numberOfPlaces'] = int(competition['numberOfPlaces'])-placesRequired
                club['points'] = int(club['points'])-placesRequired
                reserved_places[competition['name']][club['name']] += placesRequired
                flash('Great-booking complete!')
                return render_template('welcome.html', club=club, competitions=competitions)
            
        else : 
            message ='You can not book more than 12 places per competition' 
            return render_template('booking.html',club=club,competition=competition, message=message), 400


@app.route('/pointsBoard', methods=['GET'])
def pointsBoard():
        return render_template('board_points.html', clubs=clubs)


@app.route('/logout')
def logout():
    return redirect(url_for('index'))