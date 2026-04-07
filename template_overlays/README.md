# Template Overlays

`template_overlays/`는 `source/` 공통 베이스만으로 표현할 수 없는 템플릿별 차이를 둘 때 사용한다.

현재 기본 공통화 전략은 다음과 같다.

1. `source/`를 canonical authoring source로 관리한다.
2. `template-build.json`에서 템플릿별로 유지할 `.cursor` rule과 `.github` instruction을 선언한다.
3. `tools/build_templates.py`가 `source/`를 복사하고, 제외 규칙을 적용하고, 템플릿별로 불필요한 파일을 제거해 `templates/*`를 다시 생성한다.
4. 템플릿별로 추가 파일이나 문구 차이가 필요할 때만 `template_overlays/<template-name>/`를 만든다.

예시:

```text
template_overlays/
  web-app-repo/
    docs/ai/examples/custom-web-flow.md
  backend-service-repo/
    docs/ai/examples/internal-api-policy.md
```

규칙:

- `templates/*`는 직접 수정하지 않는다.
- 공통 규칙은 항상 `source/`를 수정한다.
- 템플릿별 차이는 가능하면 `template-build.json`의 keep/prune 규칙으로 해결한다.
- 그래도 표현되지 않는 차이만 `template_overlays/<template-name>/`에 둔다.
