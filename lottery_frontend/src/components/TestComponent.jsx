import React from 'react';

const TestComponent = () => {
  return (
    <div className="bg-red-500 text-white p-4 m-4 rounded-lg shadow-lg">
      <h1 className="text-2xl font-bold">Test Component</h1>
      <p className="text-lg">This is a test component to check Tailwind CSS.</p>
      <button className="bg-green-500 hover:bg-green-700 text-white font-bold py-2 px-4 rounded">Test Button</button>
    </div>
  );
};

export default TestComponent;