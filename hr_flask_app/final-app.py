from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime

# Initialisation de l'application Flask
app = Flask(__name__)
CORS(app)

# Configuration de la base de données SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///employees.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Modèle Employee
class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    EmployeeName = db.Column(db.String(100), nullable=False)
    Salary = db.Column(db.Float)
    Position = db.Column(db.String(100))
    State = db.Column(db.String(10))
    DateOfBirth = db.Column(db.String(10))
    Gender = db.Column(db.String(1))
    MaritalStatus = db.Column(db.String(20))
    HiringDate = db.Column(db.String(10))
    TerminationDate = db.Column(db.String(10), nullable=True)
    EmploymentStatus = db.Column(db.String(50))
    Department = db.Column(db.String(50))
    RecruitmentSource = db.Column(db.String(50))
    PerformanceScore = db.Column(db.String(50))
    EngagementSurvey = db.Column(db.Float)
    EmployeeSatisfaction = db.Column(db.Integer)
    absences = db.relationship('Absence', backref='employee', lazy=True)
    trainings = db.relationship('TrainingEnrollment', backref='employee', lazy=True)

# Modèle Absence
class Absence(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    EmployeeID = db.Column(db.Integer, db.ForeignKey('employee.id'), nullable=False)
    AbsenceDate = db.Column(db.String(10), nullable=False)
    Reason = db.Column(db.String(200))

# Modèle Formation
class Training(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    duration_hours = db.Column(db.Integer)
    skill_category = db.Column(db.String(100))
    max_participants = db.Column(db.Integer)
    status = db.Column(db.String(50))
    creation_date = db.Column(db.DateTime, default=datetime.utcnow)
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
    enrollments = db.relationship('TrainingEnrollment', backref='training', lazy=True)

# Modèle Inscription Formation
class TrainingEnrollment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'), nullable=False)
    training_id = db.Column(db.Integer, db.ForeignKey('training.id'), nullable=False)
    enrollment_date = db.Column(db.DateTime, default=datetime.utcnow)
    completion_date = db.Column(db.DateTime)
    status = db.Column(db.String(50))
    score = db.Column(db.Float)
    feedback = db.Column(db.Text)
    impact_score = db.Column(db.Integer)

# Routes pour la gestion des employés

@app.route('/api/employees', methods=['GET'])
def get_employees():
    employees = Employee.query.all()
    employees_list = [
        {
            "EmployeeID": emp.id,
            "EmployeeName": emp.EmployeeName,
            "Salary": emp.Salary,
            "Position": emp.Position,
            "State": emp.State,
            "DateOfBirth": emp.DateOfBirth,
            "Gender": emp.Gender,
            "MaritalStatus": emp.MaritalStatus,
            "HiringDate": emp.HiringDate,
            "TerminationDate": emp.TerminationDate,
            "EmploymentStatus": emp.EmploymentStatus,
            "Department": emp.Department,
            "RecruitmentSource": emp.RecruitmentSource,
            "PerformanceScore": emp.PerformanceScore,
            "EngagementSurvey": emp.EngagementSurvey,
            "EmployeeSatisfaction": emp.EmployeeSatisfaction,
            "AbsenceCount": len(emp.absences),
            "TrainingCount": len(emp.trainings)
        } for emp in employees
    ]
    return jsonify(employees_list)

@app.route('/api/employees', methods=['POST'])
def add_employee():
    data = request.get_json()
    if not data:
        return jsonify({'message': 'Aucune donnée reçue'}), 400

    new_employee = Employee(
        EmployeeName=data['EmployeeName'],
        Salary=data.get('Salary'),
        Position=data.get('Position'),
        State=data.get('State'),
        DateOfBirth=data.get('DateOfBirth'),
        Gender=data.get('Gender'),
        MaritalStatus=data.get('MaritalStatus'),
        HiringDate=data.get('HiringDate'),
        TerminationDate=data.get('TerminationDate'),
        EmploymentStatus=data.get('EmploymentStatus'),
        Department=data.get('Department'),
        RecruitmentSource=data.get('RecruitmentSource'),
        PerformanceScore=data.get('PerformanceScore'),
        EngagementSurvey=data.get('EngagementSurvey'),
        EmployeeSatisfaction=data.get('EmployeeSatisfaction')
    )
    db.session.add(new_employee)
    db.session.commit()
    return jsonify({'message': 'Employé ajouté avec succès', 'id': new_employee.id}), 201

@app.route('/api/employees/<int:employee_id>', methods=['PUT'])
def update_employee(employee_id):
    employee = Employee.query.get_or_404(employee_id)
    data = request.get_json()

    if not data:
        return jsonify({'message': 'Aucune donnée reçue'}), 400

    for key, value in data.items():
        if hasattr(employee, key):
            setattr(employee, key, value)

    db.session.commit()
    return jsonify({'message': 'Employé mis à jour avec succès'})

@app.route('/api/employees/<int:employee_id>', methods=['DELETE'])
def delete_employee(employee_id):
    employee = Employee.query.get_or_404(employee_id)
    db.session.delete(employee)
    db.session.commit()
    return jsonify({'message': 'Employé supprimé avec succès'})

# Routes pour la gestion des absences

@app.route('/api/absences', methods=['POST'])
def add_absence():
    data = request.get_json()
    if not data:
        return jsonify({'message': 'Aucune donnée reçue'}), 400

    if 'EmployeeID' not in data or 'AbsenceDate' not in data:
        return jsonify({'message': 'Données incomplètes'}), 400

    new_absence = Absence(
        EmployeeID=data['EmployeeID'],
        AbsenceDate=data['AbsenceDate'],
        Reason=data.get('Reason')
    )
    db.session.add(new_absence)
    db.session.commit()
    return jsonify({'message': 'Absence ajoutée avec succès'}), 201

@app.route('/api/absences/<int:absence_id>', methods=['DELETE'])
def delete_absence(absence_id):
    absence = Absence.query.get_or_404(absence_id)
    db.session.delete(absence)
    db.session.commit()
    return jsonify({'message': 'Absence supprimée avec succès'})

# Routes pour la gestion des formations

@app.route('/api/trainings', methods=['GET'])
def get_trainings():
    trainings = Training.query.all()
    return jsonify([{
        'id': t.id,
        'title': t.title,
        'description': t.description,
        'duration_hours': t.duration_hours,
        'skill_category': t.skill_category,
        'max_participants': t.max_participants,
        'status': t.status,
        'start_date': t.start_date.isoformat() if t.start_date else None,
        'end_date': t.end_date.isoformat() if t.end_date else None,
        'enrolled_count': len(t.enrollments)
    } for t in trainings])

@app.route('/api/trainings', methods=['POST'])
def create_training():
    data = request.get_json()
    if not data:
        return jsonify({'message': 'Aucune donnée reçue'}), 400

    new_training = Training(
        title=data['title'],
        description=data.get('description'),
        duration_hours=data.get('duration_hours'),
        skill_category=data.get('skill_category'),
        max_participants=data.get('max_participants'),
        status=data.get('status', 'planned'),
        start_date=datetime.fromisoformat(data['start_date']) if 'start_date' in data else None,
        end_date=datetime.fromisoformat(data['end_date']) if 'end_date' in data else None
    )
    
    db.session.add(new_training)
    db.session.commit()
    return jsonify({'message': 'Formation créée avec succès', 'id': new_training.id}), 201

@app.route('/api/trainings/<int:training_id>', methods=['PUT'])
def update_training(training_id):
    training = Training.query.get_or_404(training_id)
    data = request.get_json()

    if 'title' in data:
        training.title = data['title']
    if 'description' in data:
        training.description = data['description']
    if 'duration_hours' in data:
        training.duration_hours = data['duration_hours']
    if 'skill_category' in data:
        training.skill_category = data['skill_category']
    if 'max_participants' in data:
        training.max_participants = data['max_participants']
    if 'status' in data:
        training.status = data['status']
    if 'start_date' in data:
        training.start_date = datetime.fromisoformat(data['start_date'])
    if 'end_date' in data:
        training.end_date = datetime.fromisoformat(data['end_date'])

    db.session.commit()
    return jsonify({'message': 'Formation mise à jour avec succès'})

@app.route('/api/training-enrollments', methods=['POST'])
def enroll_employee():
    data = request.get_json()
    if not data or 'employee_id' not in data or 'training_id' not in data:
        return jsonify({'message': 'Données manquantes'}), 400

    # Vérifications
    employee = Employee.query.get_or_404(data['employee_id'])
    training = Training.query.get_or_404(data['training_id'])

    existing_enrollment = TrainingEnrollment.query.filter_by(
        employee_id=data['employee_id'],
        training_id=data['training_id']
    ).first()

    if existing_enrollment:
        return jsonify({'message': 'Employé déjà inscrit à cette formation'}), 400

    if training.max_participants and len(training.enrollments) >= training.max_participants:
        return jsonify({'message': 'Formation complète'}), 400

    new_enrollment = TrainingEnrollment(
        employee_id=data['employee_id'],
        training_id=data['training_id'],
        status='enrolled'
    )
    
    db.session.add(new_enrollment)
    db.session.commit()
    return jsonify({'message': 'Inscription réussie'}), 201

@app.route('/api/training-enrollments/<int:enrollment_id>', methods=['PUT'])
def update_enrollment(enrollment_id):
    enrollment = TrainingEnrollment.query.get_or_404(enrollment_id)
    data = request.get_json()

    if 'status' in data:
        enrollment.status = data['status']
    if 'score' in data:
        enrollment.score = data['score']
    if 'feedback' in data:
        enrollment.feedback = data['feedback']
    if 'impact_score' in data:
        enrollment.impact_score = data['impact_score']
    if 'completion_date' in data:
        enrollment.completion_date = datetime.fromisoformat(data['completion_date'])

    db.session.commit()
    return jsonify({'message': 'Inscription mise à jour avec succès'})

@app.route('/api/employees/<int:employee_id>/training-stats', methods=['GET'])
def get_employee_training_stats(employee_id):
    employee = Employee.query.get_or_404(employee_id)
    enrollments = TrainingEnrollment.query.filter_by(employee_id=employee_id).all()
    
    completed_trainings = [e for e in enrollments if e.status == 'completed']
    avg_score = sum(e.score for e in completed_trainings if e.score) / len(completed_trainings) if completed_trainings else 0
    
    return jsonify({
        'total_trainings': len(enrollments),
        'completed_trainings': len(completed_trainings),
        'in_progress_trainings': len([e for e in enrollments if e.status == 'in_progress']),
        'average_score': round(avg_score, 2),
        'total_training_hours': sum(e.training.duration_hours for e in completed_trainings),
        'skills_acquired': list(set(e.training.skill_category for e in completed_trainings))
    })

# Création des tables dans la base de données
with app.app_context():
    db.create_all()

# Lancement de l'application
if __name__ == '__main__':
    app.run(debug=True)
