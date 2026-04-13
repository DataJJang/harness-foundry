package __PACKAGE_NAME__.api;

import __PACKAGE_NAME__.service.SystemHealthService;
import org.junit.jupiter.api.Test;

import java.util.Map;

import static org.junit.jupiter.api.Assertions.assertEquals;

class SystemHealthControllerTests {

    @Test
    void healthReturnsServicePayload() {
        SystemHealthService service = () -> Map.of("status", "UP");
        SystemHealthController controller = new SystemHealthController(service);

        Map<String, Object> response = controller.health();

        assertEquals("UP", response.get("status"));
    }
}
