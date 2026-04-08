package __PACKAGE_NAME__.model;

import jakarta.validation.constraints.NotBlank;

public class InboundMessageRequest {

    @NotBlank
    private String source;

    @NotBlank
    private String messageId;

    @NotBlank
    private String payload;

    public String getSource() {
        return source;
    }

    public void setSource(String source) {
        this.source = source;
    }

    public String getMessageId() {
        return messageId;
    }

    public void setMessageId(String messageId) {
        this.messageId = messageId;
    }

    public String getPayload() {
        return payload;
    }

    public void setPayload(String payload) {
        this.payload = payload;
    }
}
