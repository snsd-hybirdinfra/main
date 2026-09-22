# Network · Cloud · AI Infrastructure Labs

「IT·보안 데일리 브리핑」의 뉴스를 읽고 **기술 문제를 뽑아 직접 시험한** 네트워크·클라우드·보안·AI 인프라 포트폴리오입니다. 각 기록은 **원문 → 내가 세운 질문 → 실습 → 관측 증적 → 검증 한계**로 이어집니다.

> 상태: BGP/ECMP와 EVPN/VXLAN 실습을 FRR 컨테이너에서 로컬 검증했습니다. 백업·복구, AAA/RADIUS, AI Agent Security, AI DC Network는 범위를 제한한 합성 환경에서 로컬 검증했습니다. RESTCONF/Python과 IAM/STS는 설계 상태입니다.

## 읽는 순서

1. [뉴스에서 시작한 기술 실습: 출처·질문·증적](docs/news-to-labs.md)
2. [브리핑에서 추린 기술 흐름](docs/industry-trends.md)
3. [실습 로드맵과 검증 기준](docs/lab-roadmap.md)
4. [커리어 로드맵](docs/career-roadmap.md)
5. [개인 프로젝트 연결](docs/project-map.md)
6. [업데이트 기록](docs/update-log.md)

## 뉴스가 실습으로 이어진 예

| 확인한 원문 | 내가 검증한 기술 질문 | 실제 결과 |
|---|---|---|
| [Cisco의 AI 네트워크 글](https://blogs.cisco.com/news/the-ai-era-demands-more-than-speed-building-secure-intelligent-networks-from-silicon-to-optics) | Spine 장애에도 BGP/ECMP 경로와 통신이 유지되는가? | [FRR 실습](labs/01-bgp-ecmp/README.md)에서 대체 경로 1개·ping 3/3 |
| [AWS의 DR 계획 글](https://aws.amazon.com/blogs/compute/planning-for-disaster-recovery-using-aws-local-zones-and-aws-outposts-racks/) | 백업으로 합성 서비스를 얼마나 빨리 되살리는가? | [복구 실습](labs/05-backup-recovery/README.md)에서 RTO 1.627초·손실 2건 |
| [Google Cloud의 Agent 보안 글](https://cloud.google.com/blog/topics/systems/using-ai-agents-to-secure-google-infrastructure/) | 도구 사용과 외부 통신을 정책으로 거부할 수 있는가? | [로컬 하네스](labs/07-ai-agent-security/README.md)의 허용·거부 확인 |

위 기술 질문은 원문에서 **내가 도출한 실험 설계**입니다. 기사 속 제품이나 실제 AI 워크로드를 시험했다는 뜻은 아닙니다. 8개 실습의 연결은 [뉴스 → 기술 실습 기록](docs/news-to-labs.md)에 있습니다.

## 학습 흐름

```text
Routing & Switching → BGP/ECMP → Spine-Leaf → EVPN/VXLAN
                   → Network Automation → Private/Cloud Networking
                   → Kubernetes → AI Data Center Infrastructure
```

## 완료한 실습

- [BGP/ECMP Spine-Leaf: 정상 경로 2개, Spine 장애 시 통신 유지, 복구 후 경로 재형성](labs/01-bgp-ecmp/README.md)
- [EVPN/VXLAN: VNI 100·200 통신과 VNI 간 격리](labs/02-evpn-vxlan/README.md)
- [백업·복구: 합성 서비스 RTO 1.627초, 손실 2건](labs/05-backup-recovery/README.md)
- [AAA/RADIUS: 승인 1건, 거부 2건](labs/06-aaa-radius/README.md)
- [AI Agent Security: 도구·통신·예산·합성 승인 경계](labs/07-ai-agent-security/README.md)
- [AI DC Network: 20 Mbit/s 가상 병목의 처리량·지연](labs/08-ai-dc-network/README.md)

## 설계 중인 실습

- [RESTCONF/Python: 공개 IOS XE 샌드박스 HTTP 401, 실제 CLI 대조 대기](labs/03-restconf-python/README.md)
- [IAM/STS: AWS 계정 검증 대기](labs/04-iam-sts/README.md)

## 운영 원칙

- 뉴스와 업계 전망은 **주제 선정의 배경**으로 기록합니다.
- 실습은 **문제 → 가설 → 구성 → 정상·장애·보안 검증 → 결과 → 한계** 순서로 정리합니다.
- **계획 / 설계 / 로컬 검증 / 런타임 검증** 상태를 구분합니다.
- 출처 링크와 보도일, 사건 발생일을 함께 남기며 같은 뉴스를 중복 적재하지 않습니다.
- 실제 자격증명·계정 식별자, 고객 정보, 원시 로그는 올리지 않습니다. 실습용 합성 계정은 별도로 표시합니다.

## 연결된 서브 프로젝트

[snsd-multicloud-ops](https://github.com/snsd-hybirdinfra/snsd-multicloud-ops)는 가상 증권사 비운영 환경을 위한 **Hybrid-Ready Private Cloud IDP** 프로젝트입니다. 이 main 저장소는 서브 프로젝트의 실제 구현·검증을 참조하되, 이곳 `main`의 뉴스·학습·실습 기록과 상태를 혼동하지 않습니다. 현재 퍼블릭 클라우드 연동은 검증되지 않았습니다.
