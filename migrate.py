from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from app import flask_app
from app import db



migrate = Migrate(flask_app, db)
manager = Manager(flask_app)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()