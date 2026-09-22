# 03 RESTCONF / Python: 인터페이스 상태 대조

## 뉴스에서 나온 질문

[Nokia의 네트워크 자동화 발표(2026-09-17)](https://www.nokia.com/newsroom/nokia-accelerates-network-automation-through-agentic-unified-data-foundation-with-microsoft/)에서 신뢰할 수 있는 상태 데이터의 필요성을 읽고 **API 조회 결과를 CLI와 대조할 수 있는가?**를 기초 질문으로 정했다. RESTCONF는 내가 선택한 검증 방법이며 발표 속 Nokia·Microsoft 구현을 시험한 것은 아니다.

## 질문과 범위

장비의 RESTCONF 운영 데이터가 SSH CLI의 현재 상태와 일치하는가? Cisco IOS XE의 `Cisco-IOS-XE-interfaces-oper:interfaces`를 GET으로 읽고 `show interfaces`의 관리 상태와 프로토콜 상태를 인터페이스 이름별로 대조한다. 공유 DevNet 장비에는 변경 요청을 보내지 않는다.

**상태: 설계.** 2026-09-22에 두 공개 샌드박스의 HTTPS/SSH 포트 접근을 확인했다. 공개 예시 계정으로 RESTCONF GET을 시도했으나 두 장비 모두 HTTP 401이어서 실제 데이터와 CLI를 대조하지 못했다. [접속 증적](evidence/2026-09-22.txt)을 참조한다.

## 실행

WSL Ubuntu에 Python 3과 `sshpass`가 필요하다. 장비 계정은 환경 변수로 전달한다. 실행 결과에는 비밀번호와 원시 장비 출력을 저장하지 않는다.

```bash
export IOSXE_HOST=sandbox-iosxe-latest-1.cisco.com
export IOSXE_USER='<계정>'
read -rsp 'IOS XE password: ' IOSXE_PASSWORD; export IOSXE_PASSWORD; echo
python3 compare.py --sandbox-insecure-tls > comparison.json
unset IOSXE_PASSWORD
```

일반 장비에서는 인증서 검증을 기본으로 사용한다. 사설 CA라면 `--ca-bundle path/to/ca.pem`을 지정한다. 공개 DevNet 장비의 인증서 이름 불일치 때문에 필요한 `--sandbox-insecure-tls`은 코드에서 두 Cisco 샌드박스 호스트명으로만 제한했다. 조직 장비에 이 옵션을 사용하지 않는다. SSH는 최초 연결 시 호스트 키를 기록하고 이후에는 변경을 확인한다.

`compare.py`는 HTTPS GET이 성공한 경우에만 SSH에서 `show interfaces`를 실행한다. 각 인터페이스의 API 관리·운영 상태와 CLI 관리·프로토콜 상태를 비교하며, 비교된 수·불일치 수·한쪽에만 있는 이름을 JSON으로 출력한다. 비교 대상이 없거나 상태를 해석할 수 없으면 통과로 처리하지 않는다. 장비 상태가 수집 사이에 바뀔 수 있으므로 불일치가 나오면 즉시 재수집해야 한다.

## 확인 기준과 현재 결과

| 확인 | 기대 | 2026-09-22 |
|---|---|---|
| RESTCONF GET | HTTP 200, 인터페이스 목록 | 두 공개 장비 모두 HTTP 401 |
| SSH CLI 수집 | 같은 장비의 `show interfaces` | API 인증 실패로 미실행 |
| 상태 대조 | 공통 인터페이스 ≥1, 불일치 0 | 미실행 |
| 거부 경로 | 인증 실패 시 성공 증적을 만들지 않음 | 확인: 종료 코드 2, 비교 미실행 |

이 실습은 계정 접근이 가능한 IOS XE 장비나 DevNet 예약형 샌드박스에서 다시 실행해 실제 JSON·CLI 대조 요약을 추가해야 **런타임 검증**으로 바뀐다. 원시 출력에 장비 주소·구성이 있을 수 있으므로 공개 저장소에는 정제 결과만 남긴다.

## 출처와 개인 프로젝트 연결

- [Cisco DevNet IOS XE Sandbox](https://developer.cisco.com/docs/ios-xe-voip/sandbox/): 공유/예약형 장비 범위.
- [Cisco DevNet IOS XE OpenAPI 예시](https://github.com/CiscoDevNet/cisco-ios-xe-openapi-swagger/blob/main/docs/GETTING_STARTED.md): 운영 데이터 GET 경로와 응답 필드.
- 개인 프로젝트의 네트워크 자동화에도 같은 패턴(읽기 → CLI 대조 → 불일치 시 중지)을 적용할 수 있다. 이 코드는 개인 프로젝트 장비에 실행한 증거가 아니다.
