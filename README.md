# Dedicated 9.4 Report Remediation Prompt Pack (`PROMPT_SEQUENCE_94_FINAL_REPORT_FIXES.md`)

This prompt pack contains **5 targeted developer prompts** engineered for **Google Antigravity Agentic IDE** to resolve the exact new defects identified in the latest 9.4/10 evaluation report: Paymob Aman/Masary Kiosk integration with `bill_reference`, Storefront Server/Client action boundary separation in `home-client-view.tsx`, Paymob workflow step DI container resolution, ETA manual vs native BullMQ retry reconciliation, Bosta governorate substring match strictness guard (`normalized.length >= 3`), Medusa v2 complete cart path formatting, dynamic root `<html>` locale reflection, and Dockerfile storefront health probe URL standardization. Zero older problems are included.

> [!IMPORTANT]
> **Subagent Directive**: Send these 5 prompts sequentially (Prompt 1 through Prompt 5) to your developer Antigravity instance. Every prompt explicitly instructs the agent to delegate research or sub-tasks to subagents (`invoke_subagent`).

---

## Part 1: Payment & Storefront Boundaries (Prompts 1–2)

---
### Developer Prompt 1: Add Paymob Aman/Masary Kiosk Integration (`bill_reference`) & Unify DI in Paymob Workflow Step

```markdown
/goal

<TASK>
Add `kioskIntegrationId` / `amanIntegrationId` to `PaymobModuleOptions` in `apps/backend/src/modules/paymob/types.ts`, extract `bill_reference` from the Paymob Accept response in `apps/backend/src/modules/paymob/service.ts`, and resolve `paymobPayment` from the Medusa DI container in `apps/backend/src/workflows/paymob-payment-workflow.ts:L31`.
</TASK>

<SUBAGENT_DELEGATION_DIRECTIVE>
- Use `invoke_subagent` (Role: "Payment Architecture Researcher", TypeName: "research") to inspect Paymob module options, payment service Kiosk response handling, and `paymob-payment-workflow.ts` DI resolution.
</SUBAGENT_DELEGATION_DIRECTIVE>

<ANTIGRAVITY_SLASH_COMMANDS>
- /goal: Execute autonomously until Paymob supports Aman/Masary Kiosk cash collection and workflow resolves client via DI container.
- /learn: Persist Paymob Kiosk integration and workflow DI resolution rules to .gemini/rules.
</ANTIGRAVITY_SLASH_COMMANDS>

<ANTIGRAVITY_WORKFLOW>
1. RESEARCH & INSPECTION PHASE:
   - View `apps/backend/src/modules/paymob/types.ts` (`PaymobModuleOptions` and payment data interfaces).
   - View `apps/backend/src/modules/paymob/service.ts` (`initiatePayment` / `authorizePayment` methods).
   - View `apps/backend/src/workflows/paymob-payment-workflow.ts` (line 31 container resolution).

2. IMPLEMENTATION PHASE:
   - Target files: `apps/backend/src/modules/paymob/types.ts`, `apps/backend/src/modules/paymob/service.ts`, `apps/backend/src/workflows/paymob-payment-workflow.ts`
   - **Paymob Kiosk / Aman Integration Options** (`types.ts` & `service.ts`):
     Add `kioskIntegrationId?: string` and `amanIntegrationId?: string` to `PaymobModuleOptions`.
     In `service.ts:initiatePayment()`, when a kiosk/cash payment method is selected (or when the integration corresponds to Kiosk/Aman), capture and return `data.bill_reference` (and `data.data.bill_reference` / `data.data.masary_code`) from the Paymob API response in the payment session data so customers receive their reference code for over-the-counter retail cash payments.
   - **Unify DI in Paymob Workflow Step** (`paymob-payment-workflow.ts:L31`):
     Replace direct `new PaymobClient(...)` instantiation with Medusa container resolution:
     ```typescript
     // BEFORE:
     const client = new PaymobClient(options)

     // AFTER:
     const paymentModuleService = container.resolve(Modules.PAYMENT) // or container.resolve("paymobPayment")
     ```
     *Rationale*: Matches the clean container resolution pattern established in `bosta-fulfillment-workflow.ts` and `eta-tax-workflow.ts`.

3. EMPIRICAL VERIFICATION & TESTING PHASE:
   - Run TypeScript check: `cd apps/backend && npx tsc --noEmit`
   - Run backend build verification: `cd apps/backend && npm run build`

4. PROCESS CLEANUP & LEARNING DIRECTIVE (CRITICAL):
   - Execute `/learn` to store Paymob Kiosk rules.
   - Terminate any running subagents, background dev servers, or processes before completing turn.
</ANTIGRAVITY_WORKFLOW>

<ACCEPTANCE_CRITERIA>
- [ ] Subagents delegated for Paymob types, service, and workflow inspection.
- [ ] `PaymobModuleOptions` includes `kioskIntegrationId` and `amanIntegrationId`.
- [ ] Kiosk `bill_reference` extracted and returned in payment session data.
- [ ] `paymob-payment-workflow.ts` resolves payment service via container DI.
- [ ] Backend build completes with exit code 0.
- [ ] All subagents and background tasks are cleanly terminated.
</ACCEPTANCE_CRITERIA>
```

---
### Developer Prompt 2: Fix Server/Client Action Boundary in `home-client-view.tsx` & Medusa v2 Cart Complete Path

```markdown
/goal

<TASK>
Refactor `apps/storefront/src/modules/home/components/home-client-view.tsx:L10` to call a dedicated Server Action or Next.js Route Handler `/api/products` instead of importing server-only `fetchLiveStorefrontProducts`, and standardize the cart completion path in `apps/storefront/src/modules/checkout/components/checkout-view.tsx:L37` to `POST /store/carts/${cartId}/complete`.
</TASK>

<SUBAGENT_DELEGATION_DIRECTIVE>
- Use `invoke_subagent` to inspect `home-client-view.tsx` client imports and `checkout-view.tsx` cart completion API call paths.
</SUBAGENT_DELEGATION_DIRECTIVE>

<ANTIGRAVITY_SLASH_COMMANDS>
- /goal: Execute autonomously until RSC client boundary violations are resolved and cart completion endpoint matches Medusa v2 spec.
- /learn: Persist Next.js RSC boundary separation and Medusa v2 cart completion rules to .gemini/rules.
</ANTIGRAVITY_SLASH_COMMANDS>

<ANTIGRAVITY_WORKFLOW>
1. RESEARCH & INSPECTION PHASE:
   - View `apps/storefront/src/modules/home/components/home-client-view.tsx` (line 10 imports).
   - View `apps/storefront/src/modules/checkout/components/checkout-view.tsx` (line 37 cart completion).

2. IMPLEMENTATION PHASE:
   - Target files: `apps/storefront/src/modules/home/components/home-client-view.tsx`, `apps/storefront/src/app/api/products/route.ts` (or server action), `apps/storefront/src/modules/checkout/components/checkout-view.tsx`
   - **RSC Boundary Separation** (`home-client-view.tsx`):
     Remove direct client-side imports of `fetchLiveStorefrontProducts` (which uses server-only `next/cache` and `@medusajs/js-sdk` server config). Instead, either pass pre-fetched product data as props from the parent async Server Component (`page.tsx`) or fetch from a dedicated Next.js Route Handler (`/api/products?countryCode=...`) using standard client fetch.
   - **Medusa v2 Complete Cart Endpoint Path** (`checkout-view.tsx:L37`):
     Ensure the cart completion request is formatted exactly as:
     ```typescript
     POST /store/carts/${cartId}/complete
     ```
     matching the Medusa v2 Store REST API standard specification.

3. EMPIRICAL VERIFICATION & TESTING PHASE:
   - Run storefront typecheck: `cd apps/storefront && npx tsc --noEmit`
   - Run storefront build: `cd apps/storefront && npm run build`

4. PROCESS CLEANUP & LEARNING DIRECTIVE (CRITICAL):
   - Execute `/learn` to store RSC boundary and cart API rules.
   - Terminate any running subagents, background dev servers, or processes before completing turn.
</ANTIGRAVITY_WORKFLOW>

<ACCEPTANCE_CRITERIA>
- [ ] Subagents delegated for RSC boundary and cart endpoint inspection.
- [ ] `home-client-view.tsx` no longer imports server-only cached fetch functions.
- [ ] `checkout-view.tsx` calls `POST /store/carts/${cartId}/complete`.
- [ ] Storefront build completes cleanly with exit code 0.
- [ ] All subagents and background tasks are cleanly terminated.
</ACCEPTANCE_CRITERIA>
```

---

## Part 2: Logistics Edge-Cases & Worker Retry Reconciliation (Prompts 3–4)

---
### Developer Prompt 3: Add Length Guard to Bosta Location Substring Matching & Reconcile ETA BullMQ Retries

```markdown
/goal

<TASK>
Add a minimum length guard (`normalized.length >= 3`) to the fallback substring match in `apps/backend/src/modules/bosta/location-mapper.ts:L124`, and reconcile manual BullMQ retry enqueueing with BullMQ's native job-level retry backoff in `apps/backend/src/subscribers/order-placed-eta.ts` and `apps/backend/src/jobs/background-queue.ts`.
</TASK>

<SUBAGENT_DELEGATION_DIRECTIVE>
- Use `invoke_subagent` to inspect `location-mapper.ts` substring matching logic and compare `order-placed-eta.ts` manual queue enqueueing against BullMQ worker retry configuration in `background-queue.ts`.
</SUBAGENT_DELEGATION_DIRECTIVE>

<ANTIGRAVITY_SLASH_COMMANDS>
- /goal: Execute autonomously until Bosta location matcher guards against short substrings and ETA worker retry logic is deduplicated.
- /learn: Persist location mapping guard and BullMQ retry reconciliation rules to .gemini/rules.
</ANTIGRAVITY_SLASH_COMMANDS>

<ANTIGRAVITY_WORKFLOW>
1. RESEARCH & INSPECTION PHASE:
   - View `apps/backend/src/modules/bosta/location-mapper.ts` (lines 115–135).
   - View `apps/backend/src/subscribers/order-placed-eta.ts` (lines 70–95).
   - View `apps/backend/src/jobs/background-queue.ts` (lines 165–185).

2. IMPLEMENTATION PHASE:
   - Target files: `apps/backend/src/modules/bosta/location-mapper.ts`, `apps/backend/src/subscribers/order-placed-eta.ts`, `apps/backend/src/jobs/background-queue.ts`
   - **Bosta Governorate Substring Match Strictness** (`location-mapper.ts:L124`):
     Add `normalized.length >= 3` to the fallback substring search condition:
     ```typescript
     // BEFORE:
     if (alias.includes(normalized) || normalized.includes(alias))

     // AFTER:
     if (normalized.length >= 3 && (alias.includes(normalized) || (alias.length >= 3 && normalized.includes(alias))))
     ```
     *Rationale*: Prevents 1-2 character generic inputs (e.g. "el", "al", "st") from inadvertently matching long governorate aliases like "Qalyubia" or "Alexandria".

   - **Reconcile Dual-Layer Retries in ETA Tax Worker** (`order-placed-eta.ts` & `background-queue.ts`):
     Rely on BullMQ's native job `attempts` configuration (`attempts: 5`, `backoff: { type: "exponential", delay: 2000 }`) rather than manually calling `queue.add()` inside the worker catch block. Only on final attempt exhaustion (`job.attemptsMade >= (job.opts.attempts || 5)`), trigger `dispatchDlqAlertWebhook` and record `FAILED_DLQ` in the audit log.
     *Rationale*: Eliminates duplicate queue entries and race conditions caused by mixing manual retry enqueueing with BullMQ's built-in scheduler.

3. EMPIRICAL VERIFICATION & TESTING PHASE:
   - Run TypeScript check: `cd apps/backend && npx tsc --noEmit`
   - Run backend build verification: `cd apps/backend && npm run build`

4. PROCESS CLEANUP & LEARNING DIRECTIVE (CRITICAL):
   - Execute `/learn` to store Bosta location and BullMQ retry rules.
   - Terminate any running subagents, background dev servers, or processes before completing turn.
</ANTIGRAVITY_WORKFLOW>

<ACCEPTANCE_CRITERIA>
- [ ] Subagents delegated for location mapper and BullMQ retry inspection.
- [ ] `location-mapper.ts` enforces `normalized.length >= 3` on substring fallback.
- [ ] ETA job retries managed natively by BullMQ retry options without duplicate manual queue adds.
- [ ] Backend build completes with exit code 0.
- [ ] All subagents and background tasks are cleanly terminated.
</ACCEPTANCE_CRITERIA>
```

---
### Developer Prompt 4: Reflect Dynamic `dir` / `lang` on Root `<html>` & Standardize Dockerfile Storefront Health Probe

```markdown
/goal

<TASK>
Reflect `dir="rtl"` and `lang="ar"` dynamically on the root `<html>` element in `apps/storefront/src/app/[countryCode]/layout.tsx` (or root layout), and align the healthcheck probe in `infrastructure/docker/Dockerfile.storefront:L47` to `http://localhost:3000/api/health`.
</TASK>

<SUBAGENT_DELEGATION_DIRECTIVE>
- Use `invoke_subagent` to inspect root and nested layout `<html>` attribute rendering and compare `Dockerfile.storefront` healthcheck with `docker-compose.tenant.yml`.
</SUBAGENT_DELEGATION_DIRECTIVE>

<ANTIGRAVITY_SLASH_COMMANDS>
- /goal: Execute autonomously until root html reflects dynamic locale and Dockerfile storefront healthcheck targets /api/health.
- /learn: Persist Next.js i18n html attributes and Docker health probe rules to .gemini/rules.
</ANTIGRAVITY_SLASH_COMMANDS>

<ANTIGRAVITY_WORKFLOW>
1. RESEARCH & INSPECTION PHASE:
   - View `apps/storefront/src/app/layout.tsx` and `apps/storefront/src/app/[countryCode]/layout.tsx`.
   - View `infrastructure/docker/Dockerfile.storefront` (line 47).
   - View `infrastructure/docker/docker-compose.tenant.yml` (storefront healthcheck).

2. IMPLEMENTATION PHASE:
   - Target files: `apps/storefront/src/app/layout.tsx`, `apps/storefront/src/app/[countryCode]/layout.tsx`, `infrastructure/docker/Dockerfile.storefront`
   - **Dynamic Root `<html>` Locale Reflection**:
     Ensure `lang` and `dir` are dynamically computed based on `countryCode` (e.g., `countryCode === "eg" || countryCode === "ar"` -> `dir="rtl"`, `lang="ar"`; otherwise `dir="ltr"`, `lang="en"`) on the `<html>` element to maximize SEO indexing and accessibility for Arabic search engine crawlers.
   - **Standardize Dockerfile Health Probe Path** (`Dockerfile.storefront:L47`):
     ```dockerfile
     # BEFORE:
     HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
       CMD wget --no-verbose --tries=1 --spider http://localhost:3000/ || exit 1

     # AFTER:
     HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
       CMD wget --no-verbose --tries=1 --spider http://localhost:3000/api/health || exit 1
     ```
     *Rationale*: Aligns with `docker-compose.tenant.yml` and targets the lightweight dedicated health route `/api/health`, avoiding expensive root page SSR renders during automated container liveness polling.

3. EMPIRICAL VERIFICATION & TESTING PHASE:
   - Run storefront build verification: `cd apps/storefront && npm run build`
   - Validate Docker Compose config: `docker compose -f infrastructure/docker/docker-compose.tenant.yml config` (if available)

4. PROCESS CLEANUP & LEARNING DIRECTIVE (CRITICAL):
   - Terminate any running subagents, background dev servers, or processes before completing turn.
</ANTIGRAVITY_WORKFLOW>

<ACCEPTANCE_CRITERIA>
- [ ] Subagents delegated for layout html attributes and Dockerfile health probe inspection.
- [ ] Root/localized layout sets `dir="rtl"` / `lang="ar"` dynamically for Egyptian locale.
- [ ] `Dockerfile.storefront` health probe tests `http://localhost:3000/api/health`.
- [ ] Storefront build completes with exit code 0.
- [ ] All subagents and background tasks are cleanly terminated.
</ACCEPTANCE_CRITERIA>
```

---

## Part 3: Monorepo Final Verification (Prompt 5)

---
### Developer Prompt 5: Comprehensive Monorepo Typecheck, Build, & Integration Verification

```markdown
/goal

<TASK>
Execute full monorepo typechecks, builds, and sanity checks across `@dtc/shared-types`, `apps/backend`, and `apps/storefront` to ensure 100% clean compilation and deployment readiness.
</TASK>

<SUBAGENT_DELEGATION_DIRECTIVE>
- Use `invoke_subagent` (Role: "Build Verification Specialist", TypeName: "research") to run TypeScript typechecks and production builds in parallel across all workspaces.
</SUBAGENT_DELEGATION_DIRECTIVE>

<ANTIGRAVITY_SLASH_COMMANDS>
- /goal: Execute autonomously until all packages build cleanly with exit code 0.
</ANTIGRAVITY_SLASH_COMMANDS>

<ANTIGRAVITY_WORKFLOW>
1. VERIFICATION COMMAND SEQUENCE:
   - Shared Types Build: `cd packages/shared-types && npm run build`
   - Backend Typecheck: `cd apps/backend && npx tsc --noEmit`
   - Backend Medusa Build: `cd apps/backend && npm run build`
   - Storefront Typecheck: `cd apps/storefront && npx tsc --noEmit`
   - Storefront Production Build: `cd apps/storefront && npm run build`
   - Provisioning Script Syntax: `bash -n infrastructure/scripts/provision-tenant.sh`
   - Caddy Router Script Syntax: `bash -n infrastructure/scripts/caddy-domain-router.sh`

2. ACCEPTANCE VERIFICATION:
   - Confirm 0 TypeScript compilation errors in all workspaces.
   - Confirm backend bundles Medusa core + admin dashboard cleanly.
   - Confirm Next.js storefront compiles all static and dynamic pages with Turbopack.

3. PROCESS CLEANUP DIRECTIVE (CRITICAL):
   - Terminate any active subagents, background worker loops, or dev server processes.
</ANTIGRAVITY_WORKFLOW>

<ACCEPTANCE_CRITERIA>
- [ ] `packages/shared-types` compiles with exit code 0.
- [ ] `apps/backend` typecheck and Medusa build complete with exit code 0.
- [ ] `apps/storefront` typecheck and Next.js build complete with exit code 0.
- [ ] Infrastructure shell scripts pass syntax validation (`bash -n`).
- [ ] All subagents and background tasks cleanly terminated.
</ACCEPTANCE_CRITERIA>
```
