import { useState, useEffect } from 'react';
import { API_URL } from "../const.ts";
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button";
import { Select } from "@/components/ui/select";

type TradeConfig = {
  exchange: string;
  apiKey: string;
  apiSecret: string;
  passphrase: string;
  longInputPct: number;
  shortInputPct: number;
  isRunning: boolean;
}

export default function TradeSidebar() {
  const [isEditing, setIsEditing] = useState(false);
  const [config, setConfig] = useState<TradeConfig>({
    exchange: "",
    apiKey: "",
    apiSecret: "",
    passphrase: "",
    longInputPct: 0,
    shortInputPct: 0,
    isRunning: false,
  });


  const saveConfig = async (
    configData: TradeConfig,
    successMsg: string,
    errorMsg: string
  ) => {
    try {
      const res = await fetch(`${API_URL}/api/trade/config`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(configData),
      });
      if (!res.ok) throw new Error();
      setConfig(configData);
      alert(successMsg);
    } catch {
      alert(errorMsg);
    }
  };

  const reloadConfig = async () => {
    try {
      const res = await fetch(`${API_URL}/api/trade/config`);
      if (!res.ok) throw new Error();
      const data: TradeConfig = await res.json();
      setConfig(data);
    } catch (err) {
      console.error("Failed to reload config:", err);
    }
  };

  useEffect(() => {
    reloadConfig();
  }, []);

  // 저장 버튼
  const handleSave = async () => {
    await saveConfig(config, "저장 성공!", "저장 실패");
    setIsEditing(false)
  };

  // 실행/중지 버튼
  const handleToggle = async () => {
    const updated = { ...config, isRunning: !config.isRunning };
    await saveConfig(
      updated,
      updated.isRunning ? "실행 시작!" : "실행 중지!",
      "실행/중지 실패"
    );
  };

  return (
    <aside className="sidebar">
      <div className="sidebar-header">
        BTC TRADE CONFIG
        <span className="sidebar-version">v1.0</span>
      </div>

      <div className="sidebar-form">
        {/* Exchange */}
        <select
          disabled={!isEditing}
          value={config.exchange}
          onChange={(e) =>
            setConfig({ ...config, exchange: e.target.value })
          }
        >
          <option value="">Select Exchange</option>
          <option value="OKX">OKX</option>
        </select>

        {/* API Key */}
        <label>
          API KEY
          <Input
            type="password"
            disabled={!isEditing}
            value={config.apiKey}
            onChange={(e) =>
              setConfig({ ...config, apiKey: e.target.value })
            }
          />
        </label>

        {/* API Secret */}
        <label>
          API SECRET
          <Input
            type="password"
            disabled={!isEditing}
            value={config.apiSecret}
            onChange={(e) =>
              setConfig({ ...config, apiSecret: e.target.value })
            }
          />
        </label>

        {/* API passphrase */}
        <label>
          API Passphrase
          <Input
            type="password"
            disabled={!isEditing}
            value={config.passphrase}
            onChange={(e) =>
              setConfig({ ...config, passphrase: e.target.value })
            }
          />
        </label>

        {/* Long % */}
        <label>
          Long %
          <Input
            type="number"
            step="0.01"
            disabled={!isEditing}
            value={config.longInputPct}
            onChange={(e) =>
              setConfig({ ...config, longInputPct: Number(e.target.value) })
            }
          />
        </label>

        {/* Short % */}
        <label>
          Short %
          <Input
            type="number"
            step="0.01"
            placeholder="Short %"
            disabled={!isEditing}
            value={config.shortInputPct}
            onChange={(e) =>
              setConfig({ ...config, shortInputPct: Number(e.target.value) })
            }
          />
        </label>
      </div>

      <div className="sidebar-buttons">
        {!isEditing ? (
          <Button onClick={() => setIsEditing(true)}>수정</Button>
        ) : (
          <Button onClick={handleSave}>저장</Button>
        )}

        {/* 실행/중지 버튼 */}
        <Button
          className={config.isRunning ? "stop-btn" : "start-btn"}
          onClick={handleToggle}
        >
          {config.isRunning ? "중지" : "실행"}
        </Button>
      </div>
    </aside>
  );
}
