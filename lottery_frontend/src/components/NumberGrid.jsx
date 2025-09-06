import React from 'react';

const NumberGrid = ({ selectedNumbers, onNumberClick }) => {
  return (
    <div className="grid grid-cols-10 gap-2">
      {Array.from({ length: 99 }, (_, i) => i + 1).map(num => (
        <button
          key={num}
          className={`p-2 rounded ${selectedNumbers.includes(num) ? 'bg-blue-500 text-white' : 'bg-gray-200 text-gray-800'}`}
          onClick={() => onNumberClick(num)}
        >
          {num}
        </button>
      ))}
    </div>
  );
};

export default NumberGrid;