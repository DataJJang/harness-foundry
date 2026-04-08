# Repo-Local Overrides

이 문서는 공통 템플릿 기본값과 다른 선택, bootstrap 이후 refinement 결정, defer note를 저장소 로컬 기준으로 남기는 문서다.

## 언제 쓰는가

- 공통 권장 스택과 다른 언어, 프레임워크, 빌드 도구, 테스트 도구를 쓴다.
- 생성 직후 refinement 질문에서 `decide-now`, `keep-default`, `defer-with-note`를 정리해야 한다.
- pre-commit, command-catalog, architecture-map, 운영 문서를 repo-local 실정에 맞게 보정한다.

## 담아야 할 내용

- 공통 기본값과 다른 선택
- 왜 그렇게 유지하는지에 대한 근거
- 지금 결정한 항목과 유지한 기본값
- defer한 항목과 이유, 나중에 결정할 주체
- 어떤 문서나 설정을 같이 갱신했는지

## 담지 말아야 할 내용

- 공통 규칙 전체 본문 복사
- 기능별 운영 절차 전체
- 긴 구현 설계 본문

## 추천 흐름

1. `.agent-base/refinement-manifest.json`에서 high-priority module을 본다.
2. `.agent-base/refinement-status.json`에 현재 상태를 반영한다.
3. 가능하면 `python3 scripts/update_refinement_status.py --interactive --append-to-overrides`로 결정 로그를 함께 반영한다.
4. 이 문서에 왜 기본값을 유지했는지, 어떤 예외를 허용했는지, 무엇을 defer했는지 남긴다.
5. 필요한 실제 반영은 `command-catalog`, `architecture-map`, `pre-commit-config`, 운영 문서에 한다.

## 최소 섹션 예시

- Bootstrap snapshot
- Non-default choices
- High-priority modules
- Current decisions
- Deferred items
- Updated docs and configs
- Automated decision logs from `update_refinement_status.py`
