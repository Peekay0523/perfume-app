import React, { useState } from 'react';
import { useAuth } from '../context/AuthContext';
import { Eye, EyeOff } from 'lucide-react';

interface FormData {
  username: string;
  email: string;
  password: string;
  confirmPassword: string;
}

interface AuthFormProps {
  mode: 'login' | 'signup';
  onModeChange: (mode: 'login' | 'signup') => void;
}

export default function AuthForm({ mode, onModeChange }: AuthFormProps) {
  const [formData, setFormData] = useState<FormData>({
    username: '',
    email: '',
    password: '',
    confirmPassword: ''
  });
  const [showPassword, setShowPassword] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const { login, signup } = useAuth();

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
    if (error) setError(null); // Clear error when user starts typing
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    if (mode === 'signup') {
      // Validate password match for signup
      if (formData.password !== formData.confirmPassword) {
        setError('Passwords do not match');
        setLoading(false);
        return;
      }

      const success = await signup(formData.username, formData.email, formData.password);
      if (!success) {
        setError('Signup failed. Please check your details and try again.');
      }
    } else {
      const success = await login(formData.username, formData.password);
      if (!success) {
        setError('Invalid credentials. Please try again.');
      }
    }

    setLoading(false);
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-slate-50 via-rose-50/30 to-amber-50/20 p-4">
      <div className="w-full max-w-md">
        <div className="bg-white rounded-2xl shadow-xl p-8">
          <div className="text-center mb-8">
            <h1 className="text-3xl font-bold text-slate-900 mb-2 font-serif-display">
              {mode === 'login' ? 'Welcome Back' : 'Create Account'}
            </h1>
            <p className="text-slate-600">
              {mode === 'login' 
                ? 'Sign in to continue your journey' 
                : 'Join us to discover your signature scent'}
            </p>
          </div>

          {error && (
            <div className="mb-6 p-3 bg-red-50 text-red-700 rounded-lg text-sm">
              {error}
            </div>
          )}

          <form onSubmit={handleSubmit}>
            {mode === 'signup' && (
              <div className="mb-4">
                <label htmlFor="email" className="block text-sm font-medium text-slate-700 mb-1">
                  Email
                </label>
                <input
                  type="email"
                  id="email"
                  name="email"
                  value={formData.email}
                  onChange={handleChange}
                  required
                  className="w-full px-4 py-3 border border-slate-300 rounded-lg focus:ring-2 focus:ring-rose-500 focus:border-transparent"
                  placeholder="your@email.com"
                />
              </div>
            )}

            <div className="mb-4">
              <label htmlFor="username" className="block text-sm font-medium text-slate-700 mb-1">
                {mode === 'signup' ? 'Username' : 'Username or Email'}
              </label>
              <input
                type="text"
                id="username"
                name="username"
                value={formData.username}
                onChange={handleChange}
                required
                className="w-full px-4 py-3 border border-slate-300 rounded-lg focus:ring-2 focus:ring-rose-500 focus:border-transparent"
                placeholder={mode === 'signup' ? 'Choose a username' : 'Enter your username or email'}
              />
            </div>

            <div className="mb-4">
              <label htmlFor="password" className="block text-sm font-medium text-slate-700 mb-1">
                Password
              </label>
              <div className="relative">
                <input
                  type={showPassword ? 'text' : 'password'}
                  id="password"
                  name="password"
                  value={formData.password}
                  onChange={handleChange}
                  required
                  className="w-full px-4 py-3 pr-12 border border-slate-300 rounded-lg focus:ring-2 focus:ring-rose-500 focus:border-transparent"
                  placeholder="••••••••"
                />
                <button
                  type="button"
                  className="absolute right-3 top-1/2 transform -translate-y-1/2 text-slate-500 hover:text-slate-700"
                  onClick={() => setShowPassword(!showPassword)}
                >
                  {showPassword ? <EyeOff className="w-5 h-5" /> : <Eye className="w-5 h-5" />}
                </button>
              </div>
            </div>

            {mode === 'signup' && (
              <div className="mb-6">
                <label htmlFor="confirmPassword" className="block text-sm font-medium text-slate-700 mb-1">
                  Confirm Password
                </label>
                <input
                  type="password"
                  id="confirmPassword"
                  name="confirmPassword"
                  value={formData.confirmPassword}
                  onChange={handleChange}
                  required
                  className="w-full px-4 py-3 border border-slate-300 rounded-lg focus:ring-2 focus:ring-rose-500 focus:border-transparent"
                  placeholder="••••••••"
                />
              </div>
            )}

            <button
              type="submit"
              disabled={loading}
              className={`w-full py-3 px-4 rounded-lg font-semibold text-white transition-all ${
                loading 
                  ? 'bg-gray-400 cursor-not-allowed' 
                  : 'bg-gradient-to-r from-rose-600 to-rose-700 hover:shadow-lg hover:from-rose-700 hover:to-rose-800'
              }`}
            >
              {loading ? 'Processing...' : mode === 'login' ? 'Sign In' : 'Create Account'}
            </button>
          </form>

          <div className="mt-6 text-center">
            <p className="text-slate-600">
              {mode === 'login' 
                ? "Don't have an account? " 
                : "Already have an account? "}
              <button
                type="button"
                onClick={() => onModeChange(mode === 'login' ? 'signup' : 'login')}
                className="text-rose-600 font-semibold hover:text-rose-700 transition-colors"
              >
                {mode === 'login' ? 'Sign up' : 'Sign in'}
              </button>
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}