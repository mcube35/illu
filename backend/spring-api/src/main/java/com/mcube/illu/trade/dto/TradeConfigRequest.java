package com.mcube.illu.trade.dto;

import java.math.BigDecimal;

public record TradeConfigRequest(
        String exchange,
        String apiKey,
        String apiSecret,
        BigDecimal longInputPct,
        BigDecimal shortInputPct,
        Boolean isRunning
) {}