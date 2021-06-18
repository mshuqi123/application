# -*- coding: utf-8 -*-
"""
    :author: Shuqi Ma (马树起)
    :url:
    :copyright:
    :license: MIT, see LICENSE for more details.
"""

from flask_mongoengine import MongoEngine
from flask_wtf import CSRFProtect
from flask_caching import Cache
from flask_celery import Celery

# from flask_bootstrap import Bootstrap
# from flask_ckeditor import CKEditor
# from flask_login import LoginManager
# from flask_mail import Mail
# from flask_moment import Moment
# from flask_debugtoolbar import DebugToolbarExtension
# from flask_migrate import Migrate
from flask_debugtoolbar import DebugToolbarExtension

mongo = MongoEngine()
cache = Cache()
csrf = CSRFProtect()
celery = Cache()

# bootstrap = Bootstrap()
# db = SQLAlchemy()
# login_manager = LoginManager()
# ckeditor = CKEditor()
# mail = Mail()
# moment = Moment()
# toolbar = DebugToolbarExtension()
# migrate = Migrate()


# @login_manager.user_loader
# def load_user(user_id):
#     from bluelog.models import Admin
#     user = Admin.query.get(int(user_id))
#     return user


# login_manager.login_view = 'auth.login'
# login_manager.login_message = 'Your custom message'
# login_manager.login_message_category = 'warning'
