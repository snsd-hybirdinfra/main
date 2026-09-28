# 04 IAM / STS: Workload Identity 최소 권한

## 문제와 출처

[Google Threat Intelligence Group의 적대적 AI 분석](https://cloud.google.com/blog/topics/threat-intelligence/from-prompting-to-autonomy-the-evolution-of-adversarial-ai)(2026-09-08)은 클라우드 자격증명 오용 위험을 다뤘다. [Microsoft Security Research의 Storm-3168 분석](https://www.microsoft.com/en-us/security/blog/2026/09/25/storm-3168-agentic-driven-cloud-attacks-using-compromised-service-principals/)(2026-09-25)은 탈취된 Azure Service Principal이 대량 자원 삭제와 자격증명 수집에 사용됐고, 일부 삭제는 Resource Lock과 삭제 보호가 차단했다고 보고했다.

여기서 **“신뢰 관계, 역할 권한, 세션 경계, 명시적 거부를 함께 적용하면 탈취된 Workload Identity의 행동 범위를 제한할 수 있는가?”**라는 질문을 도출했다. AWS 형식 정책을 사용한 구현은 기사에 없는 내 로컬 실험 설계다.

## 상태와 범위

- 상태: **로컬 검증 — 정책 판정 로직만**
- 환경: Python 3 표준 라이브러리와 합성 AWS ARN·버킷
- 실제 AWS/Azure 계정, STS 토큰, Service Principal, Resource Lock은 사용하지 않음
- `111122223333`과 `lab-synthetic-artifacts`는 합성 값

## 구성

- `caller-permissions.example.json`: 지정된 역할에만 `AssumeRole` 요청 허용
- `trust-policy.example.json`: 지정한 호출자 역할만 신뢰
- `role-permissions.example.json`: 합성 버킷 조회 허용, 객체 쓰기·삭제 명시적 거부
- `session-policy.example.json`: 세션을 버킷 목록 조회 하나로 축소
- `scenarios.json`: 허용·신뢰 실패·세션 축소·명시적 거부 시나리오 7개
- `evaluate_policy.py`: 위 정책의 제한된 부분만 판정하는 결정적 로컬 평가기

이 평가기는 AWS IAM Policy Simulator가 아니며 조건 키, SCP, Permission Boundary, Resource Policy 전체 의미론을 구현하지 않는다.

## 실행

```powershell
cd F:\main\labs\04-iam-sts
python .\evaluate_policy.py --directory . --evidence .\evidence\2026-09-28.json
```

## 실제 결과

| 시나리오 | 관측 | 결과 |
|---|---|---|
| 지정 호출자의 역할 요청 | 호출자 정책과 신뢰 정책 모두 일치 | 허용 |
| 비신뢰 호출자의 역할 요청 | 신뢰 정책 불일치 | 거부 |
| 합성 버킷 목록 | 역할·세션 정책 교집합 | 허용 |
| 객체 조회 | 역할은 허용하지만 세션 정책에 없음 | 묵시적 거부 |
| 객체 쓰기·삭제 | 역할 정책의 `NoBucketWrites` | 명시적 거부 2건 |
| 계정 전체 버킷 조회 | 어느 정책도 허용하지 않음 | 묵시적 거부 |

예상한 7개 판정이 모두 일치했다. 허용 2건, 거부 5건이다.

- [실행 증적 JSON](evidence/2026-09-28.json)

## 검증하지 않은 것

- AWS `AssumeRole`과 임시 자격증명 발급·만료
- Azure Service Principal과 실제 RBAC
- 자격증명 탈취·폐기·회전
- Azure Resource Lock·삭제 보호의 실제 차단
- 운영 자원에 대한 공격 또는 삭제

따라서 이 결과는 **최소 권한 정책 조합의 로컬 판정 검증**이며, AWS/Azure 방어 효과나 실제 Workload Identity 런타임 검증이 아니다.

## 실제 계정 연결 후 확인 절차

1. 격리된 합성 버킷과 호출자·대상 역할을 생성한다.
2. 900초 세션 정책으로 `AssumeRole`을 호출하고 비밀 값 없이 만료 시각만 기록한다.
3. 범위 내 조회 성공, 범위 밖 조회와 쓰기·삭제 실패를 확인한다.
4. 만료 후 `ExpiredToken`을 확인한다.
5. 역할과 버킷을 제거하고 정제된 결정·오류 코드만 증적으로 남긴다.

## 프로젝트 연결

서브 프로젝트의 향후 Public Cloud Adapter와 Agent Workload Identity 관문에 연결할 수 있다. 어댑터가 `DEFERRED`이고 외부 런타임이 연결되지 않았으므로 서브 프로젝트의 하이브리드 클라우드 또는 Workload Identity 구현 증거로 간주하지 않는다.