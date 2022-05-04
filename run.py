from app import create_app, db

app = create_app()

from app.blueprints.blog.models import Post, User

@app.shell_context_processor
def make_context():
    return {
        'db': db,
        'User': User,
        'Post': Post
    }