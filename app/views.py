from flask import render_template, flash, request
from app import app
from app.forms import PostForm
from app.ojhtml2markdown import OJHtml2Markdown

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index(markdown=None):
    form = PostForm()
    if form.validate_on_submit():
        url = request.form['url']
        ojhtml2markdown = OJHtml2Markdown(url, prefer_leetcode=True)
        markdown = ojhtml2markdown.gen_markdown()
        return render_template(
            'index.html',
            title='Home',
            form=form,
            markdown=markdown)
    return render_template(
        'index.html',
        title='Home',
        form=form)
