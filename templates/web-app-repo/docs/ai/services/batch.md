# Batch Service Rules

## 1. 적용 대상

- scheduler 또는 batch 처리 중심의 Java 저장소

## 2. 구조 원칙

### 모듈 단위 구성

배치 기능은 업무 모듈 기준으로 관리한다.

예시:

- `opsalert`
- `mqtt`
- `datausage`
- `cnsmwatt`
- `statistics`

### 모듈 내부 구성

- `mapper`
- `model`
- `service`

### 스케줄 진입점

- 잡 등록과 스케줄 트리거는 `jobs` 중심 패턴을 따른다.

## 3. 구현 원칙

- job, service, mapper, model, XML, SQL 문서를 함께 본다.
- eGovFrame batch 계열은 `pom.xml`, batch config, tasklet/chunk, mapper XML, 운영 SQL 문서를 함께 본다.
- 운영성 기능은 SQL 문서와 runbook 동반 여부를 항상 검토한다.
- `ops-alerting-v1/sql` 같은 문서 자산이 이미 있는 기능은 반드시 함께 갱신 여부를 확인한다.
- schema, seed, backfill, history table 변경은 [`database-rules.md`](../database-rules.md)를 함께 따른다.

## 4. DB 및 SQL 기준

- mapper XML과 migration SQL은 naming과 COMMENT 기준을 지켜야 한다.
- history, queue, retry, dead-letter 테이블은 append-only 여부를 먼저 구분한다.
- data correction, cleanup, backfill이 있으면 배포 순서와 rollback 가능성을 같이 적는다.
- 위험 SQL 또는 운영 직접 수정이 있으면 [`../../../checklists/database-change.md`](../../../checklists/database-change.md)를 확인한다.

## 5. 운영 포인트

- scheduler 실행 여부
- job 시작/종료 로그
- history 적재
- retry, dead-letter, cleanup
- 외부 연동 토큰과 enable flag

## 6. 검증 기준

- 최소 `./gradlew compileJava`, `./gradlew test`, `mvn compile`, `mvn test` 중 실제 저장소 명령
- 필요 시 mapper regression, service test, job 흐름 smoke
- 운영성 기능은 runbook/checklist 갱신 여부 확인
- schema/data change가 있으면 verification query 또는 영향 범위 확인

## 7. 체크리스트

- [ ] 신규 잡이면 `jobs` 등록 포인트를 확인했는가
- [ ] service, mapper, model, XML 또는 SQL 문서를 함께 검토했는가
- [ ] eGovFrame batch 계열이면 job config, tasklet/chunk, mapper XML, datasource 설정을 함께 검토했는가
- [ ] 스케줄러, 재시도, 중복 실행 영향을 검토했는가
- [ ] 시작, 종료, 실패 로그가 추적 가능하게 남는가
- [ ] DB naming, abbreviation, COMMENT, migration 기준을 확인했는가
- [ ] 위험 SQL, cleanup, backfill, rollback을 검토했는가
- [ ] compile 또는 test를 수행했는가
- [ ] 운영 문서 갱신 여부를 확인했는가
