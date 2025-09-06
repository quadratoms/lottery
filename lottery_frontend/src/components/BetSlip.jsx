import React from 'react';

const BetSlip = ({ selectedNumbers, stake, onStakeChange, onPlaceBet, isPlacingBet }) => {
  return (
    <div className="bg-white p-8 rounded-lg shadow-md">
      <h2 className="text-2xl font-bold mb-4">Your Bet Slip</h2>
      <div className="mb-4">
        <h3 className="text-lg font-bold mb-2">Selected Numbers</h3>
        <div className="flex flex-wrap gap-2">
          {selectedNumbers.map(num => (
            <span key={num} className="bg-blue-500 text-white px-3 py-1 rounded-full">
              {num}
            </span>
          ))}
        </div>
      </div>
      <div className="mb-4">
        <h3 className="text-lg font-bold mb-2">Stake</h3>
        <input
          type="number"
          className="w-full p-2 border rounded"
          placeholder="Enter stake amount"
          value={stake}
          onChange={(e) => onStakeChange(Number(e.target.value))}
          min="0"
        />
      </div>
      <button
        className="bg-green-500 hover:bg-green-700 text-white font-bold py-2 px-4 rounded w-full"
        onClick={onPlaceBet}
        disabled={isPlacingBet}
      >
        {isPlacingBet ? 'Placing Bet...' : 'Place Bet'}
      </button>
    </div>
  );
};

export default BetSlip;