# 업데이트 기록

## 2026-09-22 — 초기 정리

- 처음 공유한 GitHub 정리안의 8개 실습 주제를 로드맵으로 구성.
- 「IT·보안 데일리 브리핑」의 누적 요약을 기술 흐름과 커리어 로드맵으로 분류.
- `F:\main`을 주 저장소, `snsd-multicloud-ops`를 연결된 서브 프로젝트로 구분.

## 2026-09-22 — BGP/ECMP 첫 실습

- WSL2 FRR 10.7.0에서 2 Spine·2 Leaf·2 Host 토폴로지를 구성.
- 정상 경로 2개, Spine1 중단 후 Spine2 경로 1개와 Host 간 ping 3/3, 복구 후 경로 2개와 ping 3/3 확인.
- [설정과 정제 출력](../labs/01-bgp-ecmp/README.md)을 추가하고 상태를 로컬 검증으로 변경.

## 2026-09-22 — EVPN/VXLAN 두 번째 실습

- FRR 두 Leaf와 VNI 100·200의 BGP EVPN 제어면 및 VXLAN dataplane 구성.
- 같은 VNI의 Host 간 ping은 각각 3/3, 다른 VNI의 Host 간 ping은 0/2 확인.
- [설정과 출력](../labs/02-evpn-vxlan/README.md)을 추가하고 상태를 로컬 검증으로 변경.

## 2026-09-22 — RESTCONF/Python 접근 확인

- Cisco DevNet 공개 IOS XE 장비 두 곳에서 RESTCONF 인터페이스 GET을 시도했으나 공개 예시 계정이 HTTP 401을 반환.
- [읽기 전용 대조 코드](../labs/03-restconf-python/README.md)와 거부 증적을 추가. API·CLI 일치는 검증하지 않았으므로 상태는 설계.
## 이후 갱신 양식

### YYYY-MM-DD

- **새 소식:** 출처, 보도일, 사건일.
- **기존 흐름과의 관계:** 강화 / 수정 / 새 주제.
- **학습·실습에 반영:** 바뀐 파일과 이유.
- **검증 상태:** 계획 / 설계 / 로컬 검증 / 런타임 검증.
