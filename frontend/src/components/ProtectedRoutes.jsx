import { Navigate, Outlet } from "react-router-dom";
import { useAuth } from "../features/auth/AuthProvider";
import { Spinner } from "./ui/Spinner";

export default function ProtectedRoutes() {
  const { loading, user } = useAuth();

  if (loading) {
    return <Spinner />;
  }

  if (!user) {
    return <Navigate to={"/login"} replace />;
  }

  return <Outlet />;
}
