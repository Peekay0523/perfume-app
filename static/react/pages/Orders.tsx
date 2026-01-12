import { useState, useEffect } from 'react';
import { Link } from 'react-router';
import { Loader2, Package } from 'lucide-react';
import { useAuth } from '../context/AuthContext';
import Navbar from '../components/Navbar';
import type { Order } from '../shared/types';

export default function Orders() {
  const { user, loginWithGoogle } = useAuth();
  const [orders, setOrders] = useState<Order[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    if (!user) return;

    const fetchOrders = async () => {
      try {
        const response = await fetch('/api/orders');
        if (response.ok) {
          const data = await response.json();
          setOrders(data);
        }
      } catch (error) {
        console.error('Error fetching orders:', error);
      } finally {
        setIsLoading(false);
      }
    };

    fetchOrders();
  }, [user]);

  if (!user) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-50 via-rose-50/30 to-amber-50/20">
        <Navbar />
        <div className="container mx-auto px-6 py-12 text-center">
          <h2 className="text-2xl font-semibold text-slate-900 mb-4" style={{ fontFamily: 'Playfair Display, serif' }}>
            Sign in to view your orders
          </h2>
          <Link
            to="/auth"
            className="px-8 py-3 bg-gradient-to-r from-rose-600 to-rose-700 text-white font-semibold rounded-lg hover:shadow-lg transition-shadow inline-block"
          >
            Sign In
          </Link>
        </div>
      </div>
    );
  }

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-50 via-rose-50/30 to-amber-50/20">
        <Navbar />
        <div className="flex items-center justify-center min-h-[60vh]">
          <div className="animate-spin">
            <Loader2 className="w-10 h-10 text-rose-600" />
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-rose-50/30 to-amber-50/20">
      <Navbar />
      
      <div className="container mx-auto px-6 py-12">
        <h1 className="text-4xl lg:text-5xl font-bold text-slate-900 mb-8" style={{ fontFamily: 'Playfair Display, serif' }}>
          My Orders
        </h1>
        
        {orders.length === 0 ? (
          <div className="text-center py-16 bg-white/60 backdrop-blur-sm rounded-2xl border border-slate-200/50">
            <Package className="w-16 h-16 text-slate-300 mx-auto mb-4" />
            <p className="text-xl text-slate-600 mb-6">No orders yet</p>
            <Link
              to="/shop"
              className="inline-block px-8 py-3 bg-gradient-to-r from-rose-600 to-rose-700 text-white font-semibold rounded-lg hover:shadow-lg transition-shadow"
            >
              Start Shopping
            </Link>
          </div>
        ) : (
          <div className="space-y-4">
            {orders.map((order) => (
              <Link
                key={order.id}
                to={`/orders/${order.id}`}
                className="block bg-white/60 backdrop-blur-sm rounded-2xl p-6 border border-slate-200/50 hover:shadow-lg transition-shadow"
              >
                <div className="flex justify-between items-start mb-4">
                  <div>
                    <p className="text-sm text-slate-600">Order #{order.id}</p>
                    <p className="text-lg font-semibold text-slate-900">
                      {new Date(order.created_at).toLocaleDateString('en-US', {
                        year: 'numeric',
                        month: 'long',
                        day: 'numeric',
                      })}
                    </p>
                  </div>
                  <div className="text-right">
                    <p className="text-sm text-slate-600">Total</p>
                    <p className="text-2xl font-bold text-slate-900">
                      ${order.total.toFixed(2)}
                    </p>
                  </div>
                </div>
                <div className="flex items-center gap-2">
                  <span className="px-3 py-1 bg-rose-100 text-rose-700 rounded-full text-sm font-medium capitalize">
                    {order.status}
                  </span>
                </div>
              </Link>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
