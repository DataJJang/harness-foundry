# Adoption Checklist

## 1. 도입 대상 확정

- [ ] 이 패키지를 `새 프로젝트 생성`에 쓸지, `기존 저장소 규칙 정비`에 쓸지 결정했다
- [ ] 대상 프로젝트의 `projectFamily`를 결정했다
- [ ] 필요 시 하위 `runtimeRole[]`를 결정했다
- [ ] 적합한 `templates/*-repo` 패키지를 선택했다

## 2. 생성 또는 복사 전 확인

- [ ] `source/AGENTS.md`와 `source/docs/ai/README.md`를 읽었다
- [ ] `project-bootstrap`, `project-generation-spec`, `project-family-map`, `project-selection-mapping`을 검토했다
- [ ] `stack-matrix.md` 기준으로 언어, 프레임워크, 버전을 검토했다
- [ ] DB를 소유하는 프로젝트면 `database-rules.md`와 `database-change.md`를 검토했다
- [ ] 보안 baseline, 배포 유형, 운영 문서 필요 여부를 확인했다

## 3. 생성 후 필수 보정

- [ ] `AGENTS.md`의 저장소 설명이 실제 대상과 맞는지 확인했다
- [ ] `docs/ai/command-catalog.md`에 실제 build, compile, test, smoke 명령을 적었다
- [ ] `docs/ai/architecture-map.md`에 실제 코드/설정/system of record 구조를 적었다
- [ ] `python3 scripts/install_git_hooks.py`로 local pre-commit gate를 설치했다
- [ ] `.agent-base/pre-commit-config.json`을 저장소 실정에 맞게 검토했다
- [ ] path-specific instruction과 Cursor rule이 실제 경로 구조와 맞는지 확인했다
- [ ] 템플릿이 generated artifact임을 이해했고, 장기 유지보수는 `source/` 기준으로 진행하기로 했다
- [ ] 공통 권장값에서 벗어나는 항목이 있으면 repo-local 오버레이 문서에 이유를 기록했다
- [ ] 첫 프롬프트 실행 예시와 첫 검증 체크리스트가 실제 저장소 기준으로 읽히는지 확인했다

## 4. 연동 문서 확인

- [ ] 기존 `README`, `runbook`, `deployment-checklist`, `manual`, `validation guide`와 충돌하지 않는지 확인했다
- [ ] 프로젝트 고유 문서가 필요하면 `document-routing.md` 기준으로 적절한 문서 위치를 정했다
- [ ] DB, 보안, 배포, 운영 문서가 필요한 프로젝트인지 판단했다

## 5. 적용 후 검증

- [ ] `AGENTS.md`에서 상세 규칙과 프롬프트 라이브러리로 자연스럽게 이동된다
- [ ] `project-creation`, `first-delivery`, `database-change` 체크리스트가 필요한 범위에 포함되었다
- [ ] Copilot repo-wide instruction과 path-specific instruction이 모두 존재한다
- [ ] Cursor base rule과 해당 서비스 또는 패밀리 rule만 남아 있다
- [ ] 절대 경로와 개인 환경 경로가 남아 있지 않다
- [ ] 대상 프로젝트 패밀리와 무관한 파일이 과도하게 포함되지 않았다
