# eGov UI Accessibility Review Prompt

공공기관 또는 전자정부프레임워크 성격의 UI를 검토하려고 한다.

다음 순서로 읽고 시작하라.

1. `AGENTS.md`
2. `docs/ai/org-specific/egov-public-sector-guide.md`
3. `checklists/public-sector-ui-review.md`
4. 관련 화면 코드, 템플릿, 정적 리소스, 디자인 시안

검토 원칙:

- 일반적인 예쁨보다 공공서비스형 사용성, 일관성, 접근성을 우선한다.
- 현재 코드와 실제 화면 구조를 근거로 판단한다.
- KRDS 또는 기관 공통 UI 기준과 크게 어긋나는 부분을 먼저 찾는다.
- 신규 UI든 migration UI든 before/after parity와 사용성 저하 가능성을 같이 본다.

반드시 점검할 항목:

- 페이지 제목, heading 구조, breadcrumb, 주요 CTA의 일관성
- 입력 폼의 라벨, 필수 표시, 도움말, 검증/에러 메시지
- 표, 검색조건, 결과 목록, 상세/수정 패턴
- 첨부파일, 다운로드, 팝업/모달, 단계형 흐름
- 키보드 접근성, focus, semantic markup, 명도 대비
- 개인정보/민감정보 노출 위험

출력 형식:

1. 화면/기능 범위
2. 잘 맞는 점
3. 공공 프로젝트 관점 주요 문제
4. KRDS/접근성 우선 수정 항목
5. parity 또는 수동 검증이 필요한 항목
6. 권장 수정 우선순위
