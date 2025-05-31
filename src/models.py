from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, Table, Column, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column,relationship

db = SQLAlchemy()

user_planet_favorite=Table(
    "user_planet_favorite",
    db.Model.metadata,
    Column('user_id', Integer, ForeignKey('user.id'), primary_key=True),
    Column('planets_id', Integer, ForeignKey('planets.id'), primary_key=True)
)

user_character_favorite=Table(
    "user_character_favorite",
    db.Model.metadata,
    Column('user_id', Integer, ForeignKey('user.id'), primary_key=True),
    Column('character_id', Integer, ForeignKey('character.id'), primary_key=True)
)

user_vehicle_favorite=Table(
    "user_vehicle_favorite",
    db.Model.metadata,
    Column('user_id', Integer, ForeignKey('user.id'), primary_key=True),
    Column('vehicles_id', Integer, ForeignKey('vehicles.id'), primary_key=True)
)


class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)
    
    favorite_planets:Mapped[list["Planets"]]=relationship(
        secondary=user_planet_favorite,
        back_populates= "user_who_favorite_planet"
    )

    favorite_characters:Mapped[list["Character"]]=relationship(
        secondary=user_character_favorite,
        back_populates= "user_who_favorite_character"
    )

    favorite_vehicles:Mapped[list["Vehicles"]]=relationship(
        secondary=user_vehicle_favorite,
        back_populates= "user_who_favorite_vehicle"
    )

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }

class Character(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    hair_color: Mapped[str] = mapped_column(nullable=False)
    eyes_color: Mapped[str] = mapped_column(nullable=False)
    
    user_who_favorite_character:Mapped[list["User"]]=relationship(
        secondary=user_character_favorite,
        back_populates= "favorite_character" 
    )

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "hair_color": self.hair_color,
            "eyes_color": self.eyes_color,
        }

class Planets(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    population: Mapped[int] = mapped_column(nullable=False)
    climate: Mapped[str] = mapped_column(String(120), nullable=False)
    terrain: Mapped[str] = mapped_column(String(120), nullable=False)
    
    user_who_favorite_planet:Mapped[list["User"]]=relationship(
        secondary=user_planet_favorite,
        back_populates= "favorite_planets" 
    )

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "population": self.population,
            "climate": self.climate,
            "terrain": self.terrain,
        }
    
class Vehicles(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    model: Mapped[str] = mapped_column(nullable=False)
    cargo_capacity: Mapped[int] = mapped_column(nullable=False)
    passengers: Mapped[int] = mapped_column(nullable=False)

    user_who_favorite_vehicle:Mapped[list["User"]]=relationship(
        secondary=user_vehicle_favorite,
        back_populates= "favorite_vehicles" 
    )

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "model": self.model,
            "cargo_capacity": self.cargo_capacity,
            "passengers": self.passengers,
        }

