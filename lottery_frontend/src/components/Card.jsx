import React from 'react';

const Card = ({ children }) => {
  return (
    <div className="bg-white p-8 rounded-lg shadow-md w-96">
      {children}
    </div>
  );
};

export default Card;