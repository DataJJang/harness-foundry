package __PACKAGE_NAME__.controller;

import java.util.Map;
import jakarta.validation.Valid;
import __PACKAGE_NAME__.model.InboundMessageRequest;
import __PACKAGE_NAME__.service.InboundMessageService;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/inbound")
public class InboundController {

    private final InboundMessageService inboundMessageService;

    public InboundController(InboundMessageService inboundMessageService) {
        this.inboundMessageService = inboundMessageService;
    }

    @PostMapping
    public Map<String, Object> receive(@Valid @RequestBody InboundMessageRequest request) {
        return inboundMessageService.accept(
            request.getSource(),
            request.getMessageId(),
            request.getPayload()
        );
    }
}
