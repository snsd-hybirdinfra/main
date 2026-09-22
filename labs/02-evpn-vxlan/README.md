# BGP EVPN / VXLAN L2VNI Lab

## 뉴스에서 나온 질문

[Cisco의 AI 네트워크 글(2026-09-21)](https://blogs.cisco.com/news/the-ai-era-demands-more-than-speed-building-secure-intelligent-networks-from-silicon-to-optics)에서 확장형 네트워크 요구를 읽고 **패브릭의 세그먼트 간 허용·격리를 확인할 수 있는가?**를 질문으로 정했다. EVPN/VXLAN은 내가 선택한 구현 방식이며 기사가 이 토폴로지를 검증한 것은 아니다.

**상태:** 로컬 검증 완료 (2026-09-22, WSL2 FRR 컨테이너). 두 Leaf의 L2VNI 동작을 확인했으며, 2-Spine Underlay나 L3VNI는 이번 범위가 아닙니다.

## 문제와 가설

같은 물리 Underlay 위에서 두 논리 세그먼트를 운반할 때, 같은 VNI의 원격 Host는 통신하고 서로 다른 VNI의 Host는 같은 IP 대역을 사용해도 L2로 연결되지 않아야 합니다.

## 토폴로지

```text
Host1 (.11) -- VNI 100 -- Leaf1 ==== Underlay ==== Leaf2 -- VNI 100 -- Host2 (.12)
Host3 (.13) -- VNI 200 -- Leaf1 ==== 10.202.0.0/30 ==== Leaf2 -- VNI 200 -- Host4 (.14)
                                  VTEP .1              VTEP .2
```

- Leaf1/Leaf2: AS 65200의 직접 iBGP EVPN 이웃. Underlay는 10.202.0.1/30 ↔ 10.202.0.2/30 veth 링크입니다.
- VTEP: 10.255.1.1/32 ↔ 10.255.1.2/32. BGP IPv4 Unicast가 VTEP /32를 교환합니다.
- VNI 100·200: 각각 Linux bridge와 VXLAN 인터페이스에 매핑합니다. FRR의 `advertise-all-vni`가 EVPN 제어면을 활성화합니다.
- 네 Host 모두 실습용 192.0.2.0/24 대역을 사용합니다. VNI 100과 200이 분리돼 있는지 보기 위한 의도적 구성입니다.

## 실행

WSL2 Ubuntu에 Docker Engine, Compose, 비대화형 `sudo ip link`가 필요합니다.

```bash
bash /mnt/f/main/labs/02-evpn-vxlan/run-lab.sh
```

스크립트는 Docker `network_mode: none`에서 시작한 뒤 직접 veth 링크를 연결합니다. Host 연결과 VXLAN 터널은 컨테이너 네임스페이스 안에만 존재하며, 공개 포트는 없습니다. 끝나면 이 랩의 컨테이너를 제거합니다.

[Compose 설정](compose.yaml), [Leaf1 FRR 설정](configs/leaf1/frr.conf), [Leaf2 FRR 설정](configs/leaf2/frr.conf), [실행 스크립트](run-lab.sh).

## 검증 결과

[2026-09-22 실행 출력](evidence/2026-09-22.txt):

| 확인 항목 | 관측 결과 |
|---|---|
| Leaf1 BGP EVPN 이웃 | Leaf2와 Established, EVPN 프리픽스 3개 수신 |
| VNI 100/200 | 둘 다 L2 VNI로 감지, 각 VNI의 Remote VTEP 1개 |
| 원격 FDB | VNI 100의 원격 MAC이 10.255.1.2로 설치 |
| Host1 → Host2 (VNI 100) | ping 3/3 |
| Host3 → Host4 (VNI 200) | ping 3/3 |
| Host1 → Host3 (다른 VNI) | ping 0/2, 연결 안 됨 |

Host1에서 Host3으로는 같은 IP 프리픽스의 주소를 ARP로 찾지만, 서로 다른 Bridge/VNI에 있어 응답을 받지 못했습니다. 두 양성 테스트와 EVPN 이웃·VNI·FDB 출력을 함께 확인해 단순 단절이 아니라 의도한 세그먼트 분리임을 확인했습니다.

## 한계

- 두 Leaf를 직접 연결한 소규모 Underlay입니다. 멀티 홉 Spine-Leaf Fabric, Route Reflector, L3VNI, Anycast Gateway, MTU·성능 시험은 아직 하지 않았습니다.
- FRR CLI가 `vtysh.conf` 누락 및 초기 설정 처리 경고를 출력했습니다. 이웃·VNI·FDB·Host 통신은 별도로 확인했습니다.
- 이 결과는 합성 컨테이너 랩의 로컬 검증이며, 금융 네트워크 또는 실제 데이터센터의 배포 증거가 아닙니다.

## 근거 문서

- [FRR EVPN 개념, VXLAN dataplane, advertise-all-vni](https://docs.frrouting.org/en/latest/evpn.html)
- [FRR 10.7.0 릴리스](https://github.com/FRRouting/frr/releases/tag/frr-10.7.0)
