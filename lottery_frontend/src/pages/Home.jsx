import React from 'react';
import Hero from '@/components/Hero';
import HowToPlay from '@/components/HowToPlay';
import RecentWinners from '@/components/RecentWinners';
import Testimonials from '@/components/Testimonials';

const Home = () => {
  return (
    <div>
      <Hero />
      <HowToPlay />
      <RecentWinners />
      <Testimonials />
    </div>
  );
};

export default Home;