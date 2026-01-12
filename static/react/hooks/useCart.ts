import { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import type { CartItem } from '../shared/types';

export function useCart() {
  const { user } = useAuth();
  const [cart, setCart] = useState<CartItem[]>([]);
  const [isLoading, setIsLoading] = useState(false);

  const fetchCart = async () => {
    if (!user) {
      setCart([]);
      return;
    }

    try {
      setIsLoading(true);
      const response = await fetch('/api/cart');
      if (response.ok) {
        const data = await response.json();
        setCart(data);
      }
    } catch (error) {
      console.error('Error fetching cart:', error);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchCart();
  }, [user]);

  const addToCart = async (perfumeId: number, quantity: number = 1) => {
    if (!user) return;

    try {
      const response = await fetch('/api/cart/add/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ perfume_id: perfumeId, quantity }),
      });

      if (response.ok) {
        await fetchCart();
      }
    } catch (error) {
      console.error('Error adding to cart:', error);
    }
  };

  const updateCartItem = async (itemId: number, quantity: number) => {
    if (!user) return;

    try {
      const response = await fetch(`/api/cart/${itemId}/update/`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ quantity }),
      });

      if (response.ok) {
        await fetchCart();
      }
    } catch (error) {
      console.error('Error updating cart:', error);
    }
  };

  const removeFromCart = async (itemId: number) => {
    if (!user) return;

    try {
      const response = await fetch(`/api/cart/${itemId}/delete/`, {
        method: 'POST', // Changed from DELETE to POST as per Django convention
      });

      if (response.ok) {
        await fetchCart();
      }
    } catch (error) {
      console.error('Error removing from cart:', error);
    }
  };

  return {
    cart,
    isLoading,
    addToCart,
    updateCartItem,
    removeFromCart,
    refetchCart: fetchCart,
  };
}
