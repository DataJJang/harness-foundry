# Model Tier Mapping

이 문서는 실제 모델명 또는 slug를 `economy`, `standard`, `high-reasoning` tier로 연결하는 adapter-local mapping 규칙을 설명한다.

## 왜 별도 파일이 필요한가

- canonical 정책은 역할과 단계가 요구하는 reasoning 수준만 정의한다.
- 실제 도구의 모델명은 자주 바뀌고, 생성 시점 이후 새 모델이 추가될 수 있다.
- 그래서 `model-routing.json`은 stable policy를 담고, `model-tier-map.json`은 tool-specific model name 해석만 담당하게 분리하는 편이 안전하다.

## 권장 파일 경로

- 기본 경로: `.agent-base/model-tier-map.json`
- 도구별로 따로 관리하고 싶으면 adapter가 별도 파일을 만든 뒤 `python3 scripts/show_start_path.py --model-tier-map-path <path>`로 넘긴다.

## 권장 구조

```json
{
  "version": 1,
  "adapter": "codex",
  "models": {
    "gpt-5.4-mini": "economy",
    "gpt-5.4": "standard",
    "gpt-5.4-reasoning": "high-reasoning"
  },
  "patterns": [
    {
      "glob": "gpt-5.4-mini*",
      "tier": "economy"
    },
    {
      "glob": "*reasoning*",
      "tier": "high-reasoning"
    }
  ],
  "notes": [
    "Prefer exact ids first.",
    "Do not guess a tier for unknown models.",
    "Update this file when the tool adds new model ids."
  ]
}
```

exact `models`가 우선이고, 없을 때만 `patterns[].glob`를 본다.
`patterns`는 편의용이므로 너무 넓은 wildcard는 피하는 편이 좋다.

## Unknown Handling

- map 파일이 없으면 `missing-model-map` warning을 띄운다.
- map 파일은 있지만 현재 모델명이 없으면 `unknown-model-mapping` warning을 띄운다.
- 이 경우 hard block 대신 soft recommendation으로만 동작시킨다.
- 즉시 정확한 판정이 필요하면 `--current-model-tier`나 `HARNESS_MODEL_TIER`를 직접 넘긴다.

## 권장 운영 방식

- adapter가 현재 tier를 직접 알 수 있으면 mapping을 거치지 말고 tier를 바로 넘긴다.
- adapter가 모델명만 알 수 있으면 mapping 파일로 tier를 해석한다.
- 새 모델이 보이면 map을 먼저 갱신하고, 그 전에는 unknown warning을 유지한다.
- unknown 상태를 억지로 추정해서 자동 차단하는 것보다, 경고 후 확인하는 편이 더 안전하다.
