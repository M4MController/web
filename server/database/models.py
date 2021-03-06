from sqlalchemy import (
	Boolean,
	Column,
	DateTime,
	ForeignKey,
	Integer,
	String
)
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Object(Base):
	__tablename__ = 'objects'

	id = Column(Integer, primary_key=True)
	name = Column(String, nullable=False)
	user_id = Column(Integer, ForeignKey('users.id'), nullable=False)

	controllers = relationship(
		'Controller',
		uselist=True,
		lazy='noload',
	)

	user = relationship(
		'User',
		uselist=False,
		lazy='noload',
	)


class Controller(Base):
	__tablename__ = 'controllers'

	id = Column(Integer, primary_key=True)
	name = Column(String, nullable=False)
	meta = Column(String, default='')
	activation_date = Column(DateTime(timezone=False))
	deactivation_date = Column(DateTime(timezone=False))
	status = Column(Integer, default=None)
	controller_type = Column(Integer, default=None)
	mac = Column(String, nullable=False)
	object_id = Column(Integer, ForeignKey('objects.id'), nullable=False)

	sensors = relationship(
		'Sensor',
		uselist=True,
		lazy='noload',
	)

	object = relationship(
		'Object',
		uselist=False,
		lazy='noload',
	)


class Sensor(Base):
	__tablename__ = 'sensors'

	id = Column(String(32), nullable=False, primary_key=True)
	name = Column(String, nullable=False)
	activation_date = Column(DateTime(timezone=False))
	deactivation_date = Column(DateTime(timezone=False))
	status = Column(Integer, default=None)
	sensor_type = Column(Integer, default=None)
	controller_id = Column(Integer, ForeignKey('controllers.id'), nullable=False)
	company_id = Column(Integer, ForeignKey('companies.id'), nullable=True, default=None)

	# one-to-many relation
	controller = relationship(
		'Controller',
		uselist=False,
		lazy='noload',
	)

	company = relationship(
		'Company',
		uselist=False,
		lazy='noload',
	)


class User(Base):
	__tablename__ = 'users'

	id = Column(Integer, primary_key=True)
	login = Column(String, nullable=False, unique=True)
	pwd_hash = Column(String, nullable=False)

	objects = relationship(
		'Object',
		uselist=True,
		lazy='noload',
	)

	social_tokens = relationship(
		'UserSocialTokens',
		uselist=False,
		lazy='noload',
	)


class UserInfo(Base):
	__tablename__ = 'users_info'

	user_id = Column(Integer, ForeignKey('users.id'), primary_key=True, nullable=False)
	last_name = Column(String)
	first_name = Column(String)
	middle_name = Column(String)
	date_receiving = Column(Integer)
	issued_by = Column(String)
	division_number = Column(String)
	registration_addres = Column(String)
	mailing_addres = Column(String)
	birth_day = Column(String)
	sex = Column(Boolean)
	home_phone = Column(String)
	mobile_phone = Column(String)
	citizenship = Column(String)
	e_mail = Column(String)

	user = relationship(
		'User',
		uselist=False,
		lazy='noload',
	)


class UserSocialTokens(Base):
	__tablename__ = 'users_social_tokens'

	user_id = Column(Integer, ForeignKey('users.id'), primary_key=True, nullable=False)
	yandex_disk = Column(String)

	user = relationship(
		'User',
		uselist=False,
		lazy='noload',
	)


class Company(Base):
	__tablename__ = 'companies'

	id = Column(Integer, primary_key=True, nullable=False)
	name = Column(String)

	sensors = relationship(
		'Sensor',
		uselist=True,
		lazy='noload',
	)
