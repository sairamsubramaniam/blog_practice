import hashlib
import os

from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_user, login_required
import sqlalchemy as sa
from werkzeug.utils import secure_filename

from app import flask_app, db
from app.forms import LoginForm, UploadArticleForm
from app.models import User, Article 



def rearrange_for_blog_landing_page(categories_articles_rows):
    final_output = {}
    for row in categories_articles_rows:
        title = row["title"]
        category = row["primary_category"]
        subcategory = row["primary_sub_category"]

        if category not in final_output:
            final_output[category] = {subcategory: [title]}
        else:
            if subcategory not in final_output[category]:
                final_output[category][subcategory] = [title]
            else:
                final_output[category][subcategory].append(title)
    return final_output


def create_article_id(txt):
    return hashlib.md5(txt.encode('utf-8')).hexdigest()



@flask_app.route("/")
@flask_app.route("/about_me")
def about_me():
    return render_template("about_me.html")



@flask_app.route("/user_login", methods=["GET", "POST"])
def user_login():
    if current_user.is_authenticated:
        return redirect(url_for("upload_article"))
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.scalar(
            sa.select(User).where(User.email==form.username.data)
        )
        if user is None or (not (user.check_password(form.password.data) ) ):
            flash("Invalid Username or password")
            return redirect(url_for("user_login"))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for("upload_article"))
    return render_template("user_login.html", title="Sign In", form=form)




@flask_app.route('/upload_article', methods=['GET', 'POST'])
@login_required
def upload_article():
    print(current_user.is_authenticated)
    form = UploadArticleForm()

    if form.validate_on_submit():

        files = request.files.getlist(form.files.name)
        status = "draft" if form.submit_draft.data else "published"
        primary_category = form.primary_category.data
        primary_sub_category = form.primary_sub_category.data

        for fl in files:
            if fl.filename == "":
                continue

            filename = secure_filename(fl.filename)
            title = os.path.splitext(filename)[0]
            article_id = create_article_id( fl.filename )

            article = Article(
                id=article_id, 
                title=title, 
                primary_category = primary_category, 
                primary_sub_category = primary_sub_category, 
                content=fl.read().decode("utf-8"), 
                publish_status=status, 
                publisher_email=current_user.email
            )
            db.session.merge(article)
        
        db.session.commit()
        return redirect(url_for('upload_article'))

    return render_template('upload_article.html', form=form)



@flask_app.route('/blog_landing_page', methods=['GET'])
def blog_landing_page():
    qry = db.session.query(Article.title, Article.primary_category, Article.primary_sub_category)
    colnames = [ desc['name'] for desc in qry.column_descriptions ]
    result = qry.all()
    ctgr_prdcts = [dict(zip(colnames, row)) for row in result]
    articles = rearrange_for_blog_landing_page(categories_articles_rows=ctgr_prdcts)

    return render_template("blog_landing_page.html", articles=articles)


@flask_app.route("/blog_article/<title>", methods=['GET'])
def blog_article(title):
    article_id = create_article_id(title)
    article_content = db.session.query(Article.content).filter(Article.title==title).scalar()
    return article_content



