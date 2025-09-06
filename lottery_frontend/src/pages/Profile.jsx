import React, { useState } from 'react'
import { useGetKycStatusQuery, useInitiateKycMutation } from '../app/api'

const getErrorMessage = (error) => {
  if ('status' in error) {
    // you can access all properties of `FetchBaseQueryError` here
    return JSON.stringify(error.data);
  } else {
    // you can access all properties of `SerializedError` here
    return error.message;
  }
};

const Profile = () => {
  const { data: kycStatus, isLoading: kycLoading, error: kycError } = useGetKycStatusQuery()
  const [initiateKyc, { isLoading: isInitiatingKyc }] = useInitiateKycMutation()
  const [bvnNin, setBvnNin] = useState('')

  const handleKycInitiate = async () => {
    if (!bvnNin) {
      alert('Please enter BVN/NIN.')
      return
    }
    try {
      await initiateKyc({ bvn_nin: bvnNin }).unwrap()
      alert('KYC initiation successful!')
    } catch (error) {
      alert('KYC initiation failed!')
      console.error('KYC initiation error:', error)
    }
  }

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-3xl font-bold text-center mb-6">My Profile</h1>

      <div className="bg-white shadow-md rounded-lg p-6 mb-6">
        <h2 className="text-2xl font-semibold text-gray-800 mb-4">KYC Status</h2>
        {kycLoading && <p>Loading KYC status...</p>}
        {kycError && <p className="text-red-500">Error loading KYC status: {getErrorMessage(kycError)}</p>}
        {kycStatus ? (
          <div>
            <p className="text-gray-700">Status: <span className="font-bold">{kycStatus.result}</span></p>
            <p className="text-gray-700">Provider: {kycStatus.provider}</p>
            <p className="text-gray-700">Reference: {kycStatus.reference}</p>
            <p className="text-gray-700">Last Checked: {new Date(kycStatus.created_at).toLocaleString()}</p>
          </div>
        ) : (
          <div>
            <p className="text-gray-700 mb-4">No KYC information found. Please initiate KYC.</p>
            <input
              type="text"
              className="w-full p-2 border rounded mb-4 text-gray-800"
              placeholder="Enter BVN or NIN"
              value={bvnNin}
              onChange={(e) => setBvnNin(e.target.value)}
            />
            <button
              className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded w-full"
              onClick={handleKycInitiate}
              disabled={isInitiatingKyc}
            >
              {isInitiatingKyc ? 'Initiating...' : 'Initiate KYC'}
            </button>
          </div>
        )}
      </div>

      {/* Other profile settings can go here */}
    </div>
  )
}

export default Profile