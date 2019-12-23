#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#
import os
import sys
import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for, abort, jsonify
from flask_migrate import Migrate
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from datetime import datetime
from sqlalchemy import func
from forms import *
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#
print(os.environ['APP_SETTINGS'])
app = Flask(__name__)
moment = Moment(app)
app.config.from_object(os.environ['APP_SETTINGS'])
db = SQLAlchemy(app)
app.config['SQL_ALCHEMY_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI', 'postgres://amirtahmasbi@localhost:5432/fuyyerapp')

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#


class Venue(db.Model):
    __tablename__ = 'venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120), nullable=False)
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    genres = db.Column(db.String(), nullable=False)
    website = db.Column(db.String(120), nullable=True)
    seeking_talent = db.Column(db.Boolean, nullable=True)
    seeking_description = db.Column(db.String(500), nullable=True)
    shows = db.relationship('Show', backref='list', lazy=True)

class Show(db.Model):
    __tablename__ = 'show'
    id = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.TIMESTAMP, nullable=False)
    venue_id = db.Column(db.Integer, db.ForeignKey('venue.id', ondelete="CASCADE"), nullable=False)
    artist_id = db.Column(db.Integer, db.ForeignKey('artist.id', ondelete="CASCADE"), nullable=False)
    venue = db.relationship("Venue", backref="venue")
    artist = db.relationship("Artist", backref="artsit")

class Artist(db.Model):
    __tablename__ = 'artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120), nullable=False)
    genres = db.Column(db.String(120), nullable=False)
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    seeking_venue = db.Column(db.Boolean, nullable=True)
    seeking_description = db.Column(db.String(500), nullable=True)
    website = db.Column(db.String(120), nullable=True)
    show = db.relationship('Show', backref='shows_list', lazy=True, cascade="all, delete-orphan")



migrate = Migrate(app, db)
#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
    date = dateutil.parser.parse(value)
    if format == 'full':
        format="EEEE MMMM, d, y 'at' h:mma"
    elif format == 'medium':
        format="EE MM, dd, y h:mma"
    return babel.dates.format_datetime(date, format)

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
    return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():

    data = []
    cities = {}

    venues = Venue.query.all()
    for venue in venues:
        if venue.city not in cities:

            data.append({
                'city': venue.city,
                'state': venue.state,
                'venues': [
                            {
                                'id': venue.id,
                                'name': venue.name,
                                'num_upcoming_shows': len([1 for show in venue.shows if show.start_time < datetime.now()])
                            }
                        ]
                        })
            cities[venue.city] = venue.state
        else:
            entry = next(filter(lambda entry: entry['city'] == venue.city, data))
            entry['venues'].append(
                {
                    'id': venue.id,
                    'name': venue.name,
                    'num_upcoming_shows': len([1 for show in venue.shows if show.start_time < datetime.now()])
                }
            )
    return render_template('pages/venues.html', areas=data)

@app.route('/venues/search', methods=['POST'])
def search_venues():

    response = {'count': 0, 'data': []}
    data = []
    search_term = request.form.get('search_term', '')
    venues =  Venue.query.filter(Venue.name.contains(search_term)).all()
    for venue in venues:
        data.append({
            'id': venue.id,
            'name': venue.name,
            'num_upcoming_shows': len([1 for show in venue.shows if show.start_time < datetime.now()])
        })
        response['count'] += 1
        response['data'] += data

    return render_template('pages/search_venues.html', results=response, search_term=search_term)

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
    # shows the venue page with the given venue_id
    data = {}
    venue = Venue.query.filter_by(id=venue_id).first()
    data['id'] = venue.id
    data['name'] = venue.name
    data['genres'] = venue.genres.replace('{', '').replace('}', '').split(',')
    data['address']  = venue.address
    data['city'] = venue.city
    data['state'] = venue.state
    data['phone'] = venue.phone
    data['facebook_link'] =  venue.facebook_link
    data['past_shows'] = [{
        'artist_id': show.artist_id,
        'start_time': show.start_time.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
    } for show in venue.shows if  show.start_time < datetime.now()]
    data['upcoming_shows'] = [{
        'artist_id': show.artist_id,
        'start_time': show.start_time.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
    } for show in venue.shows if show.start_time > datetime.now()]
    data['past_shows_count'] = len([1 for show in venue.shows if show.start_time < datetime.now()])
    data['upcoming_shows_count'] = len([1 for show in venue.shows if show.start_time > datetime.now()])

    return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
    form = VenueForm()
    return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():

    form = VenueForm(request.form)
    if form.validate():
        request_data = request.form
        data = {}
        data['name'] = request_data['name'] or None
        name = request_data['name']
        data['city'] = request_data['city'] or None
        data['state'] = request_data['state'] or None
        data['address'] = request_data['address'] or None
        data['genres'] = request_data.getlist('genres') or None
        data['facebook_link'] = request_data['facebook_link'] or None
        data['phone'] = request_data['phone'] or None
        error = None
        try:
            venue = Venue(**data)
            db.session.add(venue)
            db.session.commit()
        except Exception as e:
            print(e)
            db.session.rollback()
            error = True
            print(sys.exc_info())
        finally:
            db.session.close()
        if error:
            flash('An error occurred. Venue ' + name + ' could not be listed.')
        else:
            flash('Venue ' + name + ' was successfully listed!')

        return redirect(url_for('index'))
    else:
        message = ''
        for key in form.errors.keys():
            message += key + ', '
        flash(f'form is not valid, make sure {message} are entered correctly.')
        return redirect(url_for('create_venue_form'))

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
    # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.

    # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
    # clicking that button delete it from the db then redirect the user to the homepage
    try:
        Venue.query.filter_by(id=venue_id).delete()
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(e)
    finally:
        db.session.close()
    return jsonify({'success': True})

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
    data = []
    artists = Artist.query.all()
    for artist in artists:
        data.append({
            "id": artist.id,
            "name": artist.name
        })

    return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
    # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
    # search for "band" should return "The Wild Sax Band".
    response = {'count': 0, 'data': []}
    data = []
    search_term = request.form.get('search_term', '')
    artists = Artist.query.filter(Artist.name.contains(search_term)).all()
    for artist in artists:
        data.append({
            'id': artist.id,
            'name': artist.name,
            'num_upcoming_shows': len([1 for show in artist.show if show.start_time < datetime.now()])
        })
        response['count'] += 1
        response['data'] += data

    return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
    # shows the venue page with the given venue_id
    data = {}
    artist = Artist.query.filter_by(id=artist_id).first()
    data['id'] = artist.id
    data['name'] = artist.name
    data['genres'] = artist.genres.replace('{', '').replace('}', '').split(',')
    data['city'] = artist.city
    data['state'] = artist.state
    data['phone'] = artist.phone
    data['facebook_link'] = artist.facebook_link
    data['past_shows'] = [{
        'artist_id': show.artist_id,
        'start_time': show.start_time.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
    } for show in artist.show if show.start_time < datetime.now()]
    data['upcoming_shows'] = [{
        'artist_id': show.artist_id,
        'start_time': show.start_time.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
    } for show in artist.show if show.start_time > datetime.now()]
    data['past_shows_count'] = len([1 for show in artist.show if show.start_time < datetime.now()])
    data['upcoming_shows_count'] = len([1 for show in artist.show if show.start_time > datetime.now()])

    return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
    artist = Artist.query.filter_by(id=artist_id).first()
    form = EditArtistForm()
    artist={
        "id": artist.id,
        "name": artist.name,
        "genres": artist.genres,
        "city": artist.city,
        "state": artist.state,
        "phone": artist.phone,
        "website": artist.website,
        "facebook_link": artist.facebook_link,
        "seeking_venue": artist.seeking_venue,
        "seeking_description": artist.seeking_description,
        "image_link": artist.image_link
    }
    return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
    request_data = request.form
    artist = Artist.query.filter_by(id=artist_id).first()
    error = None
    form = EditArtistForm(request.form)
    if form.validate():
        try:
            if artist.name:
                artist.name = request_data['name']
            if artist.genres:
                artist.genres = request_data.getlist('genres')
            if artist.city:
                artist.city = request_data['city']
            if artist.state:
                artist.state = request_data['state']
            if artist.phone:
                artist.phone = request_data['phone']
            if artist.website:
                artist.website = request_data['website']
            if artist.facebook_link:
                artist.facebook_link = request_data['facebook_link']
            if artist.seeking_venue:
                artist.seeking_venue = request_data['seeking_venue']
            if artist.seeking_description:
                artist.seeking_description = request_data['seeking_description']
            if artist.image_link:
                artist.image_link = request_data['image_link']
            db.session.commit()

        except Exception as e:
            error = True
            print(e)
            db.session.rollback()
            print(sys.exc_info())
        finally:
            db.session.close()

        if error:
            flash('An error occurred. Artist information could not be updated.')
        else:
            flash('Artist information was successfully updated!')

        return redirect(url_for('show_artist', artist_id=artist_id))
    else:
        message = ''
        for key in form.errors.keys():
            message += key + ', '
        flash(f'form is not valid, make sure {message} are entered correctly.')
        return redirect(url_for('edit_artist'))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
    venue = Venue.query.filter_by(id=venue_id).first()


    form = EditVenueForm()
    venue={
        "id": venue.id,
        "name": venue.name,
        "genres": venue.genres,
        "address": venue.address,
        "city": venue.city,
        "state": venue.state,
        "phone": venue.phone,
        "website": venue.website,
        "facebook_link": venue.facebook_link,
        "seeking_talent": venue.seeking_talent,
        "seeking_description": venue.seeking_description,
        "image_link": venue.image_link
    }

    return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):

    request_data = request.form
    venue = Venue.query.filter_by(id=venue_id).first()
    error = None
    form = EditVenueForm(request.form)
    if form.validate():
        try:
            if venue.name:
                venue.name = request_data['name']
            if venue.address:
                venue.address = request_data['address']
            if venue.genres:
                venue.genres = request_data.getlist('genres')
            if venue.city:
                venue.city = request_data['city']
            if venue.state:
                venue.state = request_data['state']
            if venue.phone:
                venue.phone = request_data['phone']
            if venue.website:
                venue.website = request_data['website']
            if venue.facebook_link:
                venue.facebook_link = request_data['facebook_link']
            if venue.seeking_talent:
                venue.seeking_talent = request_data['seeking_talent']
            if venue.seeking_description:
                venue.seeking_description = request_data['seeking_description']
            if venue.image_link:
                venue.image_link = request_data['image_link']
            db.session.commit()

        except Exception as e:
            error = True
            print(e)
            db.session.rollback()
            print(sys.exc_info())
        finally:
            db.session.close()

        if error:
            flash('An error occurred. Venue information could not be updated.')
        else:
            flash('Venue information was successfully updated!')
        # venue record with ID <venue_id> using the new attributes
        return redirect(url_for('show_venue', venue_id=venue_id))
    else:
        message = ''
        for key in form.errors.keys():
            message += key + ', '
        flash(f'form is not valid, make sure {message} are entered correctly.')
        return redirect(url_for('edit_venue'))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
    form = ArtistForm()
    return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
    form = ArtistForm(request.form)

    if form.validate():

        data = {}
        data['name'] = request.form['name'] or None
        data['city'] = request.form['city'] or None
        data['state'] = request.form['state'] or None
        data['genres'] = request.form['genres'] or None
        data['facebook_link'] = request.form['facebook_link'] or None
        data['phone'] = request.form['phone'] or None
        error = None
        try:
            artist = Artist(**data)
            db.session.add(artist)
            db.session.commit()
        except Exception as e:
            print(e)
            db.session.rollback()
            error = True
            print(sys.exc_info())
        finally:
            db.session.close()
        if error:
            flash('An error occurred. Artist ' + data['name'] + ' could not be listed.')
        else:
            flash('Artist ' + data['name'] + ' was successfully listed!')
        return redirect(url_for('index'))
    else:
        message = ''
        for key in form.errors.keys():
            message += key + ', '
        flash(f'form is not valid, make sure {message} are entered correctly.')
        return redirect(url_for('create_artist_form'))




#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
    # displays list of shows at /shows
    data = []
    shows = Show.query.all()
    for show in shows:
        data.append({
            "venue_id": show.venue_id,
            "venue_name": show.venue.name,
            "artist_id": show.artist.id,
            "artist_name": show.artist.name,
            "artist_image_link": show.artist.image_link,
            "start_time": show.start_time.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        })

    return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
    # renders form. do not touch.
    form = ShowForm()
    return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():

    form = ShowForm(request.form)
    if form.validate():
        data = {}
        data['artist_id'] = request.form['artist_id'] or None
        data['venue_id'] = request.form['venue_id'] or None
        data['start_time'] = request.form['start_time'] or None
        error=None
        try:
            show = Show(**data)
            db.session.add(show)
            db.session.commit()
        except Exception as e:
            print(e)
            db.session.rollback()
            error = True
            print(sys.exc_info())
        finally:
            db.session.close()
        if error:
            flash('An error occurred. Show could not be listed.')
        else:
            flash('Show was successfully listed!')
        return redirect(url_for('index'))
    else:
        message = ''
        for key in form.errors.keys():
            message += key + ', '
        flash(f'form is not valid, make sure {message} are entered correctly.')
        return redirect(url_for('create_shows'))



@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''