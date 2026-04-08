# Project Bootstrap CLI

## 1. 목적

이 문서는 `project-bootstrap` 절차를 실제 터미널 대화형 실행으로 옮긴 `project_bootstrap_cli.py` 사용법을 정의한다.

## 2. 언제 쓰나

- 새 프로젝트를 처음 만들 때
- Agent가 문서형 인터뷰 대신 고정된 질문 순서로 spec을 수집해야 할 때
- 인터뷰 결과를 바로 spec JSON으로 저장하고 generator까지 이어서 실행하고 싶을 때

## 3. 실행 명령

```bash
python3 source/scripts/project_bootstrap_cli.py \
  --output-root /tmp/generated-projects \
  --force
```

선택 옵션:

- `--output-root`
  - 생성될 샘플 저장소 루트 디렉토리
- `--spec-path`
  - 인터뷰 결과 spec JSON 저장 위치
- `--skip-generate`
  - spec만 저장하고 실제 샘플 저장소 생성은 건너뜀
- `--force`
  - 같은 이름의 샘플 저장소가 이미 있으면 덮어씀

## 4. 질문 순서

CLI는 아래 순서로 질문한다.

1. 프로젝트명
2. 저장소명
3. 프로젝트 목적
4. 프로젝트 패밀리
5. 프로젝트 성격
6. 저장소 구성 방식
7. 대상 사용자
8. 대상 플랫폼
9. 런타임 역할
10. 언어
11. 프레임워크
12. 런타임 버전
13. 빌드 도구
14. 테스트 도구
15. 데이터 저장소
16. cache
17. 배포 유형
18. 서비스 기동 형태
19. 로깅 방식
20. 동작 OS
21. 보안/인증 방식
22. 대상 환경
23. 핵심 외부 연동
24. DB 관련 추가 항목
25. 기본 문서 세트
26. 추가 예외/메모
27. output root
28. spec 저장 경로

## 5. 출력

CLI는 아래를 만든다.

- 정규화된 spec JSON
- spec 옆 `*.refinement.json`
- spec 옆 `*.refinement-status.json`
- 자동 파생된 `requiredAgentRoles`, `optionalAgentRoles`, `roleSpecializations`, `agentWorkflowOrder`
- 선택된 template 이름
- 선택된 scaffold profile 이름
- 생성 지원 수준
- 추천 coordination mode와 이유
- 필요 시 실제 샘플 저장소

spec은 `.agent-base/project-generation-spec.json`으로도 생성 저장소 안에 다시 남고, generator는 `.agent-base/context-manifest.json`, `.agent-base/agent-role-plan.json`, `.agent-base/refinement-manifest.json`, `.agent-base/refinement-status.json`, `.agent-base/agent-workboard.json`, `docs/ai/agent-handoff-log.md`를 같이 만든다. 이 중 `.agent-base/context-manifest.json`과 root `README.md`에는 추천 coordination mode와 이유가 같이 들어간다.

## 6. 주의사항

- `repositoryMode`가 `monorepo` 또는 `multi-repo`여도 v1 generator는 샘플 저장소 1개만 생성한다.
- 이 경우 CLI는 spec에는 해당 값을 기록하지만, 실제 다중 저장소 분리는 후속 수작업 또는 별도 생성기로 확장해야 한다.
- Java 계열은 `packageName`을 반드시 확정해야 한다.
- DB를 소유하는 저장소는 `dbEngine`, `schemaOwnership`, `migrationPath`를 함께 기록해야 한다.

## 7. 후속 작업

CLI와 generator 실행 후에는 먼저 추천 coordination mode를 확인하고 아래처럼 시작한다.

- `Lite`
  - `docs/ai/command-catalog.md`와 `.agent-base/pre-commit-config.json` 보정
  - high-priority blocker만 확인
  - 첫 build/test/smoke 실행
- `Coordinated`
  - high-priority refinement와 `docs/ai/repo-local-overrides.md` 정리
  - `.agent-base/agent-workboard.json` 확인
  - 필요 시 `--finalize-design-freeze`로 첫 execution handoff 고정
- `Full`
  - role plan, refinement, workboard를 같이 정리
  - handoff packet과 freshness check를 shared delivery 기본 절차로 사용
  - checklist, release/runbook, first validation을 역할별로 설명 가능한 상태까지 진행
