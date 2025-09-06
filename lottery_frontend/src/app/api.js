import { createApi, fetchBaseQuery } from '@reduxjs/toolkit/query/react'

export const api = createApi({
  reducerPath: 'api',
  baseQuery: fetchBaseQuery({
    baseUrl: 'http://localhost:8000/api/v1/',
    prepareHeaders: (headers) => {
      const token = localStorage.getItem('access') // Assuming you store the token in localStorage
      if (token) {
        headers.set('authorization', `Bearer ${token}`)
      }
      return headers
    },
  }),
  endpoints: (builder) => ({
    register: builder.mutation({
      query: (credentials) => ({
        url: 'register/',
        method: 'POST',
        body: credentials,
        headers:{
          'Content-Type': 'application/json',
        }
      }),
    }),
    login: builder.mutation({
      query: (credentials) => ({
        url: '../token/',
        method: 'POST',
        body: credentials,
      }),
    }),
    refreshToken: builder.mutation({
      query: (refresh) => ({
        url: '../token/refresh/',
        method: 'POST',
        body: { refresh },
      }),
    }),
    getWalletBalance: builder.query({
      query: () => 'wallet/balance/',
    }),
    getLedgerStatement: builder.query({
      query: () => 'wallet/statement/',
    }),
    getGameConfigs: builder.query({
      query: () => 'games/gameconfigs/',
    }),
    getOddsSchemes: builder.query({
      query: () => 'games/oddsschemes/',
    }),
    getDraws: builder.query({
      query: () => 'draws/draws/',
    }),
    getTickets: builder.query({
      query: () => 'tickets/history/',
    }),
    placeTicket: builder.mutation({
      query: (ticketData) => ({
        url: 'tickets/place/',
        method: 'POST',
        body: ticketData,
      }),
    }),
    getPayouts: builder.query({
      query: () => 'payouts/history/',
    }),
    initiateKyc: builder.mutation({
      query: (kycData) => ({
        url: 'kyc/initiate/',
        method: 'POST',
        body: kycData,
      }),
    }),
    getKycStatus: builder.query({
      query: () => 'kyc/status/',
    }),
  }),
})

export const { 
  useRegisterMutation,
  useLoginMutation,
  useRefreshTokenMutation,
  useGetWalletBalanceQuery,
  useGetLedgerStatementQuery,
  useGetGameConfigsQuery,
  useGetOddsSchemesQuery,
  useGetDrawsQuery,
  useGetTicketsQuery,
  usePlaceTicketMutation,
  useGetPayoutsQuery,
  useInitiateKycMutation,
  useGetKycStatusQuery,
} = api