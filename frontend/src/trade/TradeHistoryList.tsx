import { useEffect, useState } from "react";
import { API_URL } from "../const.ts";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";

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
    <div className="container mx-auto py-10">
      <h1 className="text-2xl font-bold mb-4">Trade History</h1>
      <div className="rounded-md border">
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>PNL</TableHead>
              <TableHead>PNL Ratio</TableHead>
              <TableHead>매수 시점</TableHead>
              <TableHead>매도 시점</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {history.length > 0 ? (
              history.map((h, i) => (
                <TableRow key={i}>
                  <TableCell>{h.pnl.toFixed(2)}</TableCell>
                  <TableCell>{h.pnlRatio.toFixed(2)}%</TableCell>
                  <TableCell>{formatDate(h.ctime)}</TableCell>
                  <TableCell>{formatDate(h.utime)}</TableCell>
                </TableRow>
              ))
            ) : (
              <TableRow>
                <TableCell colSpan={4} className="h-24 text-center">
                  No results.
                </TableCell>
              </TableRow>
            )}
          </TableBody>
        </Table>
      </div>
    </div>
  );
};

export default TradeHistoryList;