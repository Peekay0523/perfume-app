import { BrowserRouter as Router, Routes, Route } from "react-router";
import { AuthProvider } from "./context/AuthContext"; // Custom auth context
import HomePage from "./pages/Home";
import ShopPage from "./pages/Shop";
import ProductPage from "./pages/Product";
import CartPage from "./pages/Cart";
import CheckoutPage from "./pages/Checkout";
import OrdersPage from "./pages/Orders";
import OrderDetailsPage from "./pages/OrderDetails";
import AuthCallbackPage from "./pages/AuthCallback";
import AuthPage from "./pages/Auth";

export default function App() {
  return (
    <AuthProvider>
      <Router>
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/shop" element={<ShopPage />} />
          <Route path="/product/:id" element={<ProductPage />} />
          <Route path="/cart" element={<CartPage />} />
          <Route path="/checkout" element={<CheckoutPage />} />
          <Route path="/orders" element={<OrdersPage />} />
          <Route path="/orders/:id" element={<OrderDetailsPage />} />
          <Route path="/auth/callback" element={<AuthCallbackPage />} />
          <Route path="/auth" element={<AuthPage />} />
        </Routes>
      </Router>
    </AuthProvider>
  );
}
