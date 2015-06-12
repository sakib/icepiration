from ice import db


"""
1. There exists a many to many to many relationship between events, roles, and users.
The UserRoleEventDB class is designed as a lookup table to simulate this relationship.
2. There exists a many to many relationship between events and tags.
The EventTagDB class is designed as a lookup table to simulate this relationship.
3. A LocationDB contains an AddressDB. All Users have Addresses,
and all Events have Locations. The tables are organized as such.
"""


class EventDB(db.Model):
    """Events object stores all necessary information for a site event.
    """
    __tablename__ = 'events'
    event_id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(50), nullable=False)
    organizer_id = db.Column(db.Integer, db.ForeignKey('users.user_id'),
                             nullable=False)
    location_id = db.Column(db.Integer, db.ForeignKey('locations.location_id'),
                             nullable=False)
    price = db.Column(db.Float(precision=2), nullable=False)
    phone_num = db.Column(db.Integer)
    time = db.Column(db.DateTime)

    def __repr__(self): # Print method. Do this for all for debugging
        return '<Event %r>' % (self.name)

class RoleDB(db.Model):
    """Role object defines the role that a user has at an event (maybe on site later).
    privilege   : long int  -> could potentially be used to define privileges.
    """
    __tablename__ = 'roles'
    role_id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(50), nullable=False)
    privilege = db.Column(db.BigInteger)


class UserDB(db.Model):
    """User object stores all necessary information for a site user.
    """
    __tablename__ = 'users'
    user_id = db.Column(db.String(15), primary_key=True, nullable=False)
    address_id = db.Column(db.Integer, db.ForeignKey('addresses.address_id'),
                           nullable=False)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    phone_num = db.Column(db.Integer)


class UserRoleEventDB(db.Model):
    """Lookup table to connect users, events and roles.
    ure_id      : integer   -> unique primary key of an entry
    user_id     : integer   -> foreign key into userDB
    role_id     : integer   -> foreign key into roleDB
    event_id    : integer   -> foreign key into eventDB
    """
    __tablename__ = 'userolevent'
    ure_id = db.Column(db.Integer, primary_key=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.role_id'), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('events.event_id'), nullable=False)


class TagDB(db.Model):
    """Tag object to represent one tag on one event.
    """
    __tablename__ = 'tags'
    tag_id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(25), nullable=False)


class EventTagDB(db.Model):
    """Lookup table to connect events with tags, and similarly, users with preferences.
    """
    __tablename__ = 'eventag'
    et_id = db.Column(db.Integer, primary_key=True, nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('events.event_id'), nullable=False)
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.tag_id'), nullable=False)


class AddressDB(db.Model):
    """Address object to store necessary information. All users and locations have this.
    type    : integer   -> 0:shipping; 1:billing; 2:both
    """
    __tablename__ = 'addresses'
    address_id = db.Column(db.Integer, primary_key=True, nullable=False)
    address1 = db.Column(db.String(50), nullable=False)
    address2 = db.Column(db.String(50))
    city = db.Column(db.String(25), nullable=False)
    state = db.Column(db.String(25), nullable=False)
    country = db.Column(db.String(50), nullable=False)
    zip = db.Column(db.String(25), nullable=False)
    type = db.Column(db.Integer, nullable=False)


class LocationDB(db.Model):
    """Location object to store a map location, like a park.
    All events have this, and subsequently may have addresses.
    Includes contact information, description, name, address, etc.
    """
    __tablename__ = 'locations'
    location_id = db.Column(db.Integer, primary_key=True, nullable=False)
    address_id = db.Column(db.Integer, db.ForeignKey('addresses.address_id'))
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(250), nullable=False)
    contact_name = db.Column(db.String(50), nullable=False)
    contact_email = db.Column(db.String(50), nullable=False)
    contact_phone = db.Column(db.Integer)
