from datetime import date

from peewee import (
    CharField,
    DateField,
    IntegerField,
    ManyToManyField,
    Model,
    SqliteDatabase
)

db = SqliteDatabase(None)


class BaseModel(Model):
    class Meta:
        database = db


class Song(BaseModel):

    name = CharField(unique=True)
    key = CharField()
    hymn_ref = IntegerField(null=True)

    def __repr__(self):
        return f"Song(id={self.id}, name={self.name}, key={self.key}, hymn_ref={self.hymn_ref})"


class Arrangement(BaseModel):

    name = CharField()
    role = CharField()

    def __repr__(self):
        return f"Arrangement(id={self.id}, role={self.role}, name={self.name})"


class Worship(BaseModel):

    date = DateField()
    songs = ManyToManyField(Song)
    arrangements = ManyToManyField(Arrangement)

    def __repr__(self):
        return f"Worship(id={self.id}, date={self.date}, songs={[song for song in self.songs]}, arrangements={[arr for arr in self.arrangements]})"


WorshipSong = Worship.songs.get_through_model()
WorshipArrangement = Worship.arrangements.get_through_model()
