import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';

const RecentWinners = () => {
  const winners = [
    { name: 'John Doe', amount: 1000 },
    { name: 'Jane Smith', amount: 5000 },
    { name: 'Peter Jones', amount: 2500 },
  ];

  return (
    <div className="bg-secondary py-20">
      <div className="container mx-auto text-center">
        <h2 className="text-3xl font-bold mb-8">Recent Winners</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {winners.map((winner, index) => (
            <Card key={index}>
              <CardHeader>
                <CardTitle>{winner.name}</CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-lg">Won ${winner.amount}</p>
              </CardContent>
            </Card>
          ))}
        </div>
      </div>
    </div>
  );
};

export default RecentWinners;