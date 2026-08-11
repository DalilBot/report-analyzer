# Dedicated 8.1 Report Remediation Prompt Pack (`PROMPT_SEQUENCE_81_FINAL_REPORT_FIXES.md`)

This prompt pack contains **5 targeted developer prompts** engineered for **Google Antigravity Agentic IDE** to resolve the exact new defects identified in the latest 8.1/10 evaluation report: Bosta rate formula discrepancy / cache stampede / TTL mismatch, Paymob webhook fail-open idempotency + 5xx retry, ETA compensation rollback pattern + Redis token cache + monetary precision, backend strict TypeScript + connection pooling + AI worker idempotency, and storefront fetch revalidation + root html lang conflict. Zero older problems are included.

> [!IMPORTANT]
> **Subagent Directive**: Send these 5 prompts sequentially (Prompt 1 through Prompt 5) to your developer Antigravity instance. Every prompt explicitly instructs the agent to delegate research or sub-tasks to subagents (`invoke_subagent`).

---

## Part 1: Fulfillment & Payment Reliability (Prompts 1–2)

---
### Developer Prompt 1: Unify Bosta Express Rate Formula Between Prewarm & Service, Add Cache Stampede Protection, & Synchronize TTLs

```markdown
/goal

<TASK>
Extract Bosta shipping rate calculation into a single shared utility imported by both `service.ts` and `prewarm-bosta-rates.ts`, add Redis lock-based cache stampede protection on concurrent misses, and synchronize cache TTLs.
</TASK>

<SUBAGENT_DELEGATION_DIRECTIVE>
- Use `invoke_subagent` (Role: "Codebase Researcher", TypeName: "research") to compare the exact rate calculation code in `apps/backend/src/modules/bosta/service.ts` against `apps/backend/src/jobs/prewarm-bosta-rates.ts` — identify all formula differences (multiplier, extra fee, base rates).
- Use a second `invoke_subagent` to inspect Redis cache stampede protection patterns (SET NX lock or Promise coalescing).
</SUBAGENT_DELEGATION_DIRECTIVE>

<ANTIGRAVITY_SLASH_COMMANDS>
- /goal: Execute autonomously until Bosta rate calculations are unified, cache stampede is prevented, and TTLs match.
- /learn: Persist Bosta rate calculation and cache consistency rules to .gemini/rules.
</ANTIGRAVITY_SLASH_COMMANDS>

<ANTIGRAVITY_WORKFLOW>
1. RESEARCH & INSPECTION PHASE:
   - View `apps/backend/src/modules/bosta/service.ts` (rate calculation section — express multiplier and fees).
   - View `apps/backend/src/jobs/prewarm-bosta-rates.ts` (rate calculation section — express multiplier and fees).
   - Compare TTL values in both files.

2. IMPLEMENTATION PHASE:
   - Target files: `apps/backend/src/modules/bosta/rate-calculator.ts` (NEW), `apps/backend/src/modules/bosta/service.ts`, `apps/backend/src/jobs/prewarm-bosta-rates.ts`
   - **Shared Rate Calculator**: Extract the shipping rate calculation into a new `rate-calculator.ts` utility module with a single `calculateBostaShippingRate(governorateTier, weight, shippingOptionType)` function. Both `service.ts` and `prewarm-bosta-rates.ts` must import and call this single function — eliminating the formula discrepancy (prewarm: 1.25× + 25 EGP vs service: 1.5× + 0 EGP).
   - **Cache Stampede Protection**: When a cache miss occurs in `service.ts`, acquire a short-lived Redis lock (`SET BOSTA_LOCK_${cacheKey} 1 EX 10 NX`) before recalculating. If the lock is already held (another request is recalculating), wait briefly and re-check the cache instead of triggering a parallel recalculation.
   - **TTL Synchronization**: Define a shared constant `BOSTA_RATE_CACHE_TTL_SECONDS` (e.g., `3600`) used by both the service (currently 1h) and the prewarm job (currently 24h) so cache lifetimes are consistent.

3. EMPIRICAL VERIFICATION & TESTING PHASE:
   - Run TypeScript check: `cd apps/backend && npx tsc --noEmit`
   - Run backend build verification: `cd apps/backend && npm run build`

4. PROCESS CLEANUP & LEARNING DIRECTIVE (CRITICAL):
   - Execute `/learn` to store Bosta rate calculation consistency rules.
   - Terminate any running subagents, background dev servers, or processes before completing turn.
</ANTIGRAVITY_WORKFLOW>

<ACCEPTANCE_CRITERIA>
- [ ] Subagents delegated for rate formula comparison and cache stampede research.
- [ ] Single `rate-calculator.ts` utility used by both service and prewarm job — zero formula discrepancy.
- [ ] Cache stampede protection via Redis `NX` lock on concurrent misses.
- [ ] Shared TTL constant used consistently across service and prewarm job.
- [ ] Backend build completes with exit code 0.
- [ ] All subagents and background tasks are cleanly terminated.
</ACCEPTANCE_CRITERIA>
```

---
### Developer Prompt 2: Fix Paymob Webhook Idempotency Fail-Open Behavior & Add Client 5xx Retry Logic

```markdown
/goal

<TASK>
Make the Paymob webhook Redis idempotency lock fail closed (reject/503) when Redis is unreachable, and add transient 5xx retry logic to `paymob/client.ts`.
</TASK>

<SUBAGENT_DELEGATION_DIRECTIVE>
- Use `invoke_subagent` to inspect the `acquireAtomicRedisNxLock` function behavior when Redis connection fails and identify all Paymob client API call sites that lack retry logic.
</SUBAGENT_DELEGATION_DIRECTIVE>

<ANTIGRAVITY_SLASH_COMMANDS>
- /goal: Execute autonomously until Paymob webhook rejects on Redis failure and client retries transient 5xx errors.
- /learn: Persist webhook idempotency fail-closed and API retry rules to .gemini/rules.
</ANTIGRAVITY_SLASH_COMMANDS>

<ANTIGRAVITY_WORKFLOW>
1. RESEARCH & INSPECTION PHASE:
   - View `apps/backend/src/api/hooks/paymob/route.ts` (Redis lock acquisition and error handling).
   - View `apps/backend/src/modules/paymob/client.ts` (all API call methods).

2. IMPLEMENTATION PHASE:
   - Target files: `apps/backend/src/api/hooks/paymob/route.ts`, `apps/backend/src/modules/paymob/client.ts`
   - **Fail-Closed Idempotency** (`route.ts`): When `acquireAtomicRedisNxLock` throws a Redis connection error (not a lock contention), return HTTP `503 Service Unavailable` instead of proceeding with the webhook. This prevents duplicate payment processing when Redis is temporarily down — Paymob will retry the webhook delivery later.
   - **5xx Retry Logic** (`client.ts`): Add a retry wrapper (up to 2 retries with 1s/3s delays) around all external Paymob API calls (`authenticatePaymob`, `registerOrder`, `requestPaymentKey`, `captureTransaction`, `refundTransaction`, `voidTransaction`) for transient HTTP 5xx responses. Do NOT retry on 4xx errors.

3. EMPIRICAL VERIFICATION & TESTING PHASE:
   - Run TypeScript check: `cd apps/backend && npx tsc --noEmit`
   - Run backend build verification: `cd apps/backend && npm run build`

4. PROCESS CLEANUP & LEARNING DIRECTIVE (CRITICAL):
   - Execute `/learn` to store webhook fail-closed and API retry rules.
   - Terminate any running subagents, background dev servers, or processes before completing turn.
</ANTIGRAVITY_WORKFLOW>

<ACCEPTANCE_CRITERIA>
- [ ] Subagents delegated for Redis lock failure behavior and client retry inspection.
- [ ] Webhook route returns 503 when Redis is unreachable (fail-closed, not fail-open).
- [ ] Paymob client retries transient 5xx errors (up to 2 retries with backoff).
- [ ] 4xx errors are NOT retried.
- [ ] Backend build completes with exit code 0.
- [ ] All subagents and background tasks are cleanly terminated.
</ACCEPTANCE_CRITERIA>
```

---

## Part 2: Tax Compliance & Backend Hardening (Prompts 3–4)

---
### Developer Prompt 3: ETA Workflow Compensation Rollback Pattern, Redis-Backed OAuth2 Token Cache, & Monetary Precision Fix

```markdown
/goal

<TASK>
Refactor ETA workflow compensation to perform rollback (void receipt) instead of forward-retry, cache OAuth2 tokens in Redis instead of instance memory, and replace `.toFixed()` with integer arithmetic in `payload-builder.ts`.
</TASK>

<SUBAGENT_DELEGATION_DIRECTIVE>
- Use `invoke_subagent` to inspect ETA workflow compensation handlers, OAuth2 token caching, and IEEE 754 floating-point precision risks in monetary calculations.
</SUBAGENT_DELEGATION_DIRECTIVE>

<ANTIGRAVITY_SLASH_COMMANDS>
- /goal: Execute autonomously until ETA compensation voids receipts, tokens are Redis-cached, and monetary math uses integer piastres.
- /learn: Persist ETA compensation rollback and monetary precision rules to .gemini/rules.
</ANTIGRAVITY_SLASH_COMMANDS>

<ANTIGRAVITY_WORKFLOW>
1. RESEARCH & INSPECTION PHASE:
   - View `apps/backend/src/workflows/eta-tax-workflow.ts` (compensation handler).
   - View `apps/backend/src/modules/eta-tax/client.ts` (OAuth2 token caching — `this.cachedToken`).
   - View `apps/backend/src/modules/eta-tax/payload-builder.ts` (`.toFixed()` calls on monetary values).

2. IMPLEMENTATION PHASE:
   - Target files: `apps/backend/src/workflows/eta-tax-workflow.ts`, `apps/backend/src/modules/eta-tax/client.ts`, `apps/backend/src/modules/eta-tax/payload-builder.ts`
   - **Compensation Rollback** (`eta-tax-workflow.ts`): Refactor the `signEtaReceiptHsmStep` compensation to attempt voiding/cancelling the submitted receipt on the ETA portal (if a submission UUID exists) rather than enqueuing a forward-retry. Forward retries should be handled by the step's `retry` configuration, not compensations. Compensations are for undoing side effects.
   - **Redis Token Cache** (`client.ts`): Replace the instance-level `this.cachedToken` with Redis-backed storage (`ETA_OAUTH2_TOKEN` key with TTL matching the token's `expires_in - 60s` safety buffer). This prevents redundant OAuth2 token generation when the EtaClient is re-instantiated across different workflow executions or pod restarts.
   - **Monetary Precision** (`payload-builder.ts`): Replace floating-point `.toFixed(5)` arithmetic with integer-based piastre calculations where possible (compute in smallest currency unit, divide only for final output). For values that must be floats per ETA spec, use `Math.round(value * 100000) / 100000` instead of `.toFixed()` to avoid IEEE 754 string conversion inconsistencies.

3. EMPIRICAL VERIFICATION & TESTING PHASE:
   - Run TypeScript check: `cd apps/backend && npx tsc --noEmit`
   - Run backend build verification: `cd apps/backend && npm run build`

4. PROCESS CLEANUP & LEARNING DIRECTIVE (CRITICAL):
   - Execute `/learn` to store ETA compensation and monetary precision rules.
   - Terminate any running subagents, background dev servers, or processes before completing turn.
</ANTIGRAVITY_WORKFLOW>

<ACCEPTANCE_CRITERIA>
- [ ] Subagents delegated for ETA compensation pattern and monetary precision research.
- [ ] ETA workflow compensation attempts receipt void/cancellation (rollback), not forward-retry.
- [ ] OAuth2 tokens stored in Redis with expiry-aware TTL.
- [ ] Monetary calculations use integer arithmetic or `Math.round` instead of `.toFixed()`.
- [ ] Backend build completes with exit code 0.
- [ ] All subagents and background tasks are cleanly terminated.
</ACCEPTANCE_CRITERIA>
```

---
### Developer Prompt 4: Enable `"strict": true` in Backend tsconfig, Add Database Connection Pooling, & AI Worker Job Idempotency

```markdown
/goal

<TASK>
Enable full `"strict": true` in `apps/backend/tsconfig.json`, add database connection pool configuration in `medusa-config.ts`, and add idempotency checks in `ai-copywriter-worker.ts`.
</TASK>

<SUBAGENT_DELEGATION_DIRECTIVE>
- Use `invoke_subagent` to inspect TypeScript strict mode errors that will surface when enabling `"strict": true` and to identify AI copywriter job idempotency patterns.
</SUBAGENT_DELEGATION_DIRECTIVE>

<ANTIGRAVITY_SLASH_COMMANDS>
- /goal: Execute autonomously until backend compiles with strict TypeScript, database pooling is configured, and AI worker has idempotency checks.
- /learn: Persist TypeScript strict mode and database pooling rules to .gemini/rules.
</ANTIGRAVITY_SLASH_COMMANDS>

<ANTIGRAVITY_WORKFLOW>
1. RESEARCH & INSPECTION PHASE:
   - View `apps/backend/tsconfig.json`.
   - View `apps/backend/medusa-config.ts` (database driver options section).
   - View `apps/backend/src/jobs/ai-copywriter-worker.ts`.

2. IMPLEMENTATION PHASE:
   - Target files: `apps/backend/tsconfig.json`, `apps/backend/medusa-config.ts`, `apps/backend/src/jobs/ai-copywriter-worker.ts`
   - **Strict TypeScript** (`tsconfig.json`): Replace `"strictNullChecks": true` with full `"strict": true` (enables `noImplicitAny`, `strictPropertyInitialization`, `strictBindCallApply`, `strictFunctionTypes`). Fix any resulting compilation errors — primarily replacing `any` casts with proper interfaces.
   - **Database Connection Pooling** (`medusa-config.ts`): Add explicit pool configuration to `databaseDriverOptions`:
     ```typescript
     databaseDriverOptions: {
       pool: { min: 2, max: 10 },
       connection: { ssl: ... }
     }
     ```
   - **AI Worker Idempotency** (`ai-copywriter-worker.ts`): Before processing a job, check Redis for an existing result key (`gemini_result_${productId}`). If a completed result exists, skip processing and return the cached result — preventing duplicate AI generations from duplicate queue entries.

3. EMPIRICAL VERIFICATION & TESTING PHASE:
   - Run TypeScript check: `cd apps/backend && npx tsc --noEmit`
   - Run backend build verification: `cd apps/backend && npm run build`

4. PROCESS CLEANUP & LEARNING DIRECTIVE (CRITICAL):
   - Execute `/learn` to store TypeScript strict mode rules.
   - Terminate any running subagents, background dev servers, or processes before completing turn.
</ANTIGRAVITY_WORKFLOW>

<ACCEPTANCE_CRITERIA>
- [ ] Subagents delegated for strict mode error analysis and idempotency research.
- [ ] `tsconfig.json` has `"strict": true` and backend compiles with zero errors.
- [ ] `medusa-config.ts` includes explicit `pool: { min: 2, max: 10 }` database connection pooling.
- [ ] AI copywriter worker checks for existing results before processing (idempotent).
- [ ] Backend build completes with exit code 0.
- [ ] All subagents and background tasks are cleanly terminated.
</ACCEPTANCE_CRITERIA>
```

---

## Part 3: Storefront Performance & Accessibility (Prompt 5)

---
### Developer Prompt 5: Add Next.js Fetch Revalidation Strategies, Fix Root `<html>` Lang/Dir Conflict, & Cart Accessibility

```markdown
/goal

<TASK>
Add `unstable_cache` or `revalidate` strategies to Medusa SDK fetch calls in `apps/storefront/src/lib/data/`, fix root `<html lang="ar" dir="rtl">` conflicting with dynamic countryCode layout, and add `aria-label` to cart close button.
</TASK>

<SUBAGENT_DELEGATION_DIRECTIVE>
- Use `invoke_subagent` to inspect Next.js 15+ `unstable_cache` patterns and all storefront data fetching functions that call Medusa SDK.
</SUBAGENT_DELEGATION_DIRECTIVE>

<ANTIGRAVITY_SLASH_COMMANDS>
- /goal: Execute autonomously until storefront data fetching uses revalidation, html attributes are dynamically consistent, and cart button is accessible.
</ANTIGRAVITY_SLASH_COMMANDS>

<ANTIGRAVITY_WORKFLOW>
1. RESEARCH & INSPECTION PHASE:
   - View `apps/storefront/src/lib/data/products.ts` and other data fetching files.
   - View `apps/storefront/src/app/layout.tsx` (root `<html>` tag attributes).
   - View `apps/storefront/src/app/[countryCode]/layout.tsx` (dynamic lang/dir computation).
   - Search for cart close/dismiss buttons lacking `aria-label`.

2. IMPLEMENTATION PHASE:
   - Target files: `apps/storefront/src/lib/data/products.ts`, `apps/storefront/src/app/layout.tsx`, `apps/storefront/src/app/[countryCode]/layout.tsx`, cart component with close button
   - **Fetch Revalidation**: Wrap Medusa SDK data fetching calls with Next.js `unstable_cache` (or use `fetch` with `next: { revalidate: 60 }` / `next: { tags: ["products"] }`) to enable ISR and prevent redundant backend requests on every page load. Product listing pages should revalidate every 60 seconds; product detail pages can use on-demand revalidation via tags.
   - **Root HTML Conflict**: In `layout.tsx`, remove the hardcoded `lang="ar" dir="rtl"` from the root `<html>` tag. Instead, set neutral defaults (`lang="en" dir="ltr"`) and let the `[countryCode]/layout.tsx` dynamically override via a `<body>` wrapper or pass locale data through context. This prevents screen readers from seeing conflicting language attributes.
   - **Cart Accessibility**: Add `aria-label="Close cart"` (or Arabic equivalent based on locale) to the cart close button (`✕`).

3. EMPIRICAL VERIFICATION & TESTING PHASE:
   - Run storefront build verification: `cd apps/storefront && npm run build`

4. PROCESS CLEANUP & LEARNING DIRECTIVE (CRITICAL):
   - Terminate any running subagents, background dev servers (e.g. `next dev`) before completing turn.
</ANTIGRAVITY_WORKFLOW>

<ACCEPTANCE_CRITERIA>
- [ ] Subagents delegated for Next.js caching and accessibility research.
- [ ] Medusa SDK data fetching calls use `unstable_cache` or `revalidate` strategies.
- [ ] Root `<html>` tag uses neutral defaults; dynamic lang/dir applied at countryCode layout level.
- [ ] Cart close button has proper `aria-label` attribute.
- [ ] Storefront build completes with exit code 0.
- [ ] All subagents and background tasks are cleanly terminated.
</ACCEPTANCE_CRITERIA>
```
