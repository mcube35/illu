import './index.css'
import TradeSidebar from "./trade/TradeSidebar.tsx";
import TradeHistoryList from "./trade/TradeHistoryList";

function App() {
  return (
    <div className="flex">
      <div className="flex-1">
        <TradeHistoryList />
      </div>
      <div className="w-80">
        <TradeSidebar />
      </div>
    </div>
  )
}

export default App
