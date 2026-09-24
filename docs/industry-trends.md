# IT·보안 브리핑에서 추린 기술 흐름

기준: 2026년 9월까지의 「IT·보안 데일리 브리핑」 대화 요약. 이 문서는 당시 브리핑의 **학습 주제 분류**이며, 각 시장 전망이나 기사 수치를 독립적으로 검증한 보고서가 아닙니다. 새 사실을 추가할 때는 원문 출처와 날짜를 확인합니다. 기사별 질문·실습·한계는 [뉴스 → 기술 실습 기록](news-to-labs.md)에 적습니다.

## 1. AI 인프라 전체 스택

브리핑에서는 모델·GPU뿐 아니라 전력, 냉각, 스토리지, 네트워크, Kubernetes, 관측, 보안이 함께 언급됐습니다. 포트폴리오에서는 이 큰 흐름을 개별 기술 실습의 배경으로 사용합니다.

**학습 연결:** 데이터센터 네트워크, GPU 워크로드의 트래픽 특성, 고밀도 환경의 운영 지표.

## 2. 데이터센터 네트워크

반복 주제는 BGP, ECMP, Spine-Leaf, EVPN/VXLAN, 고속 Ethernet, RoCEv2, 혼잡 제어와 광 연결입니다. 모든 기술을 한 번에 구현했다고 주장하지 않고, 라우팅과 장애 수렴부터 순차적으로 검증합니다.

**첫 실습:** 2 Spine / 2 Leaf BGP ECMP 토폴로지와 링크 장애 전후의 경로 확인.

## 3. Hybrid·Private·Sovereign Cloud

데이터 위치, 규제, 지연, 비용과 운영 통제가 클라우드 설계에 영향을 줍니다. 개인 프로젝트의 OpenStack/k3s 경계와 연결하되, 실제 퍼블릭 클라우드 연동 전에는 `Hybrid-Ready`로만 표기합니다.

**학습 연결:** Private IaaS, IAM/STS, Terraform, Kubernetes 네트워킹.

## 4. AI Agent Security와 보안 기본기

Agent가 API·셸·저장소·클라우드 권한을 사용할 때는 최소 권한, 단기 자격증명, 격리, 외부 통신 제한, 사람 승인, 감사가 중요합니다. 동시에 Credential 관리, 패치, 네트워크 분리, 취약점 우선순위와 공급망 검증도 계속 필요합니다.

**프로젝트 연결:** `snsd-multicloud-ops`의 AI Agent Sandbox 계약과 Zero Trust 검증. 계약·로컬 테스트와 통합 런타임 검증은 별도 상태입니다.

## 5. 복구와 운영

HA, 백업, 복원, 재구축, RTO/RPO를 분리해 봅니다. 현재 개인 프로젝트 범위에서는 합성 서비스의 백업·복원·선언적 재구축이 우선이며, Multi-Region DR은 별도 학습 주제입니다.

## 6. Kubernetes·자동화·관측

브리핑에서 반복된 운영 흐름은 네트워크 CLI에서 Python/API/Telemetry로, 서버 모니터링에서 Logs·Metrics·Traces를 연결하는 방향입니다. Kubernetes는 Pod뿐 아니라 Service, Ingress/Gateway, NetworkPolicy, RBAC, Storage와 관측까지 함께 학습합니다.

**실습 연결:** RESTCONF 조회 결과와 CLI 대조, 네트워크 상태 자동 점검, 합성 워크로드 관측.

## 7. 서비스 경계의 가용성과 취약점 우선순위

9월 23일 브리핑의 [F5 BIG-IP APM 권고](https://my.f5.com/manage/s/article/K000162605)와 [CISA KEV 공지](https://www.cisa.gov/news-events/alerts/2026/09/22/cisa-adds-four-known-exploited-vulnerabilities-catalog)는 로드밸런서·접근 제어 장비가 트래픽과 인증의 공통 경계임을 보여 줍니다. 패치는 KEV, 실제 악용, 외부 노출, 자산 중요도를 함께 보고 우선순위를 정합니다.

**실습 연결:** CVE나 F5 제품을 재현하지 않고, 먼저 Nginx 로드밸런서에서 백엔드 장애·재시도·복구 후 재편입을 측정했습니다.

## 새 브리핑을 반영하는 기준

새 기사를 바로 실습 성과로 쓰지 않습니다. 출처·보도일·사건일을 확인하고, 이 문서의 기존 흐름을 강화하는지 또는 새 문제를 제시하는지 판단합니다. 실제 구성이나 측정이 생기면 [뉴스 → 기술 실습 기록](news-to-labs.md)에 원문과 증적을 연결하고 [실습 로드맵](lab-roadmap.md)의 상태를 갱신합니다.
