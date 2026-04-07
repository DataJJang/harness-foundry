# Maintenance Checklist

## 1. 규칙 변경 시 순서

1. `source/`를 먼저 수정한다
2. 공통 규칙으로 표현 가능한지 먼저 검토하고, template별 차이는 `template-build.json` 또는 `template_overlays/` 사용 여부를 결정한다
3. generator, scaffold, prompt, checklists 중 영향 범위를 확인한다
4. `python3 tools/build_templates.py`로 `templates/*`를 다시 생성한다
5. `python3 tools/build_templates.py --check`로 generated artifact가 일치하는지 확인한다
6. 링크, 도구 어댑터, path-specific instruction, 예시 문서를 같이 확인한다
7. 필요 시 top-level `README.md`, `adoption.md`, `maintenance.md`도 갱신한다

## 2. 동기화 체크 항목

- [ ] `AGENTS.md`와 `docs/ai/README.md`의 읽는 순서가 일치하는가
- [ ] `templates/*`를 직접 수정하지 않고 `source/`와 `template-build.json`에서 관리했는가
- [ ] `project-bootstrap`, `project-generation-spec`, `project-family-map`, `project-selection-mapping`, `project-generator`, `token-substitution`이 source와 templates에 같이 반영되었는가
- [ ] `database-rules.md`와 `checklists/database-change.md`가 source와 templates에 같이 반영되었는가
- [ ] `project-creation`, `project-interview`, `first-delivery`가 source와 templates에 같이 반영되었는가
- [ ] `.githooks/pre-commit`, `.agent-base/pre-commit-config.json`, `scripts/install_git_hooks.py`, `scripts/precommit_check.py`가 source와 templates에 같이 반영되었는가
- [ ] `agent-failure-learning.md`, `agent-failure-review.md`, 관련 prompt/example이 source와 templates에 같이 반영되었는가
- [ ] generator가 기대하는 scaffold profile과 실제 `source/scaffolds/*`가 일치하는가
- [ ] `CLAUDE.md`, `GEMINI.md`, Copilot, Cursor 규칙이 canonical과 충돌하지 않는가
- [ ] 새 규칙이 `templates/*`에 빠짐없이 반영되었는가
- [ ] 절대 경로나 개인 환경 경로가 새로 들어오지 않았는가
- [ ] 프로젝트 패밀리 템플릿과 런타임 역할 템플릿의 목적 구분이 유지되는가

## 3. 드리프트 발생 시 우선순위

1. 실제 생성기 동작과 scaffold 결과
2. `source/docs/ai/*`
3. `source/AGENTS.md`
4. `template-build.json`과 `template_overlays/`
5. `templates/*`
6. migration pointer 문서

## 4. 정기 점검 권장 항목

- 분기마다 프로젝트 패밀리 템플릿과 런타임 역할 템플릿 유효성 점검
- 새 도구 도입 시 adapter 추가 여부 검토
- 빌드/테스트 명령 체계 변경 시 `command-catalog` 갱신
- DB naming, migration, risky SQL 기준과 실제 자산 차이 확인
- 문서 분기 기준과 실제 문서 운영 방식 차이 확인
- 공통 권장 스택/버전과 실제 생성 기준 차이 확인
- 새 프로젝트 생성 시 반복되는 보완 사항을 `project-bootstrap`, prompt examples, generator spec에 환류
- agent failure가 반복되면 월간 단위로 failure pattern을 정리해 harness 강화 우선순위를 재평가
- `python3 tools/build_templates.py --check` 결과가 항상 clean하게 나오는지 확인
