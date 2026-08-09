# Master Developer Prompt Pack: 8.2 Audit Report Fixes (`PROMPT_SEQUENCE_82_LATEST_AUDIT_FIXES.md`)

This prompt pack contains **7 targeted developer prompts** engineered for **Google Antigravity Agentic IDE** to resolve the exact new defects, webhook container state updates, ETA API phone payload formatting, worker queue error re-throwing, storefront layout params bugs, and infrastructure build context alignment identified in the 8.2/10 audit report. Zero older problems are included.

> [!IMPORTANT]
> **Subagent Directive**: Send these 7 prompts sequentially (Prompt 1 through Prompt 7) to your developer Antigravity instance. Every prompt explicitly instructs the agent to delegate research or sub-tasks to subagents (`invoke_subagent`) to maintain clean context and maximize execution speed.

---

## Part 1: Backend Architecture & Integration Remediation (Prompts 1–4)

---
### Developer Prompt 1: Paymob & Bosta Webhook Container State Updates & Raw Error Message Preservation

```markdown
/goal

<TASK>
Invoke Medusa container services on verified webhooks in `paymob/route.ts` and `bosta/route.ts`, and preserve raw API error messages in `bosta/client.ts`.
</TASK>

<SUBAGENT_DELEGATION_DIRECTIVE>
- Use `invoke_subagent` (Role: "Codebase Researcher", TypeName: "research") to inspect Medusa 2.0 container payment session and fulfillment service state update APIs.
</SUBAGENT_DELEGATION_DIRECTIVE>

<ANTIGRAVITY_SLASH_COMMANDS>
- /goal: Execute autonomously until Paymob and Bosta webhook routes update Medusa container database states cleanly.
- /learn: Persist Medusa v2 webhook state synchronization patterns to .gemini/rules.
</ANTIGRAVITY_SLASH_COMMANDS>

<ANTIGRAVITY_WORKFLOW>
1. RESEARCH & INSPECTION PHASE:
   - View `apps/backend/src/api/hooks/paymob/route.ts`, `apps/backend/src/api/hooks/bosta/route.ts`, and `apps/backend/src/modules/bosta/client.ts`.

2. IMPLEMENTATION PHASE:
   - Target files: `apps/backend/src/api/hooks/paymob/route.ts`, `apps/backend/src/api/hooks/bosta/route.ts`, `apps/backend/src/modules/bosta/client.ts`
   - **`paymob/route.ts`**: Upon HMAC signature verification, resolve `paymentModuleService` from container (`req.scope.resolve`) and invoke `authorizePayment` / payment session state updates to update cart/order payment state in Medusa database.
   - **`bosta/client.ts`**: Preserve original API error status codes and 400 error message details in thrown errors so `bosta-fulfillment-workflow.ts` can detect duplicate reference errors.
   - **`bosta/route.ts`**: Update fulfillment status handlers to call Medusa v2 fulfillment service APIs (`fulfillmentModuleService.updateFulfillment`).

3. EMPIRICAL VERIFICATION & TESTING PHASE:
   - Run TypeScript check: `cd apps/backend && npx tsc --noEmit`
   - Run backend build verification: `cd apps/backend && npm run build`

4. PROCESS CLEANUP & LEARNING DIRECTIVE (CRITICAL):
   - Execute `/learn` to store Medusa webhook container update patterns.
   - Terminate any running subagents, background dev servers, or processes before completing turn.
</ANTIGRAVITY_WORKFLOW>

<ACCEPTANCE_CRITERIA>
- [ ] Subagents delegated for Medusa container service resolution inspection.
- [ ] Paymob webhook route updates order/payment state in Medusa database upon verified payload delivery.
- [ ] Bosta client preserves 400 error message details for duplicate reference checks.
- [ ] Backend build completes with exit code 0.
- [ ] All subagents and background tasks are cleanly terminated.
</ACCEPTANCE_CRITERIA>
```

---
### Developer Prompt 2: ETA API Phone Payload Unencrypted Formatting & Full Retry Payload Preservation

```markdown
/goal

<TASK>
Pass unencrypted customer phone numbers in external ETA API payloads in `order-placed-eta.ts` and preserve complete order item payloads in `background-queue.ts` retry jobs.
</TASK>

<SUBAGENT_DELEGATION_DIRECTIVE>
- Delegate ETA API payload formatting and BullMQ job retry data payload inspection to a subagent via `invoke_subagent`.
</SUBAGENT_DELEGATION_DIRECTIVE>

<ANTIGRAVITY_SLASH_COMMANDS>
- /goal: Execute autonomously until ETA API payload uses raw phone strings and background retry jobs preserve complete item payloads.
- /learn: Persist ETA tax payload formatting rules to .gemini/rules.
</ANTIGRAVITY_SLASH_COMMANDS>

<ANTIGRAVITY_WORKFLOW>
1. RESEARCH & INSPECTION PHASE:
   - View `apps/backend/src/subscribers/order-placed-eta.ts` and `apps/backend/src/jobs/background-queue.ts`.

2. IMPLEMENTATION PHASE:
   - Target files: `apps/backend/src/subscribers/order-placed-eta.ts`, `apps/backend/src/jobs/background-queue.ts`
   - **`order-placed-eta.ts`**: Pass raw customer phone numbers (`+201XXXXXXXXX`) to the external ETA API payload (`buyer.phone`), maintaining AES-256 PII encryption strictly for local `EtaReceiptAudit` audit logs to prevent production portal validation rejection.
   - **`background-queue.ts`**: In `handleEtaSubmissionFailure`, enqueue retry jobs containing complete items and buyer payloads so worker retries submit actual order data rather than fallback mock items.

3. EMPIRICAL VERIFICATION & TESTING PHASE:
   - Run TypeScript check: `cd apps/backend && npx tsc --noEmit`
   - Run backend build verification: `cd apps/backend && npm run build`

4. PROCESS CLEANUP & LEARNING DIRECTIVE (CRITICAL):
   - Execute `/learn` to store ETA tax payload rules.
   - Terminate any running subagents, background dev servers, or processes before completing turn.
</ANTIGRAVITY_WORKFLOW>

<ACCEPTANCE_CRITERIA>
- [ ] Subagents delegated for ETA payload and queue job data inspection.
- [ ] External ETA API payload uses unencrypted mobile phone strings.
- [ ] AES-256 PII encryption retained for local database audit logs.
- [ ] Retry jobs preserve full item and buyer payloads.
- [ ] Backend build completes with exit code 0.
- [ ] All subagents and background tasks are cleanly terminated.
</ACCEPTANCE_CRITERIA>
```

---
### Developer Prompt 3: Automated ETA OAuth2 Token Refresh Client (`https://id.eta.gov.eg/connect/token`)

```markdown
/goal

<TASK>
Implement automated OAuth2 client credentials token refresh in `apps/backend/src/modules/eta-tax/client.ts` targeting `https://id.eta.gov.eg/connect/token`.
</TASK>

<SUBAGENT_DELEGATION_DIRECTIVE>
- Use `invoke_subagent` to inspect Egyptian Tax Authority (ETA) OAuth2 Identity Server token endpoint specs.
</SUBAGENT_DELEGATION_DIRECTIVE>

<ANTIGRAVITY_SLASH_COMMANDS>
- /goal: Execute autonomously until ETA client automatically refreshes OAuth2 access tokens upon expiration.
- /browser: Verify ETA Identity Server `/connect/token` client credentials payload specs.
- /learn: Persist OAuth2 token lifecycle management rules to .gemini/rules.
</ANTIGRAVITY_SLASH_COMMANDS>

<ANTIGRAVITY_WORKFLOW>
1. RESEARCH & INSPECTION PHASE:
   - View `apps/backend/src/modules/eta-tax/client.ts`.

2. IMPLEMENTATION PHASE:
   - Target file: `apps/backend/src/modules/eta-tax/client.ts`
   - Implement `getAccessToken()` method in `EtaClient` requesting OAuth2 client credentials token from `https://id.eta.gov.eg/connect/token` using `client_id` and `client_secret`.
   - Cache access token in memory with expiry buffer, automatically refreshing tokens when expired (60-minute TTL) before making e-receipt submission calls.

3. EMPIRICAL VERIFICATION & TESTING PHASE:
   - Run TypeScript check: `cd apps/backend && npx tsc --noEmit`
   - Run backend build verification: `cd apps/backend && npm run build`

4. PROCESS CLEANUP & LEARNING DIRECTIVE (CRITICAL):
   - Execute `/learn` to store OAuth2 token refresh rules.
   - Terminate any running subagents, background dev servers, or processes before completing turn.
</ANTIGRAVITY_WORKFLOW>

<ACCEPTANCE_CRITERIA>
- [ ] Subagents delegated for ETA OAuth2 identity server endpoint research.
- [ ] `EtaClient` includes `getAccessToken()` client credentials token refresh logic.
- [ ] Access tokens automatically refresh upon expiration without requiring backend restarts.
- [ ] Backend build completes with exit code 0.
- [ ] All subagents and background tasks are cleanly terminated.
</ACCEPTANCE_CRITERIA>
```

---
### Developer Prompt 4: Gemini AI Worker Error Re-Throwing for Queue Retries & Prompt `keyFeatures` Concatenation

```markdown
/goal

<TASK>
Re-throw unhandled exceptions in `ai-copywriter-worker.ts` for BullMQ queue retries and concatenate `keyFeatures` in `gemini-ai/client.ts`.
</TASK>

<SUBAGENT_DELEGATION_DIRECTIVE>
- Use `invoke_subagent` to inspect BullMQ worker exception propagation and prompt string construction.
</SUBAGENT_DELEGATION_DIRECTIVE>

<ANTIGRAVITY_SLASH_COMMANDS>
- /goal: Execute autonomously until Gemini AI copywriter worker error propagation and prompt features compile clean.
- /learn: Persist BullMQ worker error handling rules to .gemini/rules.
</ANTIGRAVITY_SLASH_COMMANDS>

<ANTIGRAVITY_WORKFLOW>
1. RESEARCH & INSPECTION PHASE:
   - View `apps/backend/src/jobs/ai-copywriter-worker.ts` and `apps/backend/src/modules/gemini-ai/client.ts`.

2. IMPLEMENTATION PHASE:
   - Target files: `apps/backend/src/jobs/ai-copywriter-worker.ts`, `apps/backend/src/modules/gemini-ai/client.ts`
   - **`ai-copywriter-worker.ts`**: Update `processAiCopywriterJob` to re-throw unhandled errors in catch block (`throw error`) so BullMQ queue triggers exponential backoff retries and DLQ routing instead of returning a false success object.
   - **`gemini-ai/client.ts`**: Include `keyFeatures` array parameter during prompt string concatenation when generating product copywriting prompts.

3. EMPIRICAL VERIFICATION & TESTING PHASE:
   - Run TypeScript check: `cd apps/backend && npx tsc --noEmit`
   - Run backend build verification: `cd apps/backend && npm run build`

4. PROCESS CLEANUP & LEARNING DIRECTIVE (CRITICAL):
   - Execute `/learn` to store BullMQ worker exception rules.
   - Terminate any running subagents, background dev servers, or processes before completing turn.
</ANTIGRAVITY_WORKFLOW>

<ACCEPTANCE_CRITERIA>
- [ ] Subagents delegated for BullMQ worker error handling inspection.
- [ ] `processAiCopywriterJob` re-throws errors to trigger BullMQ queue retries and DLQ alerts.
- [ ] Prompt string builder incorporates `keyFeatures` input parameter.
- [ ] Backend build completes with exit code 0.
- [ ] All subagents and background tasks are cleanly terminated.
</ACCEPTANCE_CRITERIA>
```

---

## Part 2: Storefront & Infrastructure Optimizations (Prompts 5–7)

---
### Developer Prompt 5: Move Storefront Dynamic RTL/LTR Layout to `[countryCode]/layout.tsx` & Update Tailwind Scanner

```markdown
/goal

<TASK>
Move dynamic `lang` and `dir` HTML attributes to `apps/storefront/src/app/[countryCode]/layout.tsx` and add `./src/modules/**/*.tsx` to `tailwind.config.ts`.
</TASK>

<SUBAGENT_DELEGATION_DIRECTIVE>
- Delegate Next.js 15 App Router layout parameter routing and Tailwind CSS content path scanning to a subagent via `invoke_subagent`.
</SUBAGENT_DELEGATION_DIRECTIVE>

<ANTIGRAVITY_SLASH_COMMANDS>
- /goal: Execute autonomously until Storefront RTL/LTR dynamic layout switching and Tailwind module scanning build cleanly.
- /learn: Persist Next.js 15 layout parameter routing rules to .gemini/rules.
</ANTIGRAVITY_SLASH_COMMANDS>

<ANTIGRAVITY_WORKFLOW>
1. RESEARCH & INSPECTION PHASE:
   - View `apps/storefront/src/app/layout.tsx`, `apps/storefront/src/app/[countryCode]/layout.tsx`, and `apps/storefront/tailwind.config.ts`.

2. IMPLEMENTATION PHASE:
   - Target files: `apps/storefront/src/app/layout.tsx`, `apps/storefront/src/app/[countryCode]/layout.tsx`, `apps/storefront/tailwind.config.ts`
   - **`layout.tsx`**: Remove route params reading from root layout file; render clean `<html>` container.
   - **`[countryCode]/layout.tsx`**: Read `countryCode` / `locale` segment parameter and dynamically pass `lang` and `dir` (`rtl` for Arabic, `ltr` for English) to layout wrapper.
   - **`tailwind.config.ts`**: Add `./src/modules/**/*.{js,ts,jsx,tsx}` to `content` array so module component styles are preserved in production builds.

3. EMPIRICAL VERIFICATION & TESTING PHASE:
   - Run storefront build verification: `cd apps/storefront && npm run build`

4. PROCESS CLEANUP & LEARNING DIRECTIVE (CRITICAL):
   - Terminate any running subagents, background dev servers (e.g. `next dev`) before completing turn.
</ANTIGRAVITY_WORKFLOW>

<ACCEPTANCE_CRITERIA>
- [ ] Subagents delegated for Next.js layout segment research.
- [ ] Segment layout `[countryCode]/layout.tsx` handles dynamic `lang` and `dir` attributes.
- [ ] `tailwind.config.ts` content array includes `./src/modules/**/*.{js,ts,jsx,tsx}`.
- [ ] Storefront build completes with exit code 0.
- [ ] All subagents, background tasks, and dev servers are cleanly terminated.
</ACCEPTANCE_CRITERIA>
```

---
### Developer Prompt 6: Storefront Cart Context Pure Updaters & Strict `variantId` Validation on Add-to-Cart

```markdown
/goal

<TASK>
Make `setState` updater callbacks pure in `cart-context.tsx` and require valid `variantId` in `add-to-cart-button.tsx`.
</TASK>

<SUBAGENT_DELEGATION_DIRECTIVE>
- Use `invoke_subagent` to inspect React state updater purity and Medusa JS SDK line item payload validation.
</SUBAGENT_DELEGATION_DIRECTIVE>

<ANTIGRAVITY_SLASH_COMMANDS>
- /goal: Execute autonomously until Storefront Cart Context state updaters and Add-to-Cart variant validation pass build tests.
</ANTIGRAVITY_SLASH_COMMANDS>

<ANTIGRAVITY_WORKFLOW>
1. RESEARCH & INSPECTION PHASE:
   - View `apps/storefront/src/lib/context/cart-context.tsx` and `apps/storefront/src/modules/products/components/add-to-cart-button.tsx`.

2. IMPLEMENTATION PHASE:
   - Target files: `apps/storefront/src/lib/context/cart-context.tsx`, `apps/storefront/src/modules/products/components/add-to-cart-button.tsx`
   - **`cart-context.tsx`**: Move `broadcastCartState` side-effect calls outside of `setItems` updater functions to keep React state updaters pure.
   - **`add-to-cart-button.tsx`**: Validate `variantId` string before calling `addItem`, preventing product IDs from being sent as fallback `variant_id` to Medusa's line item API.

3. EMPIRICAL VERIFICATION & TESTING PHASE:
   - Run storefront build verification: `cd apps/storefront && npm run build`

4. PROCESS CLEANUP & LEARNING DIRECTIVE (CRITICAL):
   - Terminate any running subagents, background dev servers, or processes before completing turn.
</ANTIGRAVITY_WORKFLOW>

<ACCEPTANCE_CRITERIA>
- [ ] Subagents delegated for React state updater purity inspection.
- [ ] `cart-context.tsx` state updater callbacks are pure; side-effects run after state updates.
- [ ] `add-to-cart-button.tsx` validates `variantId` before calling `addItem`.
- [ ] Storefront build completes with exit code 0.
- [ ] All subagents and background tasks are cleanly terminated.
</ACCEPTANCE_CRITERIA>
```

---
### Developer Prompt 7: Tenant Provisioning Docker Root Build Context, Caddy Guard Clause, & Storefront Backend Health Dependency

```markdown
/goal

<TASK>
Update repository root Docker build context in `provision-tenant.sh`, add `Caddyfile` domain guard in `caddy-domain-router.sh`, and set storefront `depends_on` in `docker-compose.tenant.yml`.
</TASK>

<SUBAGENT_DELEGATION_DIRECTIVE>
- Use `invoke_subagent` to inspect Docker Compose repository root build context and Caddyfile guard scripts.
</SUBAGENT_DELEGATION_DIRECTIVE>

<ANTIGRAVITY_SLASH_COMMANDS>
- /goal: Execute autonomously until Docker build context, Caddy router guards, and storefront container dependencies validate cleanly.
- /learn: Persist DevOps container dependency rules to .gemini/rules.
</ANTIGRAVITY_SLASH_COMMANDS>

<ANTIGRAVITY_WORKFLOW>
1. RESEARCH & INSPECTION PHASE:
   - View `infrastructure/scripts/provision-tenant.sh`, `infrastructure/scripts/caddy-domain-router.sh`, and `infrastructure/docker/docker-compose.tenant.yml`.

2. IMPLEMENTATION PHASE:
   - Target files: `infrastructure/scripts/provision-tenant.sh`, `infrastructure/scripts/caddy-domain-router.sh`, `infrastructure/docker/docker-compose.tenant.yml`
   - **`provision-tenant.sh`**: Execute `docker compose` commands with explicit repository root context (`-f "${TENANT_DIR}/infrastructure/docker/docker-compose.tenant.yml"` running from repo root) so multi-stage Dockerfiles access `/packages/shared-types`.
   - **`caddy-domain-router.sh`**: Add `grep -q "${CUSTOM_DOMAIN}"` guard clause prior to appending fallback configuration blocks to avoid duplicate domain blocks.
   - **`docker-compose.tenant.yml`**: Update storefront service to specify `depends_on: { backend: { condition: service_healthy } }`.

3. EMPIRICAL VERIFICATION & TESTING PHASE:
   - Run Docker compose config validation: `docker compose -f infrastructure/docker/docker-compose.tenant.yml config`
   - Run bash syntax check: `bash -n infrastructure/scripts/provision-tenant.sh` and `bash -n infrastructure/scripts/caddy-domain-router.sh`

4. PROCESS CLEANUP & LEARNING DIRECTIVE (CRITICAL):
   - Terminate any active subagents or background tasks before completing turn.
</ANTIGRAVITY_WORKFLOW>

<ACCEPTANCE_CRITERIA>
- [ ] Subagents delegated for Docker build context inspection.
- [ ] `provision-tenant.sh` executes Docker compose with repository root build context.
- [ ] `caddy-domain-router.sh` prevents duplicate domain config blocks.
- [ ] Storefront depends on backend `service_healthy` condition in Docker compose.
- [ ] Docker Compose config and bash scripts pass validation tests.
- [ ] All subagents and background tasks are cleanly terminated.
</ACCEPTANCE_CRITERIA>
```
