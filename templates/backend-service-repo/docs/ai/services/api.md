# API Service Rules

## 1. 적용 대상

- Spring Boot, JPA, Querydsl 기반 API 저장소
- eGovFrame REST + MyBatis 기반 API 저장소

## 2. 구조 원칙

### 패키지 책임

- `api/<domain>` 또는 `web/<domain>`: 기능 진입점
- `common`: 공통 유틸, 예외, 결과
- `domain/entity` 또는 `model/vo`: 데이터 모델
- `domain/repository` 또는 `mapper`: 영속 계층
- `config`, `security`, `filter`: 횡단 관심사

### 기본 구성 세트

- controller
- service
- model 또는 VO
- repository 또는 mapper
- 필요 시 query repository 또는 mapper XML
- validation
- exception 처리

## 3. 구현 원칙

- controller는 HTTP 진입만 담당한다.
- 비즈니스 규칙은 service로 내린다.
- 요청과 응답은 model 또는 VO로 명시한다.
- transaction 경계는 service에서 관리하는 것을 우선 검토한다.
- backend와 service-api는 공통 Spring, JPA, Querydsl 골격을 우선 유지한다.
- eGovFrame 계열은 controller, service, mapper, mapper XML, spring context, `pom.xml`을 함께 source of truth로 본다.
- schema 또는 query 변경이 있으면 [`database-rules.md`](../database-rules.md)를 함께 따른다.

## 4. 데이터 접근 선택 기준

- 단순 CRUD: JPA repository
- 페이징, 검색, 복합 조회: Querydsl
- 복잡 집계나 DB 의존 로직: QueryRepository 또는 native SQL
- 전자정부/MyBatis 계열: mapper interface + mapper XML + 검증 SQL

## 5. DB 변경 기준

- 신규 테이블, 신규 컬럼, code value, seed는 naming과 COMMENT를 함께 검토한다.
- JPA entity 변경이 schema change를 수반하면 migration과 rollback note를 함께 검토한다.
- native query나 Querydsl projection 변경이 있으면 alias와 응답 모델 정합성을 확인한다.
- 위험 SQL 또는 data correction이 있으면 [`../../../checklists/database-change.md`](../../../checklists/database-change.md)를 확인한다.

## 6. 운영 포인트

- 대표 API 응답 여부
- config 및 security 영향
- DB 적재/조회 정합성
- exception 응답과 권한 처리
- profile mismatch 여부

## 7. 검증 기준

- 최소 `./gradlew compileJava`, `./gradlew test`, `mvn compile`, `mvn test` 중 실제 저장소 명령
- 필요 시 validation, exception, transaction smoke
- DB, API 계약, 보안 영향 회귀 확인
- schema/data change가 있으면 verification query 또는 row count 확인

## 8. 체크리스트

- [ ] controller, service, model, repository 구성이 명확한가
- [ ] validation 책임이 controller와 service에 적절히 나뉘었는가
- [ ] soft delete, audit 컬럼, 공통 코드 영향을 검토했는가
- [ ] Querydsl, native SQL, JPA 중 선택 근거가 분명한가
- [ ] MyBatis 계열이면 mapper interface, mapper XML, datasource 설정 위치가 분명한가
- [ ] DB naming, abbreviation, COMMENT, constraint 기준을 확인했는가
- [ ] 위험 SQL, rollback, verification query가 필요한가
- [ ] security 또는 config 영향이 있는가
- [ ] compile 또는 test를 수행했는가
