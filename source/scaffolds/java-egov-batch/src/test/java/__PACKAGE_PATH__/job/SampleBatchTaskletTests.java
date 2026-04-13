package __PACKAGE_NAME__.job;

import __PACKAGE_NAME__.mapper.SampleBatchMapper;
import org.junit.jupiter.api.Test;
import org.springframework.batch.repeat.RepeatStatus;

import static org.junit.jupiter.api.Assertions.assertEquals;

class SampleBatchTaskletTests {

    @Test
    void executeReturnsFinished() throws Exception {
        SampleBatchMapper mapper = () -> 1;
        SampleBatchTasklet tasklet = new SampleBatchTasklet(mapper);

        RepeatStatus status = tasklet.execute(null, null);

        assertEquals(RepeatStatus.FINISHED, status);
    }
}
