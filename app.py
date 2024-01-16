from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///jobs.db'  # Use SQLite database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Job model for the database
class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    company = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)

# Create the database tables within the application context
with app.app_context():
    db.create_all()

@app.route('/')
def home():
    job_listings = Job.query.all()
    return render_template('index.html', job_listings=job_listings)

@app.route('/add_job', methods=['POST'])
def add_job():
    if request.method == 'POST':
        title = request.form['title']
        company = request.form['company']
        location = request.form['location']
        description = request.form['description']

        new_job = Job(title=title, company=company, location=location, description=description)

        db.session.add(new_job)
        db.session.commit()

    return redirect(url_for('home'))

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        keywords = request.form['keywords'].lower()
        location = request.form['location'].lower()

        # Filter job listings based on keywords and location
        search_results = Job.query.filter(
            (db.func.lower(Job.title).contains(keywords)) |
            (db.func.lower(Job.description).contains(keywords)) &
            (db.func.lower(Job.location).contains(location))
        ).all()

        return render_template('search_results.html', results=search_results)

    return render_template('search.html')

if __name__ == '__main__':
    app.run(debug=True)
