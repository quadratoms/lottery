import React from 'react'
import { useGetWalletBalanceQuery, useGetLedgerStatementQuery } from '../app/api'

const getErrorMessage = (error) => {
  if ('status' in error) {
    // you can access all properties of `FetchBaseQueryError` here
    return JSON.stringify(error.data);
  } else {
    // you can access all properties of `SerializedError` here
    return error.message;
  }
};

const Wallet = () => {
  const { data: wallet, error: walletError, isLoading: walletLoading } = useGetWalletBalanceQuery()
  const { data: statement, error: statementError, isLoading: statementLoading } = useGetLedgerStatementQuery()

  if (walletLoading || statementLoading) return <div className="text-center">Loading wallet data...</div>
  if (walletError) return <div className="text-center text-red-500">Error loading wallet: {getErrorMessage(walletError)}</div>
  if (statementError) return <div className="text-center text-red-500">Error loading statement: {getErrorMessage(statementError)}</div>

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-3xl font-bold text-center mb-6">My Wallet</h1>

      {wallet && (
        <div className="bg-white shadow-md rounded-lg p-6 mb-6">
          <h2 className="text-2xl font-semibold text-gray-800 mb-4">Current Balance</h2>
          <p className="text-gray-700 text-xl">
            Available: <span className="font-bold">{wallet.available} {wallet.currency}</span>
          </p>
          <p className="text-gray-700 text-xl">
            Locked: <span className="font-bold">{wallet.locked} {wallet.currency}</span>
          </p>
        </div>
      )}

      <div className="bg-white shadow-md rounded-lg p-6">
        <h2 className="text-2xl font-semibold text-gray-800 mb-4">Ledger Statement</h2>
        {statement && statement.length > 0 ? (
          <ul className="divide-y divide-gray-200">
            {statement.map((entry) => (
              <li key={entry.id} className="py-4 flex justify-between items-center">
                <div>
                  <p className="text-lg font-medium text-gray-900">{entry.type}</p>
                  <p className="text-sm text-gray-500">Ref: {entry.ref}</p>
                  <p className="text-sm text-gray-500">{new Date(entry.created_at).toLocaleString()}</p>
                </div>
                <div className="text-right">
                  <p className={`text-lg font-semibold ${entry.amount > 0 ? 'text-green-600' : 'text-red-600'}`}>
                    {entry.amount} {wallet?.currency || 'NGN'}
                  </p>
                  <p className="text-sm text-gray-600">Balance: {entry.balance_after} {wallet?.currency || 'NGN'}</p>
                </div>
              </li>
            ))}
          </ul>
        ) : (
          <p className="text-gray-600">No ledger entries found.</p>
        )}
      </div>
    </div>
  )
}

export default Wallet