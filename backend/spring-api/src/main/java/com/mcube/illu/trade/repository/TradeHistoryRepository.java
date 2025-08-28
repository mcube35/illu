package com.mcube.illu.trade.repository;

import com.mcube.illu.trade.entity.TradeHistory;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;

public interface TradeHistoryRepository extends JpaRepository<TradeHistory, Long> {
    List<TradeHistory> findByUserId(Long userId);
}
