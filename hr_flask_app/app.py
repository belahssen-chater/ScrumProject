from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

# Initialisation de l'application Flask
app = Flask(__name__)
CORS(app)

# Configuration de la base de données SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///employees.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Définir le modèle Employee pour SQLAlchemy
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

# Définir le modèle Absence pour SQLAlchemy
class Absence(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    EmployeeID = db.Column(db.Integer, db.ForeignKey('employee.id'), nullable=False)
    AbsenceDate = db.Column(db.String(10), nullable=False)
    Reason = db.Column(db.String(200))
    employee = db.relationship('Employee', backref=db.backref('absences', lazy=True))

# Créer la base de données (si elle n'existe pas déjà)
with app.app_context():
    db.create_all()

# Récupérer tous les employés
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
            "AbsenceCount": len(emp.absences)
        } for emp in employees
    ]
    return jsonify(employees_list)

# Ajouter un nouvel employé
@app.route('/api/employees', methods=['POST'])
def add_employee():
    new_employee_data = request.get_json()
    if not new_employee_data:
        return jsonify({'message': 'Aucune donnée reçue'}), 400

    new_employee = Employee(
        EmployeeName=new_employee_data['EmployeeName'],
        Salary=new_employee_data.get('Salary'),
        Position=new_employee_data.get('Position'),
        State=new_employee_data.get('State'),
        DateOfBirth=new_employee_data.get('DateOfBirth'),
        Gender=new_employee_data.get('Gender'),
        MaritalStatus=new_employee_data.get('MaritalStatus'),
        HiringDate=new_employee_data.get('HiringDate'),
        TerminationDate=new_employee_data.get('TerminationDate'),
        EmploymentStatus=new_employee_data.get('EmploymentStatus'),
        Department=new_employee_data.get('Department'),
        RecruitmentSource=new_employee_data.get('RecruitmentSource'),
        PerformanceScore=new_employee_data.get('PerformanceScore'),
        EngagementSurvey=new_employee_data.get('EngagementSurvey'),
        EmployeeSatisfaction=new_employee_data.get('EmployeeSatisfaction')
    )
    db.session.add(new_employee)
    db.session.commit()
    return jsonify({'message': 'Employé ajouté avec succès'}), 201

# Mettre à jour un employé
@app.route('/api/employees/<int:employee_id>', methods=['PUT'])
def update_employee(employee_id):
    updated_data = request.get_json()
    if not updated_data:
        return jsonify({'message': 'Aucune donnée reçue'}), 400

    employee = Employee.query.get(employee_id)
    if employee:
        employee.EmployeeName = updated_data.get('EmployeeName', employee.EmployeeName)
        employee.Salary = updated_data.get('Salary', employee.Salary)
        employee.Position = updated_data.get('Position', employee.Position)
        employee.State = updated_data.get('State', employee.State)
        employee.DateOfBirth = updated_data.get('DateOfBirth', employee.DateOfBirth)
        employee.Gender = updated_data.get('Gender', employee.Gender)
        employee.MaritalStatus = updated_data.get('MaritalStatus', employee.MaritalStatus)
        employee.HiringDate = updated_data.get('HiringDate', employee.HiringDate)
        employee.TerminationDate = updated_data.get('TerminationDate', employee.TerminationDate)
        employee.EmploymentStatus = updated_data.get('EmploymentStatus', employee.EmploymentStatus)
        employee.Department = updated_data.get('Department', employee.Department)
        employee.RecruitmentSource = updated_data.get('RecruitmentSource', employee.RecruitmentSource)
        employee.PerformanceScore = updated_data.get('PerformanceScore', employee.PerformanceScore)
        employee.EngagementSurvey = updated_data.get('EngagementSurvey', employee.EngagementSurvey)
        employee.EmployeeSatisfaction = updated_data.get('EmployeeSatisfaction', employee.EmployeeSatisfaction)

        db.session.commit()
        return jsonify({'message': 'Employé mis à jour avec succès'})
    else:
        return jsonify({'message': 'Employé non trouvé'}), 404

# Supprimer un employé
@app.route('/api/employees/<int:employee_id>', methods=['DELETE'])
def delete_employee(employee_id):
    employee = Employee.query.get(employee_id)
    if employee:
        db.session.delete(employee)
        db.session.commit()
        return jsonify({'message': 'Employé supprimé avec succès'})
    else:
        return jsonify({'message': 'Employé non trouvé'}), 404

# Ajouter une absence
@app.route('/api/absences', methods=['POST'])
def add_absence():
    new_absence_data = request.get_json()
    if not new_absence_data:
        return jsonify({'message': 'Aucune donnée reçue'}), 400

    required_fields = ['EmployeeID', 'AbsenceDate']
    for field in required_fields:
        if field not in new_absence_data:
            return jsonify({'message': f'Le champ {field} est requis'}), 400

    employee = Employee.query.get(new_absence_data['EmployeeID'])
    if not employee:
        return jsonify({'message': 'Employé non trouvé'}), 404

    new_absence = Absence(
        EmployeeID=new_absence_data['EmployeeID'],
        AbsenceDate=new_absence_data['AbsenceDate'],
        Reason=new_absence_data.get('Reason')
    )
    db.session.add(new_absence)
    db.session.commit()
    return jsonify({'message': 'Absence ajoutée avec succès'}), 201

# Supprimer une absence
@app.route('/api/absences/<int:absence_id>', methods=['DELETE'])
def delete_absence(absence_id):
    absence = Absence.query.get(absence_id)
    if absence:
        db.session.delete(absence)
        db.session.commit()
        return jsonify({'message': 'Absence supprimée avec succès'})
    else:
        return jsonify({'message': 'Absence non trouvée'}), 404

# Lancer l'application Flask
if __name__ == '__main__':
    app.run(debug=True)
