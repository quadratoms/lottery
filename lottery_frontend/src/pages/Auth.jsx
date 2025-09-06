import React, { useState } from 'react';
import { useRegisterMutation, useLoginMutation } from '@/app/api';
import { Button } from "@/components/ui/button"
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"

const Auth = () => {
  const [isLogin, setIsLogin] = useState(true);
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  const [register, { isLoading: isRegistering }] = useRegisterMutation();
  const [login, { isLoading: isLoggingIn }] = useLoginMutation();

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (isLogin) {
      try {
        const result = await login({ username, password }).unwrap();
        localStorage.setItem('access', result.access);
        localStorage.setItem('refresh', result.refresh);
        alert('Login successful!');
        // Redirect or update UI
      } catch (error) {
        alert('Login failed!');
        console.error('Login error:', error);
      }
    } else {
      try {
        await register({ username, email, password }).unwrap();
        alert('Registration successful! Attempting to log in...');
        // Automatically attempt to log in after successful registration
        const result = await login({ username, password }).unwrap();
        localStorage.setItem('access', result.access);
        localStorage.setItem('refresh', result.refresh);
        alert('Automatic login successful!');
        // Redirect or update UI
      } catch (error) {
        alert('Registration or automatic login failed!');
        console.error('Registration/Login error:', error);
      }
    }
  };

  return (
    <div className="min-h-screen bg-gray-100 flex items-center justify-center p-4">
      <Card className="w-full max-w-md">
        <CardHeader className="text-center">
          <CardTitle className="text-3xl font-bold">
            {isLogin ? 'Welcome Back' : 'Join Us'}
          </CardTitle>
          <CardDescription>
            {isLogin ? 'Sign in to your account' : 'Create your account to get started'}
          </CardDescription>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSubmit} className="space-y-6">
            <div className="space-y-2">
              <Label htmlFor="username">Username</Label>
              <Input
                id="username"
                type="text"
                placeholder="Enter your username"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                required
              />
            </div>
            {!isLogin && (
              <div className="space-y-2">
                <Label htmlFor="email">Email</Label>
                <Input
                  id="email"
                  type="email"
                  placeholder="Enter your email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  required
                />
              </div>
            )}
            <div className="space-y-2">
              <Label htmlFor="password">Password</Label>
              <Input
                id="password"
                type="password"
                placeholder="Enter your password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
              />
            </div>
            <Button type="submit" disabled={isRegistering || isLoggingIn} className="w-full py-2">
              {isLogin ? (isLoggingIn ? 'Signing In...' : 'Sign In') : (isRegistering ? 'Registering...' : 'Register')}
            </Button>
          </form>
        </CardContent>
        <CardFooter className="flex justify-center">
          <p className="text-sm text-muted-foreground">
            {isLogin ? "Don't have an account? " : "Already have an account? "}
            <Button
              variant="link"
              onClick={() => setIsLogin(!isLogin)}
              className="p-0 h-auto"
            >
              {isLogin ? 'Sign Up' : 'Sign In'}
            </Button>
          </p>
        </CardFooter>
      </Card>
    </div>
  );
};

export default Auth;