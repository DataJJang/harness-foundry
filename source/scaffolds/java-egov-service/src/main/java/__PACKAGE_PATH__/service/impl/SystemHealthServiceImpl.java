package __PACKAGE_NAME__.service.impl;

import __PACKAGE_NAME__.mapper.SystemHealthMapper;
import __PACKAGE_NAME__.service.SystemHealthService;
import org.egovframe.rte.fdl.cmmn.EgovAbstractServiceImpl;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.Instant;
import java.util.LinkedHashMap;
import java.util.Map;

@Service("systemHealthService")
public class SystemHealthServiceImpl extends EgovAbstractServiceImpl implements SystemHealthService {

    private final SystemHealthMapper systemHealthMapper;

    public SystemHealthServiceImpl(SystemHealthMapper systemHealthMapper) {
        this.systemHealthMapper = systemHealthMapper;
    }

    @Override
    @Transactional(readOnly = true)
    public Map<String, Object> healthSnapshot() {
        LinkedHashMap<String, Object> response = new LinkedHashMap<>();
        response.put("project", "__PROJECT_NAME__");
        response.put("framework", "eGovFrame 4.3 REST + MyBatis");
        response.put("checkedAt", Instant.now().toString());
        response.put("database", databaseStatus());
        return response;
    }

    private Map<String, Object> databaseStatus() {
        LinkedHashMap<String, Object> status = new LinkedHashMap<>();
        try {
            status.put("reachable", true);
            status.put("ping", systemHealthMapper.selectPing());
        } catch (RuntimeException exception) {
            status.put("reachable", false);
            status.put("message", exception.getMessage());
        }
        return status;
    }
}
