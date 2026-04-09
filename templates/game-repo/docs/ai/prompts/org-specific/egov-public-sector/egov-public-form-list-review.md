# eGov Public Form/List Review Prompt

전자정부프레임워크 또는 공공기관 웹서비스의 `검색조건 + 결과 목록 + 상세/등록/수정 + 첨부파일` 흐름을 검토하려고 한다.

다음 순서로 읽고 시작하라.

1. `AGENTS.md`
2. `docs/ai/org-specific/egov-public-sector-guide.md`
3. `checklists/public-sector-ui-review.md`
4. 관련 JSP/HTML/템플릿, 공통 include/layout, 공통 JS/CSS, 첨부파일 처리 코드

검토 원칙:

- 공공서비스형 업무 흐름과 운영 현실을 기준으로 본다.
- 화면 하나만 예쁘게 바꾸는 관점이 아니라 공통 패턴/공통 자산 영향 범위를 먼저 본다.
- before/after parity와 수동 검증 포인트를 반드시 남긴다.

반드시 점검할 항목:

- 검색조건, 필터, 초기값, 초기 조회 규칙
- 결과 목록의 컬럼, 정렬, 페이징, 빈 상태, 다운로드
- 상세/등록/수정 화면의 라벨, 필수값, 도움말, 검증 메시지
- 첨부파일 업로드/다운로드/삭제/권한 처리
- 공통 include, layout, Tiles, 공통 JS/CSS를 건드리는지 여부
- 개인정보/민감정보 노출과 권한별 visibility 차이

출력 형식:

1. 검토 범위와 주요 화면 패턴
2. 공통 패턴과 예외 화면
3. parity 위험이 큰 변경 지점
4. 접근성/KRDS 관점 우선 수정 항목
5. 수동 검증이 필요한 시나리오
6. 권장 수정 순서
