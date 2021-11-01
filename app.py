from flask import Flask

import models
import views


def oauth_init_app(app):
    views.oauth.init_app(app)
    prefix = '.well-known/openid-configuration'

    # if 'GOOGLE_CLIENT_ID' in app.config:
    #     views.oauth.register(
    #         'google',
    #         server_metadata_url=f'https://accounts.google.com/{prefix}',
    #     )

    if 'AZURE_CLIENT_ID' in app.config:
        tenant = app.config['AZURE_TENANT_ID']
        views.oauth.register(
            'azure',
            server_metadata_url=f'https://login.microsoftonline.com/'
                                f'{tenant}/v2.0/{prefix}',
            client_kwargs={'scope': 'openid profile email'}
        )


def create_app(testing_config=None):
    app = Flask(__name__)

    app.config.from_pyfile('config.cfg', silent=True)
    app.config.from_mapping(testing_config)

    models.db.init_app(app)
    oauth_init_app(app)

    app.add_url_rule('/', view_func=views.home)
    app.add_url_rule('/auth/init/', view_func=views.auth_init)
    app.add_url_rule('/auth/done/', view_func=views.auth_done)
    app.add_url_rule('/logout/', view_func=views.logout)
    app.add_url_rule('/group/<int:edu_group_id>/',
                     view_func=views.schedule_group)
    app.add_url_rule('/teacher/<int:person_id>/',
                     view_func=views.schedule_teacher)
    app.add_url_rule('/room/<int:room_id>/', view_func=views.schedule_room)
    app.add_url_rule('/persons/', view_func=views.edit_persons)
    app.add_url_rule('/groups/', view_func=views.edit_edu_groups)
    app.add_url_rule('/rooms/', view_func=views.edit_rooms)
    app.add_url_rule('/courses/', view_func=views.edit_courses)
    app.add_url_rule('/event/<int:event_id>/', view_func=views.event)

    return app
