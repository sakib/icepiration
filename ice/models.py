from __init__ import app, db
from passlib.apps import custom_app_context as pwd_context
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)

"""
1. There exists a many to many to many relationship between events, roles, and users.
The UserRoleEventDB class is designed as a lookup table to simulate this relationship.
2. There exists a many to many relationship between events and tags.
The EventTagDB class is designed as a lookup table to simulate this relationship.
3. A LocationDB contains an AddressDB. All Users have Addresses,
and all Events have Locations. The tables are organized as such.
"""

class AddressDB(db.Model):
    """Address object to store necessary information. All users and locations have this.
    type    : integer   -> 0:shipping; 1:billing; 2:both
    Longitude and latitude will be calculated using a third party program based off address.
    """
    __tablename__ = 'addresses'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    address1 = db.Column(db.String(50), nullable=False)
    address2 = db.Column(db.String(50))
    city = db.Column(db.String(25), nullable=False)
    country = db.Column(db.String(50), nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    state = db.Column(db.String(25), nullable=False)
    type = db.Column(db.Integer, nullable=False)
    zip = db.Column(db.String(25), nullable=False)
 
class ContactDB(db.Model):
    """Contacts object to store necessary information. All users, events, and locations have this.
    type : integer -> integer used to define type.
    """
    __tablename__ = 'contacts'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    address = db.Column(db.Integer, db.ForeignKey('addresses.id'), nullable=False)
    contactType = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String(50))
    name = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.Integer)

class EventDB(db.Model):
    """Events object stores all necessary information for a site event. Start date necessary for global calendar display.
    """
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    contact_id = db.Column(db.Integer, db.ForeignKey('contacts.id'), nullable=False)
    event_schedule_id = db.Column(db.Integer, db.ForeignKey('event_schedules.id'), nullable=False)
    location_id = db.Column(db.Integer, db.ForeignKey('locations.id'), nullable=False)
    organizer_id = db.Column(db.String(15), db.ForeignKey('users.username'), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    price_usd = db.Column(db.Float(precision=2), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
  
class EventScheduleDB(db.Model):
    """EventSchedules object stores all necessary information for the schedule of an event day. Events have an EventSchedule for each day
    """
    __tablename__ = 'event_schedules'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    description = db.Column(db.String(250))
    event_end_time = db.Column(db.DateTime, nullable=False)
    event_start_time = db.Column(db.DateTime, nullable=False)
    
class EventTagDB(db.Model):
    """Lookup table to connect events with tags, and similarly, users with preferences.
    """
    __tablename__ = 'eventag'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'), nullable=False)
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'), nullable=False)

class LocationDB(db.Model):
    """Location object to store a map location, like a park.
    All events have this, and subsequently may have addresses.
    Includes contact information, description, name, address, etc.
    """
    __tablename__ = 'locations'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    address_id = db.Column(db.Integer, db.ForeignKey('addresses.id'))
    contact = db.Column(db.Integer, db.ForeignKey('contacts.id'), nullable=False)
    description = db.Column(db.String(500))
    name = db.Column(db.String(50), nullable=False)
    type = db.Column(db.Integer, nullable=False)
    url = db.Column(db.String(250))
  
class RoleDB(db.Model):
    """Role object defines the role that a user has at an event (maybe on site later).
    privilege   : long int  -> could potentially be used to define privileges.
    """
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(50), nullable=False)
    privilege = db.Column(db.BigInteger)

class TagDB(db.Model):
    """Tag object to represent one tag on one event.
    """
    __tablename__ = 'tags'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(25), nullable=False)

class UserDB(db.Model):
    """User object stores all necessary information for a site user.
    """
    __tablename__ = 'users'
    username = db.Column(db.String(15), primary_key=True, nullable=False)
    contact_id = db.Column(db.Integer, db.ForeignKey('contacts.id'), nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

    def generate_auth_token(self, expiration=600):
        s = Serializer(app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'username': self.username})

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None # valid token, but expired
        except BadSignature:
            return None # invalid token
        user = UserDB.query.get(data['username'])

class UserRoleEventDB(db.Model):
    """Lookup table to connect users, events and roles.
    ure_id      : integer   -> unique primary key of an entry
    user_id     : string    -> foreign key into userDB
    role_id     : integer   -> foreign key into roleDB
    event_id    : integer   -> foreign key into eventDB
    """
    __tablename__ = 'user_role_event'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable=False)
    user_id = db.Column(db.String(15), db.ForeignKey('users.username'), nullable=False)
