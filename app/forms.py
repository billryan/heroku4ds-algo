from flask_wtf import Form
from wtforms.fields.html5 import URLField
from wtforms.validators import URL

class PostForm(Form):
    url = URLField('url', validators=[URL()])
