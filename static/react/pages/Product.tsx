import { useState } from 'react';
import { useParams, useNavigate } from 'react-router';
import { Loader2, ShoppingCart, ArrowLeft } from 'lucide-react';
import { useAuth } from '../context/AuthContext';
import Navbar from '../components/Navbar';
import { usePerfume } from '../hooks/usePerfumes';
import { useCart } from '../hooks/useCart';

export default function Product() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const { user, loginWithGoogle } = useAuth();
  const { perfume, isLoading } = usePerfume(id!);
  const { addToCart } = useCart();
  const [quantity, setQuantity] = useState(1);
  const [isAdding, setIsAdding] = useState(false);

  const handleAddToCart = async () => {
    if (!user) {
      navigate('/auth');
      return;
    }

    setIsAdding(true);
    await addToCart(perfume!.id, quantity);
    setIsAdding(false);
    navigate('/cart');
  };

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

  if (!perfume) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-50 via-rose-50/30 to-amber-50/20">
        <Navbar />
        <div className="container mx-auto px-6 py-12 text-center">
          <p className="text-slate-600">Perfume not found</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-rose-50/30 to-amber-50/20">
      <Navbar />
      
      <div className="container mx-auto px-6 py-12">
        <button
          onClick={() => navigate('/shop')}
          className="flex items-center gap-2 text-slate-600 hover:text-rose-600 transition-colors mb-8"
        >
          <ArrowLeft className="w-4 h-4" />
          Back to Shop
        </button>
        
        <div className="grid lg:grid-cols-2 gap-12">
          <div className="bg-white/60 backdrop-blur-sm rounded-2xl overflow-hidden border border-slate-200/50 shadow-xl">
            <img
              src={perfume.image_url || 'https://images.unsplash.com/photo-1541643600914-78b084683601?w=800'}
              alt={perfume.name}
              className="w-full aspect-square object-cover"
            />
          </div>
          
          <div className="flex flex-col">
            <div className="mb-8">
              <p className="text-sm font-medium text-rose-600 mb-2 uppercase tracking-wider">
                {perfume.brand}
              </p>
              <h1 className="text-4xl lg:text-5xl font-bold text-slate-900 mb-4" style={{ fontFamily: 'Playfair Display, serif' }}>
                {perfume.name}
              </h1>
              <p className="text-3xl font-bold text-slate-900 mb-6">
                ${perfume.price.toFixed(2)}
              </p>
              {perfume.size_ml && (
                <p className="text-slate-600 mb-4">Size: {perfume.size_ml}ml</p>
              )}
            </div>
            
            {perfume.description && (
              <div className="mb-8">
                <h2 className="text-xl font-semibold text-slate-900 mb-3" style={{ fontFamily: 'Playfair Display, serif' }}>
                  Description
                </h2>
                <p className="text-slate-700 leading-relaxed">{perfume.description}</p>
              </div>
            )}
            
            {perfume.notes && (
              <div className="mb-8">
                <h2 className="text-xl font-semibold text-slate-900 mb-3" style={{ fontFamily: 'Playfair Display, serif' }}>
                  Fragrance Notes
                </h2>
                <div className="flex flex-wrap gap-2">
                  {perfume.notes.split(',').map((note, i) => (
                    <span
                      key={i}
                      className="px-4 py-2 bg-white/80 backdrop-blur-sm text-slate-700 rounded-full border border-slate-200 text-sm"
                    >
                      {note.trim()}
                    </span>
                  ))}
                </div>
              </div>
            )}
            
            <div className="mt-auto">
              <div className="flex items-center gap-4 mb-6">
                <label className="text-slate-700 font-medium">Quantity:</label>
                <div className="flex items-center gap-2">
                  <button
                    onClick={() => setQuantity(Math.max(1, quantity - 1))}
                    className="w-10 h-10 bg-white border border-slate-300 rounded-lg hover:bg-slate-50 transition-colors font-semibold"
                  >
                    -
                  </button>
                  <span className="w-12 text-center font-semibold text-slate-900">
                    {quantity}
                  </span>
                  <button
                    onClick={() => setQuantity(quantity + 1)}
                    className="w-10 h-10 bg-white border border-slate-300 rounded-lg hover:bg-slate-50 transition-colors font-semibold"
                  >
                    +
                  </button>
                </div>
              </div>
              
              <button
                onClick={handleAddToCart}
                disabled={isAdding}
                className="w-full px-8 py-4 bg-gradient-to-r from-rose-600 to-rose-700 text-white font-semibold rounded-lg shadow-lg shadow-rose-500/30 hover:shadow-xl hover:shadow-rose-500/40 transition-all duration-300 hover:-translate-y-0.5 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
              >
                {isAdding ? (
                  <>
                    <Loader2 className="w-5 h-5 animate-spin" />
                    Adding...
                  </>
                ) : (
                  <>
                    <ShoppingCart className="w-5 h-5" />
                    Add to Cart
                  </>
                )}
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
