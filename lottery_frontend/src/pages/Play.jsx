import React, { useState } from 'react';
import { useGetGameConfigsQuery, useGetDrawsQuery, usePlaceTicketMutation } from '@/app/api';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Label } from '@/components/ui/label';
import NumberGrid from '@/components/NumberGrid';
import BetSlip from '@/components/BetSlip';

const getErrorMessage = (error) => {
  if ('status' in error) {
    // you can access all properties of `FetchBaseQueryError` here
    return JSON.stringify(error.data);
  } else {
    // you can access all properties of `SerializedError` here
    return error.message;
  }
};

const Play = () => {
  const { data: gameConfigs, isLoading: gameConfigsLoading, error: gameConfigsError } = useGetGameConfigsQuery();
  const { data: draws, isLoading: drawsLoading, error: drawsError } = useGetDrawsQuery();
  const [placeTicket, { isLoading: isPlacingTicket }] = usePlaceTicketMutation();

  const [selectedNumbers, setSelectedNumbers] = useState([]);
  const [stake, setStake] = useState(0);
  const [selectedGameId, setSelectedGameId] = useState(null);
  const [selectedDrawId, setSelectedDrawId] = useState(null);

  if (gameConfigsLoading || drawsLoading) return <div className="text-center">Loading game data...</div>;
  if (gameConfigsError) return <div className="text-center text-red-500">Error loading game configurations: {getErrorMessage(gameConfigsError)}</div>;
  if (drawsError) return <div className="text-center text-red-500">Error loading draws: {getErrorMessage(drawsError)}</div>;

  const handleNumberClick = (num) => {
    setSelectedNumbers(prev => {
      if (prev.includes(num)) {
        return prev.filter(n => n !== num);
      } else {
        return [...prev, num];
      }
    });
  };

  const handlePlaceBet = async () => {
    if (!selectedGameId || !selectedDrawId || selectedNumbers.length === 0 || stake <= 0) {
      alert('Please select a game, draw, numbers, and stake.');
      return;
    }

    try {
      await placeTicket({
        game_id: selectedGameId,
        draw_id: selectedDrawId,
        selection: selectedNumbers[0], // Assuming pick-1 for now
        stake: stake,
      }).unwrap();
      alert('Bet placed successfully!');
      setSelectedNumbers([]);
      setStake(0);
    } catch (error) {
      alert('Failed to place bet!');
      console.error('Place bet error:', error);
    }
  };

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-3xl font-bold text-center mb-6">Play Lottery</h1>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
        <div className="md:col-span-2">
          <Card>
            <CardHeader>
              <CardTitle>Game and Draw Selection</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="space-y-2">
                <Label>Select Game</Label>
                <select
                  className="w-full p-2 border rounded"
                  onChange={(e) => setSelectedGameId(Number(e.target.value))}
                  value={selectedGameId || ''}
                >
                  <option value="">-- Select a Game --</option>
                  {gameConfigs && gameConfigs.results.map((game) => (
                    <option key={game.id} value={game.id}>
                      {game.name} (Min: {game.min_bet}, Max: {game.max_bet})
                    </option>
                  ))}
                </select>
              </div>
              <div className="space-y-2">
                <Label>Select Draw</Label>
                <select
                  className="w-full p-2 border rounded"
                  onChange={(e) => setSelectedDrawId(Number(e.target.value))}
                  value={selectedDrawId || ''}
                >
                  <option value="">-- Select a Draw --</option>
                  {draws && draws.results && Array.isArray(draws.results) && draws.results.map((draw) => (
                    <option key={draw.id} value={draw.id}>
                      Draw ID: {draw.id} - Scheduled: {new Date(draw.scheduled_at).toLocaleString()} (Status: {draw.status})
                    </option>
                  ))}
                </select>
              </div>
            </CardContent>
          </Card>
          <Card className="mt-8">
            <CardHeader>
              <CardTitle>Select Your Numbers</CardTitle>
            </CardHeader>
            <CardContent>
              <NumberGrid selectedNumbers={selectedNumbers} onNumberClick={handleNumberClick} />
            </CardContent>
          </Card>
        </div>
        <div>
          <BetSlip
            selectedNumbers={selectedNumbers}
            stake={stake}
            onStakeChange={setStake}
            onPlaceBet={handlePlaceBet}
            isPlacingBet={isPlacingTicket}
          />
        </div>
      </div>
    </div>
  );
};

export default Play;