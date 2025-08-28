package com.mcube.illu.trade.dto;

import java.math.BigDecimal;

public record TradeHistoryResponse(
        BigDecimal pnl,
        BigDecimal pnlRatio,
        String ctime,
        String utime
) {}