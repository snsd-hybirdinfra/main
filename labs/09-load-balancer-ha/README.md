# 09 Edge Load Balancer HA: 관리면 분리와 백엔드 장애 복구

## 왜 기존 실습을 넓혔는가

[F5 BIG-IP APM CVE-2026-94127 권고](https://my.f5.com/manage/s/article/K000162605)와 [CISA의 2026-09-22 KEV 공지](https://www.cisa.gov/news-events/alerts/2026/09/22/cisa-adds-four-known-exploited-vulnerabilities-catalog)를 보고 처음에는 백엔드 하나가 멈췄을 때 서비스가 유지되는지 확인했다.

이후 [Citrix NetScaler 보안 공지 CTX697096](https://support.citrix.com/external/article/CTX697096)(2026-09-27)과 [관리·데이터 Plane 분리 문서](https://docs.netscaler.com/en-us/citrix-adc/current-release/networking/mgmt-and-data-plane-separation.html)(2026-09-08)를 확인했다. 새 실습을 하나 더 만들면 기존 장애 전환 실습과 겹치기 때문에, 같은 서비스 경계에서 관리 접근 분리까지 확인하도록 09번 실습을 넓혔다.

제품 취약점을 공격한 실습은 아니다. 뉴스에서 다음 두 질문을 뽑아 로컬 컨테이너로 검증했다.

1. SSH 관리 서비스는 관리망 주소에서만 열리고 데이터망에서는 닫혀 있는가?
2. 백엔드 하나가 멈춰도 사용자 HTTP 요청이 이어지고, 복구 후 다시 풀에 참여하는가?

## 실습 구성

```text
관리망 172.31.10.0/24
Admin 172.31.10.20 ── SSH ──> Edge 172.31.10.10:22

데이터망 172.31.20.0/24
Client 172.31.20.20 ── HTTP ─> Edge 172.31.20.10:80
                                      ├─ web01 172.31.20.31
                                      └─ web02 172.31.20.32

Client ── SSH ──> Edge 172.31.20.10:22  [거부 기대]
```

- `edge`: 관리망과 데이터망에 각각 연결된 Nginx·OpenSSH 컨테이너
- `admin`: 관리망에서 일회성 공개키로 SSH를 시도하는 컨테이너
- `client`: 데이터망에서 HTTP와 SSH 거부를 확인하는 컨테이너
- `web01`, `web02`: 자신의 이름을 반환하는 Nginx 백엔드
- [compose.yaml](compose.yaml): 두 네트워크와 고정 주소 구성
- [edge-entrypoint.sh](edge-entrypoint.sh): SSH를 관리 주소에만 바인딩
- [nginx.conf](nginx.conf): HTTP를 데이터 주소에만 바인딩하고 백엔드 재시도 설정
- [run.ps1](run.ps1): 접근 경계와 정상·장애·복구 흐름을 실행하고 JSON 증적 생성

테스트용 개인키는 `admin` 컨테이너 안에서 실행할 때마다 만들고 종료 시 함께 지운다. 비밀번호 로그인은 껐고 저장소에는 개인키를 남기지 않는다.

## 실행

```powershell
./run.ps1
```

스크립트는 빌드와 검증을 마친 뒤 컨테이너와 전용 네트워크를 정리한다.

## 직접 확인한 결과

2026-09-29 실행의 [통합 JSON 증적](evidence/2026-09-29.json):

| 확인 단계 | 관측 |
|---|---|
| Admin → 관리 주소 SSH | 종료 코드 0, `management-ssh-ok` |
| Client → 데이터 주소 SSH | 종료 코드 255, 연결 실패 |
| 정상 HTTP | `web01`과 `web02` 모두 응답 |
| `web01` 중단 | `web02` 8/8, 요청 실패 없음 |
| `web01` 복구 | 두 백엔드가 다시 응답 |

이전의 순수 장애 전환 결과도 [2026-09-24 증적](evidence/2026-09-24.json)에 남겨 두었다. 당시에는 정상 4:4, `web01` 중단 중 `web02` 8/8, 복구 후 4:4를 확인했다. 이번 통합 실행에서는 분산 횟수 자체보다 양쪽 백엔드가 관측되는지를 통과 조건으로 삼았다.

## 이번 실습에서 말할 수 있는 범위

- 관리용 SSH가 관리망 주소에서 성공하고 데이터망 주소에서 실패하는 것을 확인했다.
- Nginx의 passive retry로 단일 백엔드 중단 중 HTTP 응답이 유지되고 복구 후 풀에 다시 들어오는 것을 확인했다.
- NetScaler 또는 F5 장비, 공지의 CVE, NSIP·SNIP·VIP, 실제 ACL과 HA Pair는 검증하지 않았다.
- 인터넷 노출, TLS 종료, VPN, WAF, AAA, 세션 지속성, 취약점 재현과 부하 성능은 포함하지 않았다.

다음 단계는 실제 가상 장비나 허가된 테스트 계정에서 관리 Route와 ACL을 확인하고, active health check의 장애 감지 시간과 사용자 오류율을 측정하는 것이다.
