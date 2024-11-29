import React, { useEffect, useState } from 'react';
import axios from 'axios';

const EmployeeList = () => {
  const [employees, setEmployees] = useState([]);

  useEffect(() => {
    fetchEmployees();
  }, []);

  const fetchEmployees = async () => {
    try {
      const response = await axios.get('http://127.0.0.1:5000/api/employees');
      setEmployees(response.data);
    } catch (error) {
      console.error('Erreur lors de la récupération des employés', error);
    }
  };

  return (
    <div>
      <h2>Liste des Employés</h2>
      <ul>
        {employees.map((employee) => (
          <li key={employee.EmployeeID}>
            {employee.EmployeeName} - {employee.Position}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default EmployeeList;
