# BGP ECMP Spine-Leaf Lab

**상태:** 로컬 검증 완료 (2026-09-22, WSL2 Ubuntu의 FRR 컨테이너). 실제 EVE-NG 또는 물리 데이터센터 검증은 수행하지 않았습니다.

## 문제와 목표

두 Spine 경로를 가진 L3 Fabric에서 한 Spine이 멈춰도 Leaf 간 통신이 유지되는지 확인합니다. BGP가 같은 목적지 프리픽스에 두 개의 유효한 다음 홉을 설치하는지, 장애 때 하나만 남는지, 복구 뒤 다시 둘이 되는지를 Linux 라우팅 테이블과 Host 통신으로 검증합니다.

## 토폴로지

```text
        Spine1 (AS 65000)      Spine2 (AS 65000)
          /          \            /          \
         /            \          /            \
Leaf1 (AS 65101)     Leaf2 (AS 65102)
      |                      |
 Host1 10.201.101.3    Host2 10.201.102.3
```

| 링크 | Spine 주소 | Leaf 주소 |
|---|---|---|
| Spine1–Leaf1 | 10.201.11.2/29 | 10.201.11.3/29 |
| Spine1–Leaf2 | 10.201.12.2/29 | 10.201.12.3/29 |
| Spine2–Leaf1 | 10.201.21.2/29 | 10.201.21.3/29 |
| Spine2–Leaf2 | 10.201.22.2/29 | 10.201.22.3/29 |

Leaf1은 10.201.101.0/29, Leaf2는 10.201.102.0/29를 광고합니다. 두 Spine은 같은 AS를 사용하고, Leaf의 `maximum-paths 2`가 동일한 경로의 ECMP 설치를 허용합니다.

## 환경과 실행

- WSL2 Ubuntu, Docker Engine 및 Compose
- [FRRouting 10.7.0](https://github.com/FRRouting/frr/releases/tag/frr-10.7.0) 공식 이미지 다이제스트 고정
- BusyBox 1.37.0 이미지 다이제스트 고정
- Docker `network_mode: none`과 WSL의 직접 veth 링크. 외부 네트워크 연결이나 공개 포트 없음.
- WSL 사용자에게 비대화형 `sudo ip link` 권한 필요. FRR 이미지의 daemon에는 `NET_ADMIN`, `NET_RAW`, `SYS_ADMIN` capability가 필요했습니다.

WSL에서 실행:

```bash
bash /mnt/f/main/labs/01-bgp-ecmp/run-lab.sh
```

스크립트는 라우터·호스트를 띄운 뒤 veth 6개를 연결하고, 정상 → Spine1 중단 → 복구를 검사합니다. 종료 시 이 랩의 컨테이너만 제거합니다. 설정은 [compose.yaml](compose.yaml), [FRR 설정](configs/leaf1/frr.conf), [실행 스크립트](run-lab.sh)에 있습니다.

## 검증 결과

[2026-09-22 실행 출력](evidence/2026-09-22.txt)에서 확인한 값:

| 단계 | Leaf1의 10.201.102.0/29 경로 | Host1 → Host2 |
|---|---|---|
| 정상 | Spine1 10.201.11.2 + Spine2 10.201.21.2 | ping 3/3 |
| Spine1 중단 | Spine2 10.201.21.2만 남음 | ping 3/3 |
| Spine1 복구 | 두 다음 홉 재설치 | ping 3/3 |

정상 상태의 Leaf1 BGP 이웃 2개가 모두 Established 상태였고 각 이웃에서 프리픽스 1개를 받았습니다. traceroute는 Leaf1 → Spine1 → 응답 없는 홉 → Host2를 보여줬습니다. 홉 하나의 `*`는 ICMP 응답을 받지 못했다는 뜻이며, 종단 간 ping과 라우팅 테이블을 통신·경로 검증의 주 근거로 사용했습니다.

## 한계와 다음 단계

- FRR CLI가 vtysh.conf 누락 및 초기 설정 처리 경고를 출력했습니다. BGP 이웃·커널 ECMP 경로·종단 간 통신은 별도로 확인했으며, 경고 원인은 후속 정리 대상입니다.
- 이번 실습은 WSL2 컨테이너의 합성 주소와 FRR로 검증했습니다. EVE-NG의 특정 Cisco OS 동작이나 실제 400/800G Fabric 성능을 입증하지 않습니다.
- 장애 중 애플리케이션 세션이 무손실로 유지되는지, 수렴 시간이 몇 ms인지 측정하지 않았습니다. ping 3/3은 경로가 안정된 후의 확인입니다.
- 다음 실습에서는 EVPN/VXLAN의 Underlay·Overlay 분리와 세그먼트 격리를 검증합니다.

## 근거 문서

- [FRR BGP multipath 및 maximum-paths 설명](https://docs.frrouting.org/en/latest/bgp.html)
- [FRR 10.7.0 릴리스](https://github.com/FRRouting/frr/releases/tag/frr-10.7.0)
