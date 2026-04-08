# Adoption Spec

## 1. 목적

이 문서는 기존 저장소를 분석하고 규약을 이식하거나 마이그레이션할 때 쓰는 정규화 입력 스키마를 정의한다.

## 2. 권장 JSON key

| 항목 | key | 설명 |
| --- | --- | --- |
| 소스 저장소명 | `sourceRepositoryName` | 현재 저장소 이름 |
| adoption 모드 | `adoptionMode` | `adopt-in-place`, `migrate-in-place`, `split-service`, `replatform`, `rewrite-with-parity` |
| 현재 프로젝트 패밀리 | `sourceProjectFamily` | 현재 저장소 분류 |
| 현재 언어/프레임워크 | `currentLanguage`, `currentFramework` | 실제 구현 기준 |
| 현재 런타임/빌드/테스트 | `currentRuntimeVersion`, `currentBuildTool`, `currentTestTool` | 현재 실행 기준 |
| 현재 데이터/캐시/배포 | `currentDatastore`, `currentCache`, `currentDeploymentType` | 인프라 기준 |
| migration 범위 | `migrationScope` | 코드, 설정, DB, 배포, 문서 |
| 목표 스택 | `targetStack` | 바꾸고 싶은 목표 |
| parity requirement | `parityRequirement` | 기능/계약/데이터 동등성 요구 |
| cutover / rollback | `cutoverStrategy`, `rollbackStrategy` | 전환 및 복귀 기준 |
| legacy 예외 | `legacyExceptions` | 당장 유지해야 하는 예외 |
| known risks | `knownRisks` | 이미 알려진 위험 |
| 역할 세트 | `requiredAgentRoles`, `optionalAgentRoles` | adoption에 필요한 core/extended 역할 |

## 3. 예시

```json
{
  "sourceRepositoryName": "legacy-billing-service",
  "adoptionMode": "migrate-in-place",
  "sourceProjectFamily": "backend-service",
  "currentLanguage": "Java",
  "currentFramework": "Spring Boot 2.1.x",
  "currentRuntimeVersion": "8",
  "currentBuildTool": "Gradle",
  "currentTestTool": "Gradle test",
  "currentDatastore": "MariaDB",
  "currentCache": "Redis",
  "currentDeploymentType": "VM",
  "migrationScope": ["application", "config", "docs"],
  "targetStack": {
    "language": "Java",
    "framework": "Spring Boot 3.5.x",
    "runtimeVersion": "17"
  },
  "parityRequirement": "API contract and batch side effects must remain compatible",
  "cutoverStrategy": "phased",
  "rollbackStrategy": "keep previous artifact and config bundle",
  "legacyExceptions": ["old admin login module stays until phase 2"],
  "knownRisks": ["custom auth filter", "manual SQL scripts"],
  "requiredAgentRoles": ["orchestrator", "legacy-analyst", "migration-planner", "runtime-engineer", "qa-validator", "docs-operator"],
  "optionalAgentRoles": ["data-steward", "security-reviewer", "compatibility-reviewer", "cutover-manager"]
}
```
