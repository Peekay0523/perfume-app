import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router';
import { Loader2, ArrowLeft, Package } from 'lucide-react';
import { useAuth } from '../context/AuthContext';
import Navbar from '../components/Navbar';
import type { OrderWithItems } from '../shared/types';

export default function OrderDetails() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const { user, loginWithGoogle } = useAuth();
  const [order, setOrder] = useState<OrderWithItems | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    if (!user) return;

    const fetchOrder = async () => {
      try {
        const response = await fetch(`/api/orders/${id}`);
        if (response.ok) {
          const data = await response.json();
          setOrder(data);
        } else {
          navigate('/orders');
        }
      } catch (error) {
        console.error('Error fetching order:', error);
      } finally {
        setIsLoading(false);
      }
    };

    fetchOrder();
  }, [user, id, navigate]);

  if (!user) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-50 via-rose-50/30 to-amber-50/20">
        <Navbar />
        <div className="container mx-auto px-6 py-12 text-center">
          <h2 className="text-2xl font-semibold text-slate-900 mb-4" style={{ fontFamily: 'Playfair Display, serif' }}>
            Sign in to view order details
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

  if (!order) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-50 via-rose-50/30 to-amber-50/20">
        <Navbar />
        <div className="container mx-auto px-6 py-12 text-center">
          <p className="text-slate-600">Order not found</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-rose-50/30 to-amber-50/20">
      <Navbar />
      
      <div className="container mx-auto px-6 py-12">
        <button
          onClick={() => navigate('/orders')}
          className="flex items-center gap-2 text-slate-600 hover:text-rose-600 transition-colors mb-8"
        >
          <ArrowLeft className="w-4 h-4" />
          Back to Orders
        </button>
        
        <div className="grid lg:grid-cols-3 gap-8">
          <div className="lg:col-span-2 space-y-6">
            <div className="bg-white/60 backdrop-blur-sm rounded-2xl p-8 border border-slate-200/50">
              <div className="flex items-start justify-between mb-6">
                <div>
                  <h1 className="text-3xl font-bold text-slate-900 mb-2" style={{ fontFamily: 'Playfair Display, serif' }}>
                    Order #{order.id}
                  </h1>
                  <p className="text-slate-600">
                    Placed on {new Date(order.created_at).toLocaleDateString('en-US', {
                      year: 'numeric',
                      month: 'long',
                      day: 'numeric',
                    })}
                  </p>
                </div>
                <span className="px-4 py-2 bg-rose-100 text-rose-700 rounded-full text-sm font-medium capitalize">
                  {order.status}
                </span>
              </div>
              
              <div className="space-y-4">
                <div>
                  <h3 className="text-sm font-medium text-slate-700 mb-1">Customer Name</h3>
                  <p className="text-slate-900">{order.customer_name}</p>
                </div>
                <div>
                  <h3 className="text-sm font-medium text-slate-700 mb-1">Email</h3>
                  <p className="text-slate-900">{order.customer_email}</p>
                </div>
                <div>
                  <h3 className="text-sm font-medium text-slate-700 mb-1">Shipping Address</h3>
                  <p className="text-slate-900 whitespace-pre-line">{order.shipping_address}</p>
                </div>
              </div>
            </div>
            
            <div className="bg-white/60 backdrop-blur-sm rounded-2xl p-8 border border-slate-200/50">
              <h2 className="text-2xl font-semibold text-slate-900 mb-6" style={{ fontFamily: 'Playfair Display, serif' }}>
                Items Ordered
              </h2>
              
              <div className="space-y-4">
                {order.items.map((item) => (
                  <div key={item.id} className="flex gap-4 pb-4 border-b border-slate-200 last:border-0">
                    <img
                      src={item.image_url || 'https://images.unsplash.com/photo-1541643600914-78b084683601?w=200'}
                      alt={item.name}
                      className="w-20 h-20 object-cover rounded-lg"
                    />
                    <div className="flex-1">
                      <p className="text-sm text-rose-600 font-medium">{item.brand}</p>
                      <h3 className="text-lg font-semibold text-slate-900 mb-1">
                        {item.name}
                      </h3>
                      <div className="flex justify-between items-end">
                        <p className="text-slate-600">Quantity: {item.quantity}</p>
                        <p className="text-lg font-bold text-slate-900">
                          ${(item.price * item.quantity).toFixed(2)}
                        </p>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
          
          <div className="lg:col-span-1">
            <div className="bg-white/60 backdrop-blur-sm rounded-2xl p-8 border border-slate-200/50 sticky top-24">
              <h2 className="text-2xl font-semibold text-slate-900 mb-6" style={{ fontFamily: 'Playfair Display, serif' }}>
                Order Summary
              </h2>
              
              <div className="space-y-4 mb-6">
                <div className="flex justify-between text-slate-700">
                  <span>Subtotal</span>
                  <span className="font-semibold">${order.total.toFixed(2)}</span>
                </div>
                <div className="flex justify-between text-slate-700">
                  <span>Shipping</span>
                  <span className="font-semibold">Free</span>
                </div>
                <div className="border-t border-slate-200 pt-4 flex justify-between text-lg font-bold text-slate-900">
                  <span>Total</span>
                  <span>${order.total.toFixed(2)}</span>
                </div>
              </div>
              
              <div className="bg-rose-50 rounded-lg p-4 flex items-start gap-3">
                <Package className="w-5 h-5 text-rose-600 mt-0.5" />
                <div>
                  <p className="text-sm font-medium text-rose-900 mb-1">Order Status</p>
                  <p className="text-sm text-rose-700">
                    Your order is currently {order.status}. You'll receive updates via email.
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
