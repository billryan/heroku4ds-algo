import os
from flask import Flask
from flask_pure import Pure

app = Flask(__name__)
app.config.from_object('config')
app.config['PURECSS_RESPONSIVE_GRIDS'] = True
app.config['PURECSS_USE_CDN'] = True
app.config['PURECSS_USE_MINIFIED'] = True
Pure(app)

if not app.debug and os.environ.get('HEROKU') is None:
    import logging
    app.logger.setLevel(logging.INFO)
    app.logger.info('heroku4ds-algo startup')


if os.environ.get('HEROKU') is not None:
    import logging
    stream_handler = logging.StreamHandler()
    app.logger.addHandler(stream_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info('heroku4ds-algo startup')

from app import views
