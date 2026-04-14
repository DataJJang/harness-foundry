# eGov Delivery, DevOps, And SCM Guide

## 1. 목적

이 문서는 `organizationProfile = egov-public-sector`인 프로젝트에서 `배포`, `CI/CD`, `형상관리`, `artifact 관리`, `운영환경 이관`을 어떤 기준으로 먼저 고정해야 하는지 정리한다.

핵심은 `전자정부 공식 자료에 실제로 무엇이 있는가`와 `그 자료를 현재 사업의 Git/Jenkins/GitHub Actions/Kubernetes 현실에 어떻게 해석할 것인가`를 연결하는 것이다.

## 2. 언제 먼저 보나

- 신규 구축인데 발주기관의 반입 형식과 운영환경이 이미 정해져 있다
- Git과 SVN, 수동 배포와 자동 배포, WAR/JAR와 Docker 이미지가 혼재할 수 있다
- 기관 운영팀이 별도이고, 개발팀은 build만 하며 반영은 운영팀이 맡는다
- eGovFrame 기반인데 CI/CD와 형상관리 기준이 문서에 아직 남아 있지 않다

## 3. 공식 자료에서 확인되는 축

### 개발환경 전체 관점

- eGovFrame 개발환경 소개 문서는 `버전관리`, `빌드`, `배포`까지 개발 lifecycle 지원 도구 범위에 포함한다.
- 즉 배포와 형상관리는 전자정부 프로젝트에서 부수 영역이 아니라 초기 결정 항목으로 보는 편이 맞다.

참고:

- https://www.egovframe.go.kr/wiki/doku.php?id=egovframework%3Adev4.3%3Aoverview

### 형상관리

- 공식 형상관리 가이드는 형상 식별, 버전관리, 변경관리, 형상감사, 보고까지 설명한다.
- 소스관리도구 서버 운영 문서는 현재도 `Subversion(SVN)` 중심이다.
- 다만 형상관리 개요 문서 자체는 대중적인 도구로 `SVN, Git`을 함께 언급한다.

참고:

- https://www.egovframe.go.kr/wiki/doku.php?id=egovframework%3Adev4.3%3Ascm%3Aconfiguration_management
- https://egovframe.go.kr/wiki/doku.php?id=egovframework%3Adev4.3%3Ascm%3Asourcecode_management_server

### 빌드와 CI

- 공식 프로젝트 빌드 문서는 `Maven 기반 개인 빌드 + CI 서버를 통한 통합 빌드`를 기본 축으로 설명한다.
- 통합빌드 문서는 현재 `Jenkins` 기준으로 설치와 작업 등록, JUnit 연동, 기본 사용 흐름을 다룬다.
- 내부 artifact 저장소는 `Nexus` 가이드가 별도로 있다.
- 동시에 최신 공식 개발환경 문서에는 `Gradle` 전환 가이드도 존재한다.

참고:

- https://www.egovframe.go.kr/wiki/doku.php?id=egovframework%3Adev%3Adep%3A%ED%94%84%EB%A1%9C%EC%A0%9D%ED%8A%B8_%EB%B9%8C%EB%93%9C
- https://egovframe.go.kr/wiki/doku.php?id=egovframework%3Adev4.3%3Adep%3Abuild_tool%3Aintegration_build
- https://www.egovframe.go.kr/wiki/doku.php?id=egovframework%3Adev4.3%3Adep%3Abuild_tool%3Anexus
- https://www.egovframe.go.kr/wiki/doku.php?id=egovframework%3Adev4.3%3Adep%3Abuild_tool%3Agradle

### 배포와 운영환경

- 운영환경 가이드는 `docker`, `배치운영환경`, `의사소통관리/설정관리/모니터링도구`를 별도 축으로 둔다.
- 즉 공공 eGov 프로젝트도 운영환경과 배치 운용을 문서화 대상으로 본다.

참고:

- https://www.egovframe.go.kr/wiki/doku.php?id=egovframework%3A%EC%9A%B4%EC%98%81%ED%99%98%EA%B2%BD%EA%B0%80%EC%9D%B4%EB%93%9C
- https://www.egovframe.go.kr/wiki/doku.php?id=egovframework%3Adev3.6%3Adep%3Abuild_tool%3Adocker

### 클라우드 네이티브와 MSA

- 공식 MSA 템플릿/교육 자료는 이미 `Docker`, `Kubernetes`, `Jenkins`, `config`, `logging`까지 포함한 경로를 보여준다.
- 따라서 공식 레퍼런스가 레거시형 `SVN + Maven + Jenkins + Nexus`에만 머무는 것은 아니다.
- 실무적으로는 `공식 레거시 가이드`와 `공식 최신 템플릿`을 함께 보는 편이 안전하다.

참고:

- https://egovframe.go.kr/wiki/doku.php?id=egovframework%3Adev4.1%3Aimp%3Aeditor%3Acreate_msa_template_project_wizard
- https://github.com/eGovFramework/egovframe-msa-edu
- https://github.com/egovframework

## 4. 실무 해석

- RFP나 운영 표준이 `SVN`, `수동 반입`, `JEUS/Tomcat 수동 배포`, `Jenkins only`를 박아두면 그 사업은 그 기준이 우선이다.
- RFP가 `전자정부표준프레임워크 적용`과 `운영 적합성`만 요구하고 도구를 잠그지 않았다면 Git, GitHub, GitHub Actions, GitLab CI, Jenkins Pipeline을 쓰는 것도 가능하다.
- 다만 이 경우에도 결과물은 `공공 프로젝트가 설명해야 하는 기준`으로 다시 적어야 한다.
  - source of truth 저장소
  - 반입 artifact 형식
  - 배포 순서와 승인 주체
  - 환경별 설정 분리
  - rollback 기준
  - 운영 확인 포인트

## 5. bootstrap에서 먼저 잠글 것

### 형상관리

- source of truth가 `Git`, `SVN`, `혼합` 중 무엇인가
- 운영 반입용 미러 저장소가 따로 있는가
- 기본 브랜치와 release branch가 필요한가
- commit/merge 권한과 승인 주체가 누구인가

### 빌드와 CI

- 표준 build 도구가 `Maven`, `Gradle`, `혼합` 중 무엇인가
- CI 서버가 `Jenkins`, `GitHub Actions`, `GitLab CI`, `없음/수동` 중 무엇인가
- build trigger가 `push`, `merge`, `nightly`, `수동 승인 후` 중 무엇인가
- test, compile, package 중 어느 단계까지 자동화할 것인가

### artifact 관리

- 산출물 단위가 `war`, `jar`, `docker image`, `정적 번들(zip/tar)` 중 무엇인가
- artifact 저장소가 `Nexus`, `registry`, `운영팀 공유 스토리지`, `없음` 중 무엇인가
- 배포용 버전 태그를 어디서 관리하는가

### 배포와 운영환경

- 배포 대상이 `VM`, `container`, `k8s`, `수동 WAS 반입` 중 무엇인가
- `dev/stg/prd` 승격 경로와 승인 주체가 무엇인가
- smoke owner와 rollback owner가 누구인가
- 배치와 웹/API의 반영 순서가 서로 묶이는가

### 설정과 보안

- 환경별 설정 source of truth 파일이 어디인가
- secret 전달 방식이 무엇인가
- 로그 수집 위치와 운영 확인 포인트가 무엇인가

## 6. HF 문서 반영 위치

- `docs/ai/command-catalog.md`
  - 실제 build/package/deploy/smoke 명령
- `docs/ai/repo-local-overrides.md`
  - Git/SVN, Jenkins/Nexus, 수동 반입 같은 예외
- `docs/ai/governance/git-workflow.md`
  - 브랜치, merge, 태그, release branch 전략
- `docs/ai/governance/release-and-rollback.md`
  - 반영 순서, rollback trigger, smoke owner
- `docs/ai/operations-manual.md`
  - 운영 전달 대상, 점검 포인트, 재기동/복구 절차
- `deployment-checklist.md`
  - 환경별 반영 절차와 확인 항목

## 7. HF에서 바로 물어야 할 질문

- 이 사업의 공식 형상관리 기준은 `Git`, `SVN`, `혼합` 중 무엇인가?
- CI는 어떤 도구가 운영 표준인가?
- build 결과물은 어떤 형식으로 반입되는가?
- artifact 저장소 또는 반입 경로는 무엇인가?
- 운영 반영은 누가 수행하고, 개발팀이 어디까지 자동화할 수 있는가?
- rollback 기준과 승인 주체는 누구인가?
- 배치 반영이 웹/API 반영과 시간적으로 묶이는가?

## 8. 판단 원칙

- 공식 eGovFrame 문서에 SVN/Hudson/Nexus가 있다고 해서 그 조합만 정답이라고 보면 안 된다.
- 반대로 최신 GitOps나 Kubernetes를 쓴다고 해서 공공 프로젝트 문서화 기준을 생략하면 안 된다.
- 충돌 시 우선순위는 보통 아래 순서를 따른다.

1. 과업지시서와 운영기관 표준
2. 실제 운영환경 제약
3. 공식 eGovFrame 레퍼런스와 템플릿
4. 팀의 선호 도구
