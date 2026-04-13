package __PACKAGE_NAME__.config;

import __PACKAGE_NAME__.job.SampleBatchTasklet;
import org.apache.ibatis.session.SqlSessionFactory;
import org.mybatis.spring.SqlSessionFactoryBean;
import org.mybatis.spring.annotation.MapperScan;
import org.springframework.batch.core.Job;
import org.springframework.batch.core.Step;
import org.springframework.batch.core.configuration.annotation.EnableBatchProcessing;
import org.springframework.batch.core.configuration.annotation.JobBuilderFactory;
import org.springframework.batch.core.configuration.annotation.StepBuilderFactory;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.ComponentScan;
import org.springframework.context.annotation.Configuration;
import org.springframework.context.annotation.PropertySource;
import org.springframework.context.support.PropertySourcesPlaceholderConfigurer;
import org.springframework.jdbc.datasource.DriverManagerDataSource;

import javax.sql.DataSource;

@Configuration
@EnableBatchProcessing
@PropertySource("classpath:/egovframework/egovProps/db.properties")
@ComponentScan(basePackages = "__PACKAGE_NAME__")
@MapperScan(basePackages = "__PACKAGE_NAME__.mapper", sqlSessionFactoryRef = "appSqlSessionFactory")
public class BatchApplicationConfiguration {

    @Bean
    public Job sampleJob(JobBuilderFactory jobs, Step sampleStep) {
        return jobs.get("sampleJob")
            .start(sampleStep)
            .build();
    }

    @Bean
    public Step sampleStep(StepBuilderFactory steps, SampleBatchTasklet sampleBatchTasklet) {
        return steps.get("sampleStep")
            .tasklet(sampleBatchTasklet)
            .build();
    }

    @Bean
    public DataSource appDataSource(
        @org.springframework.beans.factory.annotation.Value("${db.driverClassName}") String driverClassName,
        @org.springframework.beans.factory.annotation.Value("${db.url}") String url,
        @org.springframework.beans.factory.annotation.Value("${db.username}") String username,
        @org.springframework.beans.factory.annotation.Value("${db.password}") String password
    ) {
        DriverManagerDataSource dataSource = new DriverManagerDataSource();
        dataSource.setDriverClassName(driverClassName);
        dataSource.setUrl(url);
        dataSource.setUsername(username);
        dataSource.setPassword(password);
        return dataSource;
    }

    @Bean
    public SqlSessionFactory appSqlSessionFactory(DataSource appDataSource) throws Exception {
        SqlSessionFactoryBean factoryBean = new SqlSessionFactoryBean();
        factoryBean.setDataSource(appDataSource);
        factoryBean.setMapperLocations(
            new org.springframework.core.io.support.PathMatchingResourcePatternResolver()
                .getResources("classpath:/egovframework/mapper/**/*.xml")
        );
        return factoryBean.getObject();
    }

    @Bean
    public static PropertySourcesPlaceholderConfigurer propertySourcesPlaceholderConfigurer() {
        return new PropertySourcesPlaceholderConfigurer();
    }
}
