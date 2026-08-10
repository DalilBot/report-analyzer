# Dedicated 8.5 Report Remediation Prompt Pack — Single-Tenant (`PROMPT_SEQUENCE_85_SINGLE_TENANT_FIXES.md`)

This prompt pack contains **5 targeted developer prompts** engineered for **Google Antigravity Agentic IDE** to resolve the exact new defects identified in the 8.5/10 evaluation report: Paymob piastre heuristic undercharge bug, Paymob void Transaction ID fix, Bosta baseUrl/express-rate/Port Fuad bugs, ETA mock submission fallback & subscriber workflow bypass, and single-tenant infrastructure simplification. Zero older problems are included.

> [!IMPORTANT]
> **Single-Tenant Architecture**: This project uses **single-tenant** infrastructure. All multi-tenant provisioning, tenant isolation, and dynamic Caddy per-tenant routing complexity should be simplified to a clean single-tenant Docker Compose setup.

> [!IMPORTANT]
> **Subagent Directive**: Send these 5 prompts sequentially (Prompt 1 through Prompt 5) to your developer Antigravity instance. Every prompt explicitly instructs the agent to delegate research or sub-tasks to subagents (`invoke_subagent`).

---

## Part 1: Payment & Fulfillment Logic Fixes (Prompts 1–2)

---
### Developer Prompt 1: Fix Paymob Piastre Conversion Heuristic Undercharge Bug & Void Transaction ID in Workflow Compensation

```markdown
/goal

<TASK>
Remove the flawed `egpAmount > 5000` piastre heuristic in `paymob/client.ts` and fix the void compensation step in `paymob-payment-workflow.ts` to pass a live Transaction ID instead of an Order ID.
</TASK>

<SUBAGENT_DELEGATION_DIRECTIVE>
- Use `invoke_subagent` (Role: "Codebase Researcher", TypeName: "research") to inspect the Paymob piastre conversion function and the payment workflow void compensation step parameters.
</SUBAGENT_DELEGATION_DIRECTIVE>

<ANTIGRAVITY_SLASH_COMMANDS>
- /goal: Execute autonomously until Paymob piastre conversion is deterministic and void compensation passes live Transaction IDs.
- /learn: Persist Paymob currency conversion rules to .gemini/rules.
</ANTIGRAVITY_SLASH_COMMANDS>

<ANTIGRAVITY_WORKFLOW>
1. RESEARCH & INSPECTION PHASE:
   - View `apps/backend/src/modules/paymob/client.ts` (lines 135–143).
   - View `apps/backend/src/workflows/paymob-payment-workflow.ts` (line 71).

2. IMPLEMENTATION PHASE:
   - Target files: `apps/backend/src/modules/paymob/client.ts`, `apps/backend/src/workflows/paymob-payment-workflow.ts`
   - **`client.ts:L135-143` — Remove Heuristic**: Delete the `if (Number.isInteger(egpAmount) && egpAmount > 5000) return egpAmount;` heuristic entirely. This heuristic causes orders of 5,001 EGP to be interpreted as already in piastres (50.01 EGP), resulting in a 100x undercharge. Instead, always perform `Math.round(egpAmount * 100)` deterministically since Medusa always passes amounts in major currency units (EGP). Add a clear JSDoc comment explaining the conversion contract.
   - **`paymob-payment-workflow.ts:L71` — Fix Void ID**: Update the compensation step to pass the live Paymob `transactionId` (from the payment initiation step response) to `voidPaymobTransaction()` instead of `paymobOrderId`. The Paymob void API requires a Transaction ID, not an Order ID.

3. EMPIRICAL VERIFICATION & TESTING PHASE:
   - Run TypeScript check: `cd apps/backend && npx tsc --noEmit`
   - Run backend build verification: `cd apps/backend && npm run build`

4. PROCESS CLEANUP & LEARNING DIRECTIVE (CRITICAL):
   - Execute `/learn` to store Paymob currency conversion rules.
   - Terminate any running subagents, background dev servers, or processes before completing turn.
</ANTIGRAVITY_WORKFLOW>

<ACCEPTANCE_CRITERIA>
- [ ] Subagents delegated for Paymob conversion and workflow inspection.
- [ ] Zero heuristic-based piastre conversion logic in `client.ts` — deterministic `Math.round(egpAmount * 100)` only.
- [ ] Void compensation step passes live `transactionId` to Paymob void API.
- [ ] Backend build completes with exit code 0.
- [ ] All subagents and background tasks are cleanly terminated.
</ACCEPTANCE_CRITERIA>
```

---
### Developer Prompt 2: Fix Bosta `baseUrl` Passthrough, Express Rate Multiplier, & Port Fuad Governorate Mapping

```markdown
/goal

<TASK>
Pass `options.baseUrl` to `BostaClient` constructor in `bosta/service.ts`, differentiate `bosta-express` rates from `bosta-standard`, and fix Port Fuad ("بورفؤاد") governorate assignment from Alexandria (EG-03) to Port Said (EG-12).
</TASK>

<SUBAGENT_DELEGATION_DIRECTIVE>
- Delegate Bosta API base URL configuration, shipping option rate differentiation, and Egyptian governorate geographic mapping to a subagent via `invoke_subagent`.
</SUBAGENT_DELEGATION_DIRECTIVE>

<ANTIGRAVITY_SLASH_COMMANDS>
- /goal: Execute autonomously until Bosta client uses configured base URL, express rates differ from standard, and Port Fuad maps to Port Said.
- /learn: Persist Bosta service configuration and governorate mapping rules to .gemini/rules.
</ANTIGRAVITY_SLASH_COMMANDS>

<ANTIGRAVITY_WORKFLOW>
1. RESEARCH & INSPECTION PHASE:
   - View `apps/backend/src/modules/bosta/service.ts` (lines 82–83 and rate calculation section).
   - View `apps/backend/src/modules/bosta/location-mapper.ts` (search for "بورفؤاد" or "Port Fuad").

2. IMPLEMENTATION PHASE:
   - Target files: `apps/backend/src/modules/bosta/service.ts`, `apps/backend/src/modules/bosta/location-mapper.ts`
   - **`service.ts:L82-83` — Pass Base URL**: Forward `this.options_.baseUrl` (or `process.env.BOSTA_API_BASE_URL`) to the `BostaClient` constructor so the client targets the correct Bosta API environment (staging vs production).
   - **Express Rate Multiplier**: Apply a 1.5x or configurable multiplier to `bosta-express` shipping option rates so express and standard rates are differentiated. Currently both options return identical pricing.
   - **`location-mapper.ts` — Port Fuad Fix**: Move "بورفؤاد" (Port Fuad) from the Alexandria (EG-03) sub-district list to Port Said (EG-12) where it geographically belongs.

3. EMPIRICAL VERIFICATION & TESTING PHASE:
   - Run TypeScript check: `cd apps/backend && npx tsc --noEmit`
   - Run backend build verification: `cd apps/backend && npm run build`

4. PROCESS CLEANUP & LEARNING DIRECTIVE (CRITICAL):
   - Execute `/learn` to store Bosta service configuration rules.
   - Terminate any running subagents, background dev servers, or processes before completing turn.
</ANTIGRAVITY_WORKFLOW>

<ACCEPTANCE_CRITERIA>
- [ ] Subagents delegated for Bosta API configuration and governorate research.
- [ ] `BostaClient` receives `baseUrl` from service options.
- [ ] `bosta-express` applies rate multiplier differentiating from `bosta-standard`.
- [ ] Port Fuad ("بورفؤاد") mapped to Port Said (EG-12) instead of Alexandria (EG-03).
- [ ] Backend build completes with exit code 0.
- [ ] All subagents and background tasks are cleanly terminated.
</ACCEPTANCE_CRITERIA>
```

---

## Part 2: ETA Tax Compliance Fix (Prompt 3)

---
### Developer Prompt 3: Throw on Missing ETA Credentials in Production & Route Subscriber Through `submitEtaTaxReceiptWorkflow`

```markdown
/goal

<TASK>
Replace mock success fallback in `eta-tax/client.ts` with a production exception when ETA credentials are missing, and update `order-placed-eta.ts` to invoke the `submitEtaTaxReceiptWorkflow` instead of calling service methods directly.
</TASK>

<SUBAGENT_DELEGATION_DIRECTIVE>
- Use `invoke_subagent` to inspect ETA client credential guards and the subscriber-to-workflow invocation pattern.
</SUBAGENT_DELEGATION_DIRECTIVE>

<ANTIGRAVITY_SLASH_COMMANDS>
- /goal: Execute autonomously until ETA client throws on missing production credentials and the subscriber routes through the defined workflow.
- /learn: Persist ETA credential enforcement and subscriber-workflow routing rules to .gemini/rules.
</ANTIGRAVITY_SLASH_COMMANDS>

<ANTIGRAVITY_WORKFLOW>
1. RESEARCH & INSPECTION PHASE:
   - View `apps/backend/src/modules/eta-tax/client.ts` (lines 142–152).
   - View `apps/backend/src/subscribers/order-placed-eta.ts` (lines 210–240).
   - View `apps/backend/src/workflows/eta-tax-workflow.ts`.

2. IMPLEMENTATION PHASE:
   - Target files: `apps/backend/src/modules/eta-tax/client.ts`, `apps/backend/src/subscribers/order-placed-eta.ts`
   - **`client.ts:L142-152` — Remove Mock Fallback**: When `ETA_CLIENT_ID` or `ETA_CLIENT_SECRET` are missing in production (`NODE_ENV === "production"`), throw an explicit `Error("ETA API credentials (ETA_CLIENT_ID, ETA_CLIENT_SECRET) are required in production")` instead of silently returning a mock success response (`MOCK_SUB_...`). In development, log a warning and return a clearly labeled dev-only mock.
   - **`order-placed-eta.ts:L210-240` — Use Workflow**: Replace direct `etaTaxModuleService.submitAndAuditReceipt(...)` calls with `submitEtaTaxReceiptWorkflow.run({ input: { orderId, items, buyer } })` to leverage the defined workflow's compensation handlers, retry logic, and transactional guarantees.

3. EMPIRICAL VERIFICATION & TESTING PHASE:
   - Run TypeScript check: `cd apps/backend && npx tsc --noEmit`
   - Run backend build verification: `cd apps/backend && npm run build`

4. PROCESS CLEANUP & LEARNING DIRECTIVE (CRITICAL):
   - Execute `/learn` to store ETA credential enforcement rules.
   - Terminate any running subagents, background dev servers, or processes before completing turn.
</ANTIGRAVITY_WORKFLOW>

<ACCEPTANCE_CRITERIA>
- [ ] Subagents delegated for ETA client and subscriber inspection.
- [ ] `client.ts` throws explicit error in production when ETA credentials are missing.
- [ ] `order-placed-eta.ts` invokes `submitEtaTaxReceiptWorkflow` instead of calling service methods directly.
- [ ] Backend build completes with exit code 0.
- [ ] All subagents and background tasks are cleanly terminated.
</ACCEPTANCE_CRITERIA>
```

---

## Part 3: Single-Tenant Infrastructure Simplification (Prompts 4–5)

---
### Developer Prompt 4: Simplify Docker Compose to Single-Tenant, Fix Environment Variable Names, & Add `.dockerignore`

```markdown
/goal

<TASK>
Simplify `docker-compose.tenant.yml` to a clean **single-tenant** Docker Compose setup, align storefront environment variable names, and create a root `.dockerignore` file. This project is SINGLE-TENANT — remove all multi-tenant provisioning complexity.
</TASK>

<SUBAGENT_DELEGATION_DIRECTIVE>
- Use `invoke_subagent` to inspect Docker Compose environment variable references and Dockerfile build contexts for single-tenant alignment.
</SUBAGENT_DELEGATION_DIRECTIVE>

<ANTIGRAVITY_SLASH_COMMANDS>
- /goal: Execute autonomously until Docker Compose runs a clean single-tenant stack with correct environment variable names.
- /learn: Persist single-tenant Docker configuration rules to .gemini/rules.
</ANTIGRAVITY_SLASH_COMMANDS>

<ANTIGRAVITY_WORKFLOW>
1. RESEARCH & INSPECTION PHASE:
   - View `infrastructure/docker/docker-compose.tenant.yml` (line 158 and full file).
   - View `infrastructure/scripts/provision-tenant.sh` (line 101 and `.env` output section).
   - Check for `.dockerignore` in the repository root.

2. IMPLEMENTATION PHASE:
   - Target files: `infrastructure/docker/docker-compose.tenant.yml`, `infrastructure/docker/docker-compose.yml` (create if needed), `.dockerignore`
   - **Rename / Simplify Compose File**: Rename or create a primary `docker-compose.yml` (or simplify `docker-compose.tenant.yml`) for single-tenant deployment. Remove multi-tenant `${TENANT_ID}` templating, dynamic port offsets, and tenant-scoped volume naming.
   - **Fix Environment Variable Mismatch** (`docker-compose.tenant.yml:L158`): Align the storefront service's backend URL variable — use `NEXT_PUBLIC_MEDUSA_BACKEND_URL` consistently (matching what `.env` and `provision-tenant.sh` output) instead of `TENANT_PUBLIC_BACKEND_URL`.
   - **Create `.dockerignore`**: Add a root `.dockerignore` excluding `node_modules/`, `.git/`, `dist/`, `.next/`, `*.log`, `.env*`, and IDE/editor files to reduce Docker build context size and prevent secret leakage.
   - **Redis Sentinel**: Since this is single-tenant, simplify to a single Redis instance (remove 3-node Sentinel quorum complexity) unless the user explicitly needs HA.

3. EMPIRICAL VERIFICATION & TESTING PHASE:
   - Run Docker compose config validation: `docker compose -f infrastructure/docker/docker-compose.tenant.yml config`

4. PROCESS CLEANUP & LEARNING DIRECTIVE (CRITICAL):
   - Execute `/learn` to store single-tenant Docker configuration rules.
   - Terminate any active subagents or background tasks before completing turn.
</ANTIGRAVITY_WORKFLOW>

<ACCEPTANCE_CRITERIA>
- [ ] Subagents delegated for Docker Compose environment variable inspection.
- [ ] Docker Compose simplified for single-tenant deployment (no `${TENANT_ID}` templating).
- [ ] Storefront uses `NEXT_PUBLIC_MEDUSA_BACKEND_URL` consistently.
- [ ] Root `.dockerignore` created excluding `node_modules`, `.git`, `.next`, `.env*`.
- [ ] Redis configuration simplified to single instance.
- [ ] Docker Compose config passes validation.
- [ ] All subagents and background tasks are cleanly terminated.
</ACCEPTANCE_CRITERIA>
```

---
### Developer Prompt 5: Fix Provisioning Script Build Context for Single-Tenant & Simplify Deployment

```markdown
/goal

<TASK>
Simplify `provision-tenant.sh` for **single-tenant** deployment — fix Docker build context so source code is available during `docker compose build`, and remove multi-tenant tenant directory copying logic.
</TASK>

<SUBAGENT_DELEGATION_DIRECTIVE>
- Use `invoke_subagent` to inspect the provisioning script's Docker build context setup and multi-tenant removal points.
</SUBAGENT_DELEGATION_DIRECTIVE>

<ANTIGRAVITY_SLASH_COMMANDS>
- /goal: Execute autonomously until provisioning script builds containers from repository root with full source code context.
- /learn: Persist single-tenant provisioning rules to .gemini/rules.
</ANTIGRAVITY_SLASH_COMMANDS>

<ANTIGRAVITY_WORKFLOW>
1. RESEARCH & INSPECTION PHASE:
   - View `infrastructure/scripts/provision-tenant.sh` (line 101 and full file).

2. IMPLEMENTATION PHASE:
   - Target file: `infrastructure/scripts/provision-tenant.sh`
   - **Fix Build Context** (`provision-tenant.sh:L101`): Remove the logic that copies only compose files into a tenant directory without source code. Instead, run `docker compose build` from the repository root so Dockerfiles have access to `apps/backend/`, `apps/storefront/`, and `packages/shared-types/`.
   - **Simplify for Single-Tenant**: Remove tenant directory creation (`/tenants/${TENANT_ID}/`), tenant ID parameterization, and multi-tenant isolation logic. The script should provision a single production instance directly.
   - **Keep Secret Generation**: Retain the cryptographic secret generation (`openssl rand -base64 32`) and idempotent `.env` sourcing — these are valuable for single-tenant too.
   - **Keep Database Readiness Polling**: Retain `pg_isready` polling and migration commands.

3. EMPIRICAL VERIFICATION & TESTING PHASE:
   - Run bash syntax check: `bash -n infrastructure/scripts/provision-tenant.sh`

4. PROCESS CLEANUP & LEARNING DIRECTIVE (CRITICAL):
   - Terminate any active subagents or background tasks before completing turn.
</ANTIGRAVITY_WORKFLOW>

<ACCEPTANCE_CRITERIA>
- [ ] Subagents delegated for provisioning script inspection.
- [ ] `docker compose build` runs from repository root with full source code context.
- [ ] Multi-tenant tenant directory and `${TENANT_ID}` logic removed.
- [ ] Cryptographic secret generation and `pg_isready` polling retained.
- [ ] Script passes `bash -n` syntax check cleanly.
- [ ] All subagents and background tasks are cleanly terminated.
</ACCEPTANCE_CRITERIA>
```
