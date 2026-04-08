# Compatibility Matrix

## 1. 목적

현재 스택과 목표 스택 사이의 호환성, 예외, breaking point를 정리하는 기준이다.

## 2. 최소 비교 축

- 언어와 런타임 버전
- framework major/minor
- build tool
- test tool
- deployment/runtime
- DB driver와 dialect
- security/auth layer
- external protocol

## 3. 분류

- `compatible`
- `compatible-with-note`
- `breaking`
- `unknown`

## 4. 기록 예시

- `Java 11 -> Java 17`: compatible-with-note
- `Spring Boot 2.7.x -> 3.5.x`: breaking
- `custom auth filter -> Spring Security standard`: breaking
