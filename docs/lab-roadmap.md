# 실습 로드맵

각 주제를 선택한 뉴스 원문, 내가 도출한 질문, 실제 증적과 한계는 [뉴스 → 기술 실습 기록](news-to-labs.md)에 있습니다.

상태 표기는 `계획`, `설계`, `로컬 검증`, `런타임 검증`을 사용합니다. 현재 11개 실습 중 10개는 컨테이너·코드·합성 모델에서 **로컬 검증**, RESTCONF/Python 1개는 **설계** 상태입니다. 실제 운영 환경에서 검증한 실습은 없습니다.

| 순서 | 주제 | 직접 확인할 질문 | 남길 증적 |
|---|---|---|---|
| 1 | [BGP/ECMP Spine-Leaf](../labs/01-bgp-ecmp/README.md) — 로컬 검증 | 링크 또는 Spine 장애 후 경로가 수렴하고 통신이 유지되는가? | [설정과 실행 출력](../labs/01-bgp-ecmp/evidence/2026-09-22.txt), 장애 전후 경로·ping |
| 2 | [EVPN/VXLAN](../labs/02-evpn-vxlan/README.md) — 로컬 검증 | 분리된 세그먼트의 허용·거부 통신이 의도대로 동작하는가? | [BGP EVPN·VNI·FDB 및 ping 출력](../labs/02-evpn-vxlan/evidence/2026-09-22.txt) |
| 3 | [RESTCONF/Python](../labs/03-restconf-python/README.md) — 설계 | API 조회 결과가 장비 CLI 상태와 일치하는가? | [읽기 전용 코드와 HTTP 401 증적](../labs/03-restconf-python/evidence/2026-09-22.txt); 실제 대조 대기 |
| 4 | [IAM/STS](../labs/04-iam-sts/README.md) — 로컬 검증 | 신뢰 관계·역할·세션 정책·명시적 거부로 Workload Identity 행동 범위를 줄일 수 있는가? | [합성 정책 판정 7/7 일치](../labs/04-iam-sts/evidence/2026-09-28.json); AWS/Azure 발급·만료·Resource Lock은 미검증 |
| 5 | [백업·복구](../labs/05-backup-recovery/README.md) — 로컬 검증 | 합성 서비스를 복원하거나 재구축하는 데 얼마나 걸리는가? | [RTO 1.627초·손실 2건](../labs/05-backup-recovery/evidence/2026-09-22.json) |
| 6 | [AAA/RADIUS](../labs/06-aaa-radius/README.md) — 로컬 검증 | 등록된 사용자만 RADIUS 인증을 통과하는가? | [Access-Accept 1건·Access-Reject 2건](../labs/06-aaa-radius/evidence/2026-09-22.txt) |
| 7 | [AI Agent Security](../labs/07-ai-agent-security/README.md) — 로컬 검증 | 도구의 권한·통신·예산·합성 승인 경계가 지켜지는가? | [결정적 게이트 실행 결과](../labs/07-ai-agent-security/evidence/2026-09-22.json); 실제 Agent 런타임 대기 |
| 8 | [AI DC Network](../labs/08-ai-dc-network/README.md) — 로컬 검증 | 공유 병목에서 TCP 처리량과 지연이 어떻게 바뀌는가? | [20 Mbit/s 가상 링크 측정](../labs/08-ai-dc-network/evidence/2026-09-22.json); RoCE/ECN/PFC는 미검증 |
| 9 | [Load Balancer HA](../labs/09-load-balancer-ha/README.md) — 로컬 검증 | 백엔드 하나가 중단돼도 서비스가 유지되고 복구 후 다시 풀에 참여하는가? | [정상 4:4·장애 중 web02 8/8·복구 4:4](../labs/09-load-balancer-ha/evidence/2026-09-24.json); F5/CVE는 미검증 |
| 10 | [Network Digital Twin](../labs/10-network-digital-twin/README.md) — 로컬 검증 | 읽기 전용 모델로 애플리케이션 경로·장애 내성·세그멘테이션 의도를 판정할 수 있는가? | [정상 2경로·단일 장애 1경로·이중 장애 0경로·정책 거부](../labs/10-network-digital-twin/evidence/2026-09-26.json); 실제 장비/IP Fabric은 미검증 |
| 11 | [Vulnerability Prioritization](../labs/11-vulnerability-prioritization/README.md) — 로컬 검증 | KEV·노출·중요도·관리 Plane·기한을 합쳐 조치 순서를 일관되게 판정할 수 있는가? | [P0 2건·P2 1건·P3 2건과 입력 일치 검사](../labs/11-vulnerability-prioritization/evidence/2026-09-27.json); 실제 자산·패치는 미검증 |

## 실습 README 공통 양식

1. 문제와 브리핑 출처
2. 범위·상태와 구성 환경
3. 토폴로지 및 설정
4. 정상 상태의 기대값과 실제 출력
5. 장애 또는 거부 경로 테스트
6. 복구와 재검증
7. 결과·한계·개인 프로젝트와의 연결

증적이 없으면 `Result`에 성공 문장을 먼저 채우지 않습니다. 장비 이미지·버전에 따라 명령이 다르면 사용 환경을 명시합니다.
