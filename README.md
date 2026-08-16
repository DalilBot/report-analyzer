# Dedicated 9.0 Report Remediation Prompt Pack (`PROMPT_SEQUENCE_90_FINAL_REPORT_FIXES.md`)

This prompt pack contains **5 targeted developer prompts** engineered for **Google Antigravity Agentic IDE** to resolve the exact new defects identified in the latest 9.0/10 evaluation report: Redis key casing mismatch in Bosta prewarm job, hardcoded Bosta COD shipment type, ETA fallback EGS item code TRN calculation, HSM signer proxy URL option fallback, worker DLQ error handling bypass, top-level custom module registration for `eta-tax`, BullMQ worker bootstrapping loader, and storefront shared package dependency link. Zero older problems are included.

> [!IMPORTANT]
> **Subagent Directive**: Send these 5 prompts sequentially (Prompt 1 through Prompt 5) to your developer Antigravity instance. Every prompt explicitly instructs the agent to delegate research or sub-tasks to subagents (`invoke_subagent`).

---

## Part 1: High Priority Functional & Regulatory Fixes (Prompts 1–2)

---
### Developer Prompt 1: Fix ETA Fallback EGS Item Code TRN & HSM Proxy URL Constructor Option Fallback

```markdown
/goal

<TASK>
Update `apps/backend/src/modules/eta-tax/payload-builder.ts:L222` to use the issuer's actual Tax Registration Number instead of hardcoded `EG-100200300`, and fix `apps/backend/src/modules/eta-tax/hsm-signer.ts:L42` to check `this.hsmProxyUrl` instead of ignoring constructor options.
</TASK>

<SUBAGENT_DELEGATION_DIRECTIVE>
- Use `invoke_subagent` (Role: "Codebase Researcher", TypeName: "research") to inspect `payload-builder.ts` line 222 and `hsm-signer.ts` line 42 to verify current property references.
</SUBAGENT_DELEGATION_DIRECTIVE>

<ANTIGRAVITY_SLASH_COMMANDS>
- /goal: Execute autonomously until EGS item codes use dynamic issuer TRNs and HSM signer checks constructor instance properties.
- /learn: Persist ETA tax payload EGS code formatting and HSM configuration rules to .gemini/rules.
</ANTIGRAVITY_SLASH_COMMANDS>

<ANTIGRAVITY_WORKFLOW>
1. RESEARCH & INSPECTION PHASE:
   - View `apps/backend/src/modules/eta-tax/payload-builder.ts` (lines 215–230).
   - View `apps/backend/src/modules/eta-tax/hsm-signer.ts` (lines 35–50).

2. IMPLEMENTATION PHASE:
   - Target files: `apps/backend/src/modules/eta-tax/payload-builder.ts`, `apps/backend/src/modules/eta-tax/hsm-signer.ts`
   - **Fix Fallback EGS Item Code** (`payload-builder.ts:L222`):
     ```typescript
     // BEFORE:
     itemCode: item.itemCode || `EG-100200300-${item.sku || index + 1}`,

     // AFTER:
     itemCode: item.itemCode || `EG-${defaultIssuer.taxRegistrationNumber}-${item.sku || index + 1}`,
     ```
     *Rationale*: Fallback EGS item codes must use the merchant's actual Tax Registration Number (`defaultIssuer.taxRegistrationNumber`), not a hardcoded dummy TRN (`100200300`), to pass Egyptian Tax Authority validation.

   - **Fix HSM Proxy URL Guard** (`hsm-signer.ts:L42`):
     ```typescript
     // BEFORE:
     if (!this.enabled || !process.env.ETA_HSM_PROXY_URL) {

     // AFTER:
     if (!this.enabled || !this.hsmProxyUrl) {
     ```
     *Rationale*: Check the resolved instance property `this.hsmProxyUrl` (which receives constructor options from module config) instead of bypassing constructor options when `process.env.ETA_HSM_PROXY_URL` is omitted.

3. EMPIRICAL VERIFICATION & TESTING PHASE:
   - Run TypeScript check: `cd apps/backend && npx tsc --noEmit`
   - Run backend build verification: `cd apps/backend && npm run build`

4. PROCESS CLEANUP & LEARNING DIRECTIVE (CRITICAL):
   - Execute `/learn` to store ETA tax configuration rules.
   - Terminate any running subagents, background dev servers, or processes before completing turn.
</ANTIGRAVITY_WORKFLOW>

<ACCEPTANCE_CRITERIA>
- [ ] Subagents delegated for ETA payload builder and HSM signer code inspection.
- [ ] `payload-builder.ts` constructs fallback EGS item codes using `defaultIssuer.taxRegistrationNumber`.
- [ ] `hsm-signer.ts` checks `this.hsmProxyUrl` instead of relying solely on `process.env.ETA_HSM_PROXY_URL`.
- [ ] Backend typecheck passes with 0 errors (`tsc --noEmit`).
- [ ] Backend build completes with exit code 0.
- [ ] All subagents and background tasks are cleanly terminated.
</ACCEPTANCE_CRITERIA>
```

---
### Developer Prompt 2: Fix Bosta Prewarm Redis Key Casing Mismatch & Dynamic COD Shipment Type

```markdown
/goal

<TASK>
Fix Redis key casing in `apps/backend/src/jobs/prewarm-bosta-rates.ts:L56` from uppercase to lowercase to match `service.ts`, and update `apps/backend/src/modules/bosta/service.ts:L254` to set shipment type dynamically based on COD amount.
</TASK>

<SUBAGENT_DELEGATION_DIRECTIVE>
- Use `invoke_subagent` to inspect `prewarm-bosta-rates.ts` line 56 and `bosta/service.ts` line 254 side-by-side to verify exact Redis key strings and shipment type fields.
</SUBAGENT_DELEGATION_DIRECTIVE>

<ANTIGRAVITY_SLASH_COMMANDS>
- /goal: Execute autonomously until prewarm Redis keys match service cache reads and Bosta shipment type is dynamic.
- /learn: Persist Redis cache key casing and Bosta shipment type rules to .gemini/rules.
</ANTIGRAVITY_SLASH_COMMANDS>

<ANTIGRAVITY_WORKFLOW>
1. RESEARCH & INSPECTION PHASE:
   - View `apps/backend/src/jobs/prewarm-bosta-rates.ts` (lines 50–65).
   - View `apps/backend/src/modules/bosta/service.ts` (lines 170–185 for cache read, and lines 245–260 for shipment creation).

2. IMPLEMENTATION PHASE:
   - Target files: `apps/backend/src/jobs/prewarm-bosta-rates.ts`, `apps/backend/src/modules/bosta/service.ts`
   - **Fix Redis Key Casing** (`prewarm-bosta-rates.ts:L56`):
     ```typescript
     // BEFORE:
     const redisKey = `BOSTA_RATE_${option.id}_${gov.cityId}_W${weightKey}`;

     // AFTER:
     const redisKey = `bosta_rate_${option.id}_${gov.cityId}_W${weightKey}`;
     ```
     *Rationale*: `BostaFulfillmentProviderService.calculatePrice()` in `service.ts:L178` reads lowercase keys (`bosta_rate_...`). Writing uppercase keys in the prewarm job causes 100% cache misses due to Redis key case sensitivity.

   - **Fix Dynamic COD Shipment Type** (`bosta/service.ts:L254-256`):
     ```typescript
     // BEFORE:
     type: 10,

     // AFTER:
     type: Number(codAmount) > 0 ? 10 : 1,
     ```
     *Rationale*: Bosta API type `10` is Cash Collection (COD). Prepaid orders (credit card, mobile wallet) must use type `1` (Standard Delivery). Hardcoding type `10` forces Bosta couriers to collect cash on already paid orders.

3. EMPIRICAL VERIFICATION & TESTING PHASE:
   - Run TypeScript check: `cd apps/backend && npx tsc --noEmit`
   - Run backend build verification: `cd apps/backend && npm run build`

4. PROCESS CLEANUP & LEARNING DIRECTIVE (CRITICAL):
   - Execute `/learn` to store Bosta logistics configuration rules.
   - Terminate any running subagents, background dev servers, or processes before completing turn.
</ANTIGRAVITY_WORKFLOW>

<ACCEPTANCE_CRITERIA>
- [ ] Subagents delegated for Bosta prewarm job and service inspection.
- [ ] `prewarm-bosta-rates.ts` writes lowercase `bosta_rate_` Redis keys matching `service.ts` reads.
- [ ] `bosta/service.ts` sets `type: Number(codAmount) > 0 ? 10 : 1` dynamically.
- [ ] Backend typecheck passes with 0 errors (`tsc --noEmit`).
- [ ] Backend build completes with exit code 0.
- [ ] All subagents and background tasks are cleanly terminated.
</ACCEPTANCE_CRITERIA>
```

---

## Part 2: Structural Refactoring & Module Architecture (Prompts 3–4)

---
### Developer Prompt 3: Register `eta-tax` as Top-Level Custom Module & Fix Background Queue Worker DLQ Retry Bypass

```markdown
/goal

<TASK>
Register `eta-tax` as a standalone top-level module in `apps/backend/medusa-config.ts` so `container.resolve("etaTax")` is globally available, and update `apps/backend/src/jobs/background-queue.ts:L145-151` to re-invoke `handleEtaSubmissionFailure()` on worker catch.
</TASK>

<SUBAGENT_DELEGATION_DIRECTIVE>
- Use `invoke_subagent` to inspect `medusa-config.ts` module registrations and `background-queue.ts` worker catch blocks.
</SUBAGENT_DELEGATION_DIRECTIVE>

<ANTIGRAVITY_SLASH_COMMANDS>
- /goal: Execute autonomously until eta-tax is globally resolvable from container and worker failures update DLQ status.
- /learn: Persist Medusa v2 top-level module registration and worker error handling rules to .gemini/rules.
</ANTIGRAVITY_SLASH_COMMANDS>

<ANTIGRAVITY_WORKFLOW>
1. RESEARCH & INSPECTION PHASE:
   - View `apps/backend/medusa-config.ts` (lines 95–120).
   - View `apps/backend/src/modules/eta-tax/index.ts`.
   - View `apps/backend/src/jobs/background-queue.ts` (lines 140–155).

2. IMPLEMENTATION PHASE:
   - Target files: `apps/backend/medusa-config.ts`, `apps/backend/src/jobs/background-queue.ts`
   - **Top-Level Custom Module Registration** (`medusa-config.ts`):
     Register `eta-tax` in the `modules: [...]` array as a top-level module (matching the `gemini-ai` registration pattern) alongside its provider registration under `@medusajs/medusa/tax`:
     ```typescript
     {
       resolve: "./src/modules/eta-tax",
       options: {
         clientId: process.env.ETA_CLIENT_ID,
         clientSecret: process.env.ETA_CLIENT_SECRET,
         taxRegistrationNumber: process.env.ETA_TAX_REGISTRATION_NUMBER,
         hsmProxyUrl: process.env.ETA_HSM_PROXY_URL,
         environment: process.env.ETA_ENVIRONMENT || "preprod",
       },
     },
     ```
     *Rationale*: This enables `container.resolve("etaTax")` (or `container.resolve(ETA_TAX_MODULE)`) across all subscribers and workflows without needing brittle fallback strings.

   - **Worker DLQ Failure Handler Re-invocation** (`background-queue.ts:L145-151`):
     In the worker catch block for ETA jobs, ensure `handleEtaSubmissionFailure(job.data, error)` is explicitly called before re-throwing or moving to DLQ:
     ```typescript
     // AFTER:
     catch (error) {
       await handleEtaSubmissionFailure(job.data, error as Error);
       throw error;
     }
     ```
     *Rationale*: Currently, the worker catches errors without invoking `handleEtaSubmissionFailure()`, bypassing `FAILED_DLQ` status updates in the audit log and suppressing webhook alert dispatches.

3. EMPIRICAL VERIFICATION & TESTING PHASE:
   - Run TypeScript check: `cd apps/backend && npx tsc --noEmit`
   - Run backend build verification: `cd apps/backend && npm run build`

4. PROCESS CLEANUP & LEARNING DIRECTIVE (CRITICAL):
   - Execute `/learn` to store module registration and DLQ rules.
   - Terminate any running subagents, background dev servers, or processes before completing turn.
</ANTIGRAVITY_WORKFLOW>

<ACCEPTANCE_CRITERIA>
- [ ] Subagents delegated for module config and background queue code inspection.
- [ ] `eta-tax` registered in `medusa-config.ts` `modules: [...]` array.
- [ ] Worker catch block in `background-queue.ts` invokes `handleEtaSubmissionFailure()`.
- [ ] Backend typecheck passes with 0 errors (`tsc --noEmit`).
- [ ] Backend build completes with exit code 0.
- [ ] All subagents and background tasks are cleanly terminated.
</ACCEPTANCE_CRITERIA>
```

---
### Developer Prompt 4: Bootstrap BullMQ Worker on Server Startup & Add Volumetric Weight Calculation to Bosta Service

```markdown
/goal

<TASK>
Add a Medusa loader to bootstrap `startWorker()` from `background-queue.ts` on server startup, and implement volumetric weight calculation (`(L × W × H) / 5000`) in `apps/backend/src/modules/bosta/service.ts`.
</TASK>

<SUBAGENT_DELEGATION_DIRECTIVE>
- Use `invoke_subagent` to inspect Medusa v2 loader conventions (`apps/backend/src/loaders/`) and Bosta weight calculation in `service.ts`.
</SUBAGENT_DELEGATION_DIRECTIVE>

<ANTIGRAVITY_SLASH_COMMANDS>
- /goal: Execute autonomously until background worker boots automatically on backend startup and Bosta calculates volumetric weight.
- /learn: Persist Medusa loader startup and volumetric weight calculation rules to .gemini/rules.
</ANTIGRAVITY_SLASH_COMMANDS>

<ANTIGRAVITY_WORKFLOW>
1. RESEARCH & INSPECTION PHASE:
   - Check `apps/backend/src/loaders/` (or create if missing).
   - View `apps/backend/src/jobs/background-queue.ts` (`startWorker` export).
   - View `apps/backend/src/modules/bosta/service.ts` (weight calculation methods).

2. IMPLEMENTATION PHASE:
   - Target files: `apps/backend/src/loaders/worker-loader.ts` (NEW), `apps/backend/src/modules/bosta/service.ts`
   - **BullMQ Worker Bootstrapping Loader** (`loaders/worker-loader.ts`):
     Create a Medusa loader that invokes `startWorker()` during backend initialization:
     ```typescript
     import { LoaderOptions } from "@medusajs/framework/types"
     import { startWorker } from "../jobs/background-queue"

     export default async function workerLoader({ container }: LoaderOptions) {
       console.log("[WorkerLoader] Bootstrapping background queue worker...")
       startWorker(container)
     }
     ```
     *Rationale*: Ensures background queue workers start automatically when `medusa start` boots the server, preventing jobs from sitting unprocessed in Redis.

   - **Volumetric Weight Calculation** (`bosta/service.ts`):
     Update rate calculation and shipment creation to compute chargeable weight as `Math.max(actualWeightKg, volumetricWeightKg)` where `volumetricWeightKg = (lengthCm * widthCm * heightCm) / 5000`:
     ```typescript
     const volumetricWeightKg = (dimensions.length * dimensions.width * dimensions.height) / 5000;
     const chargeableWeightKg = Math.max(actualWeightKg, volumetricWeightKg);
     ```
     *Rationale*: Aligns with Egyptian courier billing tiers (Bosta, Aramex) where bulky goods are billed based on volumetric weight when it exceeds actual physical weight.

3. EMPIRICAL VERIFICATION & TESTING PHASE:
   - Run TypeScript check: `cd apps/backend && npx tsc --noEmit`
   - Run backend build verification: `cd apps/backend && npm run build`

4. PROCESS CLEANUP & LEARNING DIRECTIVE (CRITICAL):
   - Execute `/learn` to store worker loader and volumetric weight rules.
   - Terminate any running subagents, background dev servers, or processes before completing turn.
</ANTIGRAVITY_WORKFLOW>

<ACCEPTANCE_CRITERIA>
- [ ] Subagents delegated for loader conventions and Bosta weight calculation inspection.
- [ ] `worker-loader.ts` created and registered to bootstrap `startWorker()` on server boot.
- [ ] `bosta/service.ts` computes `Math.max(actualWeight, volumetricWeight)` using 5000 divisor.
- [ ] Backend typecheck passes with 0 errors (`tsc --noEmit`).
- [ ] Backend build completes with exit code 0.
- [ ] All subagents and background tasks are cleanly terminated.
</ACCEPTANCE_CRITERIA>
```

---

## Part 3: Storefront & Infrastructure Cleanup (Prompt 5)

---
### Developer Prompt 5: Add Shared Types Dependency to Storefront & Prune Dev Dependencies in Docker Runner Stage

```markdown
/goal

<TASK>
Add `"@dtc/shared-types": "*"` to `apps/storefront/package.json` to eliminate duplicate interfaces, and add `RUN npm prune --omit=dev` to `infrastructure/docker/Dockerfile.backend` runner stage.
</TASK>

<SUBAGENT_DELEGATION_DIRECTIVE>
- Use `invoke_subagent` to inspect `apps/storefront/package.json` and `infrastructure/docker/Dockerfile.backend`.
</SUBAGENT_DELEGATION_DIRECTIVE>

<ANTIGRAVITY_SLASH_COMMANDS>
- /goal: Execute autonomously until storefront links shared-types workspace dependency and Dockerfile prunes dev dependencies.
- /learn: Persist workspace dependency and Docker multi-stage optimization rules to .gemini/rules.
</ANTIGRAVITY_SLASH_COMMANDS>

<ANTIGRAVITY_WORKFLOW>
1. RESEARCH & INSPECTION PHASE:
   - View `apps/storefront/package.json` (dependencies block).
   - View `infrastructure/docker/Dockerfile.backend` (runner stage).

2. IMPLEMENTATION PHASE:
   - Target files: `apps/storefront/package.json`, `infrastructure/docker/Dockerfile.backend`
   - **Storefront Shared Package Dependency Link** (`apps/storefront/package.json`):
     Add `@dtc/shared-types` using the npm workspace protocol:
     ```json
     "dependencies": {
       "@dtc/shared-types": "*",
       ...
     }
     ```
     *Rationale*: Eliminates duplicate governorate and phone utility interface declarations across apps by sharing the canonical types from `packages/shared-types`.

   - **Backend Docker Image Pruning** (`Dockerfile.backend`):
     Add a prune step before copying node modules into the final runner image:
     ```dockerfile
     # In builder / runner stage:
     RUN npm prune --omit=dev
     ```
     *Rationale*: Reduces production Docker image size by stripping dev dependencies (TypeScript, compilers, linters) from the runtime container.

3. EMPIRICAL VERIFICATION & TESTING PHASE:
   - Run shared-types build: `cd packages/shared-types && npm run build`
   - Run storefront typecheck: `cd apps/storefront && npx tsc --noEmit`
   - Run storefront build: `cd apps/storefront && npm run build`

4. PROCESS CLEANUP & LEARNING DIRECTIVE (CRITICAL):
   - Terminate any running subagents, background dev servers, or processes before completing turn.
</ANTIGRAVITY_WORKFLOW>

<ACCEPTANCE_CRITERIA>
- [ ] Subagents delegated for storefront package.json and Dockerfile inspection.
- [ ] `apps/storefront/package.json` includes `"@dtc/shared-types": "*"`.
- [ ] `Dockerfile.backend` includes `npm prune --omit=dev` in runner stage.
- [ ] All monorepo projects (`shared-types`, `apps/backend`, `apps/storefront`) pass typecheck and build cleanly with exit code 0.
- [ ] All subagents and background tasks are cleanly terminated.
</ACCEPTANCE_CRITERIA>
```
