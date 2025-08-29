import './index.css';
import './App.css';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { SidebarProvider, SidebarTrigger } from "@/components/ui/sidebar";
import TradeHistoryList from "./trade/TradeHistoryList";
import TradeSidebar from "./trade/TradeSidebar.tsx";
import Login from './auth/Login.tsx';

function App() {
  return (
    <Router>
      <SidebarProvider>
        <div className="min-h-screen w-full">
          <Routes>
            <Route
              path="/trade"
              element={
                <div className="flex relative w-full">
                  <TradeHistoryList />
                  <SidebarTrigger/>
                  <TradeSidebar />
                </div>
              }
            />
            <Route path='/auth/login' element={<Login />} />
          </Routes>
        </div>
      </SidebarProvider>
    </Router>
  );
}

export default App;