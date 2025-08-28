package com.mcube.illu.trade.repository;

import com.mcube.illu.trade.entity.TradeHistory;
import org.springframework.data.jpa.repository.JpaRepository;

public interface TradeHistoryRepository extends JpaRepository<TradeHistory, Long> {
    TradeHistory findByUserId(Long userId);
}
