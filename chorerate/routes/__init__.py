from . import home, chores, household, auth


def init_app(app):
    '''Registers the blueprints with the app'''
    app.register_blueprint(home.bp)
    app.register_blueprint(chores.bp)
    app.register_blueprint(household.bp)
    app.register_blueprint(auth.bp)
