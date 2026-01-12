import { Link, useNavigate } from 'react-router';
import { Trash2, Plus, Minus, ShoppingBag } from 'lucide-react';
import { useAuth } from '../context/AuthContext';
import Navbar from '../components/Navbar';
import { useCart } from '../hooks/useCart';

export default function Cart() {
  const { user, loginWithGoogle } = useAuth();
  const navigate = useNavigate();
  const { cart, updateCartItem, removeFromCart } = useCart();

  if (!user) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-50 via-rose-50/30 to-amber-50/20">
        <Navbar />
        <div className="container mx-auto px-6 py-12 text-center">
          <ShoppingBag className="w-16 h-16 text-slate-300 mx-auto mb-4" />
          <h2 className="text-2xl font-semibold text-slate-900 mb-4" style={{ fontFamily: 'Playfair Display, serif' }}>
            Sign in to view your cart
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

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-rose-50/30 to-amber-50/20">
      <Navbar />
      
      <div className="container mx-auto px-6 py-12">
        <h1 className="text-4xl lg:text-5xl font-bold text-slate-900 mb-8" style={{ fontFamily: 'Playfair Display, serif' }}>
          Shopping Cart
        </h1>
        
        {cart.length === 0 ? (
          <div className="text-center py-16 bg-white/60 backdrop-blur-sm rounded-2xl border border-slate-200/50">
            <ShoppingBag className="w-16 h-16 text-slate-300 mx-auto mb-4" />
            <p className="text-xl text-slate-600 mb-6">Your cart is empty</p>
            <Link
              to="/shop"
              className="inline-block px-8 py-3 bg-gradient-to-r from-rose-600 to-rose-700 text-white font-semibold rounded-lg hover:shadow-lg transition-shadow"
            >
              Continue Shopping
            </Link>
          </div>
        ) : (
          <div className="grid lg:grid-cols-3 gap-8">
            <div className="lg:col-span-2 space-y-4">
              {cart.map((item) => (
                <div
                  key={item.id}
                  className="bg-white/60 backdrop-blur-sm rounded-2xl p-6 border border-slate-200/50 hover:shadow-lg transition-shadow"
                >
                  <div className="flex gap-6">
                    <img
                      src={item.image_url || 'https://images.unsplash.com/photo-1541643600914-78b084683601?w=200'}
                      alt={item.name}
                      className="w-24 h-24 object-cover rounded-lg"
                    />
                    
                    <div className="flex-1">
                      <p className="text-sm text-rose-600 font-medium">{item.brand}</p>
                      <h3 className="text-lg font-semibold text-slate-900 mb-1" style={{ fontFamily: 'Playfair Display, serif' }}>
                        {item.name}
                      </h3>
                      <p className="text-slate-600 mb-4">${item.price.toFixed(2)}</p>
                      
                      <div className="flex items-center gap-4">
                        <div className="flex items-center gap-2">
                          <button
                            onClick={() => updateCartItem(item.id, Math.max(1, item.quantity - 1))}
                            className="w-8 h-8 bg-white border border-slate-300 rounded-lg hover:bg-slate-50 transition-colors flex items-center justify-center"
                          >
                            <Minus className="w-4 h-4" />
                          </button>
                          <span className="w-12 text-center font-semibold">
                            {item.quantity}
                          </span>
                          <button
                            onClick={() => updateCartItem(item.id, item.quantity + 1)}
                            className="w-8 h-8 bg-white border border-slate-300 rounded-lg hover:bg-slate-50 transition-colors flex items-center justify-center"
                          >
                            <Plus className="w-4 h-4" />
                          </button>
                        </div>
                        
                        <button
                          onClick={() => removeFromCart(item.id)}
                          className="ml-auto text-slate-400 hover:text-red-600 transition-colors"
                        >
                          <Trash2 className="w-5 h-5" />
                        </button>
                      </div>
                    </div>
                  </div>
                </div>
              ))}
            </div>
            
            <div className="lg:col-span-1">
              <div className="bg-white/60 backdrop-blur-sm rounded-2xl p-8 border border-slate-200/50 sticky top-24">
                <h2 className="text-2xl font-semibold text-slate-900 mb-6" style={{ fontFamily: 'Playfair Display, serif' }}>
                  Order Summary
                </h2>
                
                <div className="space-y-4 mb-6">
                  <div className="flex justify-between text-slate-700">
                    <span>Subtotal</span>
                    <span className="font-semibold">${subtotal.toFixed(2)}</span>
                  </div>
                  <div className="flex justify-between text-slate-700">
                    <span>Shipping</span>
                    <span className="font-semibold">Free</span>
                  </div>
                  <div className="border-t border-slate-200 pt-4 flex justify-between text-lg font-bold text-slate-900">
                    <span>Total</span>
                    <span>${subtotal.toFixed(2)}</span>
                  </div>
                </div>
                
                <button
                  onClick={() => navigate('/checkout')}
                  className="w-full px-8 py-4 bg-gradient-to-r from-rose-600 to-rose-700 text-white font-semibold rounded-lg shadow-lg shadow-rose-500/30 hover:shadow-xl hover:shadow-rose-500/40 transition-all duration-300 hover:-translate-y-0.5"
                >
                  Proceed to Checkout
                </button>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
