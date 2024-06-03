from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from app.models import db, Product, Address, Order


admin = Admin(name='Admin Panel', template_mode='bootstrap3')
admin.add_view(ModelView(Product, db.session))
admin.add_view(ModelView(Address, db.session))
admin.add_view(ModelView(Order, db.session))