from app import app, db
from models import User, Clinic, Specialty, Doctor, Appointment
from datetime import date, time, timedelta

def seed():
    with app.app_context():
        # Clean existing data
        db.drop_all()
        db.create_all()

        # Users
        admin = User(document_id='1001', full_name='Admin Mediconnect', email='admin@mediconnect.com', phone='5550001', role='Administrador')
        admin.set_password('admin123')

        recep = User(document_id='1002', full_name='Rosa Recepción', email='recepcion@mediconnect.com', phone='5550002', role='Recepcionista')
        recep.set_password('recep123')

        medico1 = User(document_id='2001', full_name='Dr. Juan Perez', email='juan.perez@mediconnect.com', phone='5550003', role='Medico')
        medico1.set_password('medico123')

        medico2 = User(document_id='2002', full_name='Dra. Maria Lopez', email='maria.lopez@mediconnect.com', phone='5550004', role='Medico')
        medico2.set_password('medico123')

        paciente1 = User(document_id='3001', full_name='Carlos Cliente', email='carlos@paciente.com', phone='5550005', role='Paciente')
        paciente1.set_password('paciente123')

        db.session.add_all([admin, recep, medico1, medico2, paciente1])
        db.session.commit()

        # Clinics
        c1 = Clinic(name='Sede Norte', address='Calle 100 # 15-20')
        c2 = Clinic(name='Sede Sur', address='Carrera 10 # 1-50')
        db.session.add_all([c1, c2])
        db.session.commit()

        # Specialties
        s1 = Specialty(name='Medicina General')
        s2 = Specialty(name='Pediatría')
        s3 = Specialty(name='Cardiología')
        db.session.add_all([s1, s2, s3])
        db.session.commit()

        # Doctors
        d1 = Doctor(user_id=medico1.id, specialty_id=s1.id, clinic_id=c1.id)
        d2 = Doctor(user_id=medico2.id, specialty_id=s2.id, clinic_id=c2.id)
        db.session.add_all([d1, d2])
        db.session.commit()

        # Appointments
        today = date.today()
        a1 = Appointment(patient_id=paciente1.id, doctor_id=d1.id, clinic_id=c1.id, date=today, time=time(8, 0), status='Agendada')
        a2 = Appointment(patient_id=paciente1.id, doctor_id=d1.id, clinic_id=c1.id, date=today - timedelta(days=5), time=time(9, 0), status='Atendida')
        a3 = Appointment(patient_id=paciente1.id, doctor_id=d2.id, clinic_id=c2.id, date=today - timedelta(days=2), time=time(10, 0), status='Ausente')

        db.session.add_all([a1, a2, a3])
        db.session.commit()

        print("Database seeded successfully!")

if __name__ == '__main__':
    seed()
