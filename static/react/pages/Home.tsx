import { useEffect } from 'react';
import { Link } from 'react-router';
import { Sparkles } from 'lucide-react';
import Navbar from '../components/Navbar';

export default function Home() {
  useEffect(() => {
    const link = document.createElement('link');
    link.href = 'https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;500;600;700&family=Inter:wght@300;400;500;600&display=swap';
    link.rel = 'stylesheet';
    document.head.appendChild(link);
  }, []);

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-rose-50/30 to-amber-50/20">
      <Navbar />
      
      <div className="relative overflow-hidden">
        {/* Hero Section */}
        <div className="container mx-auto px-6 py-20 lg:py-32">
          <div className="grid lg:grid-cols-2 gap-12 items-center">
            <div className="space-y-8">
              <div className="inline-flex items-center gap-2 px-4 py-2 bg-white/80 backdrop-blur-sm rounded-full border border-rose-200/50 shadow-sm">
                <Sparkles className="w-4 h-4 text-rose-500" />
                <span className="text-sm font-medium text-slate-700">Luxury Fragrances</span>
              </div>
              
              <h1 className="text-5xl lg:text-7xl font-bold text-slate-900 leading-tight" style={{ fontFamily: 'Playfair Display, serif' }}>
                Discover Your
                <span className="block bg-gradient-to-r from-rose-600 to-amber-600 bg-clip-text text-transparent">
                  Signature Scent
                </span>
              </h1>
              
              <p className="text-lg text-slate-600 leading-relaxed max-w-lg">
                Explore our curated collection of luxury perfumes from the world's most prestigious houses. Each fragrance tells a unique story.
              </p>
              
              <div className="flex gap-4">
                <Link
                  to="/shop"
                  className="px-8 py-4 bg-gradient-to-r from-rose-600 to-rose-700 text-white font-semibold rounded-lg shadow-lg shadow-rose-500/30 hover:shadow-xl hover:shadow-rose-500/40 transition-all duration-300 hover:-translate-y-0.5"
                >
                  Shop Collection
                </Link>
                <Link
                  to="/shop"
                  className="px-8 py-4 bg-white/80 backdrop-blur-sm text-slate-700 font-semibold rounded-lg border border-slate-200 hover:bg-white hover:border-slate-300 transition-all duration-300"
                >
                  Learn More
                </Link>
              </div>
            </div>
            
            <div className="relative">
              <div className="absolute inset-0 bg-gradient-to-tr from-rose-400/20 to-amber-400/20 blur-3xl rounded-full"></div>
              <img
                src="https://images.unsplash.com/photo-1541643600914-78b084683601?w=800&q=80"
                alt="Luxury perfume bottle"
                className="relative rounded-2xl shadow-2xl w-full object-cover aspect-square"
              />
              <div className="absolute -bottom-6 -right-6 bg-white/95 backdrop-blur-sm p-6 rounded-2xl shadow-xl border border-slate-100">
                <p className="text-sm text-slate-600 mb-1">Featured Collection</p>
                <p className="text-2xl font-bold text-slate-900" style={{ fontFamily: 'Playfair Display, serif' }}>8 Fragrances</p>
              </div>
            </div>
          </div>
        </div>
        
        {/* Features */}
        <div className="container mx-auto px-6 py-20">
          <div className="grid md:grid-cols-3 gap-8">
            {[
              { title: 'Authentic Products', desc: 'Only genuine luxury fragrances from authorized distributors' },
              { title: 'Free Shipping', desc: 'Complimentary shipping on all orders over $100' },
              { title: 'Expert Curation', desc: 'Hand-selected by our team of fragrance specialists' }
            ].map((feature, i) => (
              <div key={i} className="p-8 bg-white/60 backdrop-blur-sm rounded-2xl border border-slate-200/50 hover:bg-white hover:shadow-lg transition-all duration-300">
                <h3 className="text-xl font-semibold text-slate-900 mb-3" style={{ fontFamily: 'Playfair Display, serif' }}>
                  {feature.title}
                </h3>
                <p className="text-slate-600">{feature.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
