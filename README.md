# Master Developer Prompt Pack: Latest Codebase Audit Fixes (`PROMPT_SEQUENCE_LATEST_AUDIT.md`)

This prompt pack contains **11 hyper-focused developer prompts** engineered for **Google Antigravity Agentic IDE** to resolve every critical bug, security vulnerability, financial logic gap, and deployment issue identified in the latest codebase evaluation report. Zero older problems are included.

> [!IMPORTANT]
> **Subagent Directive**: Every prompt explicitly instructs the receiving Antigravity agent to invoke subagents (`invoke_subagent`) for codebase research, file inspections, or parallel sub-tasks to maintain clean context and maximize execution speed.

---

## Part 1: Backend Core, Security & Financial API Fixes (Prompts 1–6)

---
### Developer Prompt 1: Strict Production CORS & Bosta Webhook HMAC Signature Verification

```markdown
/goal

<TASK>
Enforce strict production CORS fallbacks in `medusa-config.ts` and implement Bosta webhook HMAC signature verification in `apps/backend/src/api/hooks/bosta/route.ts`.
</TASK>

<SUBAGENT_DELEGATION_DIRECTIVE>
- Use `invoke_subagent` (Role: "Codebase Researcher", TypeName: "research") to inspect Bosta webhook authentication documentation and HMAC header validation.
</SUBAGENT_DELEGATION_DIRECTIVE>

<ANTIGRAVITY_SLASH_COMMANDS>
- /goal: Execute autonomously until Bosta webhook HMAC verification and CORS safety pass backend build checks.
- /learn: Persist webhook security and HMAC verification rules to .gemini/rules.
</ANTIGRAVITY_SLASH_COMMANDS>

<ANTIGRAVITY_WORKFLOW>
1. RESEARCH & INSPECTION PHASE:
   - View `apps/backend/medusa-config.ts` (lines 10–12) and `apps/backend/src/api/hooks/bosta/route.ts` (lines 15–24).

2. IMPLEMENTATION PHASE:
   - Target files: `apps/backend/medusa-config.ts`, `apps/backend/src/api/hooks/bosta/route.ts`
   - **`medusa-config.ts`**: Throw an error if CORS environment variables (`STORE_CORS`, `ADMIN_CORS`) are missing in production (`process.env.NODE_ENV === "production"`) instead of exposing `localhost` development ports.
   - **`bosta/route.ts`**: Validate incoming Bosta webhook signature headers (`x-bosta-signature` or `authorization`) against `process.env.BOSTA_WEBHOOK_SECRET`. Return HTTP `401 Unauthorized` if signature is missing or invalid.

3. EMPIRICAL VERIFICATION & TESTING PHASE:
   - Run TypeScript check: `cd apps/backend && npx tsc --noEmit`
   - Run backend build verification: `cd apps/backend && npm run build`

4. PROCESS CLEANUP & LEARNING DIRECTIVE (CRITICAL):
   - Execute `/learn` to store Bosta webhook security patterns.
   - Terminate any running subagents, background dev servers, or processes before completing turn.
</ANTIGRAVITY_WORKFLOW>

<ACCEPTANCE_CRITERIA>
- [ ] Subagents delegated for Bosta webhook HMAC header research.
- [ ] `medusa-config.ts` throws error in production if CORS origins are unconfigured.
- [ ] Bosta webhook endpoint returns HTTP `401 Unauthorized` on missing or invalid signature.
- [ ] Backend build completes with exit code 0.
- [ ] All subagents, background tasks, and dev servers are cleanly terminated.
</ACCEPTANCE_CRITERIA>
```

---
### Developer Prompt 2: Implement Real Paymob `authorizePayment` & `capturePayment` API Calls + Compensation Void

```markdown
/goal

<TASK>
Implement real HTTP requests for `authorizePayment` and `capturePayment` in `apps/backend/src/modules/paymob/service.ts`, and add `voidTransaction` API call in `paymob-payment-workflow.ts` compensation step.
</TASK>

<SUBAGENT_DELEGATION_DIRECTIVE>
- Use `invoke_subagent` (Role: "Codebase Researcher", TypeName: "research") to inspect Paymob REST API authorization, capture, and void/refund endpoint specs.
</SUBAGENT_DELEGATION_DIRECTIVE>

<ANTIGRAVITY_SLASH_COMMANDS>
- /goal: Execute autonomously until Paymob payment authorization, capture, and workflow void compensations compile clean.
- /browser: Use browser to verify Paymob capture and void endpoint specifications.
- /learn: Persist Paymob financial integration patterns to .gemini/rules.
</ANTIGRAVITY_SLASH_COMMANDS>

<ANTIGRAVITY_WORKFLOW>
1. RESEARCH & INSPECTION PHASE:
   - View `apps/backend/src/modules/paymob/service.ts` (lines 114–135) and `apps/backend/src/workflows/paymob-payment-workflow.ts`.

2. IMPLEMENTATION PHASE:
   - Target files: `apps/backend/src/modules/paymob/client.ts`, `apps/backend/src/modules/paymob/service.ts`, `apps/backend/src/workflows/paymob-payment-workflow.ts`
   - Replace stubbed `{ status: "authorized" }` returns in `authorizePayment()` and `capturePayment()` with real HTTP POST requests to Paymob capture and auth APIs.
   - In `paymob-payment-workflow.ts` compensation step, execute live HTTP POST request to Paymob void endpoint (`/api/acceptance/void_refund/void`) when downstream workflow steps fail.

3. EMPIRICAL VERIFICATION & TESTING PHASE:
   - Run TypeScript check: `cd apps/backend && npx tsc --noEmit`
   - Run backend build verification: `cd apps/backend && npm run build`

4. PROCESS CLEANUP & LEARNING DIRECTIVE (CRITICAL):
   - Execute `/learn` to store Paymob financial workflow patterns.
   - Terminate any running subagents, background dev servers, or processes before completing turn.
</ANTIGRAVITY_WORKFLOW>

<ACCEPTANCE_CRITERIA>
- [ ] Subagents invoked for Paymob capture/void REST API research.
- [ ] `authorizePayment()` and `capturePayment()` in `service.ts` call live Paymob REST APIs.
- [ ] `paymob-payment-workflow.ts` compensation step calls Paymob void API on failure.
- [ ] Backend build completes with exit code 0.
- [ ] All subagents, background tasks, and dev servers are cleanly terminated.
</ACCEPTANCE_CRITERIA>
```

---
### Developer Prompt 3: Dynamic Medusa Line Item Tax Resolution in ETA Tax Payload Builder

```markdown
/goal

<TASK>
Dynamically calculate ETA e-Receipt tax rates from Medusa order tax lines in `apps/backend/src/modules/eta-tax/payload-builder.ts` instead of hardcoding 14% VAT (`T1/V009`).
</TASK>

<SUBAGENT_DELEGATION_DIRECTIVE>
- Delegate Medusa Query Graph tax line inspection to a `research` subagent via `invoke_subagent`.
</SUBAGENT_DELEGATION_DIRECTIVE>

<ANTIGRAVITY_SLASH_COMMANDS>
- /goal: Execute autonomously until ETA e-Receipt tax calculations dynamically map Medusa order tax lines.
</ANTIGRAVITY_SLASH_COMMANDS>

<ANTIGRAVITY_WORKFLOW>
1. RESEARCH & INSPECTION PHASE:
   - View `apps/backend/src/modules/eta-tax/payload-builder.ts` (line 132).

2. IMPLEMENTATION PHASE:
   - Target file: `apps/backend/src/modules/eta-tax/payload-builder.ts`
   - Inspect Medusa line item `tax_lines` or order tax rate metadata.
   - Dynamically compute item tax amounts and map tax types (`T1` for standard 14% VAT, `V001`–`V009` based on tax line rate) instead of hardcoding fixed 14% VAT (`T1/V009`) across all items.

3. EMPIRICAL VERIFICATION & TESTING PHASE:
   - Run TypeScript check: `cd apps/backend && npx tsc --noEmit`
   - Run backend build verification: `cd apps/backend && npm run build`

4. PROCESS CLEANUP & LEARNING DIRECTIVE (CRITICAL):
   - Terminate any running subagents, background processes, or dev servers before completing turn.
</ANTIGRAVITY_WORKFLOW>

<ACCEPTANCE_CRITERIA>
- [ ] Subagents delegated to inspect Medusa Order tax line schemas.
- [ ] ETA payload builder dynamically maps tax types and rates from Medusa order tax lines.
- [ ] Backend build completes with exit code 0.
- [ ] All subagents, background tasks, and dev servers are cleanly terminated.
</ACCEPTANCE_CRITERIA>
```

---
### Developer Prompt 4: Fix Gemini AI Model Target Identifier & Model Execution Safety

```markdown
/goal

<TASK>
Fix hallucinated model target identifier `"gemma-4-31b-it"` in `apps/backend/src/modules/gemini-ai/client.ts` to a valid Google AI Studio model identifier.
</TASK>

<SUBAGENT_DELEGATION_DIRECTIVE>
- Use `invoke_subagent` to check Google AI Studio SDK model string specifications.
</SUBAGENT_DELEGATION_DIRECTIVE>

<ANTIGRAVITY_SLASH_COMMANDS>
- /goal: Execute autonomously until Gemini AI client uses valid Google AI Studio model targets.
</ANTIGRAVITY_SLASH_COMMANDS>

<ANTIGRAVITY_WORKFLOW>
1. RESEARCH & INSPECTION PHASE:
   - View `apps/backend/src/modules/gemini-ai/client.ts` (line 25).

2. IMPLEMENTATION PHASE:
   - Target file: `apps/backend/src/modules/gemini-ai/client.ts`
   - Replace hallucinated model string `"gemma-4-31b-it"` on line 25 with `process.env.GEMINI_MODEL || "gemini-1.5-flash"` (or `"gemini-1.5-pro"`).
   - Ensure model execution calls Google AI Studio SDK safely without model initialization crashes.

3. EMPIRICAL VERIFICATION & TESTING PHASE:
   - Run TypeScript check: `cd apps/backend && npx tsc --noEmit`
   - Run backend build verification: `cd apps/backend && npm run build`

4. PROCESS CLEANUP & LEARNING DIRECTIVE (CRITICAL):
   - Terminate any running subagents, background processes, or dev servers before completing turn.
</ANTIGRAVITY_WORKFLOW>

<ACCEPTANCE_CRITERIA>
- [ ] Line 25 of `gemini-ai/client.ts` uses valid Google AI Studio model string (`gemini-1.5-flash` / `gemini-1.5-pro`).
- [ ] Backend build completes with exit code 0.
- [ ] All subagents, background tasks, and dev servers are cleanly terminated.
</ACCEPTANCE_CRITERIA>
```

---
### Developer Prompt 5: Fix ETA Subscriber Method Call & Postgres Audit ENUM Schema

```markdown
/goal

<TASK>
Fix method call runtime crash on line 85 of `order-placed-eta.ts` and update Postgres ENUM schema in `models/eta-audit.ts` to include `"FAILED_DLQ"`.
</TASK>

<SUBAGENT_DELEGATION_DIRECTIVE>
- Use `invoke_subagent` to inspect `EtaTaxModuleService` exported methods and `EtaReceiptAudit` entity annotations.
</SUBAGENT_DELEGATION_DIRECTIVE>

<ANTIGRAVITY_SLASH_COMMANDS>
- /goal: Execute autonomously until ETA subscriber method call and audit ENUM schema pass build checks.
- /learn: Persist Medusa entity ENUM schema rules to .gemini/rules.
</ANTIGRAVITY_SLASH_COMMANDS>

<ANTIGRAVITY_WORKFLOW>
1. RESEARCH & INSPECTION PHASE:
   - View `apps/backend/src/subscribers/order-placed-eta.ts` (lines 85 & 137) and `apps/backend/src/modules/eta-tax/models/eta-audit.ts`.

2. IMPLEMENTATION PHASE:
   - Target files: `apps/backend/src/subscribers/order-placed-eta.ts`, `apps/backend/src/modules/eta-tax/models/eta-audit.ts`
   - **Line 85**: Change `etaTaxModuleService.submitReceipt(...)` to `etaTaxModuleService.submitAndAuditReceipt(...)` to eliminate runtime `TypeError: submitReceipt is not a function` crash.
   - **`models/eta-audit.ts`**: Add `"FAILED_DLQ"` to `EtaAuditStatus` ENUM definition so database writes on line 137 do not violate Postgres ENUM constraints.

3. EMPIRICAL VERIFICATION & TESTING PHASE:
   - Run TypeScript check: `cd apps/backend && npx tsc --noEmit`
   - Run backend build verification: `cd apps/backend && npm run build`

4. PROCESS CLEANUP & LEARNING DIRECTIVE (CRITICAL):
   - Execute `/learn` to store Medusa v2 entity ENUM rules.
   - Terminate any running subagents or processes before completing turn.
</ANTIGRAVITY_WORKFLOW>

<ACCEPTANCE_CRITERIA>
- [ ] Line 85 of `order-placed-eta.ts` calls `submitAndAuditReceipt`.
- [ ] `EtaAuditStatus` ENUM in `models/eta-audit.ts` includes `"FAILED_DLQ"`.
- [ ] Backend build completes with exit code 0.
- [ ] All subagents, background tasks, and dev servers are cleanly terminated.
</ACCEPTANCE_CRITERIA>
```

---
### Developer Prompt 6: Replace Runtime `process.env` Global Mutation in Subscription Listener

```markdown
/goal

<TASK>
Replace global `process.env.TENANT_STATUS` mutation in `apps/backend/src/subscribers/subscription-listener.ts` with scoped tenant database status flags.
</TASK>

<SUBAGENT_DELEGATION_DIRECTIVE>
- Spawn a `research` subagent via `invoke_subagent` to research per-tenant context isolation patterns in Medusa v2 multi-tenancy.
</SUBAGENT_DELEGATION_DIRECTIVE>

<ANTIGRAVITY_SLASH_COMMANDS>
- /goal: Execute autonomously until subscription listener tenant state isolation compiles clean.
- /learn: Persist multi-tenant state isolation rules to .gemini/rules.
</ANTIGRAVITY_SLASH_COMMANDS>

<ANTIGRAVITY_WORKFLOW>
1. RESEARCH & INSPECTION PHASE:
   - View `apps/backend/src/subscribers/subscription-listener.ts` (line 34).

2. IMPLEMENTATION PHASE:
   - Target file: `apps/backend/src/subscribers/subscription-listener.ts`
   - Remove `process.env.TENANT_STATUS = "SOFT_SUSPENDED"` on line 34 (which globally suspends all tenants running on the Node process).
   - Update tenant status in the tenant database record or scoped Redis tenant metadata store instead of mutating Node process environment variables at runtime.

3. EMPIRICAL VERIFICATION & TESTING PHASE:
   - Run TypeScript check: `cd apps/backend && npx tsc --noEmit`
   - Run backend build verification: `cd apps/backend && npm run build`

4. PROCESS CLEANUP & LEARNING DIRECTIVE (CRITICAL):
   - Execute `/learn` to store multi-tenant isolation rules.
   - Terminate any running subagents, background dev servers, or processes before completing turn.
</ANTIGRAVITY_WORKFLOW>

<ACCEPTANCE_CRITERIA>
- [ ] Line 34 of `subscription-listener.ts` does NOT mutate `process.env.TENANT_STATUS`.
- [ ] Tenant suspension flags persist to database/Redis scoped tenant metadata.
- [ ] Backend build completes with exit code 0.
- [ ] All subagents, background tasks, and dev servers are cleanly terminated.
</ACCEPTANCE_CRITERIA>
```

---

## Part 2: Storefront Performance & Architectural Fixes (Prompts 7–9)

---
### Developer Prompt 7: Fix Storefront Layout Font Duplication, `metadataBase`, & LCP/CLS Optimization

```markdown
/goal

<TASK>
Remove duplicate Google Font `<link>` imports in `apps/storefront/src/app/layout.tsx`, use `next/font/google`, and add `metadataBase`.
</TASK>

<SUBAGENT_DELEGATION_DIRECTIVE>
- Delegate inspection of Next.js 15 layout font configuration to a subagent via `invoke_subagent`.
</SUBAGENT_DELEGATION_DIRECTIVE>

<ANTIGRAVITY_SLASH_COMMANDS>
- /goal: Execute autonomously until storefront layout font optimization and metadata pass build checks.
</ANTIGRAVITY_SLASH_COMMANDS>

<ANTIGRAVITY_WORKFLOW>
1. RESEARCH & INSPECTION PHASE:
   - View `apps/storefront/src/app/layout.tsx` (lines 41–44).

2. IMPLEMENTATION PHASE:
   - Target file: `apps/storefront/src/app/layout.tsx`
   - Remove duplicate Google Font `<link rel="stylesheet">` tags on lines 41–44. Keep `next/font/google` font loader (`Cairo` / `Inter`) to prevent layout shift (CLS) and LCP render blocking.
   - Add `metadataBase: new URL(process.env.NEXT_PUBLIC_STORE_URL || "https://egyptbrand.com")` in `export const metadata`.

3. EMPIRICAL VERIFICATION & TESTING PHASE:
   - Run storefront build verification: `cd apps/storefront && npm run build`

4. PROCESS CLEANUP & LEARNING DIRECTIVE (CRITICAL):
   - Terminate any running subagents, background dev servers (e.g. `next dev`) before completing turn.
</ANTIGRAVITY_WORKFLOW>

<ACCEPTANCE_CRITERIA>
- [ ] `layout.tsx` contains zero duplicate `<link>` font tags; uses `next/font/google`.
- [ ] Metadata includes valid `metadataBase` configuration.
- [ ] Storefront build completes with exit code 0.
- [ ] All subagents, background tasks, and dev servers are cleanly terminated.
</ACCEPTANCE_CRITERIA>
```

---
### Developer Prompt 8: Server-Side Order & Bosta Tracking Creation in Storefront Checkout

```markdown
/goal

<TASK>
Move order ID and Bosta tracking string generation from client-side state in `checkout-view.tsx` to Medusa v2 server-side workflow endpoints.
</TASK>

<SUBAGENT_DELEGATION_DIRECTIVE>
- Use `invoke_subagent` to inspect Medusa JS SDK server-side checkout complete endpoints (`sdk.store.carts.complete()`).
</SUBAGENT_DELEGATION_DIRECTIVE>

<ANTIGRAVITY_SLASH_COMMANDS>
- /goal: Execute autonomously until checkout complete workflow runs server-side with Medusa SDK.
- /learn: Persist Medusa v2 checkout completion patterns to .gemini/rules.
</ANTIGRAVITY_SLASH_COMMANDS>

<ANTIGRAVITY_WORKFLOW>
1. RESEARCH & INSPECTION PHASE:
   - View `apps/storefront/src/modules/checkout/components/checkout-view.tsx` (lines 31–43).

2. IMPLEMENTATION PHASE:
   - Target file: `apps/storefront/src/modules/checkout/components/checkout-view.tsx`
   - Remove client-side order ID generation (`"ORD_" + Math.random()`) and client Bosta tracking strings.
   - Complete cart submission via server-side Medusa API endpoint (`sdk.store.carts.complete()`), receiving canonical order and fulfillment tracking data from the backend.

3. EMPIRICAL VERIFICATION & TESTING PHASE:
   - Run storefront build verification: `cd apps/storefront && npm run build`

4. PROCESS CLEANUP & LEARNING DIRECTIVE (CRITICAL):
   - Execute `/learn` to store Medusa checkout complete rules.
   - Terminate any running subagents, background dev servers, or processes before completing turn.
</ANTIGRAVITY_WORKFLOW>

<ACCEPTANCE_CRITERIA>
- [ ] `checkout-view.tsx` contains zero client-side `Math.random()` order ID or tracking string generation.
- [ ] Order completion executes via server-side Medusa SDK workflow endpoints.
- [ ] Storefront build completes with exit code 0.
- [ ] All subagents, background tasks, and dev servers are cleanly terminated.
</ACCEPTANCE_CRITERIA>
```

---
### Developer Prompt 9: Cart Context Error Handling & API Failure Resilience

```markdown
/goal

<TASK>
Remove silent `.catch(() => {})` error swallowing in `apps/storefront/src/lib/context/cart-context.tsx` and implement error rollback toasts.
</TASK>

<SUBAGENT_DELEGATION_DIRECTIVE>
- Delegate Cart Context state management inspection to a subagent via `invoke_subagent`.
</SUBAGENT_DELEGATION_DIRECTIVE>

<ANTIGRAVITY_SLASH_COMMANDS>
- /goal: Execute autonomously until Cart Context handles API network failures cleanly.
</ANTIGRAVITY_SLASH_COMMANDS>

<ANTIGRAVITY_WORKFLOW>
1. RESEARCH & INSPECTION PHASE:
   - View `apps/storefront/src/lib/context/cart-context.tsx` (lines 121–131).

2. IMPLEMENTATION PHASE:
   - Target file: `apps/storefront/src/lib/context/cart-context.tsx`
   - Remove empty `.catch(() => {})` handlers on lines 121–131.
   - On Medusa SDK API failure: Roll back optimistic UI cart items to previous state and trigger error toast notification (`حدث خطأ أثناء تحديث السلة`).

3. EMPIRICAL VERIFICATION & TESTING PHASE:
   - Run storefront build verification: `cd apps/storefront && npm run build`

4. PROCESS CLEANUP & LEARNING DIRECTIVE (CRITICAL):
   - Terminate any running subagents, background dev servers, or processes before completing turn.
</ANTIGRAVITY_WORKFLOW>

<ACCEPTANCE_CRITERIA>
- [ ] Lines 121–131 of `cart-context.tsx` do NOT contain silent `.catch(() => {})` blocks.
- [ ] Cart Context rolls back optimistic state and notifies user on network/API failure.
- [ ] Storefront build completes with exit code 0.
- [ ] All subagents, background tasks, and dev servers are cleanly terminated.
</ACCEPTANCE_CRITERIA>
```

---

## Part 3: Infrastructure & Security Hardening Fixes (Prompts 10–11)

---
### Developer Prompt 10: Secure Tenant Provisioning Secrets with Cryptographic Random Tokens

```markdown
/goal

<TASK>
Replace predictable epoch timestamp password generation (`date +%s`) in `infrastructure/scripts/provision-tenant.sh` with `openssl rand -base64 32`.
</TASK>

<SUBAGENT_DELEGATION_DIRECTIVE>
- Use `invoke_subagent` if bash token generation syntax verification is required.
</SUBAGENT_DELEGATION_DIRECTIVE>

<ANTIGRAVITY_SLASH_COMMANDS>
- /goal: Execute autonomously until tenant provisioning script generates cryptographically secure secrets.
</ANTIGRAVITY_SLASH_COMMANDS>

<ANTIGRAVITY_WORKFLOW>
1. RESEARCH & INSPECTION PHASE:
   - View `infrastructure/scripts/provision-tenant.sh` (lines 53–59).

2. IMPLEMENTATION PHASE:
   - Target file: `infrastructure/scripts/provision-tenant.sh`
   - Change lines 53–59 from `pass_${TENANT_ID}_$(date +%s)` to cryptographically secure secret generation:
     `openssl rand -base64 32 | tr -dc 'a-zA-Z0-9' | head -c 32` for DB, Redis, and JWT secrets.

3. EMPIRICAL VERIFICATION & TESTING PHASE:
   - Run bash syntax check: `bash -n infrastructure/scripts/provision-tenant.sh`

4. PROCESS CLEANUP & LEARNING DIRECTIVE (CRITICAL):
   - Terminate any running subagents or shell tasks before completing turn.
</ANTIGRAVITY_WORKFLOW>

<ACCEPTANCE_CRITERIA>
- [ ] Lines 53–59 of `provision-tenant.sh` use `openssl rand` for secret generation.
- [ ] Script passes `bash -n` syntax check cleanly.
- [ ] All subagents and background tasks are cleanly terminated.
</ACCEPTANCE_CRITERIA>
```

---
### Developer Prompt 11: Isolate Host Interfaces in Tenant Docker Compose & Input Sanitization in Caddy Router

```markdown
/goal

<TASK>
Remove host port exposure (`5432`, `6379`) in `docker-compose.tenant.yml` and sanitize custom domain inputs in `caddy-domain-router.sh`.
</TASK>

<SUBAGENT_DELEGATION_DIRECTIVE>
- Delegate Docker Compose network isolation and bash domain regex sanitization to a subagent via `invoke_subagent`.
</SUBAGENT_DELEGATION_DIRECTIVE>

<ANTIGRAVITY_SLASH_COMMANDS>
- /goal: Execute autonomously until Docker Compose template and Caddy domain router pass security validation.
</ANTIGRAVITY_SLASH_COMMANDS>

<ANTIGRAVITY_WORKFLOW>
1. RESEARCH & INSPECTION PHASE:
   - View `infrastructure/docker/docker-compose.tenant.yml` (lines 12–13) and `infrastructure/scripts/caddy-domain-router.sh` (line 32).

2. IMPLEMENTATION PHASE:
   - Target files: `infrastructure/docker/docker-compose.tenant.yml`, `infrastructure/scripts/caddy-domain-router.sh`
   - **`docker-compose.tenant.yml`**: Remove public host port mappings (`5432:5432`, `6379:6379`) to keep PostgreSQL and Redis isolated inside the internal Docker bridge network (`127.0.0.1:5432` fallback if required).
   - **`caddy-domain-router.sh`**: Add regex domain validation (`[[ "$CUSTOM_DOMAIN" =~ ^[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$ ]]`) on line 32 to reject malformed domain strings and prevent JSON/shell injection attacks.

3. EMPIRICAL VERIFICATION & TESTING PHASE:
   - Run Docker compose config validation: `docker compose -f infrastructure/docker/docker-compose.tenant.yml config`
   - Run bash syntax check: `bash -n infrastructure/scripts/caddy-domain-router.sh`

4. PROCESS CLEANUP & LEARNING DIRECTIVE (CRITICAL):
   - Terminate any active subagents or background tasks before completing turn.
</ANTIGRAVITY_WORKFLOW>

<ACCEPTANCE_CRITERIA>
- [ ] Subagents delegated for Docker security & regex sanitization checks.
- [ ] PostgreSQL (`5432`) and Redis (`6379`) host ports are unmapped from public host interfaces.
- [ ] `caddy-domain-router.sh` validates custom domain string format before payload construction.
- [ ] Docker Compose config and bash script pass validation tests.
- [ ] All subagents and background tasks are cleanly terminated.
</ACCEPTANCE_CRITERIA>
```
