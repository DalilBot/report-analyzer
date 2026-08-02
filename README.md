# Master Developer Prompt Pack: 8.1 Rating Report Codebase Fixes (`PROMPT_SEQUENCE_81_RATING_FIXES.md`)

This prompt pack contains **7 hyper-focused developer prompts** engineered for **Google Antigravity Agentic IDE** to resolve the exact defects, workflow bugs, subscriber timing issues, and storefront layout flaws identified in the 8.1/10 rating report. Zero older problems are included.

> [!IMPORTANT]
> **Subagent Directive**: Every prompt explicitly instructs the receiving Antigravity agent to invoke subagents (`invoke_subagent`) for codebase research, file inspections, or parallel sub-tasks to maintain clean context and maximize execution speed.

---

## Part 1: Backend Modules & Workflows Fixes (Prompts 1–4)

---
### Developer Prompt 1: Paymob `getPaymentStatus` Live REST API Query

```markdown
/goal

<TASK>
Replace hardcoded `{ status: "authorized" }` in `getPaymentStatus()` (lines 260–266) in `apps/backend/src/modules/paymob/service.ts` with a live HTTP query to Paymob transaction API.
</TASK>

<SUBAGENT_DELEGATION_DIRECTIVE>
- Use `invoke_subagent` (Role: "Codebase Researcher", TypeName: "research") to inspect Paymob GET transaction status endpoint documentation.
</SUBAGENT_DELEGATION_DIRECTIVE>

<ANTIGRAVITY_SLASH_COMMANDS>
- /goal: Execute autonomously until Paymob getPaymentStatus queries live Paymob REST API.
- /browser: Verify Paymob GET transaction status API endpoint specs.
- /learn: Persist Paymob transaction status query patterns to .gemini/rules.
</ANTIGRAVITY_SLASH_COMMANDS>

<ANTIGRAVITY_WORKFLOW>
1. RESEARCH & INSPECTION PHASE:
   - View `apps/backend/src/modules/paymob/service.ts` (lines 260–266) and `apps/backend/src/modules/paymob/client.ts`.

2. IMPLEMENTATION PHASE:
   - Target files: `apps/backend/src/modules/paymob/client.ts`, `apps/backend/src/modules/paymob/service.ts`
   - Implement `getPaymobTransactionStatus(authToken, transactionId)` in `client.ts` issuing `GET https://accept.paymob.com/api/acceptance/transactions/{id}`.
   - Update `getPaymentStatus()` in `service.ts` (lines 260–266) to call `getPaymobTransactionStatus()` and map Paymob transaction status (`success`, `pending`, `refunded`, `voided`) to Medusa payment status (`captured`, `authorized`, `canceled`, `error`).

3. EMPIRICAL VERIFICATION & TESTING PHASE:
   - Run TypeScript check: `cd apps/backend && npx tsc --noEmit`
   - Run backend build verification: `cd apps/backend && npm run build`

4. PROCESS CLEANUP & LEARNING DIRECTIVE (CRITICAL):
   - Execute `/learn` to store Paymob payment status mapping rules.
   - Terminate any running subagents, background dev servers, or processes before completing turn.
</ANTIGRAVITY_WORKFLOW>

<ACCEPTANCE_CRITERIA>
- [ ] Subagents delegated for Paymob transaction status API research.
- [ ] `getPaymentStatus()` in `paymob/service.ts` queries live Paymob REST API.
- [ ] Backend build completes with exit code 0.
- [ ] All subagents, background tasks, and dev servers are cleanly terminated.
</ACCEPTANCE_CRITERIA>
```

---
### Developer Prompt 2: Fix Transaction ID String Bug in Paymob Payment Workflow Rollback

```markdown
/goal

<TASK>
Fix transaction ID bug on line 36 of `apps/backend/src/workflows/paymob-payment-workflow.ts` so step compensation passes the live Paymob transaction ID.
</TASK>

<SUBAGENT_DELEGATION_DIRECTIVE>
- Use `invoke_subagent` to inspect `initiatePaymobPaymentStep` compensation data payload structure.
</SUBAGENT_DELEGATION_DIRECTIVE>

<ANTIGRAVITY_SLASH_COMMANDS>
- /goal: Execute autonomously until Paymob workflow rollback step passes real transaction ID to void API.
- /learn: Persist Medusa workflow compensation state passing rules to .gemini/rules.
</ANTIGRAVITY_SLASH_COMMANDS>

<ANTIGRAVITY_WORKFLOW>
1. RESEARCH & INSPECTION PHASE:
   - View `apps/backend/src/workflows/paymob-payment-workflow.ts` (line 36).

2. IMPLEMENTATION PHASE:
   - Target file: `apps/backend/src/workflows/paymob-payment-workflow.ts`
   - Update `initiatePaymobPaymentStep` response to include real `paymob_transaction_id` in `StepResponse(result, { transactionId: result.transaction_id })`.
   - On workflow step rollback compensation, pass `compensationData.transactionId` to `voidPaymobTransaction` so void calls target actual Paymob payment transactions.

3. EMPIRICAL VERIFICATION & TESTING PHASE:
   - Run TypeScript check: `cd apps/backend && npx tsc --noEmit`
   - Run backend build verification: `cd apps/backend && npm run build`

4. PROCESS CLEANUP & LEARNING DIRECTIVE (CRITICAL):
   - Execute `/learn` to store workflow compensation state passing rules.
   - Terminate any running subagents, background processes, or dev servers before completing turn.
</ANTIGRAVITY_WORKFLOW>

<ACCEPTANCE_CRITERIA>
- [ ] Subagents invoked for workflow step response inspection.
- [ ] `paymob-payment-workflow.ts` compensation step passes live Paymob transaction ID to `voidPaymobTransaction`.
- [ ] Backend build completes with exit code 0.
- [ ] All subagents, background tasks, and dev servers are cleanly terminated.
</ACCEPTANCE_CRITERIA>
```

---
### Developer Prompt 3: Refactor ETA Subscriber DLQ Alert Timing to Exhaustion Only

```markdown
/goal

<TASK>
Refactor `apps/backend/src/subscribers/order-placed-eta.ts` (lines 141–173) so DLQ alert webhooks trigger only after all background retries are exhausted.
</TASK>

<SUBAGENT_DELEGATION_DIRECTIVE>
- Delegate ETA subscriber retry state inspection to a `research` subagent via `invoke_subagent`.
</SUBAGENT_DELEGATION_DIRECTIVE>

<ANTIGRAVITY_SLASH_COMMANDS>
- /goal: Execute autonomously until ETA subscriber DLQ alert webhooks fire only on final retry exhaustion.
</ANTIGRAVITY_SLASH_COMMANDS>

<ANTIGRAVITY_WORKFLOW>
1. RESEARCH & INSPECTION PHASE:
   - View `apps/backend/src/subscribers/order-placed-eta.ts` (lines 141–173).

2. IMPLEMENTATION PHASE:
   - Target file: `apps/backend/src/subscribers/order-placed-eta.ts`
   - Remove premature DLQ alert webhook dispatch from the initial failure handler.
   - Trigger DLQ alert webhook ONLY inside the final retry error handler when `attempts >= MAX_RETRIES` (3 retries exhausted).

3. EMPIRICAL VERIFICATION & TESTING PHASE:
   - Run TypeScript check: `cd apps/backend && npx tsc --noEmit`
   - Run backend build verification: `cd apps/backend && npm run build`

4. PROCESS CLEANUP & LEARNING DIRECTIVE (CRITICAL):
   - Terminate any running subagents, background dev servers, or processes before completing turn.
</ANTIGRAVITY_WORKFLOW>

<ACCEPTANCE_CRITERIA>
- [ ] Subagents delegated for subscriber retry flow inspection.
- [ ] DLQ alert webhook dispatches ONLY after all 3 retries are exhausted (`attempts >= MAX_RETRIES`).
- [ ] Backend build completes with exit code 0.
- [ ] All subagents, background tasks, and dev servers are cleanly terminated.
</ACCEPTANCE_CRITERIA>
```

---
### Developer Prompt 4: Replace In-Memory Array Queue with Redis BullMQ Queue Worker

```markdown
/goal

<TASK>
Delete in-memory array queue in `apps/backend/src/jobs/background-queue.ts` (lines 14–15) and configure native Redis BullMQ background workers.
</TASK>

<SUBAGENT_DELEGATION_DIRECTIVE>
- Use `invoke_subagent` to research BullMQ Queue and Worker setup in Medusa v2.
</SUBAGENT_DELEGATION_DIRECTIVE>

<ANTIGRAVITY_SLASH_COMMANDS>
- /goal: Execute autonomously until background job processing uses persistent Redis BullMQ queue workers.
- /learn: Persist Redis BullMQ background worker patterns to .gemini/rules.
</ANTIGRAVITY_SLASH_COMMANDS>

<ANTIGRAVITY_WORKFLOW>
1. RESEARCH & INSPECTION PHASE:
   - View `apps/backend/src/jobs/background-queue.ts` (lines 14–15).

2. IMPLEMENTATION PHASE:
   - Target file: `apps/backend/src/jobs/background-queue.ts`
   - Remove `pendingJobsQueue = []` in-memory array.
   - Instantiate BullMQ `Queue` (`background_jobs_queue`) and `Worker` connected to Redis (`process.env.REDIS_URL`), ensuring background jobs persist across container restarts.

3. EMPIRICAL VERIFICATION & TESTING PHASE:
   - Run TypeScript check: `cd apps/backend && npx tsc --noEmit`
   - Run backend build verification: `cd apps/backend && npm run build`

4. PROCESS CLEANUP & LEARNING DIRECTIVE (CRITICAL):
   - Execute `/learn` to store BullMQ worker patterns.
   - Terminate any running subagents, background processes, or dev servers before completing turn.
</ANTIGRAVITY_WORKFLOW>

<ACCEPTANCE_CRITERIA>
- [ ] Subagents delegated for BullMQ queue worker patterns research.
- [ ] `background-queue.ts` contains zero in-memory `pendingJobsQueue` arrays; uses Redis BullMQ Queue/Worker.
- [ ] Backend build completes with exit code 0.
- [ ] All subagents, background tasks, and dev servers are cleanly terminated.
</ACCEPTANCE_CRITERIA>
```

---

## Part 2: Storefront & Infrastructure Optimizations (Prompts 5–7)

---
### Developer Prompt 5: Dynamic Root HTML Direction & Language in Storefront Layout

```markdown
/goal

<TASK>
Update line 33 of `apps/storefront/src/app/layout.tsx` to dynamically set root HTML `lang` and `dir` attributes based on active route locale parameter.
</TASK>

<SUBAGENT_DELEGATION_DIRECTIVE>
- Delegate Next.js 15 App Router dynamic HTML layout inspection to a subagent via `invoke_subagent`.
</SUBAGENT_DELEGATION_DIRECTIVE>

<ANTIGRAVITY_SLASH_COMMANDS>
- /goal: Execute autonomously until storefront layout dynamically sets HTML lang and dir attributes.
</ANTIGRAVITY_SLASH_COMMANDS>

<ANTIGRAVITY_WORKFLOW>
1. RESEARCH & INSPECTION PHASE:
   - View `apps/storefront/src/app/layout.tsx` (line 33) and `apps/storefront/src/app/[countryCode]/layout.tsx`.

2. IMPLEMENTATION PHASE:
   - Target files: `apps/storefront/src/app/layout.tsx`, `apps/storefront/src/app/[countryCode]/layout.tsx`
   - Remove hardcoded `lang="ar" dir="rtl"` on line 33 of `layout.tsx`.
   - Compute dynamic HTML direction (`dir={locale === 'ar' ? 'rtl' : 'ltr'}`) and language (`lang={locale}`) based on current route params, ensuring English language views align correctly.

3. EMPIRICAL VERIFICATION & TESTING PHASE:
   - Run storefront build verification: `cd apps/storefront && npm run build`

4. PROCESS CLEANUP & LEARNING DIRECTIVE (CRITICAL):
   - Terminate any running subagents, background dev servers (e.g. `next dev`) before completing turn.
</ANTIGRAVITY_WORKFLOW>

<ACCEPTANCE_CRITERIA>
- [ ] Subagents delegated for dynamic layout prop inspection.
- [ ] Line 33 of `layout.tsx` renders dynamic `dir` and `lang` props based on active locale.
- [ ] Storefront build completes with exit code 0.
- [ ] All subagents, background tasks, and dev servers are cleanly terminated.
</ACCEPTANCE_CRITERIA>
```

---
### Developer Prompt 6: Enable Next.js Standalone Output Mode & Optimize Storefront Dockerfile

```markdown
/goal

<TASK>
Configure `output: 'standalone'` in `apps/storefront/next.config.ts` and update `infrastructure/docker/Dockerfile.storefront` for lightweight production builds.
</TASK>

<SUBAGENT_DELEGATION_DIRECTIVE>
- Use `invoke_subagent` to research Next.js standalone output deployment patterns in Docker.
</SUBAGENT_DELEGATION_DIRECTIVE>

<ANTIGRAVITY_SLASH_COMMANDS>
- /goal: Execute autonomously until Next.js storefront builds in standalone mode cleanly.
</ANTIGRAVITY_SLASH_COMMANDS>

<ANTIGRAVITY_WORKFLOW>
1. RESEARCH & INSPECTION PHASE:
   - View `apps/storefront/next.config.ts` and `infrastructure/docker/Dockerfile.storefront`.

2. IMPLEMENTATION PHASE:
   - Target files: `apps/storefront/next.config.ts`, `infrastructure/docker/Dockerfile.storefront`
   - **`next.config.ts`**: Add `output: "standalone"` to Next.js configuration object.
   - **`Dockerfile.storefront`**: Update runner stage to copy `.next/standalone` and `.next/static` assets, executing `CMD ["node", "server.js"]` for optimal container image size and memory overhead.

3. EMPIRICAL VERIFICATION & TESTING PHASE:
   - Run storefront build verification: `cd apps/storefront && npm run build`
   - Run Docker compose config validation: `docker compose -f infrastructure/docker/docker-compose.tenant.yml config`

4. PROCESS CLEANUP & LEARNING DIRECTIVE (CRITICAL):
   - Terminate any active subagents or background tasks before completing turn.
</ANTIGRAVITY_WORKFLOW>

<ACCEPTANCE_CRITERIA>
- [ ] `next.config.ts` includes `output: "standalone"`.
- [ ] `Dockerfile.storefront` copies standalone server build assets and executes `node server.js`.
- [ ] Storefront build and Docker Compose config pass validation.
- [ ] All subagents and background tasks are cleanly terminated.
</ACCEPTANCE_CRITERIA>
```

---
### Developer Prompt 7: Type-Safe Container Injection in Bosta Fulfillment Service

```markdown
/goal

<TASK>
Replace manual `(this.container_?.caching as any)` resolution in `apps/backend/src/modules/bosta/service.ts` with typed Medusa v2 container injection.
</TASK>

<SUBAGENT_DELEGATION_DIRECTIVE>
- Use `invoke_subagent` to inspect `@medusajs/framework/types` `ICacheService` injection patterns.
</SUBAGENT_DELEGATION_DIRECTIVE>

<ANTIGRAVITY_SLASH_COMMANDS>
- /goal: Execute autonomously until Bosta service uses type-safe ICacheService container injection.
</ANTIGRAVITY_SLASH_COMMANDS>

<ANTIGRAVITY_WORKFLOW>
1. RESEARCH & INSPECTION PHASE:
   - View `apps/backend/src/modules/bosta/service.ts`.

2. IMPLEMENTATION PHASE:
   - Target file: `apps/backend/src/modules/bosta/service.ts`
   - Inject `caching` container dependency via constructor or container resolution using typed `ICacheService` interface from `@medusajs/framework/types`.
   - Remove `(this.container_?.caching as any)` untyped type assertion.

3. EMPIRICAL VERIFICATION & TESTING PHASE:
   - Run TypeScript check: `cd apps/backend && npx tsc --noEmit`
   - Run backend build verification: `cd apps/backend && npm run build`

4. PROCESS CLEANUP & LEARNING DIRECTIVE (CRITICAL):
   - Terminate any running subagents or processes before completing turn.
</ANTIGRAVITY_WORKFLOW>

<ACCEPTANCE_CRITERIA>
- [ ] Subagents delegated for `ICacheService` interface inspection.
- [ ] `bosta/service.ts` uses type-safe `ICacheService` injection without untyped `any` assertions.
- [ ] Backend build completes with exit code 0.
- [ ] All subagents and background tasks are cleanly terminated.
</ACCEPTANCE_CRITERIA>
```
