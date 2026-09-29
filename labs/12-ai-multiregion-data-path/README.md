# 12 AI Multi-Region Data Path: Hub·Spoke와 로컬 캐시

## 이 구조를 정리한 이유

[AWS의 SageMaker HyperPod·Qumulo Multi-Region 학습 글](https://aws.amazon.com/blogs/machine-learning/multi-region-training-with-amazon-sagemaker-hyperpod-and-qumulo/)(2026-09-25)은 GPU가 있는 Region과 원본 데이터가 있는 Region이 다를 때 생기는 지연과 복제 비용을 다룬다.

전체 데이터를 Region마다 복제하는 방식과 매번 WAN을 건너 읽는 방식 사이에서, Hub에 원본을 하나 두고 Spoke의 로컬 캐시를 사용하는 구조가 어떤 역할을 하는지 설명할 수 있도록 한 장으로 정리했다.

이 문서는 아직 **설계** 상태다. AWS 계정, SageMaker HyperPod, Qumulo를 배포하거나 성능을 측정하지 않았다.

## 원문에서 확인한 구조

```text
Region B: Data Hub
┌───────────────────────┐
│ Qumulo Hub            │
│ Single source dataset │
└───────────┬───────────┘
            │ Cloud Data Fabric
            │ Inter-Region VPC Peering
            ▼
Region A: GPU Compute
┌───────────────────────┐
│ Qumulo Spoke          │
│ Local NVMe cache      │
└───────────┬───────────┘
            │ NFS, TCP 2049
            ▼
┌───────────────────────┐
│ SageMaker HyperPod    │
│ GPU training cluster  │
└───────────────────────┘
```

원문에서는 Hub가 원본 데이터 한 벌을 보관하고, Spoke가 같은 namespace를 제공하면서 필요한 블록을 가져와 로컬 NVMe에 캐시한다. HyperPod 노드는 원격 Hub가 아니라 같은 Region의 Spoke를 NFS로 마운트한다.

## 내가 답하려던 세 가지 질문

### 왜 데이터를 Region마다 전부 복제하지 않는가?

대규모 학습 데이터는 복제 시간, 저장 비용, 동기화 작업이 크다. 원본을 한 벌로 유지하면 데이터 오케스트레이션과 중복 저장을 줄일 수 있다. 대신 Hub 장애, Region 간 연결, 데이터 주권과 복구 계획은 별도로 설계해야 한다.

### 왜 Spoke 캐시가 필요한가?

GPU 데이터 로더가 매번 Region 간 RTT를 기다리면 WAN 지연이 학습 경로에 계속 들어온다. 로컬 캐시는 반복되거나 예측 가능한 읽기를 가까운 NVMe에서 처리해 WAN을 매 요청의 Critical Path에서 빼는 역할을 한다. 첫 실행의 Cache Warm-up 비용은 남는다.

### 왜 Network가 중요한가?

GPU가 데이터를 기다리는 시간에는 비싼 Compute가 놀게 된다. 따라서 평균 대역폭만 볼 수 없다. Region 간 RTT, NFS 처리량, Cache Hit Rate, 초기 100~150 Batch의 Warm-up, GPU Utilization을 함께 봐야 한다. VPC Peering Route와 Security Group에서 필요한 NFS TCP 2049만 허용하는 것도 데이터 경로의 일부다.

## 기사 수치와 내 상태 구분

AWS 글은 60 ms Region 간 지연 환경에서 Cold Cache가 초기 100~150 Batch 동안 느려진 뒤 Hub 수준 처리량으로 수렴했고, Warm Cache에서는 94~96%의 Cache Hit Rate와 115~116 samples/sec를 기록했다고 설명한다. 이 값은 **AWS와 Qumulo가 기사 환경에서 측정한 결과**이며 내 실습 결과가 아니다.

내가 직접 확인한 것은 원문 구조와 구성 요소의 관계뿐이다. 아래 항목은 아직 실행하지 않았다.

- 두 AWS Region의 VPC Peering과 Route Table
- Qumulo Hub·Spoke 및 Cloud Data Fabric
- NFS Mount와 Security Group TCP 2049
- SageMaker HyperPod GPU Cluster
- Cache Hit Rate, RTT, Throughput, GPU Utilization과 비용

## 실제 검증으로 바꾸는 순서

1. 비용 제한과 정리 절차를 먼저 정하고 두 Region의 테스트 VPC를 만든다.
2. VPC Peering, 양방향 Route, 최소 Security Group 규칙을 확인한다.
3. 작은 합성 Dataset으로 Hub와 Spoke namespace의 일치 여부를 확인한다.
4. Cold Cache와 Warm Cache를 나눠 RTT, Read Throughput, Cache Hit Rate를 수집한다.
5. GPU 대신 작은 CPU Reader부터 사용하고, 비용 승인을 받은 뒤에만 HyperPod로 확장한다.
6. 자원을 삭제하고 실행 로그와 비용만 정제해 증적으로 남긴다.
