import phonenumbers
from datetime import datetime
from flask_wtf import Form
from wtforms import StringField, SelectField, SelectMultipleField, DateTimeField, BooleanField, validators, ValidationError
from wtforms.validators import DataRequired, AnyOf, URL
from enum import Enum


class VenueFields(Enum):
    NAME = 'name'
    CITY = 'city'
    STATE = 'state'
    ADDRESS = 'address'
    PHONE  = 'phone'
    IMAGE_LINK = 'image_link'
    GENRES = 'genre'
    FACEBOOK_LINK = 'facebook_link'
    SEEKING_TALENT = 'seeking new talent'
    SEEKING_DESCRIPTION = 'seeking description'


class ArtistFields(Enum):
    NAME = 'name'
    CITY = 'city'
    STATE = 'state'
    ADDRESS = 'address'
    PHONE  = 'phone'
    IMAGE_LINK = 'image_link'
    GENRES = 'genre'
    FACEBOOK_LINK = 'facebook_link'
    SEEKING_TALENT = 'seeking new talent'
    SEEKING_DESCRIPTION = 'seeking description'
    SEEKING_VENUE = 'seeking venue'


def validate_phone(form, phone):
    try:
        p = phonenumbers.parse(phone.data)
        if not phonenumbers.is_valid_number(p):
            raise  ValidationError('Invalid phone number')
    except (phonenumbers.phonenumberutil.NumberParseException, ValueError):
        raise ValidationError('Invalid phone number')

class ShowForm(Form):
    artist_id = StringField(
        'artist_id'
    )
    venue_id = StringField(
        'venue_id'
    )
    start_time = DateTimeField(
        'start_time',
        validators=[DataRequired()],
        default= datetime.today()
    )

class VenueForm(Form):
    name = StringField(
        VenueFields.NAME, validators=[DataRequired()]
    )
    city = StringField(
        VenueFields.CITY, validators=[DataRequired()]
    )
    state = SelectField(
        VenueFields.STATE, validators=[DataRequired()],
        choices=[
            ('AL', 'AL'),
            ('AK', 'AK'),
            ('AZ', 'AZ'),
            ('AR', 'AR'),
            ('CA', 'CA'),
            ('CO', 'CO'),
            ('CT', 'CT'),
            ('DE', 'DE'),
            ('DC', 'DC'),
            ('FL', 'FL'),
            ('GA', 'GA'),
            ('HI', 'HI'),
            ('ID', 'ID'),
            ('IL', 'IL'),
            ('IN', 'IN'),
            ('IA', 'IA'),
            ('KS', 'KS'),
            ('KY', 'KY'),
            ('LA', 'LA'),
            ('ME', 'ME'),
            ('MT', 'MT'),
            ('NE', 'NE'),
            ('NV', 'NV'),
            ('NH', 'NH'),
            ('NJ', 'NJ'),
            ('NM', 'NM'),
            ('NY', 'NY'),
            ('NC', 'NC'),
            ('ND', 'ND'),
            ('OH', 'OH'),
            ('OK', 'OK'),
            ('OR', 'OR'),
            ('MD', 'MD'),
            ('MA', 'MA'),
            ('MI', 'MI'),
            ('MN', 'MN'),
            ('MS', 'MS'),
            ('MO', 'MO'),
            ('PA', 'PA'),
            ('RI', 'RI'),
            ('SC', 'SC'),
            ('SD', 'SD'),
            ('TN', 'TN'),
            ('TX', 'TX'),
            ('UT', 'UT'),
            ('VT', 'VT'),
            ('VA', 'VA'),
            ('WA', 'WA'),
            ('WV', 'WV'),
            ('WI', 'WI'),
            ('WY', 'WY'),
        ]
    )
    address = StringField(
        VenueFields.ADDRESS, validators=[DataRequired()]
    )
    phone = StringField(
        VenueFields.PHONE, validators=[DataRequired(), validate_phone]
    )

    genres = SelectMultipleField(
        VenueFields.GENRES, validators=[DataRequired()],
        choices=[
            ('Alternative', 'Alternative'),
            ('Blues', 'Blues'),
            ('Classical', 'Classical'),
            ('Country', 'Country'),
            ('Electronic', 'Electronic'),
            ('Folk', 'Folk'),
            ('Funk', 'Funk'),
            ('Hip-Hop', 'Hip-Hop'),
            ('Heavy Metal', 'Heavy Metal'),
            ('Instrumental', 'Instrumental'),
            ('Jazz', 'Jazz'),
            ('Musical Theatre', 'Musical Theatre'),
            ('Pop', 'Pop'),
            ('Punk', 'Punk'),
            ('R&B', 'R&B'),
            ('Reggae', 'Reggae'),
            ('Rock n Roll', 'Rock n Roll'),
            ('Soul', 'Soul'),
            ('Other', 'Other'),
        ]
    )
    facebook_link = StringField(
        VenueFields.FACEBOOK_LINK, validators=[URL()]
    )
    seeking_talent = BooleanField(
        VenueFields.SEEKING_TALENT, )

    seeking_description = StringField(
        VenueFields.SEEKING_DESCRIPTION, validators=[validators.Length(min=10, max=500)])
    image_link = StringField(
        VenueFields.IMAGE_LINK, validators=[DataRequired, validators.Length(min=10, max=500)])


class ArtistForm(Form):
    name = StringField(
       ArtistFields.NAME , validators=[DataRequired()]
    )
    city = StringField(
        ArtistFields.CITY, validators=[DataRequired()]
    )
    state = SelectField(
        ArtistFields.STATE, validators=[DataRequired()],
        choices=[
            ('AL', 'AL'),
            ('AK', 'AK'),
            ('AZ', 'AZ'),
            ('AR', 'AR'),
            ('CA', 'CA'),
            ('CO', 'CO'),
            ('CT', 'CT'),
            ('DE', 'DE'),
            ('DC', 'DC'),
            ('FL', 'FL'),
            ('GA', 'GA'),
            ('HI', 'HI'),
            ('ID', 'ID'),
            ('IL', 'IL'),
            ('IN', 'IN'),
            ('IA', 'IA'),
            ('KS', 'KS'),
            ('KY', 'KY'),
            ('LA', 'LA'),
            ('ME', 'ME'),
            ('MT', 'MT'),
            ('NE', 'NE'),
            ('NV', 'NV'),
            ('NH', 'NH'),
            ('NJ', 'NJ'),
            ('NM', 'NM'),
            ('NY', 'NY'),
            ('NC', 'NC'),
            ('ND', 'ND'),
            ('OH', 'OH'),
            ('OK', 'OK'),
            ('OR', 'OR'),
            ('MD', 'MD'),
            ('MA', 'MA'),
            ('MI', 'MI'),
            ('MN', 'MN'),
            ('MS', 'MS'),
            ('MO', 'MO'),
            ('PA', 'PA'),
            ('RI', 'RI'),
            ('SC', 'SC'),
            ('SD', 'SD'),
            ('TN', 'TN'),
            ('TX', 'TX'),
            ('UT', 'UT'),
            ('VT', 'VT'),
            ('VA', 'VA'),
            ('WA', 'WA'),
            ('WV', 'WV'),
            ('WI', 'WI'),
            ('WY', 'WY'),
        ]
    )
    phone = StringField(
        # TODO implement validation logic for state
        ArtistFields.PHONE, validators=[DataRequired(), validate_phone]
    )

    genres = SelectMultipleField(

        ArtistFields.GENRES, validators=[DataRequired()],
        choices=[
            ('Alternative', 'Alternative'),
            ('Blues', 'Blues'),
            ('Classical', 'Classical'),
            ('Country', 'Country'),
            ('Electronic', 'Electronic'),
            ('Folk', 'Folk'),
            ('Funk', 'Funk'),
            ('Hip-Hop', 'Hip-Hop'),
            ('Heavy Metal', 'Heavy Metal'),
            ('Instrumental', 'Instrumental'),
            ('Jazz', 'Jazz'),
            ('Musical Theatre', 'Musical Theatre'),
            ('Pop', 'Pop'),
            ('Punk', 'Punk'),
            ('R&B', 'R&B'),
            ('Reggae', 'Reggae'),
            ('Rock n Roll', 'Rock n Roll'),
            ('Soul', 'Soul'),
            ('Other', 'Other'),
        ]
    )
    facebook_link = StringField(
        ArtistFields.FACEBOOK_LINK, validators=[URL()]
    )
    seeking_venue = BooleanField(
        ArtistFields.SEEKING_VENUE)

    seeking_description = StringField(
        ArtistFields.SEEKING_DESCRIPTION, validators=[validators.Length(min=10, max=500)])


    # def validate_phone(self, phone):
    #     try:
    #         p = phonenumbers.parse(phone.data)
    #         if not phonenumbers.is_valid_number(p):
    #             raise ValueError()
    #     except (phonenumbers.phonenumberutil.NumberParseException, ValueError):
    #         raise ValidationError('Invalid phone number')

# TODO IMPLEMENT NEW ARTIST FORM AND NEW SHOW FORM
