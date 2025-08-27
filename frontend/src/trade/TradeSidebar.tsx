import { useState, useEffect } from 'react';
import './TradeSidebar.css';
import { API_URL } from "../const.ts";

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
          className="sidebar-select"
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
          <input
            type="password"
            className="sidebar-input"
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
          <input
            type="password"
            className="sidebar-input"
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
          <input
            type="password"
            className="sidebar-input"
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
          <input
            type="number"
            step="0.01"
            className="sidebar-input"
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
          <input
            type="number"
            step="0.01"
            placeholder="Short %"
            className="sidebar-input"
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
          <button onClick={() => setIsEditing(true)}>수정</button>
        ) : (
          <button onClick={handleSave}>저장</button>
        )}

        {/* 실행/중지 버튼 */}
        <button
          className={config.isRunning ? "stop-btn" : "start-btn"}
          onClick={handleToggle}
        >
          {config.isRunning ? "중지" : "실행"}
        </button>
      </div>
    </aside>
  );
}
