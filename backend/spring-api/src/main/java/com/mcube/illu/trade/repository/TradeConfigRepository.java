package com.mcube.illu.trade.repository;

import com.mcube.illu.trade.entity.TradeConfig;
import org.springframework.data.jpa.repository.JpaRepository;

public interface TradeConfigRepository extends JpaRepository<TradeConfig, Long> {
    TradeConfig findByUserId(Long userId);
}
