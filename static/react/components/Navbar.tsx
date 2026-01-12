import { Link, useNavigate } from 'react-router';
import { ShoppingBag, User, LogOut, LogIn } from 'lucide-react';
import { useAuth } from '../context/AuthContext';
import { useCart } from '../hooks/useCart';

export default function Navbar() {
  const { user, logout, loginWithGoogle } = useAuth();
  const { cart } = useCart();
  const navigate = useNavigate();

  const cartItemCount = cart?.reduce((sum, item) => sum + item.quantity, 0) || 0;

  const handleLogin = () => {
    // Navigate to auth page for login/signup
    navigate('/auth');
  };

  const handleLogout = async () => {
    await logout();
  };

  return (
    <nav className="bg-white/80 backdrop-blur-md border-b border-slate-200/50 sticky top-0 z-50">
      <div className="container mx-auto px-6 py-4">
        <div className="flex items-center justify-between">
          <Link to="/" className="text-2xl font-bold text-slate-900" style={{ fontFamily: 'Playfair Display, serif' }}>
            Essence
          </Link>

          <div className="flex items-center gap-8">
            <Link to="/shop" className="text-slate-700 hover:text-rose-600 transition-colors font-medium">
              Shop
            </Link>

            {user && (
              <Link to="/orders" className="text-slate-700 hover:text-rose-600 transition-colors font-medium">
                Orders
              </Link>
            )}

            <Link to="/cart" className="relative text-slate-700 hover:text-rose-600 transition-colors">
              <ShoppingBag className="w-5 h-5" />
              {cartItemCount > 0 && (
                <span className="absolute -top-2 -right-2 bg-rose-600 text-white text-xs font-semibold rounded-full w-5 h-5 flex items-center justify-center">
                  {cartItemCount}
                </span>
              )}
            </Link>

            {user ? (
              <div className="flex items-center gap-4">
                <div className="flex items-center gap-2">
                  <User className="w-5 h-5 text-slate-700" />
                  <span className="text-sm text-slate-700 max-w-[120px] truncate">
                    {user.username || user.email}
                  </span>
                </div>
                <button
                  onClick={handleLogout}
                  className="text-slate-700 hover:text-rose-600 transition-colors"
                  title="Sign out"
                >
                  <LogOut className="w-5 h-5" />
                </button>
              </div>
            ) : (
              <Link
                to="/auth"
                className="px-4 py-2 bg-gradient-to-r from-rose-600 to-rose-700 text-white font-semibold rounded-lg hover:shadow-lg transition-shadow inline-flex items-center gap-2"
              >
                <LogIn className="w-4 h-4" />
                Sign In
              </Link>
            )}
          </div>
        </div>
      </div>
    </nav>
  );
}
