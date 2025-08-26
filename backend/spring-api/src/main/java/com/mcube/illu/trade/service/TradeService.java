package com.mcube.illu.trade.service;

import com.mcube.illu.trade.dto.TradeConfigRequest;
import com.mcube.illu.trade.dto.TradeConfigResponse;
import com.mcube.illu.trade.entity.TradeConfig;
import com.mcube.illu.trade.repository.TradeConfigRepository;
import com.mcube.illu.user.entity.User;
import com.mcube.illu.user.repository.UserRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Service;
import org.springframework.scheduling.annotation.Async;
import org.springframework.web.client.RestTemplate;

import java.util.Map;

@Service
@RequiredArgsConstructor
public class TradeService {
    private final TradeConfigRepository tradeConfigRepository;
    private final UserRepository userRepository;

    private final RestTemplate restTemplate = new RestTemplate();
    private final String pythonUrl = "http://localhost:8000/trade/okx_auto";

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
                .isRunning(req.isRunning())
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
        entity.setIsRunning(e.isRunning());
        return toResponse(tradeConfigRepository.save(entity));
    }

    public void deleteConfig() {
        Long userId = getDummyUserId();
        TradeConfig e = tradeConfigRepository.findByUserId(userId);
        tradeConfigRepository.deleteById(e.getId());
        sendTradingCommandAsync(userId.toString(), "stop");
    }

    private TradeConfigResponse toResponse(TradeConfig config) {
        return new TradeConfigResponse(
                config.getExchange(),
                config.getApiKey(),
                config.getApiSecret(),
                config.getLongInputPct(),
                config.getShortInputPct(),
                config.getIsRunning()
        );
    }

    @Async
    public void sendTradingCommandAsync(String userId, String action) {
        Map<String, String> requestBody = Map.of(
                "user_id", userId,
                "action", action
        );

        HttpHeaders headers = new HttpHeaders();
        headers.setContentType(MediaType.APPLICATION_JSON);

        HttpEntity<Map<String, String>> request = new HttpEntity<>(requestBody, headers);

        try {
            ResponseEntity<String> response = restTemplate.postForEntity(pythonUrl, request, String.class);
            System.out.println("Python response: " + response.getBody());
        } catch (Exception e) {
            System.err.println("Failed to send trading command: " + e.getMessage());
        }
    }
}