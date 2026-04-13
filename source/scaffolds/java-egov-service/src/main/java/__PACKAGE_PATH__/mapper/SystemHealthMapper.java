package __PACKAGE_NAME__.mapper;

import org.egovframe.rte.psl.dataaccess.mapper.Mapper;

@Mapper("systemHealthMapper")
public interface SystemHealthMapper {

    Integer selectPing();
}
