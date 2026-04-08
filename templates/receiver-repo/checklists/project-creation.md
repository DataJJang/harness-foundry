# Project Creation Checklist

## 1. 인터뷰 완료 직후

- [ ] 프로젝트 패밀리를 확정했다
- [ ] 프로젝트 성격을 확정했다
- [ ] 저장소 구성 방식을 확정했다
- [ ] 대상 플랫폼을 확정했다
- [ ] 런타임 역할을 하나 이상 확정했다
- [ ] 언어와 프레임워크를 확정했다
- [ ] 데이터 저장소, cache, 배포 유형, 서비스 기동 형태, 로깅 방식, 동작 OS를 확정했다
- [ ] `docs/ai/project-generation-spec.md` 입력값을 모두 채웠다
- [ ] `docs/ai/project-selection-mapping.md` 기준으로 템플릿 후보를 검토했다

## 2. 템플릿 복사 직후

- [ ] 프로젝트 패밀리에 맞는 템플릿을 선택했다
- [ ] 저장소명, 기본 브랜치, 설명, 패키지명 또는 그룹명을 확정했다
- [ ] `repositoryMode`가 `single-repo`, `monorepo`, `multi-repo` 중 어디인지 기록했다
- [ ] `docs/ai/stack-matrix.md` 기준으로 권장 언어, 프레임워크, 런타임, 빌드 도구를 검토했다
- [ ] DB를 소유하는 저장소면 DB 엔진/버전, migration 위치, schema ownership을 확정했다

## 3. 규약 문서 보정

- [ ] `AGENTS.md`의 프로젝트 패밀리와 런타임 역할 설명을 맞췄다
- [ ] `.agent-base/refinement-manifest.json`의 high-priority module을 검토했다
- [ ] `python3 scripts/update_refinement_status.py --interactive --append-to-overrides` 또는 동등 절차로 refinement 상태를 갱신했다
- [ ] `.agent-base/refinement-status.json`에 현재 refinement 상태를 반영했다
- [ ] `docs/ai/repo-local-overrides.md`에 기본값 유지 이유, 예외, defer note를 기록했다
- [ ] `.agent-base/agent-workboard.json`에서 execution lane과 owned path를 확정했다
- [ ] blocker가 풀렸다면 `python3 scripts/update_agent_workboard.py --finalize-design-freeze` 또는 동등 절차로 첫 execution packet을 만들었다
- [ ] `python3 scripts/update_agent_workboard.py --interactive --append-handoff` 또는 동등 절차로 첫 handoff를 남겼다
- [ ] `docs/ai/command-catalog.md`에 첫 build/compile/test/smoke 기준을 기록했다
- [ ] `python3 scripts/install_git_hooks.py`로 local pre-commit gate를 설치했다
- [ ] `.agent-base/pre-commit-config.json`을 저장소 실정에 맞게 검토했다
- [ ] pre-commit preset profile이 프로젝트 패밀리와 실제 명령 체계에 맞는지 확인했다
- [ ] `docs/ai/architecture-map.md`에 저장소 고유 문서 위치를 반영했다
- [ ] DB를 소유하는 저장소면 `docs/ai/database-rules.md`를 읽고 repo-local 예외 여부를 기록했다
- [ ] 권장 기준과 다른 선택이 있으면 repo-local 오버레이 문서에 이유를 기록했다

## 4. 첫 프롬프트 실행

- [ ] `project-bootstrap-interview` 결과를 정리했다
- [ ] `project-spec-finalizer`로 generation spec을 확정했다
- [ ] `scaffold-planning`으로 초기 구조와 문서 세트를 정리했다
- [ ] `post-bootstrap-refinement`로 decide-now / keep-default / defer-with-note를 정리했다
- [ ] `build-guide` 문서를 생성했다
- [ ] `test-plan` 문서를 생성했다
- [ ] DB를 소유하는 저장소면 `database-review` 또는 `impact-analysis`를 생성했다
- [ ] 필요 시 `deployment-checklist` 또는 `operations-manual` 초안을 생성했다
- [ ] planning -> execution 전환이 있었다면 `docs/ai/handoff-packets/` 아래 current packet이 있다
- [ ] 실행 역할이 둘 이상이면 `docs/ai/agent-handoff-log.md`에 첫 baton이 기록되었다

## 5. 첫 기술 검증

- [ ] 첫 build 명령을 실행했다
- [ ] 첫 compile 또는 test 명령을 실행했다
- [ ] 최소 smoke 절차를 문서화했다
- [ ] 미검증 항목과 이유를 기록했다
