import React, { useEffect, useState } from "react";
import { API_URL } from "../const.ts";

interface TradeHistory {
  pnl: number;
  pnlRatio: number;
  ctime: string;
  utime: string;
}

const TradeHistoryList: React.FC = () => {
  const [history, setHistory] = useState<TradeHistory[]>([]);

  useEffect(() => {
    fetch(`${API_URL}/api/trade/history`)
      .then((res) => res.json())
      .then((data) => setHistory(data))
      .catch((err) => console.error(err));
  }, []);

  const formatDate = (ms: string) => {
    const d = new Date(Number(ms));
    return d.toLocaleString();
  };

  return (
    <div className="p-6">
      <h1 className="text-xl font-bold mb-4">Trade History</h1>
      <table className="min-w-full border border-gray-300">
        <thead>
          <tr className="bg-gray-100">
            <th className="p-2 border">PNL</th>
            <th className="p-2 border">PNL Ratio</th>
            <th className="p-2 border">매수 시점</th>
            <th className="p-2 border">매도 시점</th>
          </tr>
        </thead>
        <tbody>
          {history.map((h, i) => (
            <tr key={i} className="text-center">
              <td className={`p-2 border ${h.pnl >= 0 ? "text-green-600" : "text-red-600"}`}>
                {h.pnl.toFixed(2)}
              </td>
              <td className={`p-2 border ${h.pnlRatio >= 0 ? "text-green-600" : "text-red-600"}`}>
                {h.pnlRatio.toFixed(2)}%
              </td>
              <td className="p-2 border">{formatDate(h.ctime)}</td>
              <td className="p-2 border">{formatDate(h.utime)}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default TradeHistoryList;
