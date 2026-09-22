# 실습 로드맵

상태 표기는 `계획`, `설계`, `로컬 검증`, `런타임 검증`을 사용합니다. 1·2번은 FRR 컨테이너에서 **로컬 검증**을 완료했습니다. 3번은 공개 장비 인증 실패를 기록한 **설계** 상태이며, 실제 API·CLI 대조는 아직 수행하지 못했습니다. 4번은 AWS 계정 없이 작성한 **설계**, 5번은 합성 서비스로 **로컬 검증**했습니다. 6번은 FreeRADIUS에서 **로컬 검증**했습니다. 7·8번은 별도 증적이 연결되기 전까지 **계획**입니다.

| 순서 | 주제 | 직접 확인할 질문 | 남길 증적 |
|---|---|---|---|
| 1 | [BGP/ECMP Spine-Leaf](../labs/01-bgp-ecmp/README.md) — 로컬 검증 | 링크 또는 Spine 장애 후 경로가 수렴하고 통신이 유지되는가? | [설정과 실행 출력](../labs/01-bgp-ecmp/evidence/2026-09-22.txt), 장애 전후 경로·ping |
| 2 | [EVPN/VXLAN](../labs/02-evpn-vxlan/README.md) — 로컬 검증 | 분리된 세그먼트의 허용·거부 통신이 의도대로 동작하는가? | [BGP EVPN·VNI·FDB 및 ping 출력](../labs/02-evpn-vxlan/evidence/2026-09-22.txt) |
| 3 | [RESTCONF/Python](../labs/03-restconf-python/README.md) — 설계 | API 조회 결과가 장비 CLI 상태와 일치하는가? | [읽기 전용 코드와 HTTP 401 증적](../labs/03-restconf-python/evidence/2026-09-22.txt); 실제 대조 대기 |
| 4 | [IAM/STS](../labs/04-iam-sts/README.md) — 설계 | 역할 위임, 최소 권한, 자격증명 만료가 동작하는가? | 예시 정책 4개; 계정 실행 대기 |
| 5 | [백업·복구](../labs/05-backup-recovery/README.md) — 로컬 검증 | 합성 서비스를 복원하거나 재구축하는 데 얼마나 걸리는가? | [RTO 1.627초·손실 2건](../labs/05-backup-recovery/evidence/2026-09-22.json) |
| 6 | [AAA/RADIUS](../labs/06-aaa-radius/README.md) — 로컬 검증 | 등록된 사용자만 RADIUS 인증을 통과하는가? | [Access-Accept 1건·Access-Reject 2건](../labs/06-aaa-radius/evidence/2026-09-22.txt) |
| 7 | AI Agent Security | Agent의 권한·통신·예산·승인 경계가 지켜지는가? | 정책, 로컬 테스트, 인가된 런타임 결과 |
| 8 | AI DC Network | 네트워크 설계에 필요한 추가 성능·혼잡 개념은 무엇인가? | 기술 조사와 재현 가능한 소규모 실험 |

## 실습 README 공통 양식

1. 문제와 브리핑 출처
2. 범위·상태와 구성 환경
3. 토폴로지 및 설정
4. 정상 상태의 기대값과 실제 출력
5. 장애 또는 거부 경로 테스트
6. 복구와 재검증
7. 결과·한계·개인 프로젝트와의 연결

증적이 없으면 `Result`에 성공 문장을 먼저 채우지 않습니다. 장비 이미지·버전에 따라 명령이 다르면 사용 환경을 명시합니다.
