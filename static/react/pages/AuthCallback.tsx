import { useEffect } from 'react';
import { useNavigate, useSearchParams } from 'react-router';
import { useAuth } from '../context/AuthContext';
import { Loader2 } from 'lucide-react';

export default function AuthCallback() {
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const code = searchParams.get('code');

  useEffect(() => {
    const handleCallback = async () => {
      if (code) {
        try {
          // Exchange code for session token with Django backend
          const response = await fetch('/api/auth/sessions/', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({ code }),
          });

          if (response.ok) {
            // Reload the page to update auth state
            window.location.href = '/';
          } else {
            console.error('Authentication failed');
            navigate('/');
          }
        } catch (error) {
          console.error('Authentication error:', error);
          navigate('/');
        }
      } else {
        navigate('/');
      }
    };

    handleCallback();
  }, [code, navigate]);

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gradient-to-br from-slate-50 via-rose-50/30 to-amber-50/20">
      <div className="animate-spin mb-4">
        <Loader2 className="w-10 h-10 text-rose-600" />
      </div>
      <p className="text-slate-600">Completing sign in...</p>
    </div>
  );
}
