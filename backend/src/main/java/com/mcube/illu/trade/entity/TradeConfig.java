package com.mcube.illu.trade.entity;

import com.mcube.illu.user.entity.User;
import jakarta.persistence.*;
import lombok.Getter;
import lombok.Setter;

import java.math.BigDecimal;

@Entity
@Setter
@Getter
public class TradeConfig {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @ManyToOne
    @JoinColumn(name = "user_id")
    private User user;

    private String exchange;
    private String apiKey;
    private String apiSecret;

    private BigDecimal longInputPct;
    private BigDecimal shortInputPct;
}