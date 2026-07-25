import {
  BrowserRouter,
  Navigate,
  Route,
  Routes,
  useNavigate,
} from "react-router-dom";
import LoginPage from "./features/auth/LoginPage";
import ProtectedRoutes from "./components/ProtectedRoutes";
import Dashboard from "./features/dashboard/Dashboard";
import ModalRenderer from "./components/modal/ModalRenderer";
import AppLayout from "./components/AppLayout";
import Test from "./Test.jsx";
import Profile from "./features/profiles/Profile";
import Categories from "./features/categories/Categories";
import Tags from "./features/tags/Tags";
import AddTransaction from "./features/transactions/AddTransactionPage";
import TransactionsPage from "./features/transactions/TransactionsPage";
import Setup from "./features/setup/SetupPage";
import RequireProfile from "./features/profiles/RequireProfile";

function Home() {
  <Navigate to={"/dashboard"} replace />;
}
function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/login" element={<LoginPage />}></Route>
        <Route element={<ProtectedRoutes />}>
          <Route path="/setup" element={<Setup />} />
          <Route element={<RequireProfile />}>
            <Route element={<AppLayout />}>
              <Route path="/dashboard" element={<Dashboard />} />
              <Route path="/history" element={<TransactionsPage />} />
              <Route path="/profile" element={<Profile />} />
              <Route path="/profile/categories" element={<Categories />} />
              <Route path="/profile/tags" element={<Tags />} />
            </Route>
            <Route path="/add-transaction" element={<AddTransaction />} />
          </Route>
        </Route>
        <Route path="/test" element={<Test />} />
      </Routes>
      <ModalRenderer />
    </BrowserRouter>
  );
}

export default App;
