package __PACKAGE_NAME__;

import __PACKAGE_NAME__.config.BatchApplicationConfiguration;
import org.springframework.batch.core.Job;
import org.springframework.batch.core.JobExecution;
import org.springframework.batch.core.JobParameters;
import org.springframework.batch.core.JobParametersBuilder;
import org.springframework.batch.core.launch.JobLauncher;
import org.springframework.context.annotation.AnnotationConfigApplicationContext;

public class __MAIN_CLASS_NAME__ {

    public static void main(String[] args) throws Exception {
        try (AnnotationConfigApplicationContext context =
                     new AnnotationConfigApplicationContext(BatchApplicationConfiguration.class)) {
            JobLauncher jobLauncher = context.getBean(JobLauncher.class);
            Job sampleJob = context.getBean("sampleJob", Job.class);
            JobParameters parameters = new JobParametersBuilder()
                .addLong("requestTime", System.currentTimeMillis())
                .toJobParameters();

            JobExecution execution = jobLauncher.run(sampleJob, parameters);
            System.out.println("__PROJECT_NAME__ job status: " + execution.getStatus());
        }
    }
}
