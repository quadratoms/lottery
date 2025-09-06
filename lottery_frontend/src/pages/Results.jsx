import React from 'react'
import { useGetDrawsQuery } from '../app/api'

const getErrorMessage = (error) => {
  if ('status' in error) {
    // you can access all properties of `FetchBaseQueryError` here
    return JSON.stringify(error.data);
  } else {
    // you can access all properties of `SerializedError` here
    return error.message;
  }
};

const Results = () => {
  const { data: draws, isLoading, error } = useGetDrawsQuery()

  if (isLoading) return <div className="text-center">Loading results...</div>
  if (error) return <div className="text-center text-red-500">Error loading results: {getErrorMessage(error)}</div>

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-3xl font-bold text-center mb-6">Lottery Results</h1>

      {draws && draws.results.length > 0 ? (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {draws.results.map((draw) => (
            <div key={draw.id} className="bg-white shadow-md rounded-lg p-6">
              <h2 className="text-xl font-semibold text-gray-800 mb-2">Draw ID: {draw.id}</h2>
              <p className="text-gray-700">Game: {draw.game}</p>
              <p className="text-gray-700">Scheduled: {new Date(draw.scheduled_at).toLocaleString()}</p>
              <p className="text-gray-700">Locked: {new Date(draw.locked_at).toLocaleString()}</p>
              <p className="text-gray-700">Status: <span className="font-medium">{draw.status}</span></p>
              {draw.winning_number && (
                <p className="text-2xl font-bold text-green-600 mt-2">Winning Number: {draw.winning_number}</p>
              )}
              {draw.seed_commit_hash && (
                <p className="text-sm text-gray-600 mt-1">Commit Hash: {draw.seed_commit_hash.substring(0, 10)}...</p>
              )}
              {draw.seed_reveal && (
                <p className="text-sm text-gray-600">Reveal: {draw.seed_reveal.substring(0, 10)}...</p>
              )}
            </div>
          ))}
        </div>
      ) : (
        <p className="text-center text-gray-600">No draw results found.</p>
      )}
    </div>
  )
}

export default Results