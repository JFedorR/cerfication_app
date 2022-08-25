from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

def create_app():
    app = Flask(__name__)

    # /// = relative path, //// = absolute path
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db = SQLAlchemy(app)

    # Init_app
    db.init_app(app)

    # Schema for database
    class Certifications(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        title = db.Column(db.String(200))

    # Create database
    db.create_all()

    # Home for app
    @app.route('/', methods=['GET'])
    def home():
        certification_list = db.session.query(Certifications).all()
        return render_template('base.html', certification_list=certification_list)

    # Endpoint to add certification
    @app.route('/add', methods=['POST'])
    def add():
        title = request.form.get('title')
        new_certification = Certifications(title=title)
        db.session.add(new_certification)
        db.session.commit()
        return redirect(url_for('home'))

    # Endpoint to delete certification
    @app.route('/delete/<int:certification_id>', methods=['GET'])
    def delete(certification_id):
        certification = db.session.query(Certifications).filter(
            Certifications.id == certification_id).first()
        db.session.delete(certification)
        db.session.commit()
        return redirect(url_for('home'))

    return app

if __name__ == "__main__":
    app = create_app()
    app.run()