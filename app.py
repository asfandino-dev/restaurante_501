import os
from flask import Flask, render_template, redirect, url_for, flash, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_migrate import Migrate
from functools import wraps
from datetime import datetime, date, timedelta
from sqlalchemy import func

from models import db, User, Clinic, Specialty, Doctor, Appointment

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mediconnect-secret-key-12345'
# Using SQLite as default for local execution if DATABASE_URL is not set
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///mediconnect.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

# RBAC Decorator
def role_required(*roles):
    def decorator(f):
        @wraps(f)
        @login_required
        def decorated_function(*args, **kwargs):
            if current_user.role not in roles:
                flash('No tienes permiso para acceder a esta página.', 'danger')
                return redirect(url_for('index'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator

# --- Routes ---

@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('dashboard'))
        flash('Credenciales inválidas.', 'danger')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    today = date.today()
    if current_user.role == 'Administrador':
        # Dashboard metrics for last 30 days
        thirty_days_ago = today - timedelta(days=30)
        total_apps = Appointment.query.filter(Appointment.date >= thirty_days_ago).count()
        attended_apps = Appointment.query.filter(Appointment.date >= thirty_days_ago, Appointment.status == 'Atendida').count()
        absent_apps = Appointment.query.filter(Appointment.date >= thirty_days_ago, Appointment.status == 'Ausente').count()

        occupancy = (attended_apps / total_apps * 100) if total_apps > 0 else 0
        absenteeism = (absent_apps / total_apps * 100) if total_apps > 0 else 0

        return render_template('dashboard.html', occupancy=occupancy, absenteeism=absenteeism, total_apps=total_apps)

    elif current_user.role == 'Medico':
        # Daily agenda for doctor
        doctor = Doctor.query.filter_by(user_id=current_user.id).first()
        appointments = Appointment.query.filter_by(doctor_id=doctor.id, date=today).order_by(Appointment.time).all()
        return render_template('dashboard.html', appointments=appointments)

    elif current_user.role == 'Paciente':
        # Patient's upcoming appointments
        appointments = Appointment.query.filter(Appointment.patient_id == current_user.id, Appointment.date >= today).order_by(Appointment.date, Appointment.time).all()
        return render_template('dashboard.html', appointments=appointments)

    elif current_user.role == 'Recepcionista':
        # Today's appointments across the clinic
        appointments = Appointment.query.filter_by(date=today).order_by(Appointment.time).all()
        return render_template('dashboard.html', appointments=appointments)

    return render_template('dashboard.html')

# HU 10: CRUD Sedes and Especialidades
@app.route('/entities', methods=['GET', 'POST'])
@role_required('Administrador')
def entities():
    clinics = Clinic.query.all()
    specialties = Specialty.query.all()
    return render_template('entities.html', clinics=clinics, specialties=specialties)

@app.route('/clinic/add', methods=['POST'])
@role_required('Administrador')
def add_clinic():
    name = request.form.get('name')
    address = request.form.get('address')
    new_clinic = Clinic(name=name, address=address)
    db.session.add(new_clinic)
    db.session.commit()
    flash('Sede agregada.', 'success')
    return redirect(url_for('entities'))

@app.route('/specialty/add', methods=['POST'])
@role_required('Administrador')
def add_specialty():
    name = request.form.get('name')
    new_specialty = Specialty(name=name)
    db.session.add(new_specialty)
    db.session.commit()
    flash('Especialidad agregada.', 'success')
    return redirect(url_for('entities'))

@app.route('/clinic/edit/<int:id>', methods=['POST'])
@role_required('Administrador')
def edit_clinic(id):
    clinic = db.session.get(Clinic, id)
    clinic.name = request.form.get('name')
    clinic.address = request.form.get('address')
    db.session.commit()
    flash('Sede actualizada.', 'success')
    return redirect(url_for('entities'))

@app.route('/clinic/delete/<int:id>')
@role_required('Administrador')
def delete_clinic(id):
    clinic = db.session.get(Clinic, id)
    db.session.delete(clinic)
    db.session.commit()
    flash('Sede eliminada.', 'success')
    return redirect(url_for('entities'))

@app.route('/specialty/edit/<int:id>', methods=['POST'])
@role_required('Administrador')
def edit_specialty(id):
    specialty = db.session.get(Specialty, id)
    specialty.name = request.form.get('name')
    db.session.commit()
    flash('Especialidad actualizada.', 'success')
    return redirect(url_for('entities'))

@app.route('/specialty/delete/<int:id>')
@role_required('Administrador')
def delete_specialty(id):
    specialty = db.session.get(Specialty, id)
    db.session.delete(specialty)
    db.session.commit()
    flash('Especialidad eliminada.', 'success')
    return redirect(url_for('entities'))

# HU 02: Booking
@app.route('/booking', methods=['GET', 'POST'])
@role_required('Paciente')
def booking():
    if request.method == 'POST':
        doctor_id = request.form.get('doctor_id')
        clinic_id = request.form.get('clinic_id')
        date_str = request.form.get('date')
        time_str = request.form.get('time')

        app_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        app_time = datetime.strptime(time_str, '%H:%M').time()

        # Check availability
        existing = Appointment.query.filter_by(
            doctor_id=doctor_id,
            date=app_date,
            time=app_time,
            status='Agendada'
        ).first()

        if existing:
            flash('El horario ya no está disponible.', 'danger')
        else:
            new_app = Appointment(
                patient_id=current_user.id,
                doctor_id=doctor_id,
                clinic_id=clinic_id,
                date=app_date,
                time=app_time,
                status='Agendada'
            )
            db.session.add(new_app)
            try:
                db.session.commit()
                flash('Cita reservada con éxito.', 'success')
                return redirect(url_for('dashboard'))
            except Exception as e:
                db.session.rollback()
                flash('Error al reservar la cita. Intente de nuevo.', 'danger')

    doctors = Doctor.query.all()
    clinics = Clinic.query.all()
    return render_template('booking.html', doctors=doctors, clinics=clinics, today=date.today().isoformat())

# HU 03: Cancel Appointment
@app.route('/appointment/cancel/<int:id>')
@login_required
def cancel_appointment(id):
    appointment = db.session.get(Appointment, id)
    if not appointment:
        flash('Cita no encontrada.', 'danger')
        return redirect(url_for('dashboard'))
    if current_user.role == 'Paciente' and appointment.patient_id != current_user.id:
        flash('No autorizado.', 'danger')
        return redirect(url_for('dashboard'))

    appointment.status = 'Cancelada'
    db.session.commit()
    flash('Cita cancelada.', 'success')
    return redirect(url_for('dashboard'))

# HU 08: Master Agenda for Receptionist
@app.route('/calendar')
@role_required('Recepcionista', 'Administrador')
def calendar():
    doctors = Doctor.query.all()
    appointments = Appointment.query.all()
    return render_template('calendar.html', doctors=doctors, appointments=appointments)

# HU 11: Doctor checks appointment info
@app.route('/appointment/status/<int:id>/<string:status>')
@role_required('Medico', 'Recepcionista')
def update_appointment_status(id, status):
    appointment = db.session.get(Appointment, id)
    if not appointment:
        flash('Cita no encontrada.', 'danger')
        return redirect(url_for('dashboard'))
    if status in ['Atendida', 'Ausente', 'Agendada', 'Cancelada']:
        appointment.status = status
        db.session.commit()
        flash(f'Estado de la cita actualizado a {status}.', 'success')
    return redirect(request.referrer or url_for('dashboard'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5000)
