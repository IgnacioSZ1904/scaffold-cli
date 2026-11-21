package com.example.$package_name;

import static org.junit.jupiter.api.Assertions.assertEquals;

import java.util.Map;

import org.junit.jupiter.api.Test;

class HealthControllerTest {

    @Test
    void healthReturnsOk() {
        assertEquals(Map.of("status", "ok"), new HealthController().health());
    }
}
