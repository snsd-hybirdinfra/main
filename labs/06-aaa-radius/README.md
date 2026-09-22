# 06 AAA / RADIUS: 승인·거부 정책 확인

## 뉴스에서 나온 질문

[Cisco ISE RADIUS 서비스 거부 권고(2026-09-16)](https://sec.cloudapps.cisco.com/security/center/content/CiscoSecurityAdvisory/cisco-sa-ise-RADIUS-dos-wR3hYPMw)를 보고 인증 기반 서비스의 중요성을 확인했다. **RADIUS의 기본 인증·거부 판정이 정확히 작동하는가?**부터 실습했다. 권고의 취약점·서비스 거부를 재현하거나 Cisco ISE를 시험하지는 않았다.

**상태: 로컬 검증.** FreeRADIUS 3.2.10 공식 컨테이너와 `radtest`를 같은 네트워크 네임스페이스의 루프백에서 실행했다. 실제 스위치·VPN·관리망 로그인은 검증하지 않았다.

## 질문과 가설

등록된 관리 계정의 올바른 비밀번호만 RADIUS 인증을 통과하는가? 틀린 비밀번호나 미등록 계정은 거부되는가?

## 구성

- [`run-lab.sh`](run-lab.sh)가 실행 때 무작위 테스트 비밀번호와 RADIUS 공유 비밀을 생성한다.
- 임시 `clients.conf`에는 `127.0.0.1` 클라이언트만 지정한다.
- 임시 `authorize`에는 합성 `lab-admin` 계정만 포함한다.
- 컨테이너는 `--network none`으로 실행하며 포트를 호스트에 게시하지 않는다.
- 실행 종료 시 컨테이너와 임시 설정을 삭제한다. 설정의 비밀번호·공유 비밀은 Git 증적에 포함하지 않는다.

공식 이미지 `freeradius/freeradius-server:3.2.10-alpine`를 `sha256:91acbee4a1f532e3a266ae3d7f153a5cf21f5faa9bc14116d5d1fe2c2a746c27`로 고정했다.

## 실행

WSL2 Ubuntu에서 Docker Engine이 실행 중이어야 한다.

```bash
bash /mnt/f/main/labs/06-aaa-radius/run-lab.sh
```

## 결과

[2026-09-22 정제 결과](evidence/2026-09-22.txt):

| 요청 | 기대 | 실제 |
|---|---|---|
| 등록된 계정·올바른 비밀번호 | Access-Accept | Access-Accept |
| 등록된 계정·틀린 비밀번호 | Access-Reject | Access-Reject |
| 미등록 계정 | Access-Reject | Access-Reject |

실제 네트워크 장비의 관리 접근 제어, RADIUS 클라이언트 IP 제한, TLS 터널, 계정 잠금, MFA, 회계(Accounting) 기록은 검증하지 않았다. 이 결과는 서버 측 인증 판정만 보여준다. 서브 프로젝트에서 AAA를 붙일 때는 NAS 장비와 실제 관리 경로에서 재검증해야 한다.

## 참고

- [FreeRADIUS Basic Configuration HOWTO](https://wiki.freeradius.org/guide/Basic-configuration-HOWTO)
- [FreeRADIUS radtest 매뉴얼](https://www.freeradius.org/radiusd/man/radtest.html)
- [공식 FreeRADIUS 컨테이너 이미지](https://hub.docker.com/r/freeradius/freeradius-server/tags)
