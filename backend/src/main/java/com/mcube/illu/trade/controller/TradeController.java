package com.mcube.illu.trade.controller;

import com.mcube.illu.trade.entity.TradeConfig;
import com.mcube.illu.trade.service.TradeService;
import lombok.RequiredArgsConstructor;
import org.springframework.web.bind.annotation.*;

@RestController
@RequiredArgsConstructor
@RequestMapping("/api/trade")
public class TradeController {
    private final TradeService tradeService;

    @GetMapping("/config")
    public TradeConfig getConfig() {
        return tradeService.getConfig();
    }

    @PostMapping("/config")
    public TradeConfig createConfig(@RequestBody TradeConfig e) {
        return tradeService.createConfig(e);
    }

    @DeleteMapping("/config")
    public void deleteConfig() {
        tradeService.deleteConfig();
    }
}
