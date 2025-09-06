import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';

const Testimonials = () => {
  const testimonials = [
    {
      quote: 'I won $1000! This is the best lottery ever!',
      author: 'John Doe',
    },
    {
      quote: 'I can\'t believe I won! I\'m so happy!',
      author: 'Jane Smith',
    },
    {
      quote: 'I\'ve been playing for a few weeks and I finally won! I\'m so excited!',
      author: 'Peter Jones',
    },
  ];

  return (
    <div className="py-20">
      <div className="container mx-auto text-center">
        <h2 className="text-3xl font-bold mb-8">What Our Players Are Saying</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {testimonials.map((testimonial, index) => (
            <Card key={index}>
              <CardHeader>
                <CardTitle>"{testimonial.quote}"</CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-muted-foreground">- {testimonial.author}</p>
              </CardContent>
            </Card>
          ))}
        </div>
      </div>
    </div>
  );
};

export default Testimonials;
