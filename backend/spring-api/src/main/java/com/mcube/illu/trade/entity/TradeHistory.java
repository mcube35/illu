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
public class TradeHistory {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @ManyToOne
    @JoinColumn(name = "user_id", nullable = false)
    private User user;

    @Column(nullable = false)
    private String cTime; // 매수 시점 (cTime)

    private String uTime; // 마지막 시점 (uTime)

    @Column(precision = 20, scale = 8)
    private BigDecimal pnl; // 수익금 (realizedPnl)

    @Column(precision = 20, scale = 8)
    private BigDecimal pnlRatio;
}