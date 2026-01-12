import { useState, useEffect } from 'react';
import type { Perfume } from '@/shared/types';

export function usePerfumes() {
  const [perfumes, setPerfumes] = useState<Perfume[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const fetchPerfumes = async () => {
      try {
        const response = await fetch('/api/perfumes');
        if (response.ok) {
          const data = await response.json();
          setPerfumes(data);
        }
      } catch (error) {
        console.error('Error fetching perfumes:', error);
      } finally {
        setIsLoading(false);
      }
    };

    fetchPerfumes();
  }, []);

  return { perfumes, isLoading };
}

export function usePerfume(id: string) {
  const [perfume, setPerfume] = useState<Perfume | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const fetchPerfume = async () => {
      try {
        const response = await fetch(`/api/perfumes/${id}`);
        if (response.ok) {
          const data = await response.json();
          setPerfume(data);
        }
      } catch (error) {
        console.error('Error fetching perfume:', error);
      } finally {
        setIsLoading(false);
      }
    };

    fetchPerfume();
  }, [id]);

  return { perfume, isLoading };
}
