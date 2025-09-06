import React from 'react';
import { Link } from 'react-router-dom';
import { Button } from '@/components/ui/button';

const Hero = () => {
  return (
    <div className="bg-primary text-primary-foreground py-20">
      <div className="container mx-auto text-center">
        <h1 className="text-5xl font-bold mb-4">Your Chance to Win Big!</h1>
        <p className="text-lg mb-8">Participate in our exciting lottery and make your dreams come true.</p>
        <Link to="/play">
          <Button size="lg">Play Now</Button>
        </Link>
      </div>
    </div>
  );
};

export default Hero;