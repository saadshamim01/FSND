#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#
import sys
import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from flask_migrate import Migrate
from alembic import op
from forms import *
from flask import abort
from datetime import datetime
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# TODO: connect to a local postgresql database

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

#Setting up the show Database
class Show(db.Model):
  __tablename__ = 'Show'
  id = db.Column(db.Integer, primary_key=True)
  venue_id = db.Column(db.Integer, db.ForeignKey(
        'Venue.id'), nullable=False)
  artist_id = db.Column(db.Integer, db.ForeignKey(
        'Artist.id'), nullable=False)
  start_time = db.Column(db.DateTime, nullable=False)

  def __repr__(self):
    return f'<Show Id: {self.id} Venue_ID: {self.venue_id}, Artist_ID: {self.artist_id}>'

#Setting up the Venue Database
class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.ARRAY(db.String), nullable=False)
    facebook_link = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    website_link = db.Column(db.String(120))
    seeking_talent = db.Column(db.Boolean(), nullable=False, default=False)
    seeking_description = db.Column(db.String(500))
    shows = db.relationship('Show', backref='Venue', lazy=True, cascade='all, delete-orphan')

    def serialize_with_num_upcoming_shows(self):
        return {
        'id': self.id,
        'name': self.name,
        'num_shows': Show.query.filter(
                    Show.Start_time > datetime.now(),
                    Show.venue_id == self.id).count()
                }

    def __repr__(self):
      return f'<Artist {self.id} {self.name} {self.city} {self.state} {self.address} {self.phone} {self.genres} {self.facebook_link} {self.image_link} {self.website_link} {self.seeking_talent} {self.seeking_description}>'

#Setting up the Artist Database
class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.ARRAY(db.String), nullable=False)
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    seeking_venue = db.Column(db.Boolean(), nullable=False, default=False)
    seeking_description = db.Column(db.String(500))
    website_link = db.Column(db.String(120))
    shows = db.relationship('Show', backref='Artist', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
      return f'<Venue {self.id} {self.name} {self.city} {self.state} {self.phone} {self.genres} {self.image_link} {self.facebook_link} {self.facebook_link} {self.seeking_venue} {self.seeking_description}>'



# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format, locale='en')

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
  try:
    data = []
    venues = Venue.query.all()
    places = Venue.query.distinct(Venue.city, Venue.state).all()
    for place in places:
      data.append({
                  'city': place.city,
                  'state': place.state,
                  'venues': [{
                  'id': venue.id,
                  'name': venue.name,
                  'num_upcoming_shows': len([show for show in venue.shows if show.start_time > datetime.now()])
                  } for venue in venues if
                  venue.city == place.city and venue.state == place.state]
                  })
    return render_template('pages/venues.html', areas=data)
  except:
    flash('Unable to find the venue, please try later!')


@app.route('/venues/search', methods=['POST'])
def search_venues():
  try:
    search_term=request.form.get('search_term', '')
    venue_partial_search = db.session.query(Venue).filter(Venue.name.ilike('%{}%'.format(search_term))).all()
    venue_found = len(venue_partial_search)
    response = {
    "number of venues": venue_found,
    "data": venue_partial_search
    }
    return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))
  except:
    flash('Couldnt find the Venue.')
    return render_template("pages/home.html")


@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  #data = Venue.query.get(venue_id)
  venue = Venue.query.filter_by(id=venue_id).first_or_404()

  past_shows =  db.session.query(Artist, Show).join(Show).join(Venue).filter(
                                                                             Show.venue_id == venue_id,
                                                                             Show.artist_id == Artist.id,
                                                                             Show.start_time < datetime.now()).all()

  upcoming_shows = db.session.query(Artist, Show).join(Show).join(Venue).filter(Show.venue_id == venue_id,
                                                                                 Show.artist_id == Artist.id,
                                                                                 Show.start_time > datetime.now()).all()

  data = {
  'id': venue.id,
  'name': venue.name,
  'city': venue.city,
  'state': venue.state,
  'address': venue.address,
  'phone': venue.phone,
  'genres': venue.genres,
  'facebook_link': venue.facebook_link,
  'image_link': venue.image_link,
  'website_link': venue.website_link,
  'seeking_talent': venue.seeking_talent,
  'seeking_description': venue.seeking_description,
  'past_shows': list([{
                     'artist_id': artist.id,
                     'artist_name': artist.name,
                     'artist_image_link': artist.image_link,
                     'start_time': show.start_time.strftime("%m/%d/%Y, %H:%M")
                     } for artist, show in past_shows]),
  'upcoming_shows': list([{
                         'artist_id': artist.id,
                         'artist_name': artist.name,
                         'artist_image_link': artist.image_link,
                         'start_time': show.start_time.strftime("%m/%d/%Y, %H:%M")
                         } for artist, show in upcoming_shows]),
  'past_shows_count': len(past_shows),
  'upcoming_shows_count': len(upcoming_shows)

  }


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
  try:
    venue = Venue(
                  name = form.name.data,
                  city = form.city.data,
                  state = form.state.data,
                  address = form.address.data,
                  phone = form.phone.data,
                  genres = form.genres.data,
                  facebook_link = form.facebook_link.data,
                  image_link = form.image_link.data,
                  website_link = form.website_link.data,
                  seeking_talent = form.seeking_talent.data,
                  seeking_description = form.seeking_description.data)
    db.session.add(venue)
    db.session.commit()
    flash('Venue ' + request.form['name'] + ' was successfully listed!')
  except:
    db.session.rollback()
    print(sys.exc_info())
    flash('An error occured. Venue ' + request.form['name'] + ' could not be succesfully listed.')
    db.session.close()
  return render_template('pages/home.html')


@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  error = False
  venue = Venue.query.get(venue_id)
  try:
    db.session.delete(venue)
    db.session.commit()
    #flash('Venue ' + request.form['name'] + ' was successfully deleted!')
  except:
    db.session.rollback()
    error = True
    #flash('Venue ' + request.form['name'] + ' was couldnt be successfully deleted!')
  finally:
    db.session.close()
  return None


#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # TODO: replace with real data returned from querying the database
  data = Artist.query.order_by('id').all()
  return render_template('pages/artists.html', artists=data)


@app.route('/artists/search', methods=['POST'])
def search_artists():
  try:
    search_term = request.form.get('search_term', '')
    artist_partial_search = db.session.query(Artist).filter(Artist.name.ilike('%{}%'.format(search_term))).all()
    artist_found = len(artist_partial_search)
    response = {
    "number of artists": artist_found,
    "data": artist_partial_search
    }
    return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))
  except:
    flash('Couldnt find the Artist')


@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  #artist = Artist.query.get(artist_id)
  #return render_template('pages/show_artist.html', artist=artist)
  artist = Artist.query.filter_by(id=artist_id).first_or_404()

  past_shows =  db.session.query(Venue, Show).join(Show).join(Artist).filter(Show.artist_id == artist_id,
                                                                             Show.venue_id == Venue.id,
                                                                             Show.start_time < datetime.now()).all()

  print(past_shows)
  upcoming_shows = db.session.query(Venue, Show).join(Show).join(Artist).filter(Show.artist_id == artist_id,
                                                                                Show.venue_id == Venue.id,
                                                                                Show.start_time > datetime.now()).all()

  data = {
  'id': artist.id,
  'name': artist.name,
  'city': artist.city,
  'state': artist.state,
  'phone': artist.phone,
  'genres': artist.genres,
  'facebook_link': artist.facebook_link,
  'image_link': artist.image_link,
  'website_link': artist.website_link,
  'seeking_venue': artist.seeking_venue,
  'seeking_description': artist.seeking_description,
  'past_shows': list([{
                     'venue_id': venue.id,
                     'venue_name': venue.name,
                     'venue_image_link': venue.image_link,
                     'start_time': show.start_time.strftime("%m/%d/%Y, %H:%M")
                     } for venue, show in past_shows]),
  'upcoming_shows': list([{
                         'venue_id': venue.id,
                         'venue_name': venue.name,
                         'venue_image_link': venue.image_link,
                         'start_time': show.start_time.strftime("%m/%d/%Y, %H:%M")
                         } for venue, show in upcoming_shows]),
  'past_shows_count': len(past_shows),
  'upcoming_shows_count': len(upcoming_shows)

  }
  return render_template('pages/show_artist.html', artist=data)


#  ----------------------------------------------------------------

@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  artist = Artist.query.get(artist_id)
  if artist is None:
    abort(404)
  form = ArtistForm(obj=artist)
  return render_template('forms/edit_artist.html', form=form, artist=artist)


@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  artist = Artist.query.first_or_404(artist_id)
  form = ArtistForm(request.form, meta={'csrf': False})
  if form.validate():
    try:
      artist.name = form.name.data
      artist.genres = form.genres.data
      artist.city = form.city.data
      artist.state = form.state.data
      artist.phone = form.phone.data
      artist.website_link = form.website_link.data
      artist.facebook_link = form.facebook_link.data
      artist.image_link = form.image_link.data
      artist.seeking_venue = form.seeking_venue.data
      artist.seeking_description = form.seeking_description.data
      db.session.commit()
      flash("It was successful")
    except ValueError as e:
      print(e)
    finally:
      db.session.close()
    return redirect(url_for('show_artist', artist_id=artist_id))
  else:
    message = []
    for field, err in form.errors.items():
      message.append(field + ' ' + '|' .join(err))
      flash('Errors ' + str(message))


@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  venue = Venue.query.get(venue_id)
  if venue is None:
    abort(404)
  form = VenueForm(obj=venue)
  return render_template('forms/edit_venue.html', form=form, venue=venue)


@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  venue=Venue.query.first_or_404(venue_id)
  form=VenueForm(request.form, meta={'csrf': False})
  if form.validate():
    try:
      venue.name = form.name.data
      venue.city = form.city.data
      venue.state = form.state.data
      venue.address = form.address.data
      venue.genres = form.genres.data
      venue.phone = form.phone.data
      venue.image_link = form.image_link.data
      venue.facebook_link = form.facebook_link.data
      venue.website_link = form.website_link.data
      venue.seeking_talent = form.seeking_talent.data
      venue.seeking_description = form.seeking_description.data
      db.session.commit()
      flash("It was successful")
    except ValueError as e:
      print(e)
    finally:
      db.session.close()
    return redirect(url_for('show_venue', venue_id=venue_id))
  else:
    message = []
    for field, err in form.errors.items():
      message.append(field + ' ' + '|' .join(err))
      flash('Errors ' + str(message))


#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  form = ArtistForm(request.form)
  try:
    artist = Artist(
                    name = form.name.data,
                    city = form.city.data,
                    state = form.state.data,
                    phone = form.phone.data,
                    genres = form.genres.data,
                    facebook_link = form.facebook_link.data,
                    image_link = form.image_link.data,
                    website_link = form.website_link.data,
                    seeking_venue = form.seeking_venue.data,
                    seeking_description = form.seeking_description.data
                    )
    db.session.add(artist)
    db.session.commit()
    flash('Artist ' + request.form['name'] + 'was successful.')
  except:
    db.session.rollback()
    flash('Artist ' + request.form['name'] + ' was unsuccessful.')
  return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------
#
@app.route('/shows')
def shows():
  result = []
  #Query: where we wanted to get dat from Venue, Artist and Show Model.
  shows_list = Show.query.join(Venue, Show.venue_id == Venue.id).join(Artist, Artist.id == Show.artist_id).filter(Show.start_time > datetime.now()).all()
  #Looping over the list of shows.
  for show in shows_list:
    compound = {
    "venue_id": show.venue_id,
    "venue_name": show.Venue.name,
    "artist_id": show.artist_id,
    "artist_name": show.Artist.name,
    "artist_image_link": show.Artist.image_link,
    #Converting it to string, because frontend cant handle datetime.
    "start_time": str(show.start_time)
    }
    result.append(compound)
  #print(compound)
  return render_template('pages/shows.html', shows=result)



@app.route('/shows/create')
def create_shows():
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  # TODO: insert form data as a new Show record in the db, instead
  show = ShowForm(request.form)
  try:
    show = Show(
                artist_id = show.artist_id.data,
                venue_id = show.venue_id.data,
                start_time = show.start_time.data
                )
    db.session.add(show)
    db.session.commit()
    flash('Show was successfully listed!')
  except Exception as e:
    flash('An error occured')
  return render_template('pages/home.html')

#Handling error.
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
