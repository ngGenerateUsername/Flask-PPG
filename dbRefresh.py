#hedhia code yrefreshi el base w
from App import db,app
from App.models import admin
db.drop_all()
db.create_all()
me = admin("admin","admin")
db.session.add(me)
db.session.commit()




