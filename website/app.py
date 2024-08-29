from flask import Flask ,render_template ,request,redirect,session,jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.hybrid import hybrid_property
from datetime import datetime
app = Flask(__name__)
app.secret_key = 'pratik_sonune'
app.config['SQLALCHEMY_DATABASE_URI']='postgresql://prat_user:pratik@localhost/fest'

db=SQLAlchemy(app)

class Student(db.Model):
    __tablename__='students'
    s_username = db.Column(db.String(40),primary_key=True)
    s_password = db.Column(db.String(40))
    s_name     = db.Column(db.String(40))
    s_gender   = db.Column(db.String(40))
    s_email    = db.Column(db.String(40))
    s_mob      = db.Column(db.Numeric(precision=10, scale=0))
    s_dept     = db.Column(db.String(40))

    def __init__(self,s_username,s_password,s_name,s_gender,s_email,s_mob,s_dept):
        self.s_username=s_username
        self.s_password=s_password
        self.s_name=s_name
        self.s_gender=s_gender
        self.s_email=s_email
        self.s_mob=s_mob
        self.s_dept=s_dept

    @classmethod
    def delete(cls, username):
        student = cls.query.get(username)
        if student:
            db.session.delete(student)
            db.session.commit()
            return jsonify(success=True, message="Student deleted successfully.")
        else:
            return jsonify(success=False, message="Student not found.")    


class Participant(db.Model):
    __tablename__='participants'
    p_username = db.Column(db.String(40),primary_key=True)
    p_password = db.Column(db.String(40))
    p_name     = db.Column(db.String(40))
    p_gender   = db.Column(db.String(40))
    p_email    = db.Column(db.String(40))
    p_mob      = db.Column(db.Numeric(precision=10, scale=0))
    p_college  = db.Column(db.String(40))
    p_dept     = db.Column(db.String(40))
    p_place    = db.Column(db.String(40))

    def __init__(self,p_username,p_password,p_name,p_gender,p_email,p_mob,p_college,p_dept,p_place):
        self.p_username=p_username
        self.p_password=p_password
        self.p_name=p_name
        self.p_gender=p_gender
        self.p_email=p_email
        self.p_mob=p_mob
        self.p_college=p_college
        self.p_dept=p_dept
        self.p_place=p_place

    @classmethod
    def delete(cls, username):
        participant = cls.query.get(username)
        if participant:
            db.session.delete(participant)
            db.session.commit()
            return jsonify(success=True, message="Participant deleted successfully.")
        else:
            return jsonify(success=False, message="Participant not found.")    

class Organizer(db.Model):
    __tablename__='organizers'
    o_username = db.Column(db.String(40),primary_key=True)
    o_password = db.Column(db.String(40))
    o_name     = db.Column(db.String(40))
    o_gender   = db.Column(db.String(40))
    o_email    = db.Column(db.String(40))
    o_mob      = db.Column(db.Numeric(precision=10, scale=0))
    o_role     = db.Column(db.String(40))

    def __init__(self,o_username,o_password,o_name,o_gender,o_email,o_mob,o_role):
        self.o_username=o_username
        self.o_password=o_password
        self.o_name=o_name
        self.o_gender=o_gender
        self.o_email=o_email
        self.o_mob=o_mob
        self.o_role=o_role

    @classmethod
    def delete(cls, username):
        organizer = cls.query.get(username)
        if organizer:
            db.session.delete(organizer)
            db.session.commit()
            return jsonify(success=True, message="Organizer deleted successfully.")
        else:
            return jsonify(success=False, message="Organizer not found.")    

class Admin(db.Model):
    __tablename__ = 'admins'
    a_username = db.Column(db.String(40), primary_key=True)
    a_password = db.Column(db.String(40))
    a_name = db.Column(db.String(40))

    def __init__(self, a_username, a_password, a_name):
        self.a_username = a_username
        self.a_password = a_password
        self.a_name = a_name

class Winner(db.Model):
    __tablename__ = 'winners'
    id = db.Column(db.Integer, primary_key=True)
    eventid = db.Column(db.String(10), db.ForeignKey('event.eventid'))
    username = db.Column(db.String(40))
    rank = db.Column(db.Integer)

    # Define relationship with Event model
    event = db.relationship('Event', backref='winners')

    def __init__(self, eventid, username, rank):
        self.eventid = eventid
        self.username = username
        self.rank = rank

class Logistic(db.Model):
    __tablename__ = 'logistic'
    username = db.Column(db.String(40), primary_key=True)
    food = db.Column(db.String(10))
    hostel = db.Column(db.String(10))
    gender = db.Column(db.String(10))

    def __init__(self, username, food, hostel, gender):
        self.username = username
        self.food = food
        self.hostel = hostel
        self.gender = gender

# Define the Event model
class Event(db.Model):
    __tablename__ = 'event'
    eventid = db.Column(db.String(10), primary_key=True)
    eventname = db.Column(db.String(255))
    type = db.Column(db.String(100))
    date = db.Column(db.Date)

    # @hybrid_property
    # def registered(self,username):
    #     return bool(Registration.query.filter_by(eventid=self.eventid,username=username).first())
    @hybrid_property
    def registered(self):
        return self.is_registered(session.get('username'))

    def is_registered(self, username):
        return bool(Registration.query.filter_by(eventid=self.eventid, username=username).first())
    @hybrid_property
    def volunteered(self):
        return self.is_volunteered(session.get('username'))
    
    def is_volunteered(self,username):
        return bool(Volunteer.query.filter_by(eventid=self.eventid, username=username).first())
    # @hybrid_property
    # def is_registered(self, username):
    #     # Check if there is a registration record for the given eventid and username
    #     registration = Registration.query.filter_by(eventid=self.eventid, username=username).first()
    #     return registration is not None
    
    # @hybrid_property
    # def is_volunteered(self, username):
    #     # Check if there is a registration record for the given eventid and username
    #     volunteer = Volunteer.query.filter_by(eventid=self.eventid, username=username).first()
    #     return volunteer is not None

class Registration(db.Model):
    __tablename__ = 'registrations'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(40))
    eventid = db.Column(db.String(10))

    def __init__(self, username, eventid):
        self.username = username
        self.eventid = eventid

# Volunteer class
class Volunteer(db.Model):
    __tablename__ = 'volunteers'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(40))
    eventid = db.Column(db.String(10))

    def __init__(self, username, eventid):
        self.username = username
        self.eventid = eventid    

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/create')
def create():
    return render_template('create.html')

@app.route('/create_admin')
def create_admin():
    return render_template('create_admin.html')

@app.route('/submit_student',methods=['POST'])
def submit_student():
    s_username = request.form['s_username']
    s_password = request.form['s_password']
    s_name     = request.form['s_name']
    s_gender   = request.form['s_gender']
    s_email    = request.form['s_email']
    s_mob      = request.form['s_mob']
    s_dept     = request.form['s_dept']

    student=Student(s_username,s_password,s_name,s_gender,s_email,s_mob,s_dept)
    db.session.add(student)
    db.session.commit()

    return render_template('index.html')

@app.route('/submit_student_admin',methods=['POST'])
def submit_student_admin():
    s_username = request.form['s_username']
    s_password = request.form['s_password']
    s_name     = request.form['s_name']
    s_gender   = request.form['s_gender']
    s_email    = request.form['s_email']
    s_mob      = request.form['s_mob']
    s_dept     = request.form['s_dept']

    student=Student(s_username,s_password,s_name,s_gender,s_email,s_mob,s_dept)
    db.session.add(student)
    db.session.commit()

    return redirect('/admin_home')

@app.route('/submit_participant',methods=['POST'])
def submit_participant():
    p_username = request.form['p_username']
    p_password = request.form['p_password']
    p_name     = request.form['p_name']
    p_gender   = request.form['p_gender']
    p_email    = request.form['p_email']
    p_mob      = request.form['p_mob']
    p_college  = request.form['p_college']
    p_dept     = request.form['p_dept']
    p_place    = request.form['p_place']

    participant=Participant(p_username,p_password,p_name,p_gender,p_email,p_mob,p_college,p_dept,p_place)
    db.session.add(participant)
    db.session.commit()

    return render_template('index.html')

@app.route('/submit_participant_admin',methods=['POST'])
def submit_participant_admin():
    p_username = request.form['p_username']
    p_password = request.form['p_password']
    p_name     = request.form['p_name']
    p_gender   = request.form['p_gender']
    p_email    = request.form['p_email']
    p_mob      = request.form['p_mob']
    p_college  = request.form['p_college']
    p_dept     = request.form['p_dept']
    p_place    = request.form['p_place']

    participant=Participant(p_username,p_password,p_name,p_gender,p_email,p_mob,p_college,p_dept,p_place)
    db.session.add(participant)
    db.session.commit()

    return redirect('/admin_home')

@app.route('/submit_organizer',methods=['POST'])
def submit_organizer():
    o_username = request.form['o_username']
    o_password = request.form['o_password']
    o_name     = request.form['o_name']
    o_gender   = request.form['o_gender']
    o_email    = request.form['o_email']
    o_mob      = request.form['o_mob']
    o_role     = request.form['o_role']

    organizer=Organizer(o_username,o_password,o_name,o_gender,o_email,o_mob,o_role)
    db.session.add(organizer)
    db.session.commit()

    return render_template('index.html')

@app.route('/submit_organizer_admin',methods=['POST'])
def submit_organizer_admin():
    o_username = request.form['o_username']
    o_password = request.form['o_password']
    o_name     = request.form['o_name']
    o_gender   = request.form['o_gender']
    o_email    = request.form['o_email']
    o_mob      = request.form['o_mob']
    o_role     = request.form['o_role']

    organizer=Organizer(o_username,o_password,o_name,o_gender,o_email,o_mob,o_role)
    db.session.add(organizer)
    db.session.commit()

    return redirect('admin_home')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check if the user exists in any of the tables
        user = Student.query.filter_by(s_username=username, s_password=password).first()
        if user:
            
            session['username'] = username
            session['user_type'] = 'student'
            return redirect('/student_home')

        user = Participant.query.filter_by(p_username=username, p_password=password).first()
        if user:
            session['username'] = username
            session['user_type'] = 'participant'
            return redirect('/participant_home')

        user = Organizer.query.filter_by(o_username=username, o_password=password).first()
        if user:
            session['username'] = username
            session['user_type'] = 'organizer'
            return redirect('/organizer_home')
        
        user = Admin.query.filter_by(a_username=username,a_password=password).first()
        if user:
            session['username'] = username
            session['user_type']= 'admin'
            return redirect('/admin_home')

        return render_template('login.html', message='Invalid username or password')
    else:
        return render_template('login.html')

@app.route('/student_home')
def student_home():
    if 'username' in session and session['user_type'] == 'student':
        # Get today's date
        today = datetime.now().date()
        # Query events that are today or in the future
        events = Event.query.filter(Event.date >= today).all()
        # Pass the filtered events to the template

        return render_template('student.html', events=events,username=session['username'])
    else:
        return redirect('/login')
    
    
# Participant home route
@app.route('/participant_home')
def participant_home():
    if 'username' in session and session['user_type'] == 'participant':
        today = datetime.now().date()
        # Query events that are today or in the future
        events = Event.query.filter(Event.date >= today).all()
        # Pass the filtered events to the template
        return render_template('participant.html', events=events,username=session['username'])
    else:
        return redirect('/login')

# # Organizer home route
# @app.route('/organizer_home')
# def organizer_home():
#     if 'username' in session and session['user_type'] == 'organizer':
#         return render_template('organizer.html')
#     else:
#         return redirect('/login')
    
@app.route('/admin_home')
def admin_home():
    if 'username' in session and session['user_type'] == 'admin':
        # Fetch data from all three tables
        students = Student.query.all()
        participants = Participant.query.all()
        organizers = Organizer.query.all()

        return render_template('admin.html', students=students, participants=participants, organizers=organizers)
    else:
        return redirect('/login')    
@app.route('/organizer_home')
def organizer_home():
    if 'username' in session and session['user_type'] == 'organizer':
        # Retrieve all events from the database
        events = Event.query.all()

        # Create a dictionary to store volunteers for each event
        event_volunteers = {}

        # Retrieve volunteers for each event
        for event in events:
            volunteers = Volunteer.query.filter_by(eventid=event.eventid).all()
            event_volunteers[event.eventid] = volunteers

        return render_template('organizer.html', events=events, event_volunteers=event_volunteers,username=session['username'])
    else:
        return redirect('/login') 


@app.route('/delete_student/<username>', methods=['POST'])
def delete_student(username):
    student = Student.query.filter_by(s_username=username).first()
    if student:
        db.session.delete(student)
        db.session.commit()
        return jsonify(success=True, message="Student deleted successfully.")
    else:
        return jsonify(success=False, message="Student not found.")

@app.route('/delete_participant/<username>', methods=['POST'])
def delete_participant(username):
    participant = Participant.query.filter_by(p_username=username).first()
    if participant:
        db.session.delete(participant)
        db.session.commit()
        return jsonify(success=True, message="Participant deleted successfully.")
    else:
        return jsonify(success=False, message="Participant not found.")

@app.route('/delete_organizer/<username>', methods=['POST'])
def delete_organizer(username):
    organizer = Organizer.query.filter_by(o_username=username).first()
    if organizer:
        db.session.delete(organizer)
        db.session.commit()
        return jsonify(success=True, message="Organizer deleted successfully.")
    else:
        return jsonify(success=False, message="Organizer not found.")      
@app.route('/register', methods=['POST'])
def register():
    eventid = request.form['eventid']
    # username = request.form['username']
    username = session.get('username')
    # Check if the user is already registered for the event
    existing_registration = Registration.query.filter_by(username=username, eventid=eventid).first()
    if existing_registration:
        return jsonify(success=False, message="You are already registered for this event.")
    
    # Create a new registration entry in the database
    registration = Registration(username=username, eventid=eventid)
    db.session.add(registration)
    db.session.commit()
    return jsonify(success=True, message="Registration successful.")

# Route to cancel registration for an event
@app.route('/cancel_registration', methods=['POST'])
def cancel_registration():
    eventid = request.form['eventid']
    username = session['username']
    # Find the registration entry for the user and event
    registration = Registration.query.filter_by(username=username, eventid=eventid).first()
    if not registration:
        return jsonify(success=False, message="You are not registered for this event.")
    
    # Delete the registration entry from the database
    db.session.delete(registration)
    db.session.commit()
    return jsonify(success=True, message="Registration canceled successfully.")

# Route to volunteer for an event
@app.route('/volunteer', methods=['POST'])
def volunteer():
    eventid = request.form['eventid']
    username = session['username']
    # Check if the user is already volunteered for the event
    existing_volunteer = Volunteer.query.filter_by(username=username, eventid=eventid).first()
    if existing_volunteer:
        return jsonify(success=False, message="You are already volunteered for this event.")
    
    # Create a new volunteer entry in the database
    volunteer = Volunteer(username=username, eventid=eventid)
    db.session.add(volunteer)
    db.session.commit()
    return jsonify(success=True, message="Volunteering successful.")

# Route to cancel volunteering for an event
@app.route('/cancel_volunteering', methods=['POST'])
def cancel_volunteering():
    eventid = request.form['eventid']
    username = session['username']
    # Find the volunteer entry for the user and event
    volunteer = Volunteer.query.filter_by(username=username, eventid=eventid).first()
    if not volunteer:
        return jsonify(success=False, message="You are not volunteered for this event.")
    
    # Delete the volunteer entry from the database
    db.session.delete(volunteer)
    db.session.commit()
    return jsonify(success=True, message="Volunteering canceled successfully.")
@app.route('/winners2')
def winners2():
    events = db.session.query(Event).join(Winner, Event.eventid == Winner.eventid).distinct(Event.eventid).all()
    
    # Group winners by eventid
    event_winners = {}
    for event in events:
        winners = Winner.query.filter_by(eventid=event.eventid).all()
        event_winners[event] = winners
    
    # Pass the event_winners to the template
    return render_template('winner2.html', event_winners=event_winners)

@app.route('/winners')
def winners():
    # Query all events that have winners recorded in the winners table
    events = db.session.query(Event).join(Winner, Event.eventid == Winner.eventid).distinct(Event.eventid).all()
    
    # Group winners by eventid
    event_winners = {}
    for event in events:
        winners = Winner.query.filter_by(eventid=event.eventid).all()
        event_winners[event] = winners
    
    # Pass the event_winners to the template
    return render_template('winner.html', event_winners=event_winners)
# Route to display logistics form
@app.route('/logistics')
def logistics():
    return render_template('logistics.html')

@app.route('/accommodation')
def accommodation():
    # Fetch data from the Logistic table
    accommodations = Logistic.query.all()
    # Render the accommodation.html template with the fetched data
    return render_template('accommodation.html', accommodations=accommodations)
# Route to handle logistics form submission
@app.route('/submit_logistics', methods=['POST'])
def submit_logistics():
    # Get form data
    food = request.form.get('food')
    hostel = request.form.get('hostel')
    username = request.form.get('username')
    gender = request.form.get('gender')

    # Create a new logistic entry
    new_logistic = Logistic(username=username, food=food, hostel=hostel, gender=gender)

    try:
        # Add and commit to database
        db.session.add(new_logistic)
        db.session.commit()
        # flash('Your operation was successful!', 'success')
        # message = "Logistics information submitted successfully!"
        return redirect('/participant_home')
    except:
        return "There was an error submitting the logistics information."
    
@app.route('/add_winner_form')
def add_winner_form():
    return render_template('add.html')

# Route to add a winner
@app.route('/add_winner', methods=['POST'])
def add_winner():
    eventid = request.form['eventid']
    username = request.form['username']
    rank = request.form['rank']

    # Create a new Winner object
    new_winner = Winner(eventid=eventid, username=username, rank=rank)

    # Add the new winner to the database
    db.session.add(new_winner)
    db.session.commit()

    # Redirect to the add winner form
    return redirect('/add_winner_form')   
# Logout route
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')


if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)       