package com.mcube.illu.trade.entity;

import com.mcube.illu.user.entity.User;
import jakarta.persistence.*;
import lombok.*;

import java.math.BigDecimal;

@Entity
@Setter
@Getter
@Builder
@AllArgsConstructor
@NoArgsConstructor
public class TradeConfig {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @ManyToOne
    @JoinColumn(name = "user_id", nullable = false)
    private User user;

    private String exchange;
    private String apiKey;
    private String apiSecret;

    private BigDecimal longInputPct;
    private BigDecimal shortInputPct;
}