# Network · Cloud · AI Infrastructure Labs

네트워크를 기반으로 데이터센터, 클라우드, 보안, AI 인프라까지 확장하는 학습·검증 기록입니다. 「IT·보안 데일리 브리핑」에서 반복되는 기술 흐름을 주제로 고르고, 직접 구성한 실습과 검증 결과를 연결합니다.

> 상태: BGP/ECMP와 EVPN/VXLAN 실습을 FRR 컨테이너에서 로컬 검증했습니다. RESTCONF/Python은 공개 샌드박스 인증 실패로 설계 상태이며, 나머지 로드맵 항목은 계획입니다.

## 읽는 순서

1. [브리핑에서 추린 기술 흐름](docs/industry-trends.md)
2. [실습 로드맵과 검증 기준](docs/lab-roadmap.md)
3. [커리어 로드맵](docs/career-roadmap.md)
4. [개인 프로젝트 연결](docs/project-map.md)
5. [업데이트 기록](docs/update-log.md)

## 학습 흐름

```text
Routing & Switching → BGP/ECMP → Spine-Leaf → EVPN/VXLAN
                   → Network Automation → Private/Cloud Networking
                   → Kubernetes → AI Data Center Infrastructure
```

## 완료한 실습

- [BGP/ECMP Spine-Leaf: 정상 경로 2개, Spine 장애 시 통신 유지, 복구 후 경로 재형성](labs/01-bgp-ecmp/README.md)
- [EVPN/VXLAN: VNI 100·200 통신과 VNI 간 격리](labs/02-evpn-vxlan/README.md)

## 설계 중인 실습

- [RESTCONF/Python: 공개 IOS XE 샌드박스 HTTP 401, 실제 CLI 대조 대기](labs/03-restconf-python/README.md)

## 운영 원칙

- 뉴스와 업계 전망은 **주제 선정의 배경**으로 기록합니다.
- 실습은 **문제 → 가설 → 구성 → 정상·장애·보안 검증 → 결과 → 한계** 순서로 정리합니다.
- **계획 / 설계 / 로컬 검증 / 런타임 검증** 상태를 구분합니다.
- 출처 링크와 보도일, 사건 발생일을 함께 남기며 같은 뉴스를 중복 적재하지 않습니다.
- 자격증명, 계정 값, 고객 정보, 원시 로그는 올리지 않습니다.

## 연결된 서브 프로젝트

[snsd-multicloud-ops](https://github.com/snsd-hybirdinfra/snsd-multicloud-ops)는 가상 증권사 비운영 환경을 위한 **Hybrid-Ready Private Cloud IDP** 프로젝트입니다. 이 main 저장소는 서브 프로젝트의 실제 구현·검증을 참조하되, 이곳 `main`의 뉴스·학습·실습 기록과 상태를 혼동하지 않습니다. 현재 퍼블릭 클라우드 연동은 검증되지 않았습니다.
