# 개인 프로젝트 연결

## 주 프로젝트와 서브 프로젝트

- **주 정리 공간:** `F:\main` — 브리핑의 기술 흐름, 학습 계획, 독립 실습 및 결과.
- **서브 프로젝트:** [snsd-multicloud-ops](https://github.com/snsd-hybirdinfra/snsd-multicloud-ops) — 가상 증권사 비운영 환경의 Hybrid-Ready Private Cloud IDP.

서브 프로젝트의 상태 권위는 해당 저장소의 [README](https://github.com/snsd-hybirdinfra/snsd-multicloud-ops/blob/main/README.md), 아키텍처 기준선, 구현 로드맵에 있습니다. 이곳에서는 연결 관계만 정리하고 구현·검증 상태를 임의로 올리지 않습니다.

| main 실습 | 서브 프로젝트에서 연결되는 문제 |
|---|---|
| BGP/ECMP, EVPN/VXLAN | 금융 네트워크 언더레이의 라우팅, 분리, 장애 수렴 |
| RESTCONF/Python | 장비 상태 수집과 운영 자동화 |
| IAM/STS | 향후 퍼블릭 클라우드 어댑터의 단기 자격증명 설계 |
| 복구 실습 | 합성 서비스의 백업·복원·재구축 |
| AAA/RADIUS | 관리망 접근 제어 |
| AI Agent Security | Agent Sandbox의 격리·승인·통신·예산·감사 |

현재 퍼블릭 클라우드 실연동, 금융 네트워크 런타임, 플랫폼 전체 종단 간 검증은 완료 성과로 표시하지 않습니다.
