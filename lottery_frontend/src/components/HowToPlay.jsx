import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';

const HowToPlay = () => {
  return (
    <div className="py-20">
      <div className="container mx-auto text-center">
        <h2 className="text-3xl font-bold mb-8">How to Play</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          <Card>
            <CardHeader>
              <CardTitle>1. Choose Your Numbers</CardTitle>
            </CardHeader>
            <CardContent>
              <p>Select your lucky numbers from 1 to 99.</p>
            </CardContent>
          </Card>
          <Card>
            <CardHeader>
              <CardTitle>2. Place Your Bet</CardTitle>
            </CardHeader>
            <CardContent>
              <p>Choose your stake and place your bet.</p>
            </CardContent>
          </Card>
          <Card>
            <CardHeader>
              <CardTitle>3. Win Big!</CardTitle>
            </CardHeader>
            <CardContent>
              <p>Check the results and see if you are a winner.</p>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
};

export default HowToPlay;