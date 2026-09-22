# 04 IAM / STS: 최소 권한 역할 위임

## 뉴스에서 나온 질문

[Google Threat Intelligence Group의 적대적 AI 분석(2026-09-08)](https://cloud.google.com/blog/topics/threat-intelligence/from-prompting-to-autonomy-the-evolution-of-adversarial-ai)에서 클라우드 자원과 자격증명 오용 위험을 확인했다. **최소 권한 역할과 단기 자격증명을 실제로 적용할 수 있는가?**를 내 질문으로 정했으며, 현재는 정책 설계만 했고 실제 공격이나 AWS 방어 효과를 검증하지 않았다.

**상태: 설계.** 실행 가능한 AWS 실습 계정이 연결되어 있지 않아 정책 문서의 JSON 구문만 확인했다. 로컬 환경에 AWS CLI 설정 파일과 자격증명 파일도 없다. 역할 생성, `AssumeRole`, S3 허용·거부, 실제 만료는 수행하지 않았다.

## 질문

지정한 호출자만 역할을 맡고, 역할과 세션 정책의 교집합 내에서만 읽고, 임시 자격증명이 만료되는가?

## 구성

- `caller-permissions.example.json`: 지정된 실습 역할만 위임 요청.
- `trust-policy.example.json`: 지정된 호출자 역할만 신뢰.
- `role-permissions.example.json`: 합성 버킷의 조회만 허용하고 쓰기를 명시적으로 거부.
- `session-policy.example.json`: 위임 세션을 버킷 목록 조회로 더 좁힘.

`111122223333`과 `lab-synthetic-artifacts`는 예시 값이다. 실제 계정·버킷·역할 이름으로 바꾸되 운영 자원에는 연결하지 않는다. 정책만으로 계정 내 실제 권한이 증명되지는 않는다.

## 실습 계정 연결 후 확인 절차

1. 합성 버킷과 호출자/대상 역할을 만들고 위 정책을 적용한다. 생성한 리소스 ARN을 기록한다.
2. 호출자 역할에서 대상 역할로 `AssumeRole`을 900초 세션 정책과 함께 호출한다. 반환된 `Expiration`과 현재 UTC의 차이를 기록하고 비밀 키와 토큰은 저장하지 않는다.
3. 임시 세션으로 합성 버킷 `ListBucket`을 수행해 허용을 확인한다.
4. 임시 세션으로 `ListAllMyBuckets` 같은 범위 밖의 **읽기** 작업을 수행해 `AccessDenied`를 확인한다. 쓰기 거부는 AWS IAM Policy Simulator에서 대상 역할 정책의 `s3:PutObject`을 평가한다. 시뮬레이터 결과는 실제 API 거부와 구별해 기록한다.
5. 임시 세션의 `Expiration` 이후 같은 읽기 요청이 `ExpiredToken`을 반환하는지 확인한다. 중간에 자격증명을 갱신하는 SDK 설정을 쓰지 않는다.
6. 실습 역할·버킷을 정리하고 정제된 요청 시각, 결정, 오류 코드만 증적으로 남긴다.

### 검증 표

| 항목 | 성공 기준 | 현재 |
|---|---|---|
| 신뢰 관계 | 허용 호출자만 `AssumeRole` 성공 | 미실행 |
| 최소 권한 | 범위 내 조회 허용, 범위 밖 조회 거부 | 미실행 |
| 쓰기 금지 | 정책 시뮬레이터에서 명시적 거부 | 미실행 |
| 만료 | 만료 후 `ExpiredToken` | 미실행 |

AWS는 역할의 신뢰 정책과 권한 정책을 구분하고, 세션 정책을 역할 권한과 교집합으로 적용한다. `SimulatePrincipalPolicy`는 실제 API 호출을 실행하지 않는다. 만료 응답은 실제 임시 세션으로 따로 확인해야 한다.

## 출처·개인 프로젝트 연결

- [AWS STS AssumeRole API](https://docs.aws.amazon.com/STS/latest/APIReference/API_AssumeRole.html)
- [AWS IAM Policy Simulator](https://docs.aws.amazon.com/cli/latest/reference/iam/simulate-principal-policy.html)
- 서브 프로젝트의 클라우드 연동 설계 시 사용할 검증 관문이다. 현재 서브 프로젝트의 퍼블릭 클라우드 연동 증거로 간주하지 않는다.
