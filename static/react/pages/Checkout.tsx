import { useState } from 'react';
import { useNavigate } from 'react-router';
import { Loader2 } from 'lucide-react';
import { useAuth } from '../context/AuthContext';
import Navbar from '../components/Navbar';
import { useCart } from '../hooks/useCart';

export default function Checkout() {
  const { user, loginWithGoogle } = useAuth();
  const navigate = useNavigate();
  const { cart } = useCart();
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [formData, setFormData] = useState({
    customer_name: user?.username || user?.email || '',
    customer_email: user?.email || '',
    shipping_address: '',
  });

  if (!user) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-50 via-rose-50/30 to-amber-50/20">
        <Navbar />
        <div className="container mx-auto px-6 py-12 text-center">
          <h2 className="text-2xl font-semibold text-slate-900 mb-4" style={{ fontFamily: 'Playfair Display, serif' }}>
            Sign in to checkout
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

  const subtotal = cart.reduce((sum, item) => sum + item.price * item.quantity, 0);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsSubmitting(true);

    try {
      const response = await fetch('/api/orders/create/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData),
      });

      if (response.ok) {
        const data = await response.json();
        navigate(`/orders/${data.id}`);
      } else {
        alert('Failed to place order. Please try again.');
      }
    } catch (error) {
      console.error('Error placing order:', error);
      alert('An error occurred. Please try again.');
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-rose-50/30 to-amber-50/20">
      <Navbar />
      
      <div className="container mx-auto px-6 py-12">
        <h1 className="text-4xl lg:text-5xl font-bold text-slate-900 mb-8" style={{ fontFamily: 'Playfair Display, serif' }}>
          Checkout
        </h1>
        
        <div className="grid lg:grid-cols-3 gap-8">
          <div className="lg:col-span-2">
            <form onSubmit={handleSubmit} className="bg-white/60 backdrop-blur-sm rounded-2xl p-8 border border-slate-200/50">
              <h2 className="text-2xl font-semibold text-slate-900 mb-6" style={{ fontFamily: 'Playfair Display, serif' }}>
                Shipping Information
              </h2>
              
              <div className="space-y-6">
                <div>
                  <label className="block text-sm font-medium text-slate-700 mb-2">
                    Full Name
                  </label>
                  <input
                    type="text"
                    required
                    value={formData.customer_name}
                    onChange={(e) => setFormData({ ...formData, customer_name: e.target.value })}
                    className="w-full px-4 py-3 bg-white border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-rose-500 focus:border-transparent"
                  />
                </div>
                
                <div>
                  <label className="block text-sm font-medium text-slate-700 mb-2">
                    Email
                  </label>
                  <input
                    type="email"
                    required
                    value={formData.customer_email}
                    onChange={(e) => setFormData({ ...formData, customer_email: e.target.value })}
                    className="w-full px-4 py-3 bg-white border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-rose-500 focus:border-transparent"
                  />
                </div>
                
                <div>
                  <label className="block text-sm font-medium text-slate-700 mb-2">
                    Shipping Address
                  </label>
                  <textarea
                    required
                    rows={4}
                    value={formData.shipping_address}
                    onChange={(e) => setFormData({ ...formData, shipping_address: e.target.value })}
                    className="w-full px-4 py-3 bg-white border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-rose-500 focus:border-transparent resize-none"
                    placeholder="Street address, city, state, zip code, country"
                  />
                </div>
              </div>
              
              <button
                type="submit"
                disabled={isSubmitting}
                className="w-full mt-8 px-8 py-4 bg-gradient-to-r from-rose-600 to-rose-700 text-white font-semibold rounded-lg shadow-lg shadow-rose-500/30 hover:shadow-xl hover:shadow-rose-500/40 transition-all duration-300 hover:-translate-y-0.5 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
              >
                {isSubmitting ? (
                  <>
                    <Loader2 className="w-5 h-5 animate-spin" />
                    Placing Order...
                  </>
                ) : (
                  'Place Order'
                )}
              </button>
            </form>
          </div>
          
          <div className="lg:col-span-1">
            <div className="bg-white/60 backdrop-blur-sm rounded-2xl p-8 border border-slate-200/50 sticky top-24">
              <h2 className="text-2xl font-semibold text-slate-900 mb-6" style={{ fontFamily: 'Playfair Display, serif' }}>
                Order Summary
              </h2>
              
              <div className="space-y-4 mb-6">
                {cart.map((item) => (
                  <div key={item.id} className="flex justify-between text-slate-700">
                    <span className="flex-1">
                      {item.name} × {item.quantity}
                    </span>
                    <span className="font-semibold">
                      ${(item.price * item.quantity).toFixed(2)}
                    </span>
                  </div>
                ))}
              </div>
              
              <div className="border-t border-slate-200 pt-4 space-y-2 mb-6">
                <div className="flex justify-between text-slate-700">
                  <span>Subtotal</span>
                  <span className="font-semibold">${subtotal.toFixed(2)}</span>
                </div>
                <div className="flex justify-between text-slate-700">
                  <span>Shipping</span>
                  <span className="font-semibold">Free</span>
                </div>
                <div className="border-t border-slate-200 pt-2 flex justify-between text-lg font-bold text-slate-900">
                  <span>Total</span>
                  <span>${subtotal.toFixed(2)}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
