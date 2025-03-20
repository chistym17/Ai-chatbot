'use client';
import { useState } from 'react';
import Patients from './Patients';
import Doctors from './Doctors';
import Hospitals from './Hospitals';
import Diseases from './Diseases';
import MedicalRecords from './Medical_records';
import Appointments from './Appointments';

export default function Dashboard() {
  const [activeComponent, setActiveComponent] = useState(null);

  const dashboardItems = [
    {
      title: 'Patients',
      icon: '👤',
      component: Patients,
      description: 'View and manage patient records',
      color: 'bg-blue-100',
      borderColor: 'border-blue-300',
      hoverColor: 'hover:bg-blue-200',
    },
    {
      title: 'Doctors',
      icon: '👨‍⚕️',
      component: Doctors,
      description: 'Browse doctor profiles',
      color: 'bg-green-100',
      borderColor: 'border-green-300',
      hoverColor: 'hover:bg-green-200',
    },
    {
      title: 'Hospitals',
      icon: '🏥',
      component: Hospitals,
      description: 'View hospital information',
      color: 'bg-purple-100',
      borderColor: 'border-purple-300',
      hoverColor: 'hover:bg-purple-200',
    },
    {
      title: 'Diseases',
      icon: '🔬',
      component: Diseases,
      description: 'Access disease database',
      color: 'bg-red-100',
      borderColor: 'border-red-300',
      hoverColor: 'hover:bg-red-200',
    },
    {
      title: 'Medical Records',
      icon: '📋',
      component: MedicalRecords,
      description: 'View patient medical records',
      color: 'bg-orange-100',
      borderColor: 'border-orange-300',
      hoverColor: 'hover:bg-orange-200',
    },
    {
      title: 'Appointments',
      icon: '📅',
      component: Appointments,
      description: 'Manage appointments',
      color: 'bg-teal-100',
      borderColor: 'border-teal-300',
      hoverColor: 'hover:bg-teal-200',
    },
  ];

  if (activeComponent) {
    return (
      <div className="container mx-auto p-6 min-h-screen">
        <button
          onClick={() => setActiveComponent(null)}
          className="mb-6 flex items-center gap-2 text-gray-600 hover:text-gray-900 transition-colors px-4 py-2 rounded-lg hover:bg-gray-100"
        >
          <span className="text-xl">←</span>
          Back to Dashboard
        </button>
        {activeComponent}
      </div>
    );
  }

  return (
    <div className="container mx-auto p-6 min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto">
        <h1 className="text-4xl font-bold mb-8 text-gray-800 text-center">
          Healthcare Dashboard
        </h1>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {dashboardItems.map((item) => (
            <div
              key={item.title}
              className={`
                cursor-pointer rounded-xl border-2 p-8
                transition-all duration-200 transform
                hover:scale-[1.02] hover:shadow-lg
                min-h-[200px] flex flex-col justify-between
                ${item.color} ${item.borderColor} ${item.hoverColor}
              `}
              onClick={() => setActiveComponent(<item.component />)}
            >
              <div>
                <div className="flex items-center gap-4 mb-4">
                  <span className="text-4xl">{item.icon}</span>
                  <h2 className="text-2xl font-semibold text-gray-800">
                    {item.title}
                  </h2>
                </div>
                <p className="text-base text-gray-600 mb-4">
                  {item.description}
                </p>
              </div>
              
              <div className="flex justify-between items-center text-sm text-gray-500 pt-4 border-t border-gray-200">
                <span>Click to view</span>
                <span className="text-xl">→</span>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
} 