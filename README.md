# Dedicated 8.2 Report Remediation Prompt Pack (`PROMPT_SEQUENCE_82_FINAL_FIXES.md`)

This prompt pack contains **6 targeted developer prompts** engineered for **Google Antigravity Agentic IDE** to resolve the exact new defects identified in the 8.2/10 evaluation report: hardcoded test API key, CI/CD failure masking, ineffective retry backoff, ETA workflow DI token cache defeat, missing fetch timeouts, missing Bosta return fulfillment methods, worker lifecycle issues, and OpenTelemetry auto-instrumentation. Zero older problems are included.

> [!IMPORTANT]
> **Subagent Directive**: Send these 6 prompts sequentially (Prompt 1 through Prompt 6) to your developer Antigravity instance. Every prompt explicitly instructs the agent to delegate research or sub-tasks to subagents (`invoke_subagent`) to maintain clean context and maximize execution speed.

---

## Part 1: Security & CI/CD Pipeline (Prompt 1)

---
### Developer Prompt 1: Remove Hardcoded API Key from `test-gemma.ts` & Fix CI/CD `|| true` Failure Masking in `ci.yml`

```markdown
/goal

<TASK>
Remove the hardcoded plaintext API key from `apps/backend/scripts/test-gemma.ts:L6` and fix CI/CD pipeline steps in `.github/workflows/ci.yml` that swallow failures with `|| true`.
</TASK>

<SUBAGENT_DELEGATION_DIRECTIVE>
- Use `invoke_subagent` (Role: "Codebase Researcher", TypeName: "research") to search the entire monorepo for any other hardcoded API keys, secrets, or `|| true` patterns that mask failures.
</SUBAGENT_DELEGATION_DIRECTIVE>

<ANTIGRAVITY_SLASH_COMMANDS>
- /goal: Execute autonomously until all hardcoded secrets are removed and CI pipeline correctly fails on typecheck/test errors.
- /learn: Persist CI/CD pipeline integrity and secret hygiene rules to .gemini/rules.
</ANTIGRAVITY_SLASH_COMMANDS>

<ANTIGRAVITY_WORKFLOW>
1. RESEARCH & INSPECTION PHASE:
   - View `apps/backend/scripts/test-gemma.ts` (line 6).
   - View `.github/workflows/ci.yml` (lines 53 and 65).
   - Search entire monorepo for other hardcoded API keys or tokens using `grep_search` for patterns like `AQ.Ab`, `AIza`, `sk-`, `Bearer ey`.

2. IMPLEMENTATION PHASE:
   - Target files: `apps/backend/scripts/test-gemma.ts`, `.github/workflows/ci.yml`
   - **`test-gemma.ts:L6`**: Replace the hardcoded plaintext API key (`AQ.Ab8RN6KHs...`) with `process.env.GEMINI_API_KEY`. Add a guard that throws if the environment variable is missing.
   - **`ci.yml:L53`**: Remove `|| true` from the TypeScript typecheck step so the pipeline correctly fails when `tsc --noEmit` reports errors.
   - **`ci.yml:L65`**: Remove `|| true` from the unit test step so the pipeline correctly fails when tests fail.

3. EMPIRICAL VERIFICATION & TESTING PHASE:
   - Run TypeScript check: `cd apps/backend && npx tsc --noEmit`
   - Validate CI workflow YAML syntax.

4. PROCESS CLEANUP & LEARNING DIRECTIVE (CRITICAL):
   - Execute `/learn` to store CI pipeline integrity rules.
   - Terminate any running subagents, background dev servers, or processes before completing turn.
</ANTIGRAVITY_WORKFLOW>

<ACCEPTANCE_CRITERIA>
- [ ] Subagents delegated for monorepo-wide secret scan.
- [ ] Zero hardcoded API keys in `test-gemma.ts` or anywhere in the monorepo.
- [ ] `ci.yml` typecheck and test steps fail the pipeline on errors (no `|| true`).
- [ ] Backend build completes with exit code 0.
- [ ] All subagents and background tasks are cleanly terminated.
</ACCEPTANCE_CRITERIA>
```

---

## Part 2: Background Queue Retry Backoff & Worker Lifecycle (Prompt 2)

---
### Developer Prompt 2: Fix Background Queue Retry Backoff Delay, Add SIGINT/SIGTERM Graceful Shutdown, & Control Worker Auto-Start

```markdown
/goal

<TASK>
Add actual `await` delay before re-queuing failed jobs in `background-queue.ts`, implement SIGINT/SIGTERM graceful shutdown for the worker loop, and prevent auto-start on module import.
</TASK>

<SUBAGENT_DELEGATION_DIRECTIVE>
- Use `invoke_subagent` to inspect Redis queue worker lifecycle management patterns and Node.js process signal handling.
</SUBAGENT_DELEGATION_DIRECTIVE>

<ANTIGRAVITY_SLASH_COMMANDS>
- /goal: Execute autonomously until background queue retry backoff actually delays re-queuing and worker shuts down gracefully on SIGINT/SIGTERM.
- /learn: Persist background worker lifecycle management rules to .gemini/rules.
</ANTIGRAVITY_SLASH_COMMANDS>

<ANTIGRAVITY_WORKFLOW>
1. RESEARCH & INSPECTION PHASE:
   - View `apps/backend/src/jobs/background-queue.ts` (lines 121, 137–139, 154).
   - View `apps/backend/src/jobs/ai-copywriter-worker.ts` (line 121).

2. IMPLEMENTATION PHASE:
   - Target files: `apps/backend/src/jobs/background-queue.ts`, `apps/backend/src/jobs/ai-copywriter-worker.ts`
   - **Effective Retry Backoff** (`background-queue.ts:L137-139`): Before re-queuing a failed job via `rpush`, add `await new Promise(resolve => setTimeout(resolve, backoffDelayMs))` using the computed exponential backoff delay so jobs actually wait before retry instead of retrying instantly.
   - **Graceful Shutdown** (`background-queue.ts`): Add `process.on("SIGINT", ...)` and `process.on("SIGTERM", ...)` handlers that set a `shutdownRequested` flag, allowing the current BLPOP cycle to complete before exiting cleanly.
   - **Worker Lifecycle Control** (`background-queue.ts:L154`): Replace the auto-starting worker loop on module import with an explicit `startWorker()` export function that must be called intentionally, preventing uncontrolled worker spawns during imports.

3. EMPIRICAL VERIFICATION & TESTING PHASE:
   - Run TypeScript check: `cd apps/backend && npx tsc --noEmit`
   - Run backend build verification: `cd apps/backend && npm run build`

4. PROCESS CLEANUP & LEARNING DIRECTIVE (CRITICAL):
   - Execute `/learn` to store worker lifecycle rules.
   - Terminate any running subagents, background dev servers, or processes before completing turn.
</ANTIGRAVITY_WORKFLOW>

<ACCEPTANCE_CRITERIA>
- [ ] Subagents delegated for worker lifecycle pattern research.
- [ ] Failed job re-queuing in `background-queue.ts` awaits computed exponential backoff delay before `rpush`.
- [ ] SIGINT/SIGTERM handlers gracefully stop the worker loop after current job completes.
- [ ] Worker loop no longer auto-starts on module import; requires explicit `startWorker()` call.
- [ ] Backend build completes with exit code 0.
- [ ] All subagents and background tasks are cleanly terminated.
</ACCEPTANCE_CRITERIA>
```

---

## Part 3: ETA Tax Workflow DI & Compensation (Prompt 3)

---
### Developer Prompt 3: Resolve ETA Workflow Clients from DI Container (Preserve Token Cache) & Implement Real Compensation DLQ Retry

```markdown
/goal

<TASK>
Replace `new EtaClient()` and `new EtaHsmSigner()` in `eta-tax-workflow.ts` with DI container resolution to preserve OAuth2 token caching, and replace the stub compensation handler with real DLQ retry logic.
</TASK>

<SUBAGENT_DELEGATION_DIRECTIVE>
- Delegate Medusa v2 workflow step DI container resolution and compensation retry logic inspection to a subagent via `invoke_subagent`.
</SUBAGENT_DELEGATION_DIRECTIVE>

<ANTIGRAVITY_SLASH_COMMANDS>
- /goal: Execute autonomously until ETA workflow resolves clients from DI container and compensation handler triggers real DLQ retries.
- /learn: Persist Medusa workflow DI resolution and compensation rules to .gemini/rules.
</ANTIGRAVITY_SLASH_COMMANDS>

<ANTIGRAVITY_WORKFLOW>
1. RESEARCH & INSPECTION PHASE:
   - View `apps/backend/src/workflows/eta-tax-workflow.ts` (line 63 and compensation handler).
   - View `apps/backend/src/modules/eta-tax/client.ts` (token caching logic).

2. IMPLEMENTATION PHASE:
   - Target file: `apps/backend/src/workflows/eta-tax-workflow.ts`
   - **DI Container Resolution** (`eta-tax-workflow.ts:L63`): Replace `new EtaClient(...)` and `new EtaHsmSigner(...)` with `container.resolve("etaTax")` to use the singleton module service instance, preserving the in-memory OAuth2 token cache (`this.cachedToken`) across workflow executions.
   - **Real Compensation Handler**: Replace the stub `console.warn(...)` compensation with actual logic that enqueues the failed submission into the BullMQ DLQ retry queue with the complete receipt payload, triggering `submitAndAuditReceipt()` on retry.

3. EMPIRICAL VERIFICATION & TESTING PHASE:
   - Run TypeScript check: `cd apps/backend && npx tsc --noEmit`
   - Run backend build verification: `cd apps/backend && npm run build`

4. PROCESS CLEANUP & LEARNING DIRECTIVE (CRITICAL):
   - Execute `/learn` to store workflow DI resolution rules.
   - Terminate any running subagents, background dev servers, or processes before completing turn.
</ANTIGRAVITY_WORKFLOW>

<ACCEPTANCE_CRITERIA>
- [ ] Subagents delegated for workflow DI resolution inspection.
- [ ] ETA workflow resolves `EtaClient` from DI container, preserving OAuth2 token cache.
- [ ] Compensation handler enqueues failed submissions to DLQ retry queue instead of just logging a warning.
- [ ] Backend build completes with exit code 0.
- [ ] All subagents and background tasks are cleanly terminated.
</ACCEPTANCE_CRITERIA>
```

---

## Part 4: External API Fetch Timeouts (Prompt 4)

---
### Developer Prompt 4: Add `AbortController` Fetch Timeouts to All External API Clients (Paymob, Bosta, ETA, Gemini)

```markdown
/goal

<TASK>
Add `AbortController` with 30-second timeout to all external API `fetch` calls in Paymob `client.ts`, Bosta `client.ts`, ETA `client.ts`, and Gemini AI `client.ts`.
</TASK>

<SUBAGENT_DELEGATION_DIRECTIVE>
- Use `invoke_subagent` to inspect all four client files and identify every `fetch()` call that lacks an abort signal.
</SUBAGENT_DELEGATION_DIRECTIVE>

<ANTIGRAVITY_SLASH_COMMANDS>
- /goal: Execute autonomously until all external API fetch calls include AbortController timeouts.
- /learn: Persist external API fetch timeout rules to .gemini/rules.
</ANTIGRAVITY_SLASH_COMMANDS>

<ANTIGRAVITY_WORKFLOW>
1. RESEARCH & INSPECTION PHASE:
   - View `apps/backend/src/modules/paymob/client.ts`, `apps/backend/src/modules/bosta/client.ts`, `apps/backend/src/modules/eta-tax/client.ts`, and `apps/backend/src/modules/gemini-ai/client.ts`.

2. IMPLEMENTATION PHASE:
   - Target files: `apps/backend/src/modules/paymob/client.ts`, `apps/backend/src/modules/bosta/client.ts`, `apps/backend/src/modules/eta-tax/client.ts`, `apps/backend/src/modules/gemini-ai/client.ts`
   - For each external API `fetch()` call:
     ```typescript
     const controller = new AbortController();
     const timeoutId = setTimeout(() => controller.abort(), 30_000);
     try {
       const response = await fetch(url, { ...options, signal: controller.signal });
       // ... handle response
     } finally {
       clearTimeout(timeoutId);
     }
     ```
   - Add descriptive `TimeoutError` messages in catch blocks to distinguish timeout failures from network errors.

3. EMPIRICAL VERIFICATION & TESTING PHASE:
   - Run TypeScript check: `cd apps/backend && npx tsc --noEmit`
   - Run backend build verification: `cd apps/backend && npm run build`

4. PROCESS CLEANUP & LEARNING DIRECTIVE (CRITICAL):
   - Execute `/learn` to store fetch timeout patterns.
   - Terminate any running subagents, background dev servers, or processes before completing turn.
</ANTIGRAVITY_WORKFLOW>

<ACCEPTANCE_CRITERIA>
- [ ] Subagents delegated for all four client file inspections.
- [ ] Every `fetch()` call in Paymob, Bosta, ETA, and Gemini clients includes `AbortController` with 30s timeout.
- [ ] Timeout errors produce descriptive log messages.
- [ ] Backend build completes with exit code 0.
- [ ] All subagents and background tasks are cleanly terminated.
</ACCEPTANCE_CRITERIA>
```

---

## Part 5: Bosta Return Fulfillment & Cache Namespace (Prompt 5)

---
### Developer Prompt 5: Implement Bosta `createReturnFulfillment` & `getFulfillmentDocuments` Methods & Unify Prewarm Cache Namespace

```markdown
/goal

<TASK>
Implement `createReturnFulfillment()` and `getFulfillmentDocuments()` in `bosta/service.ts` and update `prewarm-bosta-rates.ts` to use Medusa `ICacheService`.
</TASK>

<SUBAGENT_DELEGATION_DIRECTIVE>
- Delegate Medusa v2 `AbstractFulfillmentProviderService` return fulfillment method signatures and `ICacheService` resolution to a subagent via `invoke_subagent`.
</SUBAGENT_DELEGATION_DIRECTIVE>

<ANTIGRAVITY_SLASH_COMMANDS>
- /goal: Execute autonomously until Bosta return fulfillment methods and cache namespace unification compile clean.
- /learn: Persist Medusa fulfillment provider return methods to .gemini/rules.
</ANTIGRAVITY_SLASH_COMMANDS>

<ANTIGRAVITY_WORKFLOW>
1. RESEARCH & INSPECTION PHASE:
   - View `apps/backend/src/modules/bosta/service.ts` and `apps/backend/src/jobs/prewarm-bosta-rates.ts`.

2. IMPLEMENTATION PHASE:
   - Target files: `apps/backend/src/modules/bosta/service.ts`, `apps/backend/src/jobs/prewarm-bosta-rates.ts`
   - **`createReturnFulfillment()`**: Implement the method in `bosta/service.ts` to create a Bosta return pickup AWB using the Bosta API reverse logistics endpoint with the original AWB reference.
   - **`getFulfillmentDocuments()`**: Implement the method to return AWB shipping label PDF URLs and tracking page URLs from Bosta.
   - **`prewarm-bosta-rates.ts`**: Replace raw `ioredis` connection with Medusa's `ICacheService` (`container.resolve("cacheService")`) to ensure pre-warmed keys write to the same cache namespace used by `service.ts` rate lookups.

3. EMPIRICAL VERIFICATION & TESTING PHASE:
   - Run TypeScript check: `cd apps/backend && npx tsc --noEmit`
   - Run backend build verification: `cd apps/backend && npm run build`

4. PROCESS CLEANUP & LEARNING DIRECTIVE (CRITICAL):
   - Execute `/learn` to store fulfillment return method rules.
   - Terminate any running subagents, background dev servers, or processes before completing turn.
</ANTIGRAVITY_WORKFLOW>

<ACCEPTANCE_CRITERIA>
- [ ] Subagents delegated for fulfillment provider return method research.
- [ ] `createReturnFulfillment()` creates Bosta return pickup AWBs.
- [ ] `getFulfillmentDocuments()` returns AWB label and tracking URLs.
- [ ] `prewarm-bosta-rates.ts` uses `ICacheService` instead of raw ioredis.
- [ ] Backend build completes with exit code 0.
- [ ] All subagents and background tasks are cleanly terminated.
</ACCEPTANCE_CRITERIA>
```

---

## Part 6: OpenTelemetry Auto-Instrumentation, Container `any` Casts, & Next.js Language Routing (Prompt 6)

---
### Developer Prompt 6: Uncomment Root OpenTelemetry `instrumentation.ts`, Replace Container `any` Casts, & Use Next.js Routing for Language Switching

```markdown
/goal

<TASK>
Uncomment root `apps/backend/instrumentation.ts` for OpenTelemetry auto-instrumentation, replace `any` casts on Medusa container resolution calls, and switch storefront language toggling to Next.js routing.
</TASK>

<SUBAGENT_DELEGATION_DIRECTIVE>
- Use `invoke_subagent` to inspect Medusa v2 container resolution types, OpenTelemetry Node.js SDK auto-instrumentation, and Next.js i18n routing patterns.
</SUBAGENT_DELEGATION_DIRECTIVE>

<ANTIGRAVITY_SLASH_COMMANDS>
- /goal: Execute autonomously until OpenTelemetry auto-instrumentation is active, container resolutions are typed, and language switching uses Next.js routing.
- /learn: Persist OpenTelemetry and Medusa type safety rules to .gemini/rules.
</ANTIGRAVITY_SLASH_COMMANDS>

<ANTIGRAVITY_WORKFLOW>
1. RESEARCH & INSPECTION PHASE:
   - View `apps/backend/instrumentation.ts` (root file — entirely commented out).
   - Search for `as any` patterns in API routes and subscribers across `apps/backend/src/`.
   - View storefront language toggle component.

2. IMPLEMENTATION PHASE:
   - Target files: `apps/backend/instrumentation.ts`, API routes and subscribers with `any` casts, storefront language toggle component
   - **Root `instrumentation.ts`**: Uncomment and configure OpenTelemetry Node.js SDK auto-instrumentation with appropriate exporter (console fallback if OTLP collector is unreachable).
   - **Container `any` Casts**: Replace `req.scope.resolve("payment") as any` and similar patterns across API routes and subscribers with properly typed resolution using Medusa DTO types (e.g., `IPaymentModuleService`, `IFulfillmentModuleService`, `RemoteQueryFunction`).
   - **Next.js Language Routing**: Replace client-side React state language toggle with Next.js routing-based language switching (`router.push(`/${targetLocale}${pathname}`)`) to preserve SEO benefits of server-rendered localized pages.

3. EMPIRICAL VERIFICATION & TESTING PHASE:
   - Run TypeScript check: `cd apps/backend && npx tsc --noEmit`
   - Run backend build verification: `cd apps/backend && npm run build`
   - Run storefront build verification: `cd apps/storefront && npm run build`

4. PROCESS CLEANUP & LEARNING DIRECTIVE (CRITICAL):
   - Execute `/learn` to store type safety and i18n routing rules.
   - Terminate any running subagents, background dev servers, or processes before completing turn.
</ANTIGRAVITY_WORKFLOW>

<ACCEPTANCE_CRITERIA>
- [ ] Subagents delegated for OpenTelemetry, Medusa types, and i18n routing research.
- [ ] Root `instrumentation.ts` uncommented and configured for OpenTelemetry auto-instrumentation.
- [ ] Zero `as any` casts on container resolution calls in API routes and subscribers.
- [ ] Language switching uses Next.js routing for SEO benefit.
- [ ] Backend and storefront builds complete with exit code 0.
- [ ] All subagents and background tasks are cleanly terminated.
</ACCEPTANCE_CRITERIA>
```
