package __PACKAGE_NAME__.service;

import java.util.Map;

public interface SystemHealthService {

    Map<String, Object> healthSnapshot();
}
