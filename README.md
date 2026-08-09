# Dedicated 7.9 Report Remediation Prompt Pack (`PROMPT_SEQUENCE_79_REPORT_FIXES.md`)

This prompt pack contains **8 targeted developer prompts** engineered for **Google Antigravity Agentic IDE** to resolve the exact 100x Paymob overcharge bug, homepage cart variant sync issue, Docker backend entrypoint mismatch, ETA canonical JSON serializer, and Bosta weight heuristic flaw identified in the 7.9/10 audit report. Zero older problems are included.

> [!IMPORTANT]
> **Subagent Directive**: Send these 8 prompts sequentially (Prompt 1 through Prompt 8) to your developer Antigravity instance. Every prompt explicitly instructs the agent to delegate research or sub-tasks to subagents (`invoke_subagent`) to maintain clean context and maximize execution speed.

---

## Part 1: Backend Financial, Logistics & Tax Fixes (Prompts 1–3)

---
### Developer Prompt 1: Fix Paymob 100x Overcharge Piastre Bug, Webhook Action Mapping, Mobile Wallet USSD & Idempotency Lock Cleanup

```markdown
/goal

<TASK>
Fix Paymob 100x piastre conversion overcharge bug in `service.ts` & `client.ts`, map dynamic webhook actions, execute `/acceptance/payments/pay` for wallet payments, and clean up Redis locks on exception.
</TASK>

<SUBAGENT_DELEGATION_DIRECTIVE>
- Use `invoke_subagent` (Role: "Codebase Researcher", TypeName: "research") to inspect Paymob piastre unit conversion functions, mobile wallet payment endpoints, and webhook action mapping.
</SUBAGENT_DELEGATION_DIRECTIVE>

<ANTIGRAVITY_SLASH_COMMANDS>
- /goal: Execute autonomously until Paymob piastre currency conversion, webhook action mapping, and wallet payment execution pass build tests.
- /browser: Verify Paymob mobile wallet USSD payment API specs (`/api/acceptance/payments/pay`).
- /learn: Persist Paymob currency unit conversion rules to .gemini/rules.
</ANTIGRAVITY_SLASH_COMMANDS>

<ANTIGRAVITY_WORKFLOW>
1. RESEARCH & INSPECTION PHASE:
   - View `apps/backend/src/modules/paymob/service.ts` (lines 134–202, 168, 433–443), `apps/backend/src/modules/paymob/client.ts` (line 182), and `apps/backend/src/api/hooks/paymob/route.ts` (line 83).

2. IMPLEMENTATION PHASE:
   - Target files: `apps/backend/src/modules/paymob/service.ts`, `apps/backend/src/modules/paymob/client.ts`, `apps/backend/src/api/hooks/paymob/route.ts`
   - **100x Overcharge Fix**: In `service.ts:L168` and `client.ts:L182`, check if `amount` is already in minor currency units (piastres) before invoking `convertEgpToPiastres()` to prevent multiplying minor units by 100 again (which causes 150.00 EGP to become 15,000.00 EGP).
   - **Dynamic Webhook Actions**: In `service.ts:L433-443` (`getWebhookActionAndData`), inspect `payload.obj.success`, `payload.obj.is_refunded`, `payload.obj.is_voided`, and `payload.obj.pending` to map dynamic actions (`"authorized"`, `"captured"`, `"refunded"`, `"failed"`) instead of hardcoding `"authorized"`.
   - **Mobile Wallet USSD Payment**: In `service.ts:L134-202`, execute Paymob `payWithWallet()` API (`POST /api/acceptance/payments/pay`) for mobile wallet payment methods to trigger USSD/OTP prompts on customer mobile devices instead of returning card iframe URLs.
   - **Redis Lock Cleanup**: In `route.ts:L83`, if payment authorization processing throws an exception, delete the Redis lock key immediately so webhook retries are not dropped for 24 hours.

3. EMPIRICAL VERIFICATION & TESTING PHASE:
   - Run TypeScript check: `cd apps/backend && npx tsc --noEmit`
   - Run backend build verification: `cd apps/backend && npm run build`

4. PROCESS CLEANUP & LEARNING DIRECTIVE (CRITICAL):
   - Execute `/learn` to store Paymob currency unit conversion rules.
   - Terminate any running subagents, background dev servers, or processes before completing turn.
</ANTIGRAVITY_WORKFLOW>

<ACCEPTANCE_CRITERIA>
- [ ] Subagents delegated for Paymob currency conversion math inspection.
- [ ] Paymob currency conversion prevents 100x piastre overcharge bug.
- [ ] Webhook action handler dynamically maps authorized, captured, refunded, and failed states.
- [ ] Wallet payment method triggers Paymob wallet payment API.
- [ ] Backend build completes with exit code 0.
- [ ] All subagents and background tasks are cleanly terminated.
</ACCEPTANCE_CRITERIA>
```

---
### Developer Prompt 2: Fix Bosta Weight Unit Heuristic, Governorate Tier Pricing Swap, Option ID Cache Key, & AWB Metadata Persistence

```markdown
/goal

<TASK>
Fix Bosta gram vs kg weight heuristic in `service.ts:L173-176`, correct Upper Egypt vs Sinai governorate tier pricing arrays, include option IDs in Redis cache keys, and write AWB metadata in workflow.
</TASK>

<SUBAGENT_DELEGATION_DIRECTIVE>
- Delegate Bosta shipping rate calculations, governorate tier mapping arrays, and workflow metadata persistence inspection to a subagent via `invoke_subagent`.
</SUBAGENT_DELEGATION_DIRECTIVE>

<ANTIGRAVITY_SLASH_COMMANDS>
- /goal: Execute autonomously until Bosta weight calculations, governorate tier arrays, and workflow AWB metadata compile clean.
- /learn: Persist fulfillment rate caching and metadata persistence rules to .gemini/rules.
</ANTIGRAVITY_SLASH_COMMANDS>

<ANTIGRAVITY_WORKFLOW>
1. RESEARCH & INSPECTION PHASE:
   - View `apps/backend/src/modules/bosta/service.ts` (lines 173–188, 219–222) and `apps/backend/src/workflows/bosta-fulfillment-workflow.ts` (line 85).

2. IMPLEMENTATION PHASE:
   - Target files: `apps/backend/src/modules/bosta/service.ts`, `apps/backend/src/workflows/bosta-fulfillment-workflow.ts`
   - **Weight Unit Heuristic**: Replace naive `if (w > 50)` check in `service.ts:L173-176` with explicit unit inspection (converting grams to kg only if item unit is `g` or weight > 200g) to prevent treating 60kg freight as 0.06kg or 40g items as 40kg.
   - **Governorate Tier Pricing Swap**: In `service.ts:L219-222`, fix swapped pricing arrays so Upper Egypt governorates (`EG-23..25` Qena, Luxor, Aswan) map to Upper Egypt tier (75 EGP) and Sinai/Red Sea (`EG-15..17`) map to Frontier tier (95 EGP).
   - **Option ID Cache Key**: Update Redis cache key format on line 188 to `BOSTA_RATE_${optionId}_${bostaCityId}_W${weight.toFixed(1)}` to prevent price crosstalk between `bosta-standard` and `bosta-express`.
   - **AWB Metadata Persistence**: In `bosta-fulfillment-workflow.ts:L85`, write `tracking_number` and `waybill_url` into the Medusa fulfillment metadata object.

3. EMPIRICAL VERIFICATION & TESTING PHASE:
   - Run TypeScript check: `cd apps/backend && npx tsc --noEmit`
   - Run backend build verification: `cd apps/backend && npm run build`

4. PROCESS CLEANUP & LEARNING DIRECTIVE (CRITICAL):
   - Execute `/learn` to store fulfillment metadata persistence rules.
   - Terminate any running subagents, background dev servers, or processes before completing turn.
</ANTIGRAVITY_WORKFLOW>

<ACCEPTANCE_CRITERIA>
- [ ] Subagents delegated for Bosta weight math inspection.
- [ ] Weight unit heuristic accurately converts grams to kg.
- [ ] Governorate pricing arrays mapped correctly for Upper Egypt and Sinai.
- [ ] Redis rate cache key includes shipping option ID.
- [ ] Workflow step persists AWB tracking number and waybill URL into fulfillment metadata.
- [ ] Backend build completes with exit code 0.
- [ ] All subagents and background tasks are cleanly terminated.
</ACCEPTANCE_CRITERIA>
```

---
### Developer Prompt 3: Implement ETA Canonical JSON Serialization, Hashing, B2B E-Invoice Schema, & Order Discounts

```markdown
/goal

<TASK>
Implement ETA canonical JSON serialization & SHA-256 hashing in `payload-builder.ts`, build B2B E-Invoice schemas (`documentType: "I"`), and map actual order discount totals.
</TASK>

<SUBAGENT_DELEGATION_DIRECTIVE>
- Use `invoke_subagent` to inspect ETA Tax e-Receipt / e-Invoice canonical serialization rules (lexicographical key sorting) and SHA-256 hashing specifications.
</SUBAGENT_DELEGATION_DIRECTIVE>

<ANTIGRAVITY_SLASH_COMMANDS>
- /goal: Execute autonomously until ETA canonical JSON serialization, SHA-256 hashing, and B2B E-Invoice schemas pass verification.
- /browser: Verify ETA Portal canonical string serialization specifications.
- /learn: Persist ETA Tax canonical serialization rules to .gemini/rules.
</ANTIGRAVITY_SLASH_COMMANDS>

<ANTIGRAVITY_WORKFLOW>
1. RESEARCH & INSPECTION PHASE:
   - View `apps/backend/src/modules/eta-tax/payload-builder.ts` (lines 109, 188, 217).

2. IMPLEMENTATION PHASE:
   - Target file: `apps/backend/src/modules/eta-tax/payload-builder.ts`
   - **Canonical JSON Serializer & SHA-256 Hash**: On line 109, implement ETA canonical serialization (recursively sorting object keys alphabetically, uppercase property names, stringifying values) and compute SHA-256 hash string before passing payload to HSM signing proxies.
   - **B2B E-Invoice Schema**: On line 188, conditionally build E-Invoice schema (`documentType: "I"`) when buyer type is `"B"` (Corporate/Business buyer with Tax Registration Number) for submissions to `/invoices/submission`.
   - **Order Discounts**: On line 217, map actual order promotion/discount amounts (`totalDiscountAmount: order.discount_total || 0`) instead of hardcoding 0.

3. EMPIRICAL VERIFICATION & TESTING PHASE:
   - Run TypeScript check: `cd apps/backend && npx tsc --noEmit`
   - Run backend build verification: `cd apps/backend && npm run build`

4. PROCESS CLEANUP & LEARNING DIRECTIVE (CRITICAL):
   - Execute `/learn` to store ETA canonical serialization rules.
   - Terminate any running subagents, background dev servers, or processes before completing turn.
</ANTIGRAVITY_WORKFLOW>

<ACCEPTANCE_CRITERIA>
- [ ] Subagents delegated for ETA canonical JSON serialization research.
- [ ] `payload-builder.ts` computes ETA canonical string and SHA-256 hash.
- [ ] Corporate buyers (`"B"`) generate E-Invoice schemas (`documentType: "I"`).
- [ ] Actual order discount amounts mapped to `totalDiscountAmount`.
- [ ] Backend build completes with exit code 0.
- [ ] All subagents and background tasks are cleanly terminated.
</ACCEPTANCE_CRITERIA>
```

---

## Part 2: Storefront & Infrastructure Fixes (Prompts 4–8)

---
### Developer Prompt 4: Fix Storefront Homepage Cart Variant Sync (`prod_` vs `variant_`) & Create `[countryCode]/page.tsx` Route

```markdown
/goal

<TASK>
Update `home-client-view.tsx` to pass `variantId` (`product.variants[0].id`) to `addItem`, and create `src/app/[countryCode]/page.tsx` route.
</TASK>

<SUBAGENT_DELEGATION_DIRECTIVE>
- Delegate Next.js 15 country code route params inspection and Storefront cart variant ID matching to a subagent via `invoke_subagent`.
</SUBAGENT_DELEGATION_DIRECTIVE>

<ANTIGRAVITY_SLASH_COMMANDS>
- /goal: Execute autonomously until Storefront homepage cart additions pass valid variant IDs and countryCode route exists.
- /learn: Persist Storefront localized routing rules to .gemini/rules.
</ANTIGRAVITY_SLASH_COMMANDS>

<ANTIGRAVITY_WORKFLOW>
1. RESEARCH & INSPECTION PHASE:
   - View `apps/storefront/src/modules/home/components/home-client-view.tsx` (line 34) and inspect `apps/storefront/src/app/[countryCode]`.

2. IMPLEMENTATION PHASE:
   - Target files: `apps/storefront/src/modules/home/components/home-client-view.tsx`, `apps/storefront/src/app/[countryCode]/page.tsx`
   - **`home-client-view.tsx:L34`**: Update `addItem` call to pass `variantId: product.variants?.[0]?.id` instead of `id: product.id` (which starts with `prod_`), enabling cart state additions to resolve `targetVariantId` and save to Medusa DB.
   - **`[countryCode]/page.tsx`**: Create `src/app/[countryCode]/page.tsx` handling localized homepage route requests (e.g. `/eg`) so storefront navigation does not return Next.js 404 errors.

3. EMPIRICAL VERIFICATION & TESTING PHASE:
   - Run storefront build verification: `cd apps/storefront && npm run build`

4. PROCESS CLEANUP & LEARNING DIRECTIVE (CRITICAL):
   - Terminate any running subagents, background dev servers (e.g. `next dev`) before completing turn.
</ANTIGRAVITY_WORKFLOW>

<ACCEPTANCE_CRITERIA>
- [ ] Subagents delegated for Storefront variant ID inspection.
- [ ] Homepage Add-to-Cart passes valid variant ID (`variant_...`) to `addItem`.
- [ ] `src/app/[countryCode]/page.tsx` created and handles localized root navigation cleanly.
- [ ] Storefront build completes with exit code 0.
- [ ] All subagents and background tasks are cleanly terminated.
</ACCEPTANCE_CRITERIA>
```

---
### Developer Prompt 5: Fix Docker Backend CMD Entrypoint (`npx medusa start`) & Localhost Image Remote Pattern Port

```markdown
/goal

<TASK>
Update line 50 of `infrastructure/docker/Dockerfile.backend` to `CMD ["npx", "medusa", "start"]` and add port `"9000"` to `next.config.ts`.
</TASK>

<SUBAGENT_DELEGATION_DIRECTIVE>
- Use `invoke_subagent` to inspect Medusa 2.0 Docker entrypoint startup commands and Next.js image remote pattern configs.
</SUBAGENT_DELEGATION_DIRECTIVE>

<ANTIGRAVITY_SLASH_COMMANDS>
- /goal: Execute autonomously until Docker backend entrypoint starts Medusa and Next.js image configuration permits local backend thumbnail uploads.
- /learn: Persist Docker entrypoint startup rules to .gemini/rules.
</ANTIGRAVITY_SLASH_COMMANDS>

<ANTIGRAVITY_WORKFLOW>
1. RESEARCH & INSPECTION PHASE:
   - View `infrastructure/docker/Dockerfile.backend` (line 50) and `apps/storefront/next.config.ts` (line 28).

2. IMPLEMENTATION PHASE:
   - Target files: `infrastructure/docker/Dockerfile.backend`, `apps/storefront/next.config.ts`
   - **`Dockerfile.backend:L50`**: Change `CMD ["node", "dist/main.js"]` to `CMD ["npx", "medusa", "start"]` to eliminate container startup failure (`Cannot find module 'dist/main.js'`).
   - **`next.config.ts:L28`**: Add `port: "9000"` to `localhost` remote patterns array to permit local backend product thumbnail uploads.

3. EMPIRICAL VERIFICATION & TESTING PHASE:
   - Run storefront build verification: `cd apps/storefront && npm run build`
   - Run Docker compose config validation: `docker compose -f infrastructure/docker/docker-compose.tenant.yml config`

4. PROCESS CLEANUP & LEARNING DIRECTIVE (CRITICAL):
   - Terminate any active subagents or background tasks before completing turn.
</ANTIGRAVITY_WORKFLOW>

<ACCEPTANCE_CRITERIA>
- [ ] `Dockerfile.backend` line 50 executes `CMD ["npx", "medusa", "start"]`.
- [ ] `next.config.ts` includes `port: "9000"` in localhost remote pattern configuration.
- [ ] Storefront build and Docker Compose config pass validation.
- [ ] All subagents and background tasks are cleanly terminated.
</ACCEPTANCE_CRITERIA>
```

---
### Developer Prompt 6: Fail-Fast DB Provisioning Script Timeout Guard & Unpersisted Queue Payload Objects

```markdown
/goal

<TASK>
Add fail-fast `exit 1` in `provision-tenant.sh` if database readiness times out, and sanitize BullMQ payload objects in `background-queue.ts`.
</TASK>

<SUBAGENT_DELEGATION_DIRECTIVE>
- Use `invoke_subagent` to inspect shell script error exit codes and BullMQ Redis payload serialization.
</SUBAGENT_DELEGATION_DIRECTIVE>

<ANTIGRAVITY_SLASH_COMMANDS>
- /goal: Execute autonomously until tenant provisioning script aborts on database timeouts and BullMQ payload serialization passes tests.
- /learn: Persist shell automation error handling rules to .gemini/rules.
</ANTIGRAVITY_SLASH_COMMANDS>

<ANTIGRAVITY_WORKFLOW>
1. RESEARCH & INSPECTION PHASE:
   - View `infrastructure/scripts/provision-tenant.sh` (lines 115–126) and `apps/backend/src/jobs/background-queue.ts` (line 133).

2. IMPLEMENTATION PHASE:
   - Target files: `infrastructure/scripts/provision-tenant.sh`, `apps/backend/src/jobs/background-queue.ts`
   - **`provision-tenant.sh:L121`**: Add explicit `exit 1` if PostgreSQL readiness polling times out after 30 seconds to prevent attempting `medusa db:migrate` against an unreachable database.
   - **`background-queue.ts:L133`**: Convert module service class instances into plain JSON-serializable DTO payload objects before enqueuing to Redis (`ETA_SUBMISSION_RETRY`).

3. EMPIRICAL VERIFICATION & TESTING PHASE:
   - Run TypeScript check: `cd apps/backend && npx tsc --noEmit`
   - Run bash syntax check: `bash -n infrastructure/scripts/provision-tenant.sh`

4. PROCESS CLEANUP & LEARNING DIRECTIVE (CRITICAL):
   - Terminate any running subagents or shell tasks before completing turn.
</ANTIGRAVITY_WORKFLOW>

<ACCEPTANCE_CRITERIA>
- [ ] Subagents delegated for shell script error handling inspection.
- [ ] `provision-tenant.sh` exits with code 1 if DB readiness times out.
- [ ] BullMQ queue payload converts service instances into plain serializable DTOs.
- [ ] Script passes `bash -n` syntax check cleanly.
- [ ] All subagents and background tasks are cleanly terminated.
</ACCEPTANCE_CRITERIA>
```

---
### Developer Prompt 7: Register ETA Tax Module as Medusa 2.0 `ITaxProvider` in `medusa-config.ts`

```markdown
/goal

<TASK>
Refactor `eta-tax` in `apps/backend/medusa-config.ts` to register as an official Medusa 2.0 tax plugin implementing `ITaxProvider`.
</TASK>

<SUBAGENT_DELEGATION_DIRECTIVE>
- Use `invoke_subagent` to inspect Medusa 2.0 `@medusajs/medusa/tax` module plugin registration patterns.
</SUBAGENT_DELEGATION_DIRECTIVE>

<ANTIGRAVITY_SLASH_COMMANDS>
- /goal: Execute autonomously until ETA Tax module registers under Medusa 2.0 tax providers.
- /learn: Persist Medusa v2 tax provider registration rules to .gemini/rules.
</ANTIGRAVITY_SLASH_COMMANDS>

<ANTIGRAVITY_WORKFLOW>
1. RESEARCH & INSPECTION PHASE:
   - View `apps/backend/medusa-config.ts` (line 96) and `apps/backend/src/modules/eta-tax/service.ts`.

2. IMPLEMENTATION PHASE:
   - Target files: `apps/backend/medusa-config.ts`, `apps/backend/src/modules/eta-tax/service.ts`
   - Register `eta-tax` inside the `modules` array under tax provider definitions (`@medusajs/medusa/tax`) with identifier `eta-tax`.
   - Implement `getTaxLines()` method in `EtaTaxModuleService` so Medusa core cart checkout steps delegate tax calculations directly to ETA tax rules.

3. EMPIRICAL VERIFICATION & TESTING PHASE:
   - Run TypeScript check: `cd apps/backend && npx tsc --noEmit`
   - Run backend build verification: `cd apps/backend && npm run build`

4. PROCESS CLEANUP & LEARNING DIRECTIVE (CRITICAL):
   - Execute `/learn` to store Medusa tax provider rules.
   - Terminate any running subagents, background dev servers, or processes before completing turn.
</ANTIGRAVITY_WORKFLOW>

<ACCEPTANCE_CRITERIA>
- [ ] Subagents delegated for Medusa tax provider registration research.
- [ ] `medusa-config.ts` registers `eta-tax` under `@medusajs/medusa/tax`.
- [ ] `EtaTaxModuleService` exposes `getTaxLines()` method for cart calculations.
- [ ] Backend build completes with exit code 0.
- [ ] All subagents and background tasks are cleanly terminated.
</ACCEPTANCE_CRITERIA>
```

---
### Developer Prompt 8: Storefront Backend Health Dependency & Redis Rate Limiting in AI Copywriter Route

```markdown
/goal

<TASK>
Add backend `service_healthy` dependency for storefront in `docker-compose.tenant.yml` and back AI rate limiter with Redis.
</TASK>

<SUBAGENT_DELEGATION_DIRECTIVE>
- Use `invoke_subagent` to inspect Docker Compose service health conditions and Redis rate limiting implementations.
</SUBAGENT_DELEGATION_DIRECTIVE>

<ANTIGRAVITY_SLASH_COMMANDS>
- /goal: Execute autonomously until storefront container depends on backend health and AI rate limiting uses Redis keys.
- /learn: Persist Redis rate limiting rules to .gemini/rules.
</ANTIGRAVITY_SLASH_COMMANDS>

<ANTIGRAVITY_WORKFLOW>
1. RESEARCH & INSPECTION PHASE:
   - View `infrastructure/docker/docker-compose.tenant.yml` and `apps/backend/src/api/admin/ai/generate-copy/route.ts` (line 5).

2. IMPLEMENTATION PHASE:
   - Target files: `infrastructure/docker/docker-compose.tenant.yml`, `apps/backend/src/api/admin/ai/generate-copy/route.ts`
   - **`docker-compose.tenant.yml`**: Update storefront service to specify `depends_on: { backend: { condition: service_healthy } }` so storefront container does not boot until backend health check passes.
   - **`generate-copy/route.ts:L5`**: Replace in-memory token bucket Map with Redis key rate limiter (`INCRBY` / `EXPIRE` on `ratelimit:ai:${ip}`) to enforce 10 req/min limit across multi-pod Node instances.

3. EMPIRICAL VERIFICATION & TESTING PHASE:
   - Run TypeScript check: `cd apps/backend && npx tsc --noEmit`
   - Run Docker compose config validation: `docker compose -f infrastructure/docker/docker-compose.tenant.yml config`

4. PROCESS CLEANUP & LEARNING DIRECTIVE (CRITICAL):
   - Terminate any active subagents or background tasks before completing turn.
</ANTIGRAVITY_WORKFLOW>

<ACCEPTANCE_CRITERIA>
- [ ] Subagents delegated for Redis rate limiter research.
- [ ] Storefront container specifies `depends_on: { backend: { condition: service_healthy } }`.
- [ ] `generate-copy/route.ts` uses Redis key rate limiting (`ratelimit:ai:${ip}`).
- [ ] Backend build and Docker Compose config pass validation.
- [ ] All subagents and background tasks are cleanly terminated.
</ACCEPTANCE_CRITERIA>
```
