# Frontend Rules

## 1. 적용 대상

- React, TypeScript 기반 frontend 저장소
- eGovFrame JSP/Spring MVC 기반 web-app 저장소

공공 `web-app`이면 먼저 `frontendArchitecturePolicy`가 무엇인지 확인한다.

- `jsp-mvc`
- `separated-frontend-api`
- `mpa-plus-ajax`

## 2. 구조 원칙

### 디렉토리 역할

React/Vite 계열은 아래 구조를 우선 본다.

- `src/elements/pages`: 라우트 단위 화면
- `src/elements/components`: 재사용 UI
- `src/elements/templates`: 큰 조립형 UI
- `src/hooks`: 커스텀 훅
- `src/store`: 상태 보조
- `src/types`: 타입 정의
- `src/lib`: 네트워크, 상수, 유틸

### 화면 파일 세트

가능한 한 아래 세트를 기준으로 구성한다.

- `ListPage`
- `DetailPage`
- `RegistrationPage`
- `ModifyPage`
- `Shared`
- `Api`

JSP/Spring MVC 계열은 아래 구조를 우선 본다.

- `src/main/webapp/WEB-INF/jsp`
- `src/main/webapp/WEB-INF/config`
- `src/main/resources/egovframework/spring`
- `src/main/java/.../web`
- 공통 include, layout, Tiles 또는 기관 공통 템플릿 경로

## 3. 구현 원칙

- server-rendered MPA, FE/BE 분리, 부분 AJAX 중 현재 저장소가 어느 전달 모델인지 먼저 고정한다.
- 페이지는 최대한 얇게 유지한다.
- 공통 폼, 상세 블록, 모달 블록은 `Shared.tsx`로 분리한다.
- API 응답은 화면에서 직접 쓰지 않고 normalize 후 사용한다.
- 목록 조건은 기존 `useListSearchParams` 패턴을 우선 사용한다.
- 서버 상태는 `react-query` 패턴을 우선 사용한다.
- JSP/Spring MVC 계열은 controller, JSP, 공통 include/layout, 공통 JS/CSS를 함께 변경 범위로 본다.
- 공공 UI는 KRDS, 접근성, 개인정보 노출 기준을 화면 단위가 아니라 공통 템플릿 범위까지 같이 확인한다.

## 4. 동반 수정 기준

새 화면이나 필드가 생기면 다음을 같이 확인한다.

- route
- type
- i18n
- API normalize
- 공통 코드 lookup
- 목록 검색 조건 복원
- 상세, 등록, 수정 간 필드 정합성

## 5. 검증과 운영 포인트

### 최소 검증

- `npm run build.*` 계열 build 또는 `mvn compile`, `mvn test`
- 필요 시 util, hook, normalize 테스트

### 운영 포인트

- route와 메뉴 노출 일치 여부
- build 산출물 반영 여부
- 정적 자산 캐시 문제 여부
- 공통 언어셋, i18n 누락 여부
- JSP, include, layout, 공통 JS/CSS 영향 범위 여부

## 6. 체크리스트

- [ ] 가장 가까운 기존 메뉴를 찾았는가
- [ ] 필요한 page/shared/api/type 세트를 갖췄는가
- [ ] `CommonTypes.ts` 또는 도메인 타입을 갱신했는가
- [ ] `i18n.ts`를 갱신했는가
- [ ] route와 메뉴 구조를 확인했는가
- [ ] API 응답을 normalize 후 사용하고 있는가
- [ ] JSP/Spring MVC 계열이면 controller, JSP, include/layout, 공통 JS/CSS를 함께 확인했는가
- [ ] build 또는 테스트를 수행했는가
