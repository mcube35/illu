package com.mcube.illu.trade.service;

import com.mcube.illu.trade.dto.TradeConfigRequest;
import com.mcube.illu.trade.dto.TradeConfigResponse;
import com.mcube.illu.trade.entity.TradeConfig;
import com.mcube.illu.trade.repository.TradeConfigRepository;
import com.mcube.illu.user.entity.User;
import com.mcube.illu.user.repository.UserRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

import java.util.Optional;

@Service
@RequiredArgsConstructor
public class TradeService {
    private final TradeConfigRepository tradeConfigRepository;
    private final UserRepository userRepository;

    private Long getDummyUserId() {
        return 1L;
    }

    public TradeConfigResponse getConfig() {
        return toResponse(tradeConfigRepository.findByUserId(getDummyUserId()));
    }

    public TradeConfigResponse createConfig(TradeConfigRequest req) {
        User user = userRepository.findById(getDummyUserId())
                .orElseThrow(() -> new IllegalArgumentException("User not found"));

        TradeConfig saved = tradeConfigRepository.save(TradeConfig.builder()
                .user(user)
                .exchange(req.exchange())
                .apiKey(req.apiKey())
                .apiSecret(req.apiSecret())
                .longInputPct(req.longInputPct())
                .shortInputPct(req.shortInputPct())
                .build()
        );
        return toResponse(saved);
    }

    public TradeConfigResponse updateConfig(TradeConfigRequest e) {
        TradeConfig entity = tradeConfigRepository.findByUserId(getDummyUserId());
        entity.setExchange(e.exchange());
        entity.setApiKey(e.apiKey());
        entity.setApiSecret(e.apiSecret());
        entity.setLongInputPct(e.longInputPct());
        entity.setShortInputPct(e.shortInputPct());
        return toResponse(tradeConfigRepository.save(entity));
    }

    public void deleteConfig() {
        TradeConfig e = tradeConfigRepository.findByUserId(getDummyUserId());
        tradeConfigRepository.deleteById(e.getId());
    }

    private TradeConfigResponse toResponse(TradeConfig config) {
        return new TradeConfigResponse(
                config.getExchange(),
                config.getApiKey(),
                config.getApiSecret(),
                config.getLongInputPct(),
                config.getShortInputPct()
        );
    }
}