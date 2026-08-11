# Dedicated 8.4 Report Remediation Prompt Pack (`PROMPT_SEQUENCE_84_FINAL_REPORT_FIXES.md`)

This prompt pack contains **5 targeted developer prompts** engineered for **Google Antigravity Agentic IDE** to resolve the exact new defects identified in the latest 8.4/10 evaluation report: the catastrophic `medusa-framework.d.ts` type override file, Gemini AI swallowed errors breaking retry semantics, Bosta shared-types code duplication / non-functional cache lock, ETA dummy phone fallback / inline self-test hacks / background queue direct instantiation, and Docker SSR networking / Redis password exposure / missing storefront error boundaries. Zero older problems are included.

> [!IMPORTANT]
> **Subagent Directive**: Send these 5 prompts sequentially (Prompt 1 through Prompt 5) to your developer Antigravity instance. Every prompt explicitly instructs the agent to delegate research or sub-tasks to subagents (`invoke_subagent`).

---

## Part 1: Type Safety & AI Error Propagation (Prompts 1–2)

---
### Developer Prompt 1: Delete `medusa-framework.d.ts` Type Override File, Fix Resulting Type Errors, & Complete `.env.template`

```markdown
/goal

<TASK>
Delete `apps/backend/src/types/medusa-framework.d.ts` which overrides every Medusa framework export with `any` (completely negating `strict: true`), fix all resulting TypeScript compilation errors with proper Medusa v2 types, and add missing keys to `.env.template`.
</TASK>

<SUBAGENT_DELEGATION_DIRECTIVE>
- Use `invoke_subagent` (Role: "Type Safety Researcher", TypeName: "research") to read `apps/backend/src/types/medusa-framework.d.ts` and catalog every type it declares as `any`.
- Use a second `invoke_subagent` to search the entire backend for imports from `@medusajs/framework` and `@medusajs/medusa` that will need proper type annotations after the `any` override is removed.
- Use a third `invoke_subagent` to compare `.env.template` against all `process.env.*` reads in `medusa-config.ts` and modules.
</SUBAGENT_DELEGATION_DIRECTIVE>

<ANTIGRAVITY_SLASH_COMMANDS>
- /goal: Execute autonomously until medusa-framework.d.ts is deleted, all type errors are resolved with proper Medusa v2 types, and .env.template is complete.
- /learn: Persist Medusa v2 type import rules to .gemini/rules.
</ANTIGRAVITY_SLASH_COMMANDS>

<ANTIGRAVITY_WORKFLOW>
1. RESEARCH & INSPECTION PHASE:
   - View `apps/backend/src/types/medusa-framework.d.ts` (full file — understand all 40+ type overrides).
   - View `apps/backend/tsconfig.json` (confirm `strict: true` is enabled).
   - View `apps/backend/.env.template` (check for missing keys).
   - View `apps/backend/medusa-config.ts` (list all env vars read).

2. IMPLEMENTATION PHASE:
   - Target files: `apps/backend/src/types/medusa-framework.d.ts` (DELETE), multiple backend source files, `apps/backend/.env.template`
   - **DELETE `medusa-framework.d.ts`**: This file declares `MedusaContainer`, `AbstractPaymentProvider`, `createStep`, `createWorkflow`, `IPaymentModuleService`, and 40+ other Medusa framework types as `any`. This completely negates `strict: true` and masks runtime type errors throughout the codebase. DELETE IT ENTIRELY.
   - **Fix Type Errors**: After deletion, run `npx tsc --noEmit` and fix every resulting error:
     - Import types from their proper Medusa v2 packages (`@medusajs/framework/types`, `@medusajs/medusa/types`, `@medusajs/framework/workflows-sdk`)
     - Replace `(service as any).method()` calls with properly typed interfaces (`IPaymentModuleService`, `IFulfillmentModuleService`, etc.)
     - Add proper type annotations to container resolution calls
   - **Complete `.env.template`**: Add all missing keys that `medusa-config.ts` and modules actually read: `GEMINI_API_KEY`, `STORE_CORS`, `ADMIN_CORS`, `AUTH_CORS`, `PAYMOB_API_KEY`, `PAYMOB_HMAC_SECRET`, `BOSTA_API_KEY`, `ETA_CLIENT_ID`, `ETA_CLIENT_SECRET`, `ETA_HSM_PRIMARY_URL`, plus any others found during research.

3. EMPIRICAL VERIFICATION & TESTING PHASE:
   - Run TypeScript check: `cd apps/backend && npx tsc --noEmit`
   - Run backend build verification: `cd apps/backend && npm run build`
   - Confirm ZERO TypeScript errors without the `any` override file.

4. PROCESS CLEANUP & LEARNING DIRECTIVE (CRITICAL):
   - Execute `/learn` to store: "Never create ambient type declaration files that override framework types with `any`. Always import Medusa v2 types from their canonical packages."
   - Terminate any running subagents, background dev servers, or processes before completing turn.
</ANTIGRAVITY_WORKFLOW>

<ACCEPTANCE_CRITERIA>
- [ ] 3 subagents delegated for type catalog, import analysis, and env template audit.
- [ ] `medusa-framework.d.ts` DELETED from the codebase.
- [ ] Backend compiles with `strict: true` and zero errors — no `any` override crutch.
- [ ] `.env.template` includes every environment variable read by the application.
- [ ] Backend build completes with exit code 0.
- [ ] All subagents and background tasks are cleanly terminated.
</ACCEPTANCE_CRITERIA>
```

---
### Developer Prompt 2: Fix Gemini AI Client Error Propagation (Re-throw Transient Errors), Fix DI Resolution Anti-Pattern, & Use Actual Token Count

```markdown
/goal

<TASK>
Modify `gemini-ai/client.ts:L121-L133` to re-throw transient errors (timeouts, 429s, 5xx) so BullMQ retries work, return fallback only for non-retryable errors. Fix the DI resolution anti-pattern in the admin API route. Use `usageMetadata.totalTokenCount` instead of `length / 4` for token estimation.
</TASK>

<SUBAGENT_DELEGATION_DIRECTIVE>
- Use `invoke_subagent` to inspect the Gemini AI client catch block, API route DI resolution, and Gemini API response metadata structure.
</SUBAGENT_DELEGATION_DIRECTIVE>

<ANTIGRAVITY_SLASH_COMMANDS>
- /goal: Execute autonomously until Gemini client re-throws transient errors, DI resolves the correct service type, and token count uses API metadata.
- /learn: Persist Gemini error propagation and DI resolution rules to .gemini/rules.
</ANTIGRAVITY_SLASH_COMMANDS>

<ANTIGRAVITY_WORKFLOW>
1. RESEARCH & INSPECTION PHASE:
   - View `apps/backend/src/modules/gemini-ai/client.ts` (lines 121–133 catch block).
   - View the admin API route that resolves the Gemini service (check type mismatch).
   - View `apps/backend/src/jobs/ai-copywriter-worker.ts` (token estimation logic).

2. IMPLEMENTATION PHASE:
   - Target files: `apps/backend/src/modules/gemini-ai/client.ts`, admin API route for AI, `apps/backend/src/jobs/ai-copywriter-worker.ts`
   - **Error Propagation** (`client.ts:L121-133`): Refactor the catch block to distinguish transient vs permanent errors:
     - **Re-throw** on: `AbortError` (timeout), HTTP 429 (rate limit), HTTP 5xx (server error) — these should bubble up to the worker so BullMQ's exponential backoff retry kicks in.
     - **Return fallback template** only on: HTTP 4xx client errors (bad request, auth failure), malformed JSON responses, prompt safety blocks — these are non-retryable.
     - Log the error classification (`retryable` vs `permanent`) with the error details.
   - **DI Resolution Fix** (admin API route): Change the container resolution type from `GeminiAIStudioClient` to `GeminiAiModuleService` (the actual service registered in the container). The current code works by structural typing accident.
   - **Actual Token Count** (`ai-copywriter-worker.ts`): Replace `Math.ceil(responseText.length / 4)` token estimation with `response.usageMetadata?.totalTokenCount ?? Math.ceil(responseText.length / 4)` — read the actual token count from the Gemini API response, falling back to estimation only when metadata is unavailable.

3. EMPIRICAL VERIFICATION & TESTING PHASE:
   - Run TypeScript check: `cd apps/backend && npx tsc --noEmit`
   - Run backend build verification: `cd apps/backend && npm run build`

4. PROCESS CLEANUP & LEARNING DIRECTIVE (CRITICAL):
   - Execute `/learn` to store Gemini error propagation rules.
   - Terminate any running subagents, background dev servers, or processes before completing turn.
</ANTIGRAVITY_WORKFLOW>

<ACCEPTANCE_CRITERIA>
- [ ] Subagents delegated for Gemini client error handling and DI inspection.
- [ ] Transient errors (timeout, 429, 5xx) are re-thrown — BullMQ retry semantics restored.
- [ ] Non-retryable errors (4xx, safety blocks) return fallback template.
- [ ] Admin API route resolves `GeminiAiModuleService` (not `GeminiAIStudioClient`).
- [ ] Token count reads `usageMetadata.totalTokenCount` from API response.
- [ ] Backend build completes with exit code 0.
- [ ] All subagents and background tasks are cleanly terminated.
</ACCEPTANCE_CRITERIA>
```

---

## Part 2: Module Code Quality & Compliance (Prompts 3–4)

---
### Developer Prompt 3: Deduplicate Bosta Phone/Governorate Utilities with `@dtc/shared-types`, Fix Non-Functional `acquireLock`, & Unblock Workflow Compensation

```markdown
/goal

<TASK>
Replace duplicated `formatEgyptianPhone` and governorate mapping in `bosta/service.ts` with imports from `@dtc/shared-types`, fix the non-functional `acquireLock` that casts `ICacheService` to `any` for a non-existent `setNx` method, and replace blocking `sleep()` in Bosta workflow compensation with framework retry config.
</TASK>

<SUBAGENT_DELEGATION_DIRECTIVE>
- Use `invoke_subagent` to compare `bosta/service.ts` phone formatting with `@dtc/shared-types/phone-utils.ts`, inspect the `acquireLock` implementation, and research Medusa v2 workflow step `retry` configuration.
</SUBAGENT_DELEGATION_DIRECTIVE>

<ANTIGRAVITY_SLASH_COMMANDS>
- /goal: Execute autonomously until Bosta uses shared-types utilities, cache lock is functional, and workflow compensation doesn't block.
- /learn: Persist shared-types import and workflow retry rules to .gemini/rules.
</ANTIGRAVITY_SLASH_COMMANDS>

<ANTIGRAVITY_WORKFLOW>
1. RESEARCH & INSPECTION PHASE:
   - View `apps/backend/src/modules/bosta/service.ts` (lines 38–62 for `formatEgyptianPhone`, and the `acquireLock` method).
   - View `packages/shared-types/src/phone-utils.ts` (the canonical phone normalization).
   - View `apps/backend/src/workflows/bosta-fulfillment-workflow.ts` (compensation handler with `sleep()`).

2. IMPLEMENTATION PHASE:
   - Target files: `apps/backend/src/modules/bosta/service.ts`, `apps/backend/src/workflows/bosta-fulfillment-workflow.ts`
   - **Deduplication**: Replace the local `formatEgyptianPhone` function (L38–62) in `service.ts` with an import from `@dtc/shared-types`: `import { normalizeEgyptianPhone } from "@dtc/shared-types"`. Do the same for any duplicated governorate mapping logic.
   - **Fix `acquireLock`**: The current implementation casts `this.cacheService_` to `any` to call `.setNx()`, which is NOT part of Medusa's `ICacheService` interface — the lock silently degrades to a no-op. Replace with a direct `ioredis` `SET key value EX ttl NX` call (resolving the Redis client from the container) for atomic lock acquisition that actually works.
   - **Unblock Workflow Compensation** (`bosta-fulfillment-workflow.ts`): Remove the `await sleep(backoffMs)` blocking call from the compensation handler. Instead, configure the step with Medusa v2's `retry` option: `{ retries: 3, backoff: { type: "exponential", delay: 2000 } }`. Compensation handlers should execute instantly — retries are the framework's responsibility.

3. EMPIRICAL VERIFICATION & TESTING PHASE:
   - Run TypeScript check: `cd apps/backend && npx tsc --noEmit`
   - Run backend build verification: `cd apps/backend && npm run build`

4. PROCESS CLEANUP & LEARNING DIRECTIVE (CRITICAL):
   - Execute `/learn` to store shared-types import and workflow retry rules.
   - Terminate any running subagents, background dev servers, or processes before completing turn.
</ANTIGRAVITY_WORKFLOW>

<ACCEPTANCE_CRITERIA>
- [ ] Subagents delegated for shared-types comparison, lock inspection, and retry config research.
- [ ] `formatEgyptianPhone` imported from `@dtc/shared-types` — zero duplication in Bosta service.
- [ ] `acquireLock` uses real Redis `SET NX` (not a cast to a non-existent `ICacheService.setNx`).
- [ ] Bosta workflow compensation is non-blocking — retry handled by framework `retry` config.
- [ ] Backend build completes with exit code 0.
- [ ] All subagents and background tasks are cleanly terminated.
</ACCEPTANCE_CRITERIA>
```

---
### Developer Prompt 4: Fix ETA Dummy Phone Fallback, Remove `declare const require` Hacks, Fix Background Queue `new EtaTaxModuleService()` Direct Instantiation

```markdown
/goal

<TASK>
Replace hardcoded dummy phone `"01000000000"` in `order-placed-eta.ts:L186` with a validation guard, remove `declare const require/module: any` hacks in `payload-builder.ts`, fix `(this as any).createEtaReceiptAudits` casts in ETA service, and replace `new EtaTaxModuleService()` in `background-queue.ts:L134` with DI container resolution.
</TASK>

<SUBAGENT_DELEGATION_DIRECTIVE>
- Use `invoke_subagent` to inspect all `declare const require` patterns across the codebase and the background queue's direct EtaTaxModuleService instantiation.
</SUBAGENT_DELEGATION_DIRECTIVE>

<ANTIGRAVITY_SLASH_COMMANDS>
- /goal: Execute autonomously until ETA subscriber validates phone, inline test hacks are removed, service type casts are fixed, and background queue uses DI.
- /learn: Persist ETA data validation and DI resolution rules to .gemini/rules.
</ANTIGRAVITY_SLASH_COMMANDS>

<ANTIGRAVITY_WORKFLOW>
1. RESEARCH & INSPECTION PHASE:
   - View `apps/backend/src/subscribers/order-placed-eta.ts` (line 186 — dummy phone fallback).
   - View `apps/backend/src/modules/eta-tax/payload-builder.ts` (lines 3–4 — `declare const require/module`).
   - View `apps/backend/src/modules/eta-tax/service.ts` (`(this as any).createEtaReceiptAudits` calls).
   - View `apps/backend/src/jobs/background-queue.ts` (line 134 — `new EtaTaxModuleService()`).

2. IMPLEMENTATION PHASE:
   - Target files: `apps/backend/src/subscribers/order-placed-eta.ts`, `apps/backend/src/modules/eta-tax/payload-builder.ts`, `apps/backend/src/modules/eta-tax/service.ts`, `apps/backend/src/jobs/background-queue.ts`
   - **Dummy Phone Guard** (`order-placed-eta.ts:L186`): Replace `customerPhone = "01000000000"` with a validation guard — if phone is missing, log a warning and skip ETA submission for this order (the ETA portal will reject dummy numbers anyway). Do NOT send fabricated data to a government tax authority.
   - **Remove `declare const require/module: any`** (`payload-builder.ts:L3-4`): Delete these CommonJS hacks used for inline self-tests. Extract the `testPayloadBuilder()` function into a proper Jest/Vitest test file (`__tests__/payload-builder.test.ts`).
   - **Fix `(this as any).createEtaReceiptAudits`** (`service.ts`): The DML-generated method `createEtaReceiptAudits` should be properly typed. Add the method signature to the service class or use Medusa's `InferTypeOf` utility to type the generated model methods.
   - **Background Queue DI** (`background-queue.ts:L134`): Replace `new EtaTaxModuleService()` with `container.resolve(ETA_TAX_MODULE)` or `container.resolve("etaTax")`. The directly instantiated service lacks database connections, injected models, and container context — `submitAndAuditReceipt` will crash when attempting DB writes.

3. EMPIRICAL VERIFICATION & TESTING PHASE:
   - Run TypeScript check: `cd apps/backend && npx tsc --noEmit`
   - Run backend build verification: `cd apps/backend && npm run build`

4. PROCESS CLEANUP & LEARNING DIRECTIVE (CRITICAL):
   - Execute `/learn` to store ETA data validation and DI resolution rules.
   - Terminate any running subagents, background dev servers, or processes before completing turn.
</ANTIGRAVITY_WORKFLOW>

<ACCEPTANCE_CRITERIA>
- [ ] Subagents delegated for `declare const require` scan and background queue DI inspection.
- [ ] Dummy phone `"01000000000"` replaced with validation guard — ETA submission skipped when phone missing.
- [ ] `declare const require/module: any` removed — self-test extracted to proper test file.
- [ ] `(this as any).createEtaReceiptAudits` replaced with properly typed method call.
- [ ] `new EtaTaxModuleService()` replaced with `container.resolve("etaTax")` in background queue.
- [ ] Backend build completes with exit code 0.
- [ ] All subagents and background tasks are cleanly terminated.
</ACCEPTANCE_CRITERIA>
```

---

## Part 3: Infrastructure & Storefront Resilience (Prompt 5)

---
### Developer Prompt 5: Fix Docker SSR Networking (Internal vs Public URLs), Secure Redis Password, Add Storefront Error Boundaries, & Guard Mock Tracking Numbers

```markdown
/goal

<TASK>
Separate internal SSR URL (`http://backend:9000`) from public client-side URL for Next.js in Docker, remove Redis password from inline `command` array, add `error.tsx` and `not-found.tsx` route error boundaries, and guard mock `BOSTA_` tracking number generation with `NODE_ENV === "development"`.
</TASK>

<SUBAGENT_DELEGATION_DIRECTIVE>
- Use `invoke_subagent` to inspect Docker Compose networking, Redis password configuration patterns, and Next.js App Router error boundary conventions.
</SUBAGENT_DELEGATION_DIRECTIVE>

<ANTIGRAVITY_SLASH_COMMANDS>
- /goal: Execute autonomously until SSR networking works in Docker, Redis password is secure, error boundaries exist, and mock tracking is dev-only.
- /learn: Persist Docker SSR networking and storefront error boundary rules to .gemini/rules.
</ANTIGRAVITY_SLASH_COMMANDS>

<ANTIGRAVITY_WORKFLOW>
1. RESEARCH & INSPECTION PHASE:
   - View `infrastructure/docker/docker-compose.tenant.yml` (storefront service env vars and Redis command).
   - View `apps/storefront/next.config.ts` (environment variable usage).
   - View storefront checkout component (search for `BOSTA_` mock tracking number generation).
   - Check for existing `apps/storefront/src/app/error.tsx` and `apps/storefront/src/app/not-found.tsx`.

2. IMPLEMENTATION PHASE:
   - Target files: `infrastructure/docker/docker-compose.tenant.yml`, `apps/storefront/next.config.ts`, `apps/storefront/src/app/error.tsx` (NEW), `apps/storefront/src/app/not-found.tsx` (NEW), checkout component
   - **SSR Networking**: Add a new non-public env var `MEDUSA_BACKEND_URL=http://backend:9000` for server-side data fetching inside Docker containers. Keep `NEXT_PUBLIC_MEDUSA_BACKEND_URL=https://api.yourdomain.com` for client-side browser requests. Update the storefront data fetching layer to use `MEDUSA_BACKEND_URL` (server-side) vs `NEXT_PUBLIC_MEDUSA_BACKEND_URL` (client-side) based on execution context (`typeof window === "undefined"`).
   - **Redis Password Security**: Move the Redis password from the inline `command: ["redis-server", "--requirepass", "${REDIS_PASSWORD}"]` array (visible via `ps`) to a Docker secret or environment variable that Redis reads from a config file. Use `command: ["redis-server", "/usr/local/etc/redis/redis.conf"]` with a mounted config.
   - **Error Boundaries**: Create `apps/storefront/src/app/error.tsx` (React Error Boundary for runtime errors — "use client" component with retry button) and `apps/storefront/src/app/not-found.tsx` (404 page with navigation back to homepage). Style them consistently with the existing storefront theme (Cairo font, RTL support, dark mode).
   - **Mock Tracking Guard**: Wrap the `BOSTA_` mock tracking number generation in the checkout catch block with `if (process.env.NODE_ENV === "development")`. In production, show a generic error message instead of creating a fake order confirmation.

3. EMPIRICAL VERIFICATION & TESTING PHASE:
   - Run storefront build verification: `cd apps/storefront && npm run build`
   - Run Docker compose config validation: `docker compose -f infrastructure/docker/docker-compose.tenant.yml config`

4. PROCESS CLEANUP & LEARNING DIRECTIVE (CRITICAL):
   - Execute `/learn` to store Docker SSR networking and error boundary rules.
   - Terminate any running subagents, background dev servers, or processes before completing turn.
</ANTIGRAVITY_WORKFLOW>

<ACCEPTANCE_CRITERIA>
- [ ] Subagents delegated for Docker networking, Redis security, and error boundary research.
- [ ] SSR fetches use internal `http://backend:9000`; client-side uses public URL.
- [ ] Redis password NOT visible in `ps` — loaded from config file or Docker secret.
- [ ] `error.tsx` and `not-found.tsx` exist with proper styling and RTL support.
- [ ] Mock `BOSTA_` tracking numbers guarded by `NODE_ENV === "development"`.
- [ ] Storefront build and Docker Compose config pass validation.
- [ ] All subagents and background tasks are cleanly terminated.
</ACCEPTANCE_CRITERIA>
```
