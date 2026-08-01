# Master Refactoring Developer Prompt Sequence: Egyptian MedusaJS v2 Platform

This prompt pack contains **15 atomic, step-by-step developer prompts** designed for **Google Antigravity Agentic IDE** with native `/goal`, `/browser`, and `/learn` slash command triggers to systematically repair and refactor all architectural, configuration, storefront, workflow, and DevOps defects.

---

## Phase 1: Backend Core & Configuration Repair

---
### Developer Prompt 1: Register Custom Modules (`bosta` and `gemini-ai`) in `medusa-config.ts`

```markdown
/goal

<TASK>
Register missing custom modules (`bosta` and `gemini-ai`) in `apps/backend/medusa-config.ts` so the Medusa v2 container resolves services correctly.
</TASK>

<ANTIGRAVITY_SLASH_COMMANDS>
- /goal: Execute autonomously until module registration passes Medusa backend build checks.
- /learn: Persist Medusa v2 custom module configuration patterns to .gemini/rules.
</ANTIGRAVITY_SLASH_COMMANDS>

<ANTIGRAVITY_WORKFLOW>
1. RESEARCH & INSPECTION PHASE:
   - View `apps/backend/medusa-config.ts` and inspect existing module declarations.
   - Inspect `apps/backend/src/modules/bosta` and `apps/backend/src/modules/gemini-ai`.

2. IMPLEMENTATION PHASE:
   - Target file: `apps/backend/medusa-config.ts`
   - Register `bosta` fulfillment provider service and `gemini-ai` service in the `modules` config array.
   - Ensure options keys (`apiKey`, `baseUrl`) are wired to environment variables.

3. EMPIRICAL VERIFICATION & TESTING PHASE:
   - Run TypeScript check: `cd apps/backend && npx tsc --noEmit`
   - Run backend build verification: `cd apps/backend && npm run build`

4. PROCESS CLEANUP & LEARNING DIRECTIVE (CRITICAL):
   - Execute `/learn` to record Medusa module registration rules.
   - Terminate any running background dev servers or processes before completing turn.
</ANTIGRAVITY_WORKFLOW>

<ACCEPTANCE_CRITERIA>
- [ ] `medusa-config.ts` includes `bosta` and `gemini-ai` module declarations in `modules` array.
- [ ] Backend build completes with exit code 0.
- [ ] All background tasks and dev servers are cleanly terminated.
</ACCEPTANCE_CRITERIA>
```

---
### Developer Prompt 2: Fix Admin UI Browser Bundle Defect (`ai-copywriter.tsx` REST API Endpoint)

```markdown
/goal

<TASK>
Fix Admin UI bundling defect by creating an authenticated REST API route `/admin/ai/generate-copy` and updating `ai-copywriter.tsx` to fetch from HTTP rather than importing backend files directly.
</TASK>

<ANTIGRAVITY_SLASH_COMMANDS>
- /goal: Execute autonomously until admin UI widget compiles without backend file imports.
- /learn: Persist Medusa Admin Extension REST communication rules to .gemini/rules.
</ANTIGRAVITY_SLASH_COMMANDS>

<ANTIGRAVITY_WORKFLOW>
1. RESEARCH & INSPECTION PHASE:
   - View `apps/backend/src/admin/widgets/ai-copywriter.tsx` and identify backend file import `../../modules/gemini-ai/client`.

2. IMPLEMENTATION PHASE:
   - Target files: `apps/backend/src/api/admin/ai/generate-copy/route.ts`, `apps/backend/src/admin/widgets/ai-copywriter.tsx`
   - Create authenticated admin REST API endpoint `POST /admin/ai/generate-copy` in backend API routes.
   - Refactor `ai-copywriter.tsx` to remove direct backend client imports and fetch data via HTTP POST request.

3. EMPIRICAL VERIFICATION & TESTING PHASE:
   - Run backend build verification: `cd apps/backend && npm run build`

4. PROCESS CLEANUP & LEARNING DIRECTIVE (CRITICAL):
   - Execute `/learn` to record Admin widget REST communication rules.
   - Terminate any running background dev servers or processes before completing turn.
</ANTIGRAVITY_WORKFLOW>

<ACCEPTANCE_CRITERIA>
- [ ] `ai-copywriter.tsx` contains zero direct imports of backend module files.
- [ ] `POST /admin/ai/generate-copy` REST API route handles Gemini AI copy generation.
- [ ] Backend build completes with exit code 0.
- [ ] All background tasks and processes are cleanly terminated.
</ACCEPTANCE_CRITERIA>
```

---
### Developer Prompt 3: Implement Native Medusa v2 Workflows (`@medusajs/workflows-sdk`)

```markdown
/goal

<TASK>
Implement transactional Medusa v2 workflows in `apps/backend/src/workflows/` with atomic steps and compensation rollbacks.
</TASK>

<ANTIGRAVITY_SLASH_COMMANDS>
- /goal: Execute autonomously until workflows pass Medusa v2 type checks.
- /browser: Verify Medusa v2 Workflows SDK patterns if needed.
- /learn: Persist Medusa v2 workflow architecture to .gemini/rules.
</ANTIGRAVITY_SLASH_COMMANDS>

<ANTIGRAVITY_WORKFLOW>
1. RESEARCH & INSPECTION PHASE:
   - Research `@medusajs/workflows-sdk` `createWorkflow` and `createStep` patterns.

2. IMPLEMENTATION PHASE:
   - Target files: `apps/backend/src/workflows/paymob-payment-workflow.ts`, `apps/backend/src/workflows/bosta-fulfillment-workflow.ts`, `apps/backend/src/workflows/eta-tax-workflow.ts`
   - Implement `createPaymobPaymentWorkflow` with atomic step to initiate payment and rollback compensation step on failure.
   - Implement `createBostaFulfillmentWorkflow` with delivery creation step and AWB rollback.
   - Implement `submitEtaTaxReceiptWorkflow` with payload formatting and retry compensation steps.

3. EMPIRICAL VERIFICATION & TESTING PHASE:
   - Run TypeScript check: `cd apps/backend && npx tsc --noEmit`
   - Run backend build verification: `cd apps/backend && npm run build`

4. PROCESS CLEANUP & LEARNING DIRECTIVE (CRITICAL):
   - Execute `/learn` to record Medusa v2 workflow execution patterns.
   - Terminate any running background dev servers or processes before completing turn.
</ANTIGRAVITY_WORKFLOW>

<ACCEPTANCE_CRITERIA>
- [ ] `src/workflows/` contains typed Medusa v2 workflows for Paymob, Bosta, and ETA Tax.
- [ ] Workflows include step compensation rollback logic.
- [ ] Backend build completes with exit code 0.
- [ ] All background tasks and processes are cleanly terminated.
</ACCEPTANCE_CRITERIA>
```

---
### Developer Prompt 4: Eliminate In-Memory `setImmediate()` Queues & Implement BullMQ Event Workers

```markdown
/goal

<TASK>
Remove fake in-memory `setImmediate()` queues and implement Redis BullMQ event workers for asynchronous background processing.
</TASK>

<ANTIGRAVITY_SLASH_COMMANDS>
- /goal: Execute autonomously until BullMQ background worker queue passes backend build tests.
</ANTIGRAVITY_SLASH_COMMANDS>

<ANTIGRAVITY_WORKFLOW>
1. RESEARCH & INSPECTION PHASE:
   - Search backend for `setImmediate` or in-memory array queues using `grep_search`.

2. IMPLEMENTATION PHASE:
   - Target files: `apps/backend/src/jobs/background-queue.ts`, `apps/backend/src/subscribers/order-placed-queue.ts`
   - Remove all `setImmediate()` in-memory queues.
   - Wire background tasks to Medusa event bus and Redis BullMQ queues (`background_jobs_queue`).

3. EMPIRICAL VERIFICATION & TESTING PHASE:
   - Run TypeScript check: `cd apps/backend && npx tsc --noEmit`
   - Run backend build verification: `cd apps/backend && npm run build`

4. PROCESS CLEANUP & LEARNING DIRECTIVE (CRITICAL):
   - Terminate any running background dev servers or processes before completing turn.
</ANTIGRAVITY_WORKFLOW>

<ACCEPTANCE_CRITERIA>
- [ ] Zero `setImmediate()` fake queues in codebase.
- [ ] Background tasks process via BullMQ / Medusa Event Bus.
- [ ] Backend build completes with exit code 0.
- [ ] All background tasks and processes are cleanly terminated.
</ACCEPTANCE_CRITERIA>
```

---
### Developer Prompt 5: Replace Local `Map` in `bosta/service.ts` with Distributed Redis Caching

```markdown
/goal

<TASK>
Replace local JavaScript `Map` rate cache in `bosta/service.ts` with distributed Redis key-value caching.
</TASK>

<ANTIGRAVITY_SLASH_COMMANDS>
- /goal: Execute autonomously until Bosta service distributed Redis caching compiles clean.
</ANTIGRAVITY_SLASH_COMMANDS>

<ANTIGRAVITY_WORKFLOW>
1. RESEARCH & INSPECTION PHASE:
   - View `apps/backend/src/modules/bosta/service.ts` and locate local `rateCacheMap`.

2. IMPLEMENTATION PHASE:
   - Target file: `apps/backend/src/modules/bosta/service.ts`
   - Replace `rateCacheMap` with Redis key-value caching (`BOSTA_RATE_<governorate_id>`, 1-hour TTL).

3. EMPIRICAL VERIFICATION & TESTING PHASE:
   - Run TypeScript check: `cd apps/backend && npx tsc --noEmit`
   - Run backend build verification: `cd apps/backend && npm run build`

4. PROCESS CLEANUP & LEARNING DIRECTIVE (CRITICAL):
   - Terminate any running background dev servers or processes before completing turn.
</ANTIGRAVITY_WORKFLOW>

<ACCEPTANCE_CRITERIA>
- [ ] `bosta/service.ts` contains zero local `Map` caches; uses Redis key-value store.
- [ ] Backend build completes with exit code 0.
- [ ] All background tasks and processes are cleanly terminated.
</ACCEPTANCE_CRITERIA>
```

---
### Developer Prompt 6: Implement Atomic Redis `NX` Transaction Lock for Paymob Webhook Idempotency

```markdown
/goal

<TASK>
Implement atomic Redis `NX` transaction locking in Paymob webhook controller to prevent duplicate callback execution.
</TASK>

<ANTIGRAVITY_SLASH_COMMANDS>
- /goal: Execute autonomously until Paymob webhook Redis lock passes build checks.
</ANTIGRAVITY_SLASH_COMMANDS>

<ANTIGRAVITY_WORKFLOW>
1. RESEARCH & INSPECTION PHASE:
   - View `apps/backend/src/api/hooks/paymob/route.ts`.

2. IMPLEMENTATION PHASE:
   - Target file: `apps/backend/src/api/hooks/paymob/route.ts`
   - Add atomic Redis key check `paymob_tx_<transactionId>` with `NX` and 24-hour TTL (86,400s).
   - If transaction key exists, return HTTP `200 OK` with `{ deduplicated: true }`.

3. EMPIRICAL VERIFICATION & TESTING PHASE:
   - Run TypeScript check: `cd apps/backend && npx tsc --noEmit`
   - Run backend build verification: `cd apps/backend && npm run build`

4. PROCESS CLEANUP & LEARNING DIRECTIVE (CRITICAL):
   - Terminate any running background dev servers or processes before completing turn.
</ANTIGRAVITY_WORKFLOW>

<ACCEPTANCE_CRITERIA>
- [ ] Paymob webhook route uses atomic Redis `NX` key lock (`paymob_tx_<id>`).
- [ ] Backend build completes with exit code 0.
- [ ] All background tasks and processes are cleanly terminated.
</ACCEPTANCE_CRITERIA>
```

---
### Developer Prompt 7: Implement ETA Subscriber Exponential Backoff & Dead-Letter Queue (DLQ)

```markdown
/goal

<TASK>
Refactor `order-placed-eta.ts` subscriber to use exponential backoff retry logic and Dead-Letter Queue (DLQ) logging.
</TASK>

<ANTIGRAVITY_SLASH_COMMANDS>
- /goal: Execute autonomously until ETA subscriber exponential backoff passes build verification.
- /learn: Persist Dead-Letter Queue (DLQ) retry patterns to .gemini/rules.
</ANTIGRAVITY_SLASH_COMMANDS>

<ANTIGRAVITY_WORKFLOW>
1. RESEARCH & INSPECTION PHASE:
   - View `apps/backend/src/subscribers/order-placed-eta.ts`.

2. IMPLEMENTATION PHASE:
   - Target file: `apps/backend/src/subscribers/order-placed-eta.ts`
   - Wrap ETA API submission in an exponential backoff retry loop (max 3 retries: 1s, 5s, 25s).
   - On final failure, write event record to `EtaReceiptAudit` table with status `FAILED_DLQ` for manual retry.

3. EMPIRICAL VERIFICATION & TESTING PHASE:
   - Run TypeScript check: `cd apps/backend && npx tsc --noEmit`
   - Run backend build verification: `cd apps/backend && npm run build`

4. PROCESS CLEANUP & LEARNING DIRECTIVE (CRITICAL):
   - Execute `/learn` to store DLQ retry patterns.
   - Terminate any running background dev servers or processes before completing turn.
</ANTIGRAVITY_WORKFLOW>

<ACCEPTANCE_CRITERIA>
- [ ] ETA subscriber includes exponential backoff retry loop (max 3 retries).
- [ ] Failed submissions log to `EtaReceiptAudit` with `FAILED_DLQ` status.
- [ ] Backend build completes with exit code 0.
- [ ] All background tasks and processes are cleanly terminated.
</ACCEPTANCE_CRITERIA>
```

---

## Phase 2: Storefront App Router & SDK Real Data Alignment

---
### Developer Prompt 8: Refactor Storefront Homepage (`app/page.tsx`) to React Server Component (Remove `"use client"`)

```markdown
/goal

<TASK>
Refactor Storefront homepage `apps/storefront/src/app/page.tsx` into a React Server Component by removing `"use client"`.
</TASK>

<ANTIGRAVITY_SLASH_COMMANDS>
- /goal: Execute autonomously until homepage compiles as a pure RSC.
</ANTIGRAVITY_SLASH_COMMANDS>

<ANTIGRAVITY_WORKFLOW>
1. RESEARCH & INSPECTION PHASE:
   - View `apps/storefront/src/app/page.tsx` and identify client-side state hooks causing `"use client"`.

2. IMPLEMENTATION PHASE:
   - Target file: `apps/storefront/src/app/page.tsx`
   - Extract interactive UI widgets (search bar, cart drawer) into small client components (`"use client"`).
   - Remove `"use client"` from `app/page.tsx` so top-level page renders as a pure React Server Component.

3. EMPIRICAL VERIFICATION & TESTING PHASE:
   - Run storefront build verification: `cd apps/storefront && npm run build`

4. PROCESS CLEANUP & LEARNING DIRECTIVE (CRITICAL):
   - Terminate any running background dev servers (e.g. `next dev`) before completing turn.
</ANTIGRAVITY_WORKFLOW>

<ACCEPTANCE_CRITERIA>
- [ ] `app/page.tsx` does NOT contain `"use client"` directive.
- [ ] Storefront build completes with exit code 0.
- [ ] All background tasks and dev servers are cleanly terminated.
</ACCEPTANCE_CRITERIA>
```

---
### Developer Prompt 9: Eliminate Hardcoded Mock Data & Wire Storefront to Live Medusa JS SDK

```markdown
/goal

<TASK>
Remove hardcoded `featuredProducts` and `sampleProducts` arrays from storefront and query live Medusa JS SDK.
</TASK>

<ANTIGRAVITY_SLASH_COMMANDS>
- /goal: Execute autonomously until storefront products load directly from Medusa JS SDK.
</ANTIGRAVITY_SLASH_COMMANDS>

<ANTIGRAVITY_WORKFLOW>
1. RESEARCH & INSPECTION PHASE:
   - Search for `sampleProducts` or `featuredProducts` across `apps/storefront` using `grep_search`.

2. IMPLEMENTATION PHASE:
   - Target files: `apps/storefront/src/app/page.tsx`, `apps/storefront/src/modules/products/components/product-list.tsx`
   - Delete mock product arrays.
   - Fetch live products using `medusa.products.list()` via `src/lib/medusa.ts`.

3. EMPIRICAL VERIFICATION & TESTING PHASE:
   - Run storefront build verification: `cd apps/storefront && npm run build`

4. PROCESS CLEANUP & LEARNING DIRECTIVE (CRITICAL):
   - Terminate any running background dev servers or processes before completing turn.
</ANTIGRAVITY_WORKFLOW>

<ACCEPTANCE_CRITERIA>
- [ ] Zero hardcoded `sampleProducts` or `featuredProducts` arrays in storefront code.
- [ ] Products fetch dynamically from Medusa SDK `medusa.products.list()`.
- [ ] Storefront build completes with exit code 0.
- [ ] All background tasks and dev servers are cleanly terminated.
</ACCEPTANCE_CRITERIA>
```

---
### Developer Prompt 10: Build Full Localized Egyptian `/checkout` Route

```markdown
/goal

<TASK>
Build complete localized Egyptian `/checkout` route with 27 Governorates selector, Paymob payment iframe, and COD submission.
</TASK>

<ANTIGRAVITY_SLASH_COMMANDS>
- /goal: Execute autonomously until checkout route passes storefront build tests.
- /learn: Persist Egyptian checkout UI flow to .gemini/rules.
</ANTIGRAVITY_SLASH_COMMANDS>

<ANTIGRAVITY_WORKFLOW>
1. RESEARCH & INSPECTION PHASE:
   - Inspect Governorate utilities `packages/shared-types/src/governorate-utils.ts` and Paymob payment provider.

2. IMPLEMENTATION PHASE:
   - Target file: `apps/storefront/src/app/[countryCode]/checkout/page.tsx`
   - Build multi-step checkout form:
     1. Customer shipping address with Egyptian Governorate & District dropdown.
     2. Bosta real-time shipping rate calculation display.
     3. Payment Method Selection (Paymob Card Iframe / Mobile Wallet OTP / ValU / COD).
     4. Order confirmation & Bosta waybill tracking link.

3. EMPIRICAL VERIFICATION & TESTING PHASE:
   - Run storefront build verification: `cd apps/storefront && npm run build`

4. PROCESS CLEANUP & LEARNING DIRECTIVE (CRITICAL):
   - Execute `/learn` to store Egyptian checkout UI patterns.
   - Terminate any running background dev servers or processes before completing turn.
</ANTIGRAVITY_WORKFLOW>

<ACCEPTANCE_CRITERIA>
- [ ] `app/[countryCode]/checkout/page.tsx` exists and compiles cleanly.
- [ ] Supports 27 Governorates selection, Bosta shipping rates, Paymob payment options, and COD.
- [ ] Storefront build completes with exit code 0.
- [ ] All background tasks and dev servers are cleanly terminated.
</ACCEPTANCE_CRITERIA>
```

---
### Developer Prompt 11: Build Customer `/account` Dashboard Route

```markdown
/goal

<TASK>
Build Customer `/account` dashboard route displaying order history, Bosta shipment tracking, and profile settings.
</TASK>

<ANTIGRAVITY_SLASH_COMMANDS>
- /goal: Execute autonomously until customer account dashboard compiles cleanly.
</ANTIGRAVITY_SLASH_COMMANDS>

<ANTIGRAVITY_WORKFLOW>
1. RESEARCH & INSPECTION PHASE:
   - Inspect Medusa JS SDK customer and order API methods.

2. IMPLEMENTATION PHASE:
   - Target file: `apps/storefront/src/app/[countryCode]/account/page.tsx`
   - Build customer dashboard UI showing placed orders, Bosta tracking links, saved shipping addresses, and phone number profile settings.

3. EMPIRICAL VERIFICATION & TESTING PHASE:
   - Run storefront build verification: `cd apps/storefront && npm run build`

4. PROCESS CLEANUP & LEARNING DIRECTIVE (CRITICAL):
   - Terminate any running background dev servers or processes before completing turn.
</ANTIGRAVITY_WORKFLOW>

<ACCEPTANCE_CRITERIA>
- [ ] `app/[countryCode]/account/page.tsx` exists and compiles cleanly.
- [ ] Displays customer order history and Bosta tracking status.
- [ ] Storefront build completes with exit code 0.
- [ ] All background tasks and dev servers are cleanly terminated.
</ACCEPTANCE_CRITERIA>
```

---
### Developer Prompt 12: Replace Standard `<img>` Tags with Optimized Next.js `<Image />` Components

```markdown
/goal

<TASK>
Replace standard HTML `<img>` tags across storefront with Next.js `<Image />` components for WebP conversion and responsive sizing.
</TASK>

<ANTIGRAVITY_SLASH_COMMANDS>
- /goal: Execute autonomously until all image tags are updated to Next.js Image components.
</ANTIGRAVITY_SLASH_COMMANDS>

<ANTIGRAVITY_WORKFLOW>
1. RESEARCH & INSPECTION PHASE:
   - Search for `<img>` tags across `apps/storefront` using `grep_search`.

2. IMPLEMENTATION PHASE:
   - Target files: `apps/storefront/src/modules/**/*`
   - Replace HTML `<img>` tags with `import Image from "next/image"`.
   - Add `alt`, `width`, `height`, `sizes`, and `priority` attributes.

3. EMPIRICAL VERIFICATION & TESTING PHASE:
   - Run storefront build verification: `cd apps/storefront && npm run build`

4. PROCESS CLEANUP & LEARNING DIRECTIVE (CRITICAL):
   - Terminate any running background dev servers or processes before completing turn.
</ANTIGRAVITY_WORKFLOW>

<ACCEPTANCE_CRITERIA>
- [ ] Zero unoptimized standard `<img>` tags in storefront components.
- [ ] Storefront build completes with exit code 0.
- [ ] All background tasks and dev servers are cleanly terminated.
</ACCEPTANCE_CRITERIA>
```

---

## Phase 3: DevOps, Monorepo & Container Optimization

---
### Developer Prompt 13: Add Root `package.json` Monorepo Workspaces Configuration

```markdown
/goal

<TASK>
Create root `package.json` with npm/pnpm workspaces configuration for monorepo package linking and hot-reloading.
</TASK>

<ANTIGRAVITY_SLASH_COMMANDS>
- /goal: Execute autonomously until workspace linking passes build check.
</ANTIGRAVITY_SLASH_COMMANDS>

<ANTIGRAVITY_WORKFLOW>
1. RESEARCH & INSPECTION PHASE:
   - Inspect workspace root directory structure using `list_dir`.

2. IMPLEMENTATION PHASE:
   - Target file: `package.json` (Root)
   - Create root `package.json` with `"private": true`, `"workspaces": ["apps/*", "packages/*"]`, and monorepo build scripts (`npm run build`).

3. EMPIRICAL VERIFICATION & TESTING PHASE:
   - Run workspace verification: `npm install && npm run build`

4. PROCESS CLEANUP & LEARNING DIRECTIVE (CRITICAL):
   - Terminate any running background dev servers or processes before completing turn.
</ANTIGRAVITY_WORKFLOW>

<ACCEPTANCE_CRITERIA>
- [ ] Root `package.json` includes `"workspaces": ["apps/*", "packages/*"]`.
- [ ] Root `npm run build` triggers build across apps and packages cleanly.
- [ ] All background tasks and dev servers are cleanly terminated.
</ACCEPTANCE_CRITERIA>
```

---
### Developer Prompt 14: Upgrade Backend & Storefront Dockerfiles to Multi-Stage Production Builds

```markdown
/goal

<TASK>
Rewrite Backend and Storefront Dockerfiles into multi-stage production builds running as non-root node users.
</TASK>

<ANTIGRAVITY_SLASH_COMMANDS>
- /goal: Execute autonomously until Docker Compose template validates with multi-stage builds.
</ANTIGRAVITY_SLASH_COMMANDS>

<ANTIGRAVITY_WORKFLOW>
1. RESEARCH & INSPECTION PHASE:
   - View `infrastructure/docker/Dockerfile.backend` and `infrastructure/docker/Dockerfile.storefront`.

2. IMPLEMENTATION PHASE:
   - Target files: `infrastructure/docker/Dockerfile.backend`, `infrastructure/docker/Dockerfile.storefront`
   - Rewrite Dockerfiles as 3-stage builds (`deps` $\rightarrow$ `builder` $\rightarrow$ `runner`).
   - Configure runner stage to execute under non-root `USER node` for security and minimal image size.

3. EMPIRICAL VERIFICATION & TESTING PHASE:
   - Run Docker config validation: `docker compose -f infrastructure/docker/docker-compose.tenant.yml config`

4. PROCESS CLEANUP & LEARNING DIRECTIVE (CRITICAL):
   - Terminate any active background tasks before completing turn.
</ANTIGRAVITY_WORKFLOW>

<ACCEPTANCE_CRITERIA>
- [ ] Dockerfiles use multi-stage builds (`deps`, `builder`, `runner`).
- [ ] Containers execute under non-root `node` user.
- [ ] All background tasks and dev servers are cleanly terminated.
</ACCEPTANCE_CRITERIA>
```

---
### Developer Prompt 15: Replace `sleep 5` in `provision-tenant.sh` with Healthcheck Polling

```markdown
/goal

<TASK>
Replace brittle `sleep 5` in `provision-tenant.sh` with PostgreSQL healthcheck polling (`pg_isready` / `curl` loop).
</TASK>

<ANTIGRAVITY_SLASH_COMMANDS>
- /goal: Execute autonomously until tenant provisioning script passes bash syntax check.
</ANTIGRAVITY_SLASH_COMMANDS>

<ANTIGRAVITY_WORKFLOW>
1. RESEARCH & INSPECTION PHASE:
   - View `infrastructure/scripts/provision-tenant.sh` and locate `sleep 5`.

2. IMPLEMENTATION PHASE:
   - Target file: `infrastructure/scripts/provision-tenant.sh`
   - Remove `sleep 5`.
   - Implement `until pg_isready ...` or Docker healthcheck polling loop to wait dynamically until PostgreSQL is ready before running `medusa db:migrate`.

3. EMPIRICAL VERIFICATION & TESTING PHASE:
   - Run bash syntax check: `bash -n infrastructure/scripts/provision-tenant.sh`

4. PROCESS CLEANUP & LEARNING DIRECTIVE (CRITICAL):
   - Terminate any running shell tasks before completing turn.
</ANTIGRAVITY_WORKFLOW>

<ACCEPTANCE_CRITERIA>
- [ ] Zero `sleep 5` arbitrary delays in `provision-tenant.sh`.
- [ ] Uses dynamic container healthcheck polling before executing database migrations.
- [ ] Script passes `bash -n` syntax check cleanly.
- [ ] All background tasks are cleanly terminated.
</ACCEPTANCE_CRITERIA>
```
