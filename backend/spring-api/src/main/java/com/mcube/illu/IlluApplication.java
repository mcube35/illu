package com.mcube.illu;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.scheduling.annotation.EnableAsync;

@SpringBootApplication
@EnableAsync
public class IlluApplication {

	public static void main(String[] args) {
		SpringApplication.run(IlluApplication.class, args);
	}

}
