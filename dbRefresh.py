#hedhia code yrefreshi el base w
from App import db,app
from App.models import admin, directeur, projet
from faker import Faker
from random import randint


db.drop_all()
db.create_all()

#Add the admin
admindb = admin("admin","admin")
db.session.add(admindb)
db.session.commit()

#Add Directeur
directeurDb = directeur()
directeurDb.name = "Ahmed"
directeurDb.lastName="Ben Hamouda"
directeurDb.departement="INFORMATIQUE"
directeurDb.email_adress="ahmed@gmail.com"
directeurDb.phone="197"
directeurDb.poste="ingenieur"
directeurDb.state = 1
directeurDb.username="ahmed"
directeurDb.password="oooooo" #7arf o mech num 0 w setta asfar
db.session.add(directeurDb)
db.session.commit()

#Add Projet to Directeur
projetDb = projet()
projetDb.projet_title='Etude/Dev application de gestion de stock'
projetDb.projet_description='La gestion de stock peut-être un vrai casse-tête, que vous possédiez un commerce, une boutique en ligne, ou toute autre activité. Depuis quelque temps, heureusement que des solutions ont vu le jour pour vous faciliter la vie et vous aider dans ce travail. Nous vous présentons dans cet article notre sélection de logiciel et d’application en matière de gestion de stock.'
projetDb.direct_id = 1


#This is Faker section (we use Faker to fill in the database with fake Data generated)
# open('allFakerAttributes.txt','a').write(' '.join(dir(F)))
#Add 5 Fake director to db
for i in range(10):
    fake = Faker()
    fakeDirecteur = directeur()
    nameAndUsername = fake.unique.first_name()
    fakeDirecteur.name = nameAndUsername
    fakeDirecteur.lastName=fake.last_name()
    fakeDirecteur.departement= fake.company()
    fakeDirecteur.email_adress=fake.unique.email()
    fakeDirecteur.phone=fake.postalcode()
    fakeDirecteur.poste=fake.job()
    fakeDirecteur.state = 1 if fake.boolean() == True else 0
    fakeDirecteur.username=nameAndUsername.lower()
    fakeDirecteur.password="oooooo" #7arf o mech num 0 w setta asfar
    db.session.add(fakeDirecteur)
    db.session.commit()

for i in range(15):
    fake = Faker()
    projetFake = projet()
    projetFake.projet_title=fake.paragraph()
    projetFake.projet_description= " ".join(fake.texts())
    projetFake.direct_id = randint(1,11)
    db.session.add(projetFake)
    db.session.commit()




