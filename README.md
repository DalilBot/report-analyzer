# Dedicated 7.9 Report Remediation Prompt Pack (`PROMPT_SEQUENCE_79_FINAL_REPORT_FIXES.md`)

This prompt pack contains **6 targeted developer prompts** engineered for **Google Antigravity Agentic IDE** to resolve the exact new defects identified in the latest 7.9/10 evaluation report: governorate ID mismatch across packages, ETA currency denomination verification, Paymob workflow mock fallback, Bosta webhook raw body HMAC, admin widget authentication, instrumentation file consolidation, storefront Suspense boundaries, and infrastructure Redis healthcheck / Caddy reload / duplicate compose cleanup. Zero older problems are included.

> [!IMPORTANT]
> **Subagent Directive**: Send these 6 prompts sequentially (Prompt 1 through Prompt 6) to your developer Antigravity instance. Every prompt explicitly instructs the agent to delegate research or sub-tasks to subagents (`invoke_subagent`).

---

## Part 1: Critical Data Alignment & Financial Integrity (Prompts 1–2)

---
### Developer Prompt 1: Fix Governorate ID Mismatch (EG-03/EG-04 Swap) Between Storefront & Shared-Types & Verify ETA Currency Denomination

```markdown
/goal

<TASK>
Fix the governorate ID swap between `apps/storefront/src/lib/data/governorates.ts` and `packages/shared-types/src/egypt-governorates.json` where EG-03/EG-04 are reversed, and verify ETA tax currency denomination logic in `order-placed-eta.ts`.
</TASK>

<SUBAGENT_DELEGATION_DIRECTIVE>
- Use `invoke_subagent` (Role: "Codebase Researcher", TypeName: "research") to read BOTH governorate data files side-by-side and identify all ID mismatches — not just EG-03/EG-04.
- Use a second `invoke_subagent` to inspect how Medusa v2's pricing module stores `tax_total` and `item.unit_price` in this project (major EGP units vs minor piastre units) by checking the database schema, seed scripts, and pricing configuration.
</SUBAGENT_DELEGATION_DIRECTIVE>

<ANTIGRAVITY_SLASH_COMMANDS>
- /goal: Execute autonomously until governorate IDs are consistent across the monorepo and ETA currency denomination is verified.
- /learn: Persist governorate ID canonical source rules to .gemini/rules.
</ANTIGRAVITY_SLASH_COMMANDS>

<ANTIGRAVITY_WORKFLOW>
1. RESEARCH & INSPECTION PHASE:
   - View `apps/storefront/src/lib/data/governorates.ts` (full file).
   - View `packages/shared-types/src/egypt-governorates.json` (full file).
   - View `apps/backend/src/modules/bosta/location-mapper.ts` governorate constants.
   - View `apps/backend/src/subscribers/order-placed-eta.ts` (lines 188 and 199).
   - View `apps/backend/medusa-config.ts` for pricing module configuration.

2. IMPLEMENTATION PHASE:
   - Target files: `apps/storefront/src/lib/data/governorates.ts`, `packages/shared-types/src/egypt-governorates.json`
   - **Governorate ID Alignment**: Establish `packages/shared-types/src/egypt-governorates.json` as the single canonical source. Update `apps/storefront/src/lib/data/governorates.ts` to match it exactly (EG-03 = Alexandria, EG-04 = Qalyubia — or whichever is geographically correct). Cross-check against Bosta's `location-mapper.ts` governorate constants.
   - **ETA Currency Denomination** (`order-placed-eta.ts`):
     - Line 188: If Medusa stores `tax_total` in minor units (piastres), remove the `* 100` multiplication. If it stores in major units (EGP), the multiplication is correct.
     - Line 199: If `item.unit_price` is in piastres, divide by 100 before passing as `unitPriceEgp`.
     - Add a defensive comment documenting the expected denomination contract.

3. EMPIRICAL VERIFICATION & TESTING PHASE:
   - Run TypeScript check: `cd apps/backend && npx tsc --noEmit`
   - Run shared-types build: `npm run build --workspace=packages/shared-types`
   - Run storefront build: `cd apps/storefront && npm run build`

4. PROCESS CLEANUP & LEARNING DIRECTIVE (CRITICAL):
   - Execute `/learn` to store governorate canonical source rules.
   - Terminate any running subagents, background dev servers, or processes before completing turn.
</ANTIGRAVITY_WORKFLOW>

<ACCEPTANCE_CRITERIA>
- [ ] Subagents delegated for governorate data comparison and Medusa pricing denomination research.
- [ ] Governorate IDs consistent across `shared-types`, `storefront/governorates.ts`, and `bosta/location-mapper.ts`.
- [ ] ETA currency denomination verified against actual Medusa pricing module output.
- [ ] All builds pass with exit code 0.
- [ ] All subagents and background tasks are cleanly terminated.
</ACCEPTANCE_CRITERIA>
```

---
### Developer Prompt 2: Remove Paymob Workflow Mock Payment Key Fallback & Fix Bosta Webhook Raw Body HMAC Verification

```markdown
/goal

<TASK>
Remove silent mock `paymentKey` fallback in `paymob-payment-workflow.ts:L67-69` and fix Bosta webhook HMAC to verify against `req.rawBody` instead of re-stringified `JSON.stringify(req.body)`.
</TASK>

<SUBAGENT_DELEGATION_DIRECTIVE>
- Use `invoke_subagent` to inspect Medusa v2 raw body access patterns for webhook routes and Paymob workflow error handling.
</SUBAGENT_DELEGATION_DIRECTIVE>

<ANTIGRAVITY_SLASH_COMMANDS>
- /goal: Execute autonomously until Paymob workflow throws on API failure and Bosta webhook uses raw body for HMAC.
- /learn: Persist webhook raw body HMAC verification rules to .gemini/rules.
</ANTIGRAVITY_SLASH_COMMANDS>

<ANTIGRAVITY_WORKFLOW>
1. RESEARCH & INSPECTION PHASE:
   - View `apps/backend/src/workflows/paymob-payment-workflow.ts` (lines 67–69).
   - View `apps/backend/src/api/hooks/bosta/route.ts` (HMAC computation section).

2. IMPLEMENTATION PHASE:
   - Target files: `apps/backend/src/workflows/paymob-payment-workflow.ts`, `apps/backend/src/api/hooks/bosta/route.ts`
   - **Paymob Workflow** (`paymob-payment-workflow.ts:L67-69`): Remove the `try/catch` block that silently generates a mock `paymentKey` when the Paymob API fails. In production, the step must throw to halt checkout — phantom orders with mock payment keys are a financial integrity risk.
   - **Bosta Webhook HMAC** (`hooks/bosta/route.ts`): Replace `JSON.stringify(req.body)` with `req.rawBody` (or equivalent raw request buffer) for HMAC computation. Re-stringification alters JSON key ordering, causing valid webhooks to fail signature verification.

3. EMPIRICAL VERIFICATION & TESTING PHASE:
   - Run TypeScript check: `cd apps/backend && npx tsc --noEmit`
   - Run backend build verification: `cd apps/backend && npm run build`

4. PROCESS CLEANUP & LEARNING DIRECTIVE (CRITICAL):
   - Execute `/learn` to store webhook HMAC raw body rules.
   - Terminate any running subagents, background dev servers, or processes before completing turn.
</ANTIGRAVITY_WORKFLOW>

<ACCEPTANCE_CRITERIA>
- [ ] Subagents delegated for raw body access pattern research.
- [ ] Paymob workflow throws on API failure instead of generating mock paymentKey.
- [ ] Bosta webhook HMAC computed from `req.rawBody`, not `JSON.stringify(req.body)`.
- [ ] Backend build completes with exit code 0.
- [ ] All subagents and background tasks are cleanly terminated.
</ACCEPTANCE_CRITERIA>
```

---

## Part 2: Admin Widget, Instrumentation & Dead Code Cleanup (Prompts 3–4)

---
### Developer Prompt 3: Fix Admin Widget Auth Headers, Route Through Async Queue, & Correct UI Copy ("Gemma" → "Gemini")

```markdown
/goal

<TASK>
Add `credentials: "include"` to admin widget fetch calls in `ai-copywriter.tsx`, route generation requests through the background worker queue, and fix the UI copy from "Gemma 4 31B" to "Gemini 1.5 Flash".
</TASK>

<SUBAGENT_DELEGATION_DIRECTIVE>
- Use `invoke_subagent` to inspect Medusa admin widget authentication patterns and background queue job submission API.
</SUBAGENT_DELEGATION_DIRECTIVE>

<ANTIGRAVITY_SLASH_COMMANDS>
- /goal: Execute autonomously until admin widget authenticates requests properly, uses async queue, and displays correct model name.
</ANTIGRAVITY_SLASH_COMMANDS>

<ANTIGRAVITY_WORKFLOW>
1. RESEARCH & INSPECTION PHASE:
   - View `apps/backend/src/admin/widgets/ai-copywriter.tsx` (full file).
   - View `apps/backend/src/jobs/background-queue.ts` (job submission API).

2. IMPLEMENTATION PHASE:
   - Target file: `apps/backend/src/admin/widgets/ai-copywriter.tsx`
   - **Authentication**: Add `credentials: "include"` to all `fetch("/admin/ai/generate-copy")` calls so admin session cookies are sent with requests.
   - **Async Queue Integration**: Instead of calling the synchronous `/admin/ai/generate-copy` endpoint directly, submit a job to the background queue and poll for results — leveraging the async AI processing architecture that was built for this purpose.
   - **UI Copy Fix**: Replace all references to "Gemma 4 31B IT REST API" with "Gemini 1.5 Flash" to match the actual model configured in the backend.

3. EMPIRICAL VERIFICATION & TESTING PHASE:
   - Run backend build verification: `cd apps/backend && npm run build`

4. PROCESS CLEANUP & LEARNING DIRECTIVE (CRITICAL):
   - Terminate any running subagents or background tasks before completing turn.
</ANTIGRAVITY_WORKFLOW>

<ACCEPTANCE_CRITERIA>
- [ ] Subagents delegated for admin widget auth pattern research.
- [ ] Admin widget fetch calls include `credentials: "include"`.
- [ ] AI copy generation routed through background queue for async processing.
- [ ] UI displays "Gemini 1.5 Flash" (not "Gemma 4 31B").
- [ ] Backend build completes with exit code 0.
- [ ] All subagents and background tasks are cleanly terminated.
</ACCEPTANCE_CRITERIA>
```

---
### Developer Prompt 4: Consolidate Duplicate Instrumentation Files, Resolve Redis from Medusa Container, & Remove Dead `encryptPii` Call

```markdown
/goal

<TASK>
Consolidate `apps/backend/instrumentation.ts` and `apps/backend/src/instrumentation.ts` into a single file, replace standalone `new Redis()` in route handlers with Medusa container resolution, and remove the dead `encryptPii` call in `order-placed-eta.ts`.
</TASK>

<SUBAGENT_DELEGATION_DIRECTIVE>
- Use `invoke_subagent` to search the backend codebase for all `new Redis()` instantiations in route handlers and all unused variable assignments.
</SUBAGENT_DELEGATION_DIRECTIVE>

<ANTIGRAVITY_SLASH_COMMANDS>
- /goal: Execute autonomously until instrumentation is consolidated, Redis connections use Medusa DI, and dead code is removed.
- /learn: Persist Medusa container Redis resolution rules to .gemini/rules.
</ANTIGRAVITY_SLASH_COMMANDS>

<ANTIGRAVITY_WORKFLOW>
1. RESEARCH & INSPECTION PHASE:
   - View `apps/backend/instrumentation.ts` (root file).
   - View `apps/backend/src/instrumentation.ts`.
   - Search for `new Redis(` across `apps/backend/src/api/`.
   - View `apps/backend/src/subscribers/order-placed-eta.ts` (lines 193–204).

2. IMPLEMENTATION PHASE:
   - Target files: `apps/backend/instrumentation.ts`, `apps/backend/src/instrumentation.ts`, route handlers with `new Redis()`, `apps/backend/src/subscribers/order-placed-eta.ts`
   - **Consolidate Instrumentation**: Merge all OpenTelemetry meter/exporter configuration into `apps/backend/src/instrumentation.ts` (the Medusa-standard location). Delete or empty the root `instrumentation.ts` to prevent duplicate metric registration.
   - **Redis Container Resolution**: Replace `new Redis()` instantiations at module scope in route handlers with `req.scope.resolve("redis")` or the appropriate Medusa container key to prevent connection leaks during hot reloads.
   - **Dead Code Removal** (`order-placed-eta.ts:L193-204`): Remove the `encryptPii(customerPhone)` call and the unused `encryptedPhone` variable. The ETA portal requires plaintext phone numbers, so the encryption result was never used.

3. EMPIRICAL VERIFICATION & TESTING PHASE:
   - Run TypeScript check: `cd apps/backend && npx tsc --noEmit`
   - Run backend build verification: `cd apps/backend && npm run build`

4. PROCESS CLEANUP & LEARNING DIRECTIVE (CRITICAL):
   - Execute `/learn` to store Redis container resolution rules.
   - Terminate any running subagents, background dev servers, or processes before completing turn.
</ANTIGRAVITY_WORKFLOW>

<ACCEPTANCE_CRITERIA>
- [ ] Subagents delegated for Redis instantiation and dead code scan.
- [ ] Single consolidated `src/instrumentation.ts` file with all OpenTelemetry configuration.
- [ ] Zero standalone `new Redis()` in route handlers — all resolved from Medusa container.
- [ ] Dead `encryptPii` call and unused `encryptedPhone` variable removed.
- [ ] Backend build completes with exit code 0.
- [ ] All subagents and background tasks are cleanly terminated.
</ACCEPTANCE_CRITERIA>
```

---

## Part 3: Storefront & Infrastructure Polish (Prompts 5–6)

---
### Developer Prompt 5: Add Storefront `<Suspense>` Boundaries for Streaming SSR, Delete Legacy `tailwind.config.ts`, & Fix Add-to-Cart Type Safety

```markdown
/goal

<TASK>
Wrap data-fetching components in `<Suspense>` boundaries on `page.tsx` and `[countryCode]/page.tsx`, delete the unused legacy `tailwind.config.ts`, and replace `(product as any).variants` with properly typed props in `add-to-cart-button.tsx`.
</TASK>

<SUBAGENT_DELEGATION_DIRECTIVE>
- Use `invoke_subagent` to inspect Next.js 15 Suspense streaming patterns and Tailwind v4 CSS-first configuration.
</SUBAGENT_DELEGATION_DIRECTIVE>

<ANTIGRAVITY_SLASH_COMMANDS>
- /goal: Execute autonomously until storefront pages use Suspense streaming, legacy config is removed, and product types are clean.
</ANTIGRAVITY_SLASH_COMMANDS>

<ANTIGRAVITY_WORKFLOW>
1. RESEARCH & INSPECTION PHASE:
   - View `apps/storefront/src/app/page.tsx`.
   - View `apps/storefront/src/app/[countryCode]/page.tsx`.
   - View `apps/storefront/tailwind.config.ts`.
   - View `apps/storefront/src/modules/products/components/add-to-cart-button.tsx`.
   - View `apps/storefront/src/app/globals.css` for Tailwind v4 CSS-first config.

2. IMPLEMENTATION PHASE:
   - Target files: `apps/storefront/src/app/page.tsx`, `apps/storefront/src/app/[countryCode]/page.tsx`, `apps/storefront/tailwind.config.ts`, `apps/storefront/src/modules/products/components/add-to-cart-button.tsx`
   - **Suspense Boundaries**: Extract the `await fetchLiveStorefrontProducts()` data-fetching call into a child async Server Component, then wrap it with `<Suspense fallback={<ProductGridSkeleton />}>` so the page shell renders immediately and product data streams in — improving TTFB.
   - **Delete Legacy Config**: Delete `apps/storefront/tailwind.config.ts` — Tailwind v4 uses CSS-based configuration in `globals.css`, making the TS config file dead code.
   - **Add-to-Cart Type Safety**: Replace `(product as any).variants` in `add-to-cart-button.tsx` with properly typed product props using the Medusa `HttpTypes.StoreProduct` type or the project's shared product type.

3. EMPIRICAL VERIFICATION & TESTING PHASE:
   - Run storefront build verification: `cd apps/storefront && npm run build`

4. PROCESS CLEANUP & LEARNING DIRECTIVE (CRITICAL):
   - Terminate any running subagents, background dev servers (e.g. `next dev`) before completing turn.
</ANTIGRAVITY_WORKFLOW>

<ACCEPTANCE_CRITERIA>
- [ ] Subagents delegated for Suspense streaming and Tailwind v4 research.
- [ ] Homepage and countryCode pages use `<Suspense>` boundaries for streaming SSR.
- [ ] Legacy `tailwind.config.ts` deleted.
- [ ] `add-to-cart-button.tsx` uses typed product props (zero `as any` on product).
- [ ] Storefront build completes with exit code 0.
- [ ] All subagents and background tasks are cleanly terminated.
</ACCEPTANCE_CRITERIA>
```

---
### Developer Prompt 6: Fix Redis Healthcheck Variable, Add Caddy Reload on Fallback, & Consolidate Duplicate Docker Compose Files

```markdown
/goal

<TASK>
Fix Redis healthcheck `REDIS_PASSWORD` injection in `docker-compose.yml`, add `caddy reload` after Caddyfile fallback append in `caddy-domain-router.sh`, and consolidate duplicate Docker Compose files.
</TASK>

<SUBAGENT_DELEGATION_DIRECTIVE>
- Use `invoke_subagent` to inspect Docker Compose Redis healthcheck environment variable injection and Caddy configuration reload commands.
</SUBAGENT_DELEGATION_DIRECTIVE>

<ANTIGRAVITY_SLASH_COMMANDS>
- /goal: Execute autonomously until Redis healthcheck authenticates properly, Caddy reloads on fallback, and duplicate compose files are consolidated.
- /learn: Persist Docker Compose healthcheck and Caddy reload rules to .gemini/rules.
</ANTIGRAVITY_SLASH_COMMANDS>

<ANTIGRAVITY_WORKFLOW>
1. RESEARCH & INSPECTION PHASE:
   - View `infrastructure/docker/docker-compose.yml` (line 37 and Redis service block).
   - View `infrastructure/docker/docker-compose.tenant.yml` (compare with above).
   - View `infrastructure/scripts/caddy-domain-router.sh` (fallback code path).

2. IMPLEMENTATION PHASE:
   - Target files: `infrastructure/docker/docker-compose.yml`, `infrastructure/docker/docker-compose.tenant.yml`, `infrastructure/scripts/caddy-domain-router.sh`
   - **Redis Healthcheck Fix** (`docker-compose.yml:L37`): Inject `REDIS_PASSWORD` into the Redis service's `environment:` block so the healthcheck command (`redis-cli -a $$REDIS_PASSWORD ping`) can authenticate. Without it, the healthcheck always falls back to default (no auth), failing on password-protected Redis.
   - **Caddy Reload** (`caddy-domain-router.sh`): After the fallback code path appends a new route block to the Caddyfile, add `caddy reload --config /etc/caddy/Caddyfile` (or `docker exec caddy caddy reload`) so the new routes actually become active.
   - **Consolidate Compose Files**: Since `docker-compose.yml` and `docker-compose.tenant.yml` are identical (2955 bytes each), delete one and keep a single canonical `docker-compose.yml`. Update any scripts that reference the deleted file.

3. EMPIRICAL VERIFICATION & TESTING PHASE:
   - Run Docker compose config validation: `docker compose -f infrastructure/docker/docker-compose.yml config`
   - Run bash syntax check: `bash -n infrastructure/scripts/caddy-domain-router.sh`

4. PROCESS CLEANUP & LEARNING DIRECTIVE (CRITICAL):
   - Execute `/learn` to store Docker healthcheck and Caddy reload rules.
   - Terminate any active subagents or background tasks before completing turn.
</ANTIGRAVITY_WORKFLOW>

<ACCEPTANCE_CRITERIA>
- [ ] Subagents delegated for Docker healthcheck and Caddy reload inspection.
- [ ] Redis service `environment:` block includes `REDIS_PASSWORD` for healthcheck auth.
- [ ] `caddy-domain-router.sh` fallback path executes `caddy reload` after Caddyfile append.
- [ ] Duplicate Docker Compose files consolidated to a single canonical file.
- [ ] Docker Compose config and bash scripts pass validation.
- [ ] All subagents and background tasks are cleanly terminated.
</ACCEPTANCE_CRITERIA>
```
