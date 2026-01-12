import React, { useState } from 'react';
import AuthForm from '../components/AuthForm';

export default function AuthPage() {
  const [mode, setMode] = useState<'login' | 'signup'>('login');

  return (
    <div>
      <AuthForm 
        mode={mode} 
        onModeChange={setMode} 
      />
    </div>
  );
}