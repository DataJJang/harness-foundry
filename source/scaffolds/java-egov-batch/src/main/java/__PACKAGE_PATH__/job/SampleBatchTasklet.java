package __PACKAGE_NAME__.job;

import __PACKAGE_NAME__.mapper.SampleBatchMapper;
import org.springframework.batch.core.StepContribution;
import org.springframework.batch.core.scope.context.ChunkContext;
import org.springframework.batch.core.step.tasklet.Tasklet;
import org.springframework.batch.repeat.RepeatStatus;
import org.springframework.stereotype.Component;

@Component
public class SampleBatchTasklet implements Tasklet {

    private final SampleBatchMapper sampleBatchMapper;

    public SampleBatchTasklet(SampleBatchMapper sampleBatchMapper) {
        this.sampleBatchMapper = sampleBatchMapper;
    }

    @Override
    public RepeatStatus execute(StepContribution contribution, ChunkContext chunkContext) {
        Integer ping = sampleBatchMapper.selectPing();
        System.out.println("__PROJECT_NAME__ batch bootstrap ping: " + ping);
        return RepeatStatus.FINISHED;
    }
}
