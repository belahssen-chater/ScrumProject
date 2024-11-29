import React, { useEffect, useState } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [employees, setEmployees] = useState([]);
  const [absences, setAbsences] = useState([]);
  const [showEmployeeList, setShowEmployeeList] = useState(false);
  const [showAbsenceList, setShowAbsenceList] = useState(false);
  const [newEmployee, setNewEmployee] = useState({
    EmployeeName: '',
    Position: '',
    Salary: '',
    EmploymentStatus: '',
    State: '',
    DateOfBirth: '',
    Gender: '',
    MaritalStatus: '',
    HiringDate: '',
    TerminationDate: '',
    Department: '',
    RecruitmentSource: '',
    PerformanceScore: '',
    EngagementSurvey: '',
    EmployeeSatisfaction: '',
    AbsenceCount: 0
  });
  const [editEmployee, setEditEmployee] = useState(null);
  const [newAbsence, setNewAbsence] = useState({
    EmployeeID: '',
    AbsenceDate: '',
    Reason: ''
  });

  useEffect(() => {
    fetchEmployees();
    fetchAbsences();
  }, []);

  const fetchEmployees = async () => {
    try {
      const response = await axios.get('http://127.0.0.1:5000/api/employees');
      setEmployees(response.data);
    } catch (error) {
      console.error('Erreur lors de la récupération des employés', error);
    }
  };

  const fetchAbsences = async () => {
    try {
      const response = await axios.get('http://127.0.0.1:5000/api/absences');
      setAbsences(response.data);
    } catch (error) {
      console.error('Erreur lors de la récupération des absences', error);
    }
  };

  const handleAddEmployee = async () => {
    try {
      await axios.post('http://127.0.0.1:5000/api/employees', newEmployee);
      fetchEmployees();
      setNewEmployee({
        EmployeeName: '',
        Position: '',
        Salary: '',
        EmploymentStatus: '',
        State: '',
        DateOfBirth: '',
        Gender: '',
        MaritalStatus: '',
        HiringDate: '',
        TerminationDate: '',
        Department: '',
        RecruitmentSource: '',
        PerformanceScore: '',
        EngagementSurvey: '',
        EmployeeSatisfaction: '',
        AbsenceCount: 0
      });
    } catch (error) {
      console.error("Erreur lors de l'ajout de l'employé", error);
    }
  };

  const handleAddAbsence = async () => {
    try {
      await axios.post('http://127.0.0.1:5000/api/absences', newAbsence);
      fetchAbsences();
      fetchEmployees();
      setNewAbsence({
        EmployeeID: '',
        AbsenceDate: '',
        Reason: ''
      });
    } catch (error) {
      console.error("Erreur lors de l'ajout de l'absence", error);
    }
  };

  const handleDeleteEmployee = async (id) => {
    try {
      await axios.delete(`http://127.0.0.1:5000/api/employees/${id}`);
      fetchEmployees();
    } catch (error) {
      console.error("Erreur lors de la suppression de l'employé", error);
    }
  };

  const handleDeleteAbsence = async (id) => {
    try {
      await axios.delete(`http://127.0.0.1:5000/api/absences/${id}`);
      fetchAbsences();
      fetchEmployees();
    } catch (error) {
      console.error("Erreur lors de la suppression de l'absence", error);
    }
  };

  const handleEditEmployee = (employee) => {
    setEditEmployee({ ...employee });
  };

  const handleUpdateEmployee = async () => {
    if (!editEmployee) {
      console.error('Aucun employé sélectionné pour la mise à jour');
      return;
    }
    try {
      await axios.put(`http://127.0.0.1:5000/api/employees/${editEmployee.EmployeeID}`, editEmployee);
      fetchEmployees();
      setEditEmployee(null);
    } catch (error) {
      console.error("Erreur lors de la mise à jour de l'employé", error);
    }
  };

  const toggleEmployeeList = () => {
    setShowEmployeeList(!showEmployeeList);
  };

  const toggleAbsenceList = () => {
    setShowAbsenceList(!showAbsenceList);
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Application de Gestion des Ressources Humaines</h1>
        <div className="buttons-container">
          <button className="toggle-button" onClick={toggleEmployeeList}>
            {showEmployeeList ? 'Cacher la Liste des Employés' : 'Afficher la Liste des Employés'}
          </button>
          <button className="toggle-button" onClick={toggleAbsenceList}>
            {showAbsenceList ? 'Cacher la Liste des Absences' : 'Afficher la Liste des Absences'}
          </button>
        </div>
        {showEmployeeList && (
          <table className="employees-table">
            <thead>
              <tr>
                <th>ID</th>
                <th>Nom</th>
                <th>Poste</th>
                <th>Salaire</th>
                <th>Statut</th>
                <th>État</th>
                <th>Date de Naissance</th>
                <th>Genre</th>
                <th>Statut Marital</th>
                <th>Date d'Embauche</th>
                <th>Date de Fin</th>
                <th>Département</th>
                <th>Source de Recrutement</th>
                <th>Score de Performance</th>
                <th>Sondage d'Engagement</th>
                <th>Satisfaction</th>
                <th>Nombre d'Absences</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {employees.length > 0 ? (
                employees.map((employee) => (
                  <tr key={employee.EmployeeID}>
                    <td>{employee.EmployeeID}</td>
                    <td>{employee.EmployeeName}</td>
                    <td>{employee.Position}</td>
                    <td>{employee.Salary}</td>
                    <td>{employee.EmploymentStatus}</td>
                    <td>{employee.State}</td>
                    <td>{employee.DateOfBirth}</td>
                    <td>{employee.Gender}</td>
                    <td>{employee.MaritalStatus}</td>
                    <td>{employee.HiringDate}</td>
                    <td>{employee.TerminationDate}</td>
                    <td>{employee.Department}</td>
                    <td>{employee.RecruitmentSource}</td>
                    <td>{employee.PerformanceScore}</td>
                    <td>{employee.EngagementSurvey}</td>
                    <td>{employee.EmployeeSatisfaction}</td>
                    <td>{employee.AbsenceCount}</td>
                    <td>
                      <button
                        className="edit-button"
                        onClick={() => handleEditEmployee(employee)}
                      >
                        Modifier
                      </button>
                      <button
                        className="delete-button"
                        onClick={() => handleDeleteEmployee(employee.EmployeeID)}
                      >
                        Supprimer
                      </button>
                    </td>
                  </tr>
                ))
              ) : (
                <tr>
                  <td colSpan="18">Aucun employé trouvé</td>
                </tr>
              )}
            </tbody>
          </table>
        )}
        {showAbsenceList && (
          <table className="absences-table">
            <thead>
              <tr>
                <th>ID de l'Absence</th>
                <th>ID de l'Employé</th>
                <th>Date d'Absence</th>
                <th>Raison</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {absences.length > 0 ? (
                absences.map((absence) => (
                  <tr key={absence.AbsenceID}>
                    <td>{absence.AbsenceID}</td>
                    <td>{absence.EmployeeID}</td>
                    <td>{absence.AbsenceDate}</td>
                    <td>{absence.Reason}</td>
                    <td>
                      <button
                        className="delete-button"
                        onClick={() => handleDeleteAbsence(absence.AbsenceID)}
                      >
                        Supprimer
                      </button>
                    </td>
                  </tr>
                ))
              ) : (
                <tr>
                  <td colSpan="5">Aucune absence trouvée</td>
                </tr>
              )}
            </tbody>
          </table>
        )}
        <div className="add-employee-form">
          <h2>{editEmployee ? 'Modifier un Employé' : 'Ajouter un Employé'}</h2>
          <form
            onSubmit={(e) => {
              e.preventDefault();
              editEmployee ? handleUpdateEmployee() : handleAddEmployee();
            }}
          >
            <input
              type="text"
              placeholder="Nom de l'employé"
              value={editEmployee ? editEmployee.EmployeeName : newEmployee.EmployeeName}
              onChange={(e) =>
                editEmployee
                  ? setEditEmployee({ ...editEmployee, EmployeeName: e.target.value })
                  : setNewEmployee({ ...newEmployee, EmployeeName: e.target.value })
              }
            />
            <input
              type="text"
              placeholder="Poste"
              value={editEmployee ? editEmployee.Position : newEmployee.Position}
              onChange={(e) =>
                editEmployee
                  ? setEditEmployee({ ...editEmployee, Position: e.target.value })
                  : setNewEmployee({ ...newEmployee, Position: e.target.value })
              }
            />
            <input
              type="number"
              placeholder="Salaire"
              value={editEmployee ? editEmployee.Salary : newEmployee.Salary}
              onChange={(e) =>
                editEmployee
                  ? setEditEmployee({ ...editEmployee, Salary: e.target.value })
                  : setNewEmployee({ ...newEmployee, Salary: e.target.value })
              }
            />
            <input
              type="text"
              placeholder="Statut"
              value={editEmployee ? editEmployee.EmploymentStatus : newEmployee.EmploymentStatus}
              onChange={(e) =>
                editEmployee
                  ? setEditEmployee({ ...editEmployee, EmploymentStatus: e.target.value })
                  : setNewEmployee({ ...newEmployee, EmploymentStatus: e.target.value })
              }
            />
            <input
              type="text"
              placeholder="État"
              value={editEmployee ? editEmployee.State : newEmployee.State}
              onChange={(e) =>
                editEmployee
                  ? setEditEmployee({ ...editEmployee, State: e.target.value })
                  : setNewEmployee({ ...newEmployee, State: e.target.value })
              }
            />
            <input
              type="date"
              placeholder="Date de Naissance"
              value={editEmployee ? editEmployee.DateOfBirth : newEmployee.DateOfBirth}
              onChange={(e) =>
                editEmployee
                  ? setEditEmployee({ ...editEmployee, DateOfBirth: e.target.value })
                  : setNewEmployee({ ...newEmployee, DateOfBirth: e.target.value })
              }
            />
            <input
              type="text"
              placeholder="Genre"
              value={editEmployee ? editEmployee.Gender : newEmployee.Gender}
              onChange={(e) =>
                editEmployee
                  ? setEditEmployee({ ...editEmployee, Gender: e.target.value })
                  : setNewEmployee({ ...newEmployee, Gender: e.target.value })
              }
            />
            <input
              type="text"
              placeholder="Statut Marital"
              value={editEmployee ? editEmployee.MaritalStatus : newEmployee.MaritalStatus}
              onChange={(e) =>
                editEmployee
                  ? setEditEmployee({ ...editEmployee, MaritalStatus: e.target.value })
                  : setNewEmployee({ ...newEmployee, MaritalStatus: e.target.value })
              }
            />
            <input
              type="date"
              placeholder="Date d'Embauche"
              value={editEmployee ? editEmployee.HiringDate : newEmployee.HiringDate}
              onChange={(e) =>
                editEmployee
                  ? setEditEmployee({ ...editEmployee, HiringDate: e.target.value })
                  : setNewEmployee({ ...newEmployee, HiringDate: e.target.value })
              }
            />
            <input
              type="date"
              placeholder="Date de Fin"
              value={editEmployee ? editEmployee.TerminationDate : newEmployee.TerminationDate}
              onChange={(e) =>
                editEmployee
                  ? setEditEmployee({ ...editEmployee, TerminationDate: e.target.value })
                  : setNewEmployee({ ...newEmployee, TerminationDate: e.target.value })
              }
            />
            <input
              type="text"
              placeholder="Département"
              value={editEmployee ? editEmployee.Department : newEmployee.Department}
              onChange={(e) =>
                editEmployee
                  ? setEditEmployee({ ...editEmployee, Department: e.target.value })
                  : setNewEmployee({ ...newEmployee, Department: e.target.value })
              }
            />
            <input
              type="text"
              placeholder="Source de Recrutement"
              value={editEmployee ? editEmployee.RecruitmentSource : newEmployee.RecruitmentSource}
              onChange={(e) =>
                editEmployee
                  ? setEditEmployee({ ...editEmployee, RecruitmentSource: e.target.value })
                  : setNewEmployee({ ...newEmployee, RecruitmentSource: e.target.value })
              }
            />
            <input
              type="text"
              placeholder="Score de Performance"
              value={editEmployee ? editEmployee.PerformanceScore : newEmployee.PerformanceScore}
              onChange={(e) =>
                editEmployee
                  ? setEditEmployee({ ...editEmployee, PerformanceScore: e.target.value })
                  : setNewEmployee({ ...newEmployee, PerformanceScore: e.target.value })
              }
            />
            <input
              type="number"
              step="0.1"
              placeholder="Sondage d'Engagement"
              value={editEmployee ? editEmployee.EngagementSurvey : newEmployee.EngagementSurvey}
              onChange={(e) =>
                editEmployee
                  ? setEditEmployee({ ...editEmployee, EngagementSurvey: e.target.value })
                  : setNewEmployee({ ...newEmployee, EngagementSurvey: e.target.value })
              }
            />
            <input
              type="number"
              placeholder="Satisfaction"
              value={editEmployee ? editEmployee.EmployeeSatisfaction : newEmployee.EmployeeSatisfaction}
              onChange={(e) =>
                editEmployee
                  ? setEditEmployee({ ...editEmployee, EmployeeSatisfaction: e.target.value })
                  : setNewEmployee({ ...newEmployee, EmployeeSatisfaction: e.target.value })
              }
            />
            <button type="submit" className={editEmployee ? 'update-button' : 'add-button'}>
              {editEmployee ? 'Mettre à Jour lEmployé' : 'Ajouter un Employé'}
            </button>
          </form>
        </div>
        <div className="add-absence-form">
          <h2>Ajouter une Absence</h2>
          <form
            onSubmit={(e) => {
              e.preventDefault();
              handleAddAbsence();
            }}
          >
            <select
              value={newAbsence.EmployeeID}
              onChange={(e) => setNewAbsence({ ...newAbsence, EmployeeID: e.target.value })}
            >
              <option value="">Sélectionner un Employé</option>
              {employees.map((employee) => (
                <option key={employee.EmployeeID} value={employee.EmployeeID}>
                  {employee.EmployeeName}
                </option>
              ))}
            </select>
            <input
              type="date"
              placeholder="Date d'Absence"
              value={newAbsence.AbsenceDate}
              onChange={(e) => setNewAbsence({ ...newAbsence, AbsenceDate: e.target.value })}
            />
            <input
              type="text"
              placeholder="Raison"
              value={newAbsence.Reason}
              onChange={(e) => setNewAbsence({ ...newAbsence, Reason: e.target.value })}
            />
            <button type="submit" className="add-button">
              Ajouter une Absence
            </button>
          </form>
        </div>
      </header>
    </div>
  );
}

export default App;
