# ADR-001: Polyglot DevSecOps & Azure PaaS Microservices Architecture

- **Status:** Accepted
- **Date:** 2026-11-19
- **Deciders:** Platform Engineering, DevSecOps & Cloud Architecture

## Context

We are building a production-grade polyglot microservices platform on Azure Kubernetes Service (AKS) that requires strict software supply-chain security, zero-trust network isolation, predictable FinOps governance, and resilient progressive delivery across `dev`, `uat`, and `prod` environments.

## Decisions

### 1. Decoupled CI/CD with Immutable `@sha256` Digests
- **CI (`ci-microservices.yml` / `reusable-service-ci.yml`)** builds, scans, signs, and pushes container images to Azure Container Registry (ACR), outputting immutable `@sha256` digests.
- **CD (`cd-progressive-deploy.yml`)** is decoupled and triggered via `workflow_dispatch` with `service_name`, `image_tag` (immutable `@sha256` digest), and `promote_to_prod`.
- **Rationale:** Decoupling prevents unintended deployments on code push, guarantees artifact immutability across `dev -> uat -> prod`, and enables independent environment promotion with manual approval gates on `production`.

### 2. Polyglot .NET 8 + Python FastAPI on AKS
- Services are implemented in **.NET 8** (enterprise APIs/frontend) and **Python FastAPI** (data/ML-adjacent backend services), packaged into distroless/minimal containers and deployed via a shared parameterized Helm chart (`charts/microservice`) with environment-specific values (`values-dev.yaml`, `values-uat.yaml`, `values-prod.yaml`).
- **Rationale:** Teams can select the optimal runtime per domain while standardizing Kubernetes manifests, health probes (`/healthz`), resource quotas, and observability.

### 3. Azure PostgreSQL Flexible Server PaaS with Private DNS & Entra ID Auth
- Persistent relational state is offloaded from in-cluster stateful pods to **Azure Database for PostgreSQL Flexible Server** (PaaS).
- Connectivity is restricted to VNet-integrated **Private Endpoints / Private DNS Zones** with **Microsoft Entra ID (Workload Identity) authentication**, eliminating static database passwords and public internet exposure.
- **Rationale:** Reduces operational toil (automated backups, HA, patching) and enforces zero-trust identity-based database access.

### 4. Layered Defense-in-Depth (SAST / SCA / DAST / SBOM / Cosign + Kyverno)
- **SAST & SCA:** Static code analysis and dependency vulnerability scanning during CI, plus IaC scanning (`TFLint`, `tfsec`, `Checkov`) and FinOps cost estimation (`Infracost`) in `infra-finops-ci.yml`.
- **SBOM & Keyless Signing:** CycloneDX SBOM generation and **Cosign OIDC keyless signing** tied to GitHub Actions workflow identity (`token.actions.githubusercontent.com`).
- **DAST:** Automated **OWASP ZAP Baseline** scan against the `dev` deployment before promotion.
- **Admission Control:** **Kyverno `ClusterPolicy`** (`k8s/policies/kyverno-verify-signed-images.yaml`) enforces Cosign signature verification on all `*.azurecr.io/*` images before pods can start in AKS.

### 5. Automated Helm Atomic Rollback
- All Helm deployments use `helm upgrade --install --atomic --wait --timeout 5m` to automatically revert failed Kubernetes rollouts.
- In `deploy-prod`, the pipeline records the pre-deploy Helm revision, runs post-deploy `/healthz` smoke tests, and executes `helm rollback` automatically if post-deploy verification fails.

## Consequences

- **Positive:** End-to-end cryptographic provenance from commit to AKS pod, zero static cloud/DB secrets via OIDC & Entra ID, automated FinOps visibility on Terraform PRs, and rapid self-healing rollbacks.
- **Trade-offs:** Requires maintaining GitHub OIDC federated credentials, Kyverno webhook availability in AKS, and strict adherence to immutable `@sha256` image references.
