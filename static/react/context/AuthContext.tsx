import React, { createContext, useState, useContext, useEffect, ReactNode } from 'react';
import { useNavigate } from 'react-router';

interface User {
  id: string;
  username: string;
  email?: string;
  first_name?: string;
  last_name?: string;
}

interface AuthContextType {
  user: User | null;
  loading: boolean;
  login: (username: string, password: string) => Promise<boolean>;
  logout: () => void;
  signup: (username: string, email: string, password: string) => Promise<boolean>;
  loginWithGoogle: () => void;
  isAuthenticated: boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

interface AuthProviderProps {
  children: ReactNode;
}

export const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    // Check if user is logged in on app start
    checkAuthStatus();
  }, []);

  const checkAuthStatus = async () => {
    try {
      const response = await fetch('/api/users/me', {
        credentials: 'include',
      });
      
      if (response.ok) {
        const userData = await response.json();
        setUser(userData);
      }
    } catch (error) {
      console.error('Error checking auth status:', error);
    } finally {
      setLoading(false);
    }
  };

  const login = async (username: string, password: string): Promise<boolean> => {
    try {
      const response = await fetch('/api/auth/token/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username, password }),
        credentials: 'include',
      });

      if (response.ok) {
        const data = await response.json();
        
        // Store tokens in localStorage (or cookies)
        localStorage.setItem('access_token', data.access);
        localStorage.setItem('refresh_token', data.refresh);
        
        setUser(data.user);
        return true;
      } else {
        return false;
      }
    } catch (error) {
      console.error('Login error:', error);
      return false;
    }
  };

  const signup = async (username: string, email: string, password: string): Promise<boolean> => {
    try {
      const response = await fetch('/api/auth/signup/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username, email, password }),
        credentials: 'include',
      });

      if (response.ok) {
        const data = await response.json();

        // Store tokens in localStorage (or cookies)
        localStorage.setItem('access_token', data.access);
        localStorage.setItem('refresh_token', data.refresh);

        setUser(data.user);
        return true;
      } else {
        const errorData = await response.json();
        console.error('Signup error:', errorData.error);
        return false;
      }
    } catch (error) {
      console.error('Signup error:', error);
      return false;
    }
  };

  const logout = async () => {
    try {
      await fetch('/api/logout/', {
        method: 'POST',
        credentials: 'include',
      });
    } catch (error) {
      console.error('Logout error:', error);
    } finally {
      localStorage.removeItem('access_token');
      localStorage.removeItem('refresh_token');
      setUser(null);
      navigate('/');
    }
  };

  const loginWithGoogle = () => {
    // Redirect to auth page instead of Google OAuth directly
    // This allows the user to choose between login/signup
    window.location.href = '/auth';
  };

  const isAuthenticated = !!user;

  const value = {
    user,
    loading,
    login,
    logout,
    signup,
    loginWithGoogle,
    isAuthenticated,
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};