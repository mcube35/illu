package com.mcube.illu.trade.service;

import com.mcube.illu.trade.dto.TradeConfigRequest;
import com.mcube.illu.trade.dto.TradeConfigResponse;
import com.mcube.illu.trade.entity.TradeConfig;
import com.mcube.illu.trade.repository.TradeConfigRepository;
import com.mcube.illu.trade.repository.TradeHistoryRepository;
import com.mcube.illu.user.entity.User;
import com.mcube.illu.user.repository.UserRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

@Service
@RequiredArgsConstructor
public class TradeService {
    private final TradeConfigRepository tradeConfigRepository;
    private final TradeHistoryRepository tradeHistoryRepository;
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
                .passphrase(req.passphrase())
                .longInputPct(req.longInputPct())
                .shortInputPct(req.shortInputPct())
                .isRunning(req.isRunning())
                .build()
        );
        return toResponse(saved);
    }

    public TradeConfigResponse updateConfig(TradeConfigRequest e) {
        Long userId = getDummyUserId();
        TradeConfig entity = tradeConfigRepository.findByUserId(userId);
        entity.setExchange(e.exchange());
        entity.setApiKey(e.apiKey());
        entity.setApiSecret(e.apiSecret());
        entity.setPassphrase(e.passphrase());
        entity.setLongInputPct(e.longInputPct());
        entity.setShortInputPct(e.shortInputPct());
        entity.setIsRunning(e.isRunning());

        return toResponse(tradeConfigRepository.save(entity));
    }

    public void deleteConfig() {
        Long userId = getDummyUserId();
        TradeConfig entity = tradeConfigRepository.findByUserId(userId);
        tradeConfigRepository.deleteById(entity.getId());
    }

    private TradeConfigResponse toResponse(TradeConfig config) {
        return new TradeConfigResponse(
                config.getExchange(),
                config.getApiKey(),
                config.getApiSecret(),
                config.getPassphrase(),
                config.getLongInputPct(),
                config.getShortInputPct(),
                config.getIsRunning()
        );
    }
}