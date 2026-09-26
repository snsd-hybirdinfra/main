# 뉴스에서 시작한 기술 실습

2026-09-26까지 ChatGPT 웹의 「IT·보안 데일리 브리핑」과 기사 원문을 대조했다. 이 저장소는 뉴스 스크랩이 아니라 **기사의 문제 → 내가 세운 기술 질문 → 직접 실행한 실습 → 증적과 한계**를 기록한다. 기사에 없는 구현 기술은 내 실험 설계로 구분한다.

| 원문과 발행일 | 내가 세운 질문 | 실습과 관측 | 검증하지 않은 것 |
|---|---|---|---|
| [Cisco AI 네트워크 글](https://blogs.cisco.com/news/the-ai-era-demands-more-than-speed-building-secure-intelligent-networks-from-silicon-to-optics), 2026-09-21 | 경로 하나가 사라져도 연결이 유지되는가? | [01 BGP/ECMP](../labs/01-bgp-ecmp/README.md): FRR Spine 장애 후 대체 경로와 ping [증적](../labs/01-bgp-ecmp/evidence/2026-09-22.txt) | AI 워크로드·상용 장비 |
| 같은 Cisco 글 | 테넌트 세그먼트를 분리할 수 있는가? | [02 EVPN/VXLAN](../labs/02-evpn-vxlan/README.md): VNI 100·200 허용·격리 [증적](../labs/02-evpn-vxlan/evidence/2026-09-22.txt) | L3VNI·상용 패브릭 |
| [Nokia 자동화 발표](https://www.nokia.com/newsroom/nokia-accelerates-network-automation-through-agentic-unified-data-foundation-with-microsoft/), 2026-09-17 | API 상태를 CLI와 대조할 수 있는가? | [03 RESTCONF/Python](../labs/03-restconf-python/README.md): 읽기 전용 코드와 HTTP 401 [증적](../labs/03-restconf-python/evidence/2026-09-22.txt). **설계** | API·CLI 실제 일치 |
| [Google 위협 분석](https://cloud.google.com/blog/topics/threat-intelligence/from-prompting-to-autonomy-the-evolution-of-adversarial-ai), 2026-09-08 | 자격증명 오용 위험에 최소 권한·단기 자격증명을 적용할 수 있는가? | [04 IAM/STS](../labs/04-iam-sts/README.md): 예시 정책 구문 확인. **설계** | AWS 계정 실행·공격 재현 |
| [AWS DR 계획 글](https://aws.amazon.com/blogs/compute/planning-for-disaster-recovery-using-aws-local-zones-and-aws-outposts-racks/), 2026-09-17 | 백업으로 복구 시간과 손실량을 잴 수 있는가? | [05 백업·복구](../labs/05-backup-recovery/README.md): 합성 서비스 RTO 1.627초·손실 2건 [증적](../labs/05-backup-recovery/evidence/2026-09-22.json) | AWS Local Zones·Outposts·운영 DR |
| [Cisco ISE RADIUS 권고](https://sec.cloudapps.cisco.com/security/center/content/CiscoSecurityAdvisory/cisco-sa-ise-RADIUS-dos-wR3hYPMw), 2026-09-16 | RADIUS의 기본 인증·거부가 정확히 작동하는가? | [06 AAA/RADIUS](../labs/06-aaa-radius/README.md): Accept 1·Reject 2 [증적](../labs/06-aaa-radius/evidence/2026-09-22.txt) | 권고의 취약점·서비스 거부·ISE |
| [Google Agent 보안 글](https://cloud.google.com/blog/topics/systems/using-ai-agents-to-secure-google-infrastructure/), 2026-09-18 | 도구 호출의 권한·통신·비용 경계를 강제할 수 있는가? | [07 AI Agent Security](../labs/07-ai-agent-security/README.md): 결정적 게이트의 허용·거부 [증적](../labs/07-ai-agent-security/evidence/2026-09-22.json) | 실제 LLM Agent·사람 승인 |
| Cisco AI 네트워크 글 | 공유 병목에서 처리량과 지연이 어떻게 바뀌는가? | [08 AI DC Network](../labs/08-ai-dc-network/README.md): 20 Mbit/s 가상 링크의 TCP 약 19 Mbit/s·부하 중 ping 69.16 ms [증적](../labs/08-ai-dc-network/evidence/2026-09-22.json) | GPU/RDMA/RoCE·ECN/PFC·광 연결 |
| [F5 CVE-2026-94127 권고](https://my.f5.com/manage/s/article/K000162605)와 [CISA KEV 공지](https://www.cisa.gov/news-events/alerts/2026/09/22/cisa-adds-four-known-exploited-vulnerabilities-catalog), 2026-09-22 | 백엔드 하나가 중단돼도 서비스가 유지되고 복구 후 다시 분산되는가? | [09 Load Balancer HA](../labs/09-load-balancer-ha/README.md): 정상 4:4, web01 중단 중 web02 8/8, 복구 후 4:4 [증적](../labs/09-load-balancer-ha/evidence/2026-09-24.json) | F5 제품·APM·OAuth·취약점 재현, TLS·WAF·성능 |
| [IP Fabric 애플리케이션 인프라 매핑 글](https://ipfabric.io/blog/application-to-infrastructure-mapping/), 2026-09-23 및 [8.1 릴리스 노트](https://docs.ipfabric.io/latest/releases/release_notes/8.1/) | 읽기 전용 모델로 애플리케이션 경로, 단일 장애 내성, 금지 흐름을 배포 전에 판정할 수 있는가? | [10 Network Digital Twin](../labs/10-network-digital-twin/README.md): 정상 경로 2개, spine1 중단 후 경로 1개, 두 Spine 중단 후 경로 0개, guest→admin 정책 거부 [증적](../labs/10-network-digital-twin/evidence/2026-09-26.json) | IP Fabric 제품·실제 장비/API, 자동 수집, 라우팅 수렴, ACL/NAT·포트 판정 |

이 표의 질문과 구현 방식은 원문을 읽고 **내가 도출한 것**이다. 각 기사에서 위 토폴로지나 측정값을 제시했다는 뜻은 아니다. 원문의 발행일을 사용했고 별도 사건일이 확인되지 않은 발표에 사건일을 임의로 붙이지 않았다.

## 업데이트 기준

1. 원문의 링크·발행일·핵심 문제를 확인하고 기존 기술 흐름과 비교한다.
2. 원문 사실과 내 기술적 추론을 분리한 뒤 정상·장애·거부 경로를 설계한다.
3. 실행 환경과 관측값을 증적으로 남긴다. 실행 전이면 **설계**, 합성 환경이면 **로컬 검증**으로 표기한다.
4. 한계와 다음 질문을 기록하고 [실습 로드맵](lab-roadmap.md)의 상태를 갱신한다.
