import React from 'react'
import { useGetTicketsQuery } from '../app/api'

const getErrorMessage = (error) => {
  if ('status' in error) {
    // you can access all properties of `FetchBaseQueryError` here
    return JSON.stringify(error.data);
  } else {
    // you can access all properties of `SerializedError` here
    return error.message;
  }
};

const Tickets = () => {
  const { data: tickets, isLoading, error } = useGetTicketsQuery()

  if (isLoading) return <div className="text-center">Loading tickets...</div>
  if (error) return <div className="text-center text-red-500">Error loading tickets: {getErrorMessage(error)}</div>

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-3xl font-bold text-center mb-6">My Tickets</h1>

      {tickets && tickets.results.length > 0 ? (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {tickets.results.map((ticket) => (
            <div key={ticket.id} className="bg-white shadow-md rounded-lg p-6">
              <h2 className="text-xl font-semibold text-gray-800 mb-2">Ticket ID: {ticket.id}</h2>
              <p className="text-gray-700">Draw: {ticket.draw}</p>
              <p className="text-gray-700">Selection: {ticket.selection}</p>
              <p className="text-gray-700">Stake: {ticket.stake}</p>
              <p className="text-gray-700">Potential Payout: {ticket.potential_payout}</p>
              <p className="text-gray-700">Status: <span className="font-medium">{ticket.status}</span></p>
              <p className="text-gray-700 text-sm">Placed At: {new Date(ticket.placed_at).toLocaleString()}</p>
              <p className="text-gray-700 text-sm">Hash: {ticket.ticket_hash.substring(0, 10)}...</p>
            </div>
          ))}
        </div>
      ) : (
        <p className="text-center text-gray-600">No tickets found.</p>
      )}
    </div>
  )
}

export default Tickets