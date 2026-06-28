import { Routes, Route, Link } from "react-router-dom";
import Dashboard from "./pages/Dashboard";
import Admin from "./pages/Admin";

export default function App() {
  return (
    <div className="min-h-screen bg-gray-50">
      <nav className="bg-white shadow-sm border-b px-6 py-3 flex items-center justify-between">
        <Link to="/" className="text-xl font-bold text-blue-600">
          SprintSense
        </Link>
        <Link
          to="/admin"
          className="text-sm text-gray-500 hover:text-gray-700"
        >
          Admin
        </Link>
      </nav>
      <main className="p-6">
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/admin" element={<Admin />} />
        </Routes>
      </main>
    </div>
  );
}
