import { Loader2 } from 'lucide-react';
import Navbar from '../components/Navbar';
import ProductCard from '../components/ProductCard';
import { usePerfumes } from '../hooks/usePerfumes';

export default function Shop() {
  const { perfumes, isLoading } = usePerfumes();

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
        <div className="mb-12">
          <h1 className="text-4xl lg:text-5xl font-bold text-slate-900 mb-4" style={{ fontFamily: 'Playfair Display, serif' }}>
            Our Collection
          </h1>
          <p className="text-lg text-slate-600">
            Discover timeless fragrances from the world's most prestigious perfume houses
          </p>
        </div>
        
        <div className="grid md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-8">
          {perfumes.map((perfume) => (
            <ProductCard key={perfume.id} perfume={perfume} />
          ))}
        </div>
      </div>
    </div>
  );
}
