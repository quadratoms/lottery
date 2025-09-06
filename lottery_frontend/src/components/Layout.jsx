import React from 'react';
import { Link } from 'react-router-dom';
import { Button } from '@/components/ui/button';

const Layout = ({ children }) => {
  return (
    <div className="min-h-screen bg-gray-100">
      <header className="bg-white shadow-md">
        <div className="container mx-auto px-4 py-6 flex justify-between items-center">
          <Link to="/" className="text-2xl font-bold text-blue-600">
            Lottery
          </Link>
          <nav className="space-x-4">
            <Link to="/" className="text-gray-600 hover:text-blue-600">Home</Link>
            <Link to="/play" className="text-gray-600 hover:text-blue-600">Play</Link>
            <Link to="/results" className="text-gray-600 hover:text-blue-600">Results</Link>
            <Link to="/wallet" className="text-gray-600 hover:text-blue-600">Wallet</Link>
            <Link to="/tickets" className="text-gray-600 hover:text-blue-600">Tickets</Link>
            <Link to="/profile" className="text-gray-600 hover:text-blue-600">Profile</Link>
          </nav>
          <div>
            <Link to="/auth">
              <Button>Login / Register</Button>
            </Link>
          </div>
        </div>
      </header>
      <main className="container mx-auto px-4 py-8">
        {children}
      </main>
      <footer className="bg-white py-6">
        <div className="container mx-auto px-4 text-center text-gray-600">
          &copy; 2025 Lottery Inc. All rights reserved.
        </div>
      </footer>
    </div>
  );
};

export default Layout;