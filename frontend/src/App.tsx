import './index.css'
import './App.css'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import TradeSidebar from "./trade/TradeSidebar.tsx";
import TradeHistoryList from "./trade/TradeHistoryList";
import Login from './auth/Login.tsx';

function App() {
  return (
    <Router>
      <Routes>
        <Route
          path="/trade"
          element={
            <div className="flex">
              <div className="flex-1">
                <TradeHistoryList />
              </div>
              <div className="w-80">
                <TradeSidebar />
              </div>
            </div>
          }
        />
        <Route path='/auth/login' element={<Login/>} />
      </Routes>
    </Router>
  )
}

export default App
