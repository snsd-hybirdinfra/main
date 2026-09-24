# 09 Load Balancer HA: Backend 장애와 복구

## 뉴스에서 나온 질문

[F5 BIG-IP APM CVE-2026-94127 권고](https://my.f5.com/manage/s/article/K000162605)와 [CISA의 2026-09-22 KEV 추가 공지](https://www.cisa.gov/news-events/alerts/2026/09/22/cisa-adds-four-known-exploited-vulnerabilities-catalog)에서 로드밸런서·접근 제어 장비가 서비스와 인증의 중요한 경계라는 점을 확인했다. 여기서 **로드밸런서 뒤의 백엔드 하나가 중단돼도 서비스가 유지되고, 복구 후 다시 풀에 참여하는가?**를 내 실험 질문으로 정했다.

이 실습은 F5 제품이나 CVE-2026-94127을 재현하지 않는다. 보안 권고에서 파생한 **가용성 기초 실험**이다.

**상태: 로컬 검증.** Docker Desktop의 Nginx 컨테이너 3개로 합성 HTTP 응답만 확인했다.

## 구성

```text
Client (127.0.0.1:18080)
            |
       Nginx LB
         /    \
     web01    web02
```

- `web01`, `web02`: 자신의 이름을 반환하는 Nginx 백엔드
- `lb`: Round Robin upstream과 실패 시 다음 upstream 재시도
- [compose.yaml](compose.yaml): 컨테이너 구성
- [nginx.conf](nginx.conf): upstream·timeout·재시도 설정
- [run.ps1](run.ps1): 정상 → `web01` 중단 → 재시작 검증과 JSON 증적 생성

## 실행

```powershell
./run.ps1
```

스크립트는 시작 전후에 전용 Compose 프로젝트와 네트워크를 정리한다.

## 관측 결과

2026-09-24 실행의 [JSON 증적](evidence/2026-09-24.json):

| 단계 | 관측 |
|---|---|
| 정상 | 8건 중 `web01` 4건, `web02` 4건 |
| `web01` 중단 | 8건 모두 `web02` 응답, HTTP 요청 실패 0건 |
| `web01` 복구 | 8건 중 `web01` 4건, `web02` 4건 |

장애 중 한 요청은 죽은 upstream 연결을 시도한 뒤 재시도되어 약 1,005 ms가 걸렸다. 서비스 응답은 유지됐지만 백엔드 장애가 지연 증가로 나타날 수 있음을 함께 확인했다.

## 결과와 한계

- 정상 상태의 Round Robin 분산, 백엔드 하나 중단 시 대체 응답, 재시작 후 풀 복귀를 확인했다.
- Nginx의 passive retry를 사용했다. F5 BIG-IP의 active health monitor나 Access Policy Manager 동작을 검증한 결과가 아니다.
- TLS 종료, 세션 지속성, SNAT, WAF, OAuth, 실제 취약점, 부하 성능은 포함하지 않았다.
- 다음 단계는 active health check 또는 별도 HAProxy 구성으로 장애 감지 시간과 사용자 오류율을 측정하는 것이다.
