import React from 'react';

interface SensorCardProps {
  title: string;
  value: number | string;
  unit?: string;
  status?: string;
}

// Відтінки для різних статусів
const statusStyles: Record<string, string> = {
  good: 'bg-green-100 text-green-800',
  moderate: 'bg-yellow-100 text-yellow-800',
  poor: 'bg-red-100 text-red-800',
  freezing: 'bg-blue-100 text-blue-800',
  cool: 'bg-blue-50 text-blue-800',
  warm: 'bg-orange-100 text-orange-800',
  hot: 'bg-red-100 text-red-800',
  dry: 'bg-yellow-50 text-yellow-800',
  normal: 'bg-green-50 text-green-800',
  humid: 'bg-blue-50 text-blue-800',
  dark: 'bg-gray-700 text-white',
  'well-lit': 'bg-yellow-200 text-gray-800',
  unknown: 'bg-gray-100 text-gray-800',
};

const SensorCard: React.FC<SensorCardProps> = ({ title, value, unit, status }) => {
  const badgeClass = status ? statusStyles[status] || statusStyles['unknown'] : '';

  return (
      <div className="bg-white rounded-2xl shadow p-4 flex flex-col justify-between">
        <div>
          <h3 className="text-sm font-medium text-gray-500 uppercase">
            {title}
          </h3>
          <p className="mt-2 text-2xl font-bold text-gray-900">
            {value}{unit || ''}
          </p>
        </div>
        {status && (
            <span
                className={
                  `mt-4 inline-block px-3 py-1 text-xs font-semibold rounded-full ${badgeClass}`
                }
            >
          {status}
        </span>
        )}
      </div>
  );
};

export default SensorCard;
