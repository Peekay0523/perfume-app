import { Link } from 'react-router';
import type { Perfume } from '../shared/types';

interface ProductCardProps {
  perfume: Perfume;
}

export default function ProductCard({ perfume }: ProductCardProps) {
  return (
    <Link
      to={`/product/${perfume.id}`}
      className="group bg-white/60 backdrop-blur-sm rounded-2xl overflow-hidden border border-slate-200/50 hover:shadow-2xl hover:border-slate-300 transition-all duration-300 hover:-translate-y-1"
    >
      <div className="aspect-square overflow-hidden bg-gradient-to-br from-slate-100 to-rose-50">
        <img
          src={perfume.image_url || 'https://images.unsplash.com/photo-1541643600914-78b084683601?w=400'}
          alt={perfume.name}
          className="w-full h-full object-cover group-hover:scale-110 transition-transform duration-500"
        />
      </div>
      
      <div className="p-6">
        <p className="text-sm font-medium text-rose-600 mb-2">{perfume.brand}</p>
        <h3 className="text-xl font-semibold text-slate-900 mb-2 line-clamp-1" style={{ fontFamily: 'Playfair Display, serif' }}>
          {perfume.name}
        </h3>
        <p className="text-sm text-slate-600 mb-4 line-clamp-2">
          {perfume.description}
        </p>
        <div className="flex items-baseline justify-between">
          <span className="text-2xl font-bold text-slate-900">
            ${perfume.price.toFixed(2)}
          </span>
          {perfume.size_ml && (
            <span className="text-sm text-slate-500">{perfume.size_ml}ml</span>
          )}
        </div>
      </div>
    </Link>
  );
}
