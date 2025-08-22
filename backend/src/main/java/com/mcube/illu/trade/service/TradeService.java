package com.mcube.illu.trade.service;

import com.mcube.illu.trade.entity.TradeConfig;
import com.mcube.illu.trade.repository.TradeConfigRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

@Service
@RequiredArgsConstructor
public class TradeService {
    private final TradeConfigRepository tradeConfigRepository;

    private Long getDummyUserId() {
        return 1L;
    }

    public TradeConfig getConfig() {
        return tradeConfigRepository.findByUserId(getDummyUserId());
    }

    public TradeConfig createConfig(TradeConfig e) {
        return tradeConfigRepository.save(e);
    }

    public void deleteConfig() {
        TradeConfig e = tradeConfigRepository.findByUserId(getDummyUserId());
        tradeConfigRepository.deleteById(e.getId());
    }
}