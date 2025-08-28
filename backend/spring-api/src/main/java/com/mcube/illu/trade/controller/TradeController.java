package com.mcube.illu.trade.controller;

import com.mcube.illu.trade.dto.TradeConfigRequest;
import com.mcube.illu.trade.dto.TradeConfigResponse;
import com.mcube.illu.trade.entity.TradeHistory;
import com.mcube.illu.trade.service.TradeService;
import lombok.RequiredArgsConstructor;
import org.springframework.web.bind.annotation.*;

@RestController
@RequiredArgsConstructor
@RequestMapping("/api/trade")
@CrossOrigin(origins = "http://localhost:5173")
public class TradeController {
    private final TradeService tradeService;

    @GetMapping("/config")
    public TradeConfigResponse getConfig() {
        return tradeService.getConfig();
    }

    @PostMapping("/config")
    public TradeConfigResponse createConfig(@RequestBody TradeConfigRequest req) {
        return tradeService.createConfig(req);
    }

    @PutMapping("/config")
    public TradeConfigResponse updateConfig(@RequestBody TradeConfigRequest req) {
        return tradeService.updateConfig(req);
    }

    @DeleteMapping("/config")
    public void deleteConfig() {
        tradeService.deleteConfig();
    }

}
