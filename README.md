# Dedicated Advanced Improvements Developer Prompt Pack (`PROMPT_SEQUENCE_ADVANCED_IMPROVEMENTS.md`)

This prompt pack contains **7 targeted developer prompts** engineered for **Google Antigravity Agentic IDE** to implement the advanced architectural enhancements identified in the comparative evaluation report. Zero older problems are included.

> [!IMPORTANT]
> **Instructions for Use**: Send these 7 prompts sequentially (Prompt 1 through Prompt 7) to your developer Antigravity instance. Every prompt starts with `/goal` and includes native `/browser`, `/learn`, `<SUBAGENT_DELEGATION_DIRECTIVE>`, and process cleanup rules.

---

### Developer Prompt 1: Implement Live Paymob Refund & Void API Calls in `paymob/service.ts`

```markdown
/goal

<TASK>
Implement live HTTP requests to Paymob's `/api/acceptance/void_refund/refund` endpoint in `refundPayment()` and void calls in `cancelPayment()` inside `apps/backend/src/modules/paymob/service.ts`.
</TASK>

<SUBAGENT_DELEGATION_DIRECTIVE>
- Use `invoke_subagent` (Role: "Codebase Researcher", TypeName: "research") to inspect Paymob REST API v2 refund payload specifications if needed.
</SUBAGENT_DELEGATION_DIRECTIVE>

<ANTIGRAVITY_SLASH_COMMANDS>
- /goal: Execute autonomously until Paymob live refund and void API calls pass TypeScript checks.
- /browser: Use browser to inspect Paymob REST API v2 refund endpoint documentation.
- /learn: Persist Paymob refund/void integration patterns to .gemini/rules.
</ANTIGRAVITY_SLASH_COMMANDS>

<ANTIGRAVITY_WORKFLOW>
1. RESEARCH & INSPECTION PHASE:
   - View `apps/backend/src/modules/paymob/client.ts` and `apps/backend/src/modules/paymob/service.ts`.

2. IMPLEMENTATION PHASE:
   - Target files: `apps/backend/src/modules/paymob/client.ts`, `apps/backend/src/modules/paymob/service.ts`
   - Implement `refundPaymobTransaction(authToken, transactionId, amountCents)` in `client.ts` calling `POST https://accept.paymob.com/api/acceptance/void_refund/refund`.
   - Update `refundPayment()` in `service.ts` to call `refundPaymobTransaction()` with real transaction ID and amount in piastres instead of returning simulated objects.
   - Update `cancelPayment()` to call Paymob void API.

3. EMPIRICAL VERIFICATION & TESTING PHASE:
   - Run TypeScript check: `cd apps/backend && npx tsc --noEmit`
   - Run backend build verification: `cd apps/backend && npm run build`

4. PROCESS CLEANUP & LEARNING DIRECTIVE (CRITICAL):
   - Execute `/learn` to store Paymob refund integration patterns.
   - Terminate any running subagents, background dev servers, or processes before completing turn.
</ANTIGRAVITY_WORKFLOW>

<ACCEPTANCE_CRITERIA>
- [ ] `PaymobClient` includes `refundPaymobTransaction()` sending HTTP POST to Paymob refund API.
- [ ] `refundPayment()` and `cancelPayment()` in `service.ts` execute live API calls.
- [ ] Backend build completes with exit code 0.
- [ ] All subagents, background tasks, and dev servers are cleanly terminated.
</ACCEPTANCE_CRITERIA>
```

---

### Developer Prompt 2: Implement Dynamic Package Weight Tiers in Bosta Fulfillment Service

```markdown
/goal

<TASK>
Enhance `calculatePrice()` in `apps/backend/src/modules/bosta/service.ts` with package weight tier pricing calculations and improved sub-district fallback lookups.
</TASK>

<SUBAGENT_DELEGATION_DIRECTIVE>
- Delegate inspection of Bosta weight tier pricing rules or governorate mapping utils to a subagent via `invoke_subagent`.
</SUBAGENT_DELEGATION_DIRECTIVE>

<ANTIGRAVITY_SLASH_COMMANDS>
- /goal: Execute autonomously until Bosta weight-tier shipping fee calculation compiles clean.
</ANTIGRAVITY_SLASH_COMMANDS>

<ANTIGRAVITY_WORKFLOW>
1. RESEARCH & INSPECTION PHASE:
   - View `apps/backend/src/modules/bosta/service.ts` and `apps/backend/src/modules/bosta/location-mapper.ts`.

2. IMPLEMENTATION PHASE:
   - Target files: `apps/backend/src/modules/bosta/service.ts`, `apps/backend/src/modules/bosta/location-mapper.ts`
   - Update `calculatePrice()` in `service.ts` to inspect package item weights (adding +10 EGP per kg for shipments exceeding 2 kg base weight).
   - Improve `location-mapper.ts` with secondary sub-district string matching before falling back to default governorate codes.

3. EMPIRICAL VERIFICATION & TESTING PHASE:
   - Run TypeScript check: `cd apps/backend && npx tsc --noEmit`
   - Run backend build verification: `cd apps/backend && npm run build`

4. PROCESS CLEANUP & LEARNING DIRECTIVE (CRITICAL):
   - Terminate any running subagents, background processes, or dev servers before completing turn.
</ANTIGRAVITY_WORKFLOW>

<ACCEPTANCE_CRITERIA>
- [ ] Bosta shipping fee calculation accounts for package weight tiers (+10 EGP/kg above 2kg).
- [ ] `location-mapper.ts` handles sub-district fallback string lookups.
- [ ] Backend build completes with exit code 0.
- [ ] All subagents, background tasks, and dev servers are cleanly terminated.
</ACCEPTANCE_CRITERIA>
```

---

### Developer Prompt 3: Add Secondary HSM Proxy Fallback Endpoint in ETA Tax Module

```markdown
/goal

<TASK>
Add secondary HSM proxy fallback endpoint configuration (`ETA_HSM_PROXY_URL_SECONDARY`) in `apps/backend/src/modules/eta-tax/hsm-signer.ts` for hardware signing high availability.
</TASK>

<SUBAGENT_DELEGATION_DIRECTIVE>
- Use `invoke_subagent` to delegate checking `EtaHsmSigner` retry mechanisms.
</SUBAGENT_DELEGATION_DIRECTIVE>

<ANTIGRAVITY_SLASH_COMMANDS>
- /goal: Execute autonomously until ETA HSM signer secondary proxy fallback passes build tests.
- /learn: Persist ETA HSM proxy fallback patterns to .gemini/rules.
</ANTIGRAVITY_SLASH_COMMANDS>

<ANTIGRAVITY_WORKFLOW>
1. RESEARCH & INSPECTION PHASE:
   - View `apps/backend/src/modules/eta-tax/hsm-signer.ts`.

2. IMPLEMENTATION PHASE:
   - Target file: `apps/backend/src/modules/eta-tax/hsm-signer.ts`
   - Add `hsmProxyUrlSecondary` option reading from `process.env.ETA_HSM_PROXY_URL_SECONDARY`.
   - In `signReceipt()`, if the primary HSM proxy times out or returns an error, automatically attempt signing via the secondary proxy URL before triggering mock/fallback signatures.

3. EMPIRICAL VERIFICATION & TESTING PHASE:
   - Run TypeScript check: `cd apps/backend && npx tsc --noEmit`
   - Run backend build verification: `cd apps/backend && npm run build`

4. PROCESS CLEANUP & LEARNING DIRECTIVE (CRITICAL):
   - Execute `/learn` to store ETA HSM proxy redundancy patterns.
   - Terminate any running subagents or processes before completing turn.
</ANTIGRAVITY_WORKFLOW>

<ACCEPTANCE_CRITERIA>
- [ ] `EtaHsmSigner` supports secondary HSM proxy URL fallback (`ETA_HSM_PROXY_URL_SECONDARY`).
- [ ] Primary proxy timeout automatically retries secondary HSM proxy.
- [ ] Backend build completes with exit code 0.
- [ ] All subagents, background tasks, and dev servers are cleanly terminated.
</ACCEPTANCE_CRITERIA>
```

---

### Developer Prompt 4: Add Exponential Retry Backoff & Telemetry to Gemini AI BullMQ Worker

```markdown
/goal

<TASK>
Add exponential rate-limit retry backoff and token usage logging to `apps/backend/src/jobs/ai-copywriter-worker.ts`.
</TASK>

<SUBAGENT_DELEGATION_DIRECTIVE>
- Delegate BullMQ worker configuration research to a subagent via `invoke_subagent`.
</SUBAGENT_DELEGATION_DIRECTIVE>

<ANTIGRAVITY_SLASH_COMMANDS>
- /goal: Execute autonomously until Gemini AI BullMQ worker passes build verification.
</ANTIGRAVITY_SLASH_COMMANDS>

<ANTIGRAVITY_WORKFLOW>
1. RESEARCH & INSPECTION PHASE:
   - View `apps/backend/src/jobs/ai-copywriter-worker.ts` and `apps/backend/src/modules/gemini-ai/service.ts`.

2. IMPLEMENTATION PHASE:
   - Target file: `apps/backend/src/jobs/ai-copywriter-worker.ts`
   - Configure BullMQ worker job options with exponential backoff: `{ attempts: 5, backoff: { type: 'exponential', delay: 2000 } }`.
   - Add token usage telemetry logging (`[Gemini AI Telemetry] Prompt Tokens, Completion Tokens`) upon successful generation.

3. EMPIRICAL VERIFICATION & TESTING PHASE:
   - Run TypeScript check: `cd apps/backend && npx tsc --noEmit`
   - Run backend build verification: `cd apps/backend && npm run build`

4. PROCESS CLEANUP & LEARNING DIRECTIVE (CRITICAL):
   - Terminate any running subagents, background dev servers, or processes before completing turn.
</ANTIGRAVITY_WORKFLOW>

<ACCEPTANCE_CRITERIA>
- [ ] BullMQ AI copywriter worker configures exponential backoff retry options (5 attempts).
- [ ] Token usage telemetry logs to console on job completion.
- [ ] Backend build completes with exit code 0.
- [ ] All subagents, background tasks, and dev servers are cleanly terminated.
</ACCEPTANCE_CRITERIA>
```

---

### Developer Prompt 5: Refactor ETA Subscriber Retries to BullMQ Delayed Jobs & Add DLQ Alert Webhooks

```markdown
/goal

<TASK>
Refactor synchronous retry loops in `apps/backend/src/subscribers/order-placed-eta.ts` to BullMQ delayed jobs and dispatch DLQ alert webhooks.
</TASK>

<SUBAGENT_DELEGATION_DIRECTIVE>
- Use `invoke_subagent` to research BullMQ delayed job schedules and alert webhook patterns.
</SUBAGENT_DELEGATION_DIRECTIVE>

<ANTIGRAVITY_SLASH_COMMANDS>
- /goal: Execute autonomously until ETA subscriber delayed jobs pass build verification.
- /learn: Persist Dead-Letter Queue alert webhook patterns to .gemini/rules.
</ANTIGRAVITY_SLASH_COMMANDS>

<ANTIGRAVITY_WORKFLOW>
1. RESEARCH & INSPECTION PHASE:
   - View `apps/backend/src/subscribers/order-placed-eta.ts`.

2. IMPLEMENTATION PHASE:
   - Target file: `apps/backend/src/subscribers/order-placed-eta.ts`
   - Replace in-memory delay loops with BullMQ delayed job processing (`{ delay: 5000, attempts: 3 }`).
   - On final DLQ failure (`FAILED_DLQ`), dispatch an alert HTTP POST payload to `process.env.ALERT_WEBHOOK_URL` (Slack/Email alert) notifying admins of failed ETA tax submission.

3. EMPIRICAL VERIFICATION & TESTING PHASE:
   - Run TypeScript check: `cd apps/backend && npx tsc --noEmit`
   - Run backend build verification: `cd apps/backend && npm run build`

4. PROCESS CLEANUP & LEARNING DIRECTIVE (CRITICAL):
   - Execute `/learn` to store DLQ alert webhook patterns.
   - Terminate any running subagents, background dev servers, or processes before completing turn.
</ANTIGRAVITY_WORKFLOW>

<ACCEPTANCE_CRITERIA>
- [ ] `order-placed-eta.ts` uses BullMQ delayed jobs instead of synchronous in-memory sleep loops.
- [ ] `FAILED_DLQ` status triggers alert notification payload to `ALERT_WEBHOOK_URL`.
- [ ] Backend build completes with exit code 0.
- [ ] All subagents, background tasks, and dev servers are cleanly terminated.
</ACCEPTANCE_CRITERIA>
```

---

### Developer Prompt 6: Add Paymob Iframe Modal Loading States & Arabic Dialogs in Storefront

```markdown
/goal

<TASK>
Add localized Arabic loading spinners, iframe modal containers, and mobile wallet OTP prompts in storefront checkout.
</TASK>

<SUBAGENT_DELEGATION_DIRECTIVE>
- Delegate storefront checkout component inspection to a subagent via `invoke_subagent`.
</SUBAGENT_DELEGATION_DIRECTIVE>

<ANTIGRAVITY_SLASH_COMMANDS>
- /goal: Execute autonomously until Paymob checkout modal component builds cleanly.
</ANTIGRAVITY_SLASH_COMMANDS>

<ANTIGRAVITY_WORKFLOW>
1. RESEARCH & INSPECTION PHASE:
   - View `apps/storefront/src/app/[countryCode]/checkout/page.tsx`.

2. IMPLEMENTATION PHASE:
   - Target files: `apps/storefront/src/modules/checkout/components/paymob-modal.tsx`, `apps/storefront/src/app/[countryCode]/checkout/page.tsx`
   - Create `PaymobModal` component rendering accessible dialog with Arabic loading spinner (`جاري تجهيز بوابة الدفع...`), Paymob iframe container, and mobile wallet OTP prompt.
   - Embed in storefront checkout page.

3. EMPIRICAL VERIFICATION & TESTING PHASE:
   - Run storefront build verification: `cd apps/storefront && npm run build`

4. PROCESS CLEANUP & LEARNING DIRECTIVE (CRITICAL):
   - Terminate any running subagents, background dev servers, or processes before completing turn.
</ANTIGRAVITY_WORKFLOW>

<ACCEPTANCE_CRITERIA>
- [ ] `PaymobModal` component provides localized Egyptian Arabic loading states and Paymob iframe container.
- [ ] Storefront build completes with exit code 0.
- [ ] All subagents, background tasks, and dev servers are cleanly terminated.
</ACCEPTANCE_CRITERIA>
```

---

### Developer Prompt 7: Add Redis Sentinel High-Availability Support in Docker Infrastructure

```markdown
/goal

<TASK>
Add Redis Sentinel / Cluster configuration options in `infrastructure/docker/docker-compose.tenant.yml` for multi-tenant high availability.
</TASK>

<SUBAGENT_DELEGATION_DIRECTIVE>
- Use `invoke_subagent` if Docker Compose Redis Sentinel service configuration requires research.
</SUBAGENT_DELEGATION_DIRECTIVE>

<ANTIGRAVITY_SLASH_COMMANDS>
- /goal: Execute autonomously until Docker Compose template validates with Redis Sentinel options.
</ANTIGRAVITY_SLASH_COMMANDS>

<ANTIGRAVITY_WORKFLOW>
1. RESEARCH & INSPECTION PHASE:
   - View `infrastructure/docker/docker-compose.tenant.yml`.

2. IMPLEMENTATION PHASE:
   - Target file: `infrastructure/docker/docker-compose.tenant.yml`
   - Add commented/configurable Redis Sentinel high-availability service definitions (`redis-master`, `redis-replica`, `redis-sentinel`).

3. EMPIRICAL VERIFICATION & TESTING PHASE:
   - Run Docker compose config validation: `docker compose -f infrastructure/docker/docker-compose.tenant.yml config`

4. PROCESS CLEANUP & LEARNING DIRECTIVE (CRITICAL):
   - Terminate any active subagents or background tasks before completing turn.
</ANTIGRAVITY_WORKFLOW>

<ACCEPTANCE_CRITERIA>
- [ ] `docker-compose.tenant.yml` includes Redis Sentinel high-availability service options.
- [ ] Docker Compose config passes validation cleanly.
- [ ] All subagents and background tasks are cleanly terminated.
</ACCEPTANCE_CRITERIA>
```
