package com.mcube.illu.trade.dto;

import java.math.BigDecimal;

public record TradeConfigRequest(
        String exchange,
        String apiKey,
        String apiSecret,
        String passphrase,
        BigDecimal longInputPct,
        BigDecimal shortInputPct,
        Boolean isRunning
) {}