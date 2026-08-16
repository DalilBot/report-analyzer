# Master 15-Defect Remediation Prompt Pack (`PROMPT_SEQUENCE_15_DEFECTS_MASTER_FIXES.md`)

This prompt pack contains **5 targeted developer prompts** engineered for **Google Antigravity Agentic IDE** to systematically resolve all **15 verified defects** (4 Critical, 4 High, 7 Medium/Low) identified in the August 2026 Comprehensive Evaluation Report, boosting the Deployment Readiness Index from **91.5% to 100.0%**:

- **🔴 Critical 1**: `Boolean(process.env.ETA_HSM_ENABLED)` string truthiness trap in `hsm-signer.ts:L31`
- **🔴 Critical 2**: Cash on Delivery (COD) misclassification on prepaid orders in `bosta/service.ts:L266-L288`
- **🔴 Critical 3**: Double `/state` path in ETA receipt cancellation URL in `eta-tax/client.ts:L280`
- **🔴 Critical 4**: Regional shipping fee drift between storefront `governorates.ts` and backend `rate-calculator.ts`
- **🟡 High 5**: BullMQ shared Redis connection stalling queue commands in `background-queue.ts:L59,L200`
- **🟡 High 6**: Unregistered `"redis"` client in Medusa container scope (`paymob/route.ts` & `worker-loader.ts`)
- **🟡 High 7**: Dual module & provider registration for ETA Tax in `medusa-config.ts:L103-L125`
- **🟡 High 8**: Protected field access `bostaClient_` in `bosta-fulfillment-workflow.ts:L48,L124`
- **🟢 Medium/Low 9–15**: CLI positional secrets & hardcoded TRN in `provision-tenant.sh`, hardcoded storefront search products in `smart-search-bar.tsx`, ETA ISO date milliseconds stripping in `payload-builder.ts`, Gemini prompt `keyFeatures` interpolation, Admin AI rate limiter keying by actor ID, hardcoded secret fallbacks in `medusa-config.ts`, and public storefront backend URL in provisioning.

> [!IMPORTANT]
> **Subagent Directive**: Send these 5 prompts sequentially (Prompt 1 through Prompt 5) to your developer Antigravity instance. Every prompt explicitly instructs the agent to delegate research or sub-tasks to subagents (`invoke_subagent`).

---

## Part 1: Critical Production & Financial Blockers (Prompt 1)

---
### Developer Prompt 1: Fix 4 Critical Blockers (HSM Boolean Trap, Bosta COD Overcharge, ETA Cancel 404 & Regional Shipping Drift)

```markdown
/goal

<TASK>
Resolve the 4 Critical Severity production defects:
1. Fix `Boolean(process.env.ETA_HSM_ENABLED)` string truthiness trap in `apps/backend/src/modules/eta-tax/hsm-signer.ts:L31`.
2. Fix Cash on Delivery (COD) misclassification on prepaid orders in `apps/backend/src/modules/bosta/service.ts:L266-L288`.
3. Fix double `/state` path in ETA receipt cancellation URL in `apps/backend/src/modules/eta-tax/client.ts:L280`.
4. Fix regional shipping fee drift in `apps/storefront/src/lib/data/governorates.ts:L28-L40` to match backend 4-tier rate matrix.
</TASK>

<SUBAGENT_DELEGATION_DIRECTIVE>
- Use `invoke_subagent` (Role: "Critical Defects Specialist", TypeName: "research") to inspect all 4 target files and verify the exact line numbers and code snippets before editing.
</SUBAGENT_DELEGATION_DIRECTIVE>

<ANTIGRAVITY_SLASH_COMMANDS>
- /goal: Execute autonomously until all 4 critical bugs are fixed, tested, and verified.
- /learn: Persist critical bug fixes and regional fee sync rules to .gemini/rules.
</ANTIGRAVITY_SLASH_COMMANDS>

<ANTIGRAVITY_WORKFLOW>
1. RESEARCH & INSPECTION PHASE:
   - View `apps/backend/src/modules/eta-tax/hsm-signer.ts` (lines 25–40).
   - View `apps/backend/src/modules/bosta/service.ts` (lines 260–295).
   - View `apps/backend/src/modules/eta-tax/client.ts` (lines 275–290).
   - View `apps/storefront/src/lib/data/governorates.ts` (lines 20–50) vs `apps/backend/src/modules/bosta/rate-calculator.ts` (lines 40–55).

2. IMPLEMENTATION PHASE:
   - **Bug 1: HSM Boolean Casting Trap** (`hsm-signer.ts:L31`):
     ```typescript
     // BEFORE:
     this.enabled = options.enabled !== undefined ? options.enabled : Boolean(process.env.ETA_HSM_ENABLED);

     // AFTER:
     this.enabled = options.enabled !== undefined
       ? options.enabled
       : process.env.ETA_HSM_ENABLED === "true";
     ```
     *Rationale*: In JS, `Boolean("false") === true`. When `ETA_HSM_ENABLED=false` in dev/CI without a physical USB token, the app previously attempted hardware connection and crashed.

   - **Bug 2: Bosta Prepaid COD Misclassification** (`bosta/service.ts:L266-L288`):
     ```typescript
     // BEFORE:
     const codAmount = (data.is_cod as boolean) || (order as any)?.payment_status === "awaiting" ? (order as any)?.total || 0 : 0;
     ...
     deliveryPayload.type = Number(codAmount) > 0 ? 10 : 1;

     // AFTER:
     const isCod = Boolean(data.is_cod);
     const codAmount = isCod ? Number((order as any)?.total || 0) : 0;
     deliveryPayload.type = isCod && codAmount > 0 ? 10 : 1;
     ```
     *Rationale*: Prevents orders paid via Paymob (with `payment_status: "awaiting"`) from being dispatched as Type 10 (Cash Collection), which caused couriers to double-charge customers in cash.

   - **Bug 3: ETA Cancel URL 404 Fix** (`eta-tax/client.ts:L280`):
     ```typescript
     // BEFORE:
     const response = await this.fetchWithTimeout(`${this.baseUrl}/receipts/state/${uuid}/state`, {

     // AFTER:
     const response = await this.fetchWithTimeout(`${this.baseUrl}/receipts/${uuid}/state`, {
     ```
     *Rationale*: Official ETA e-Receipt API endpoint is `PUT /api/v1/receipts/{uuid}/state`. The duplicated `/state/` caused SAGA rollback cancellations to 404.

   - **Bug 4: Regional Shipping Fee Parity** (`apps/storefront/src/lib/data/governorates.ts:L28-L40`):
     Update storefront governorate pricing to strictly align with backend `rate-calculator.ts` 4-tier matrix:
     - Greater Cairo (EG-01 Cairo, EG-02 Giza): **45 EGP**
     - Delta & Canal (EG-03 to EG-14): **60 EGP**
     - Upper Egypt (EG-18 to EG-25: Asyut, Sohag, Qena, Luxor, Aswan, Beni Suef, Minya, Faiyum): **75 EGP**
     - Frontier, Sinai & Red Sea (EG-15, EG-16, EG-17, EG-26, EG-27: Red Sea, New Valley, Matrouh, North/South Sinai): **95 EGP**

3. EMPIRICAL VERIFICATION & TESTING PHASE:
   - Run backend typecheck: `cd apps/backend && npx tsc --noEmit`
   - Run storefront typecheck: `cd apps/storefront && npx tsc --noEmit`

4. PROCESS CLEANUP & LEARNING DIRECTIVE (CRITICAL):
   - Execute `/learn` to store critical bug prevention rules.
   - Terminate any running subagents, background dev servers, or processes before completing turn.
</ANTIGRAVITY_WORKFLOW>

<ACCEPTANCE_CRITERIA>
- [ ] Subagents delegated for 4 critical defect inspections.
- [ ] `hsm-signer.ts` uses strict `process.env.ETA_HSM_ENABLED === "true"`.
- [ ] `bosta/service.ts` only sets `type: 10` when `data.is_cod` is explicitly true.
- [ ] `eta-tax/client.ts` cancellation URL uses `${this.baseUrl}/receipts/${uuid}/state`.
- [ ] `governorates.ts` rates match backend 4-tier pricing (45 / 60 / 75 / 95 EGP).
- [ ] All packages compile cleanly with exit code 0.
- [ ] All subagents and background tasks cleanly terminated.
</ACCEPTANCE_CRITERIA>
```

---

## Part 2: Concurrency & Architectural Defects (Prompt 2)

---
### Developer Prompt 2: Fix 4 High Severity Defects (BullMQ Redis Isolation, Container Redis DI, ETA Module Separation & Bosta Protected Accessor)

```markdown
/goal

<TASK>
Resolve the 4 High Severity architectural defects:
1. Fix BullMQ shared Redis client connection stalling queue commands in `apps/backend/src/jobs/background-queue.ts:L59,L200`.
2. Register `"redis"` client explicitly in Medusa DI container in `apps/backend/src/loaders/worker-loader.ts`.
3. Separate ETA Tax provider (`AbstractTaxProvider`) from DML audit module in `apps/backend/medusa-config.ts:L103-L125`.
4. Add public `getClient()` accessor in `apps/backend/src/modules/bosta/service.ts` to replace protected `bostaClient_` access in `bosta-fulfillment-workflow.ts:L48,L124`.
</TASK>

<SUBAGENT_DELEGATION_DIRECTIVE>
- Use `invoke_subagent` (Role: "Architecture & Concurrency Specialist", TypeName: "research") to inspect BullMQ connection pooling, Medusa loader container bindings, and Bosta workflow client resolution.
</SUBAGENT_DELEGATION_DIRECTIVE>

<ANTIGRAVITY_SLASH_COMMANDS>
- /goal: Execute autonomously until Redis connections are isolated, container DI is clean, and workflow accessors are encapsulated.
- /learn: Persist BullMQ connection isolation and Medusa container binding rules to .gemini/rules.
</ANTIGRAVITY_SLASH_COMMANDS>

<ANTIGRAVITY_WORKFLOW>
1. RESEARCH & INSPECTION PHASE:
   - View `apps/backend/src/jobs/background-queue.ts` (lines 50–65 and 190–210).
   - View `apps/backend/src/loaders/worker-loader.ts`.
   - View `apps/backend/medusa-config.ts` (lines 100–130).
   - View `apps/backend/src/modules/bosta/service.ts` and `apps/backend/src/workflows/bosta-fulfillment-workflow.ts`.

2. IMPLEMENTATION PHASE:
   - **Bug 5: BullMQ Dedicated Redis Connection Config** (`background-queue.ts`):
     Instead of passing a shared `getRedisConnection()` ioredis singleton to both `Queue` and `Worker`, pass the dedicated connection config object:
     ```typescript
     const redisConnectionOptions = {
       url: process.env.REDIS_URL || "redis://localhost:6379",
       maxRetriesPerRequest: null,
       lazyConnect: true,
     };

     this.queue = new Queue(QUEUE_NAME, { connection: redisConnectionOptions });
     this.worker = new Worker(QUEUE_NAME, async (job) => { ... }, { connection: redisConnectionOptions, concurrency: 2 });
     ```
     *Rationale*: Eliminates worker blocking commands (`brpop`) from blocking queue enqueue operations under high traffic.

   - **Bug 6: Medusa Container Redis Registration** (`worker-loader.ts`):
     In `apps/backend/src/loaders/worker-loader.ts`, explicitly bind the Redis client into the Medusa container:
     ```typescript
     import { asValue } from "awilix";
     import { getRedisConnection } from "../jobs/background-queue";

     export default async function workerLoader({ container }: LoaderOptions) {
       const redisClient = getRedisConnection();
       container.register({
         redis: asValue(redisClient),
       });
       startWorker(container);
     }
     ```
     *Rationale*: Resolves `req.scope.resolve("redis")` in `paymob/route.ts` and `generate-copy/route.ts` cleanly without 503 fallback errors.

   - **Bug 7: ETA Tax Provider vs Module Separation** (`medusa-config.ts` & `src/modules/eta-tax/`):
     Ensure `medusa-config.ts` registers `eta-tax` cleanly:
     - Under `modules`: Register `resolve: "./src/modules/eta-tax"` (which exports the custom module with `EtaReceiptAudit` DML model).
     - Under `@medusajs/medusa/tax` provider: Point to `./src/modules/eta-tax/provider` or register calculation provider options without duplicating root module declarations.

   - **Bug 8: Bosta Public Client Accessor** (`bosta/service.ts` & `bosta-fulfillment-workflow.ts`):
     In `apps/backend/src/modules/bosta/service.ts`, add:
     ```typescript
     public getClient(): BostaClient {
       return this.bostaClient_;
     }
     ```
     In `bosta-fulfillment-workflow.ts:L48,L124`, replace `bostaService?.bostaClient_` with `bostaService?.getClient() || new BostaClient(options)`.

3. EMPIRICAL VERIFICATION & TESTING PHASE:
   - Run backend typecheck: `cd apps/backend && npx tsc --noEmit`
   - Run backend build verification: `cd apps/backend && npm run build`

4. PROCESS CLEANUP & LEARNING DIRECTIVE (CRITICAL):
   - Execute `/learn` to store architecture rules.
   - Terminate any running subagents, background dev servers, or processes before completing turn.
</ANTIGRAVITY_WORKFLOW>

<ACCEPTANCE_CRITERIA>
- [ ] Subagents delegated for BullMQ, loader DI, and Bosta workflow inspection.
- [ ] `background-queue.ts` passes connection options object to `Queue` and `Worker`.
- [ ] `worker-loader.ts` registers `redis` client in Medusa DI container.
- [ ] `medusa-config.ts` cleanly structures ETA Tax provider and module registrations.
- [ ] `bosta/service.ts` exports public `getClient()` method used by workflows.
- [ ] Backend build completes with exit code 0.
- [ ] All subagents and background tasks cleanly terminated.
</ACCEPTANCE_CRITERIA>
```

---

## Part 3: Data Quality, AI Prompt Context & Security Hardening (Prompt 3)

---
### Developer Prompt 3: Fix 4 Quality Defects (ETA Millisecond Stripping, Gemini `keyFeatures`, Admin Rate Limit Actor Key & Hardcoded Secrets)

```markdown
/goal

<TASK>
Resolve 4 Medium/Low Severity defects:
1. Strip millisecond fraction from ETA ISO date strings in `apps/backend/src/modules/eta-tax/payload-builder.ts:L142`.
2. Interpolate `keyFeatures` in Gemini AI prompt builder in `apps/backend/src/modules/gemini-ai/client.ts:L79`.
3. Key Admin AI rate limiter by authenticated `actor_id || clientIp` in `apps/backend/src/api/admin/ai/generate-copy/route.ts:L65`.
4. Remove insecure development secret fallbacks from production paths in `apps/backend/medusa-config.ts:L60-L61`.
</TASK>

<SUBAGENT_DELEGATION_DIRECTIVE>
- Use `invoke_subagent` to inspect `payload-builder.ts` date formatting, `gemini-ai/client.ts` prompt templates, `generate-copy/route.ts` rate limiting, and `medusa-config.ts` secret options.
</SUBAGENT_DELEGATION_DIRECTIVE>

<ANTIGRAVITY_SLASH_COMMANDS>
- /goal: Execute autonomously until ETA dates comply with strict ISO schema, Gemini prompts include keyFeatures, and rate limiting keys by actor ID.
- /learn: Persist ETA date schema and Gemini prompt context rules to .gemini/rules.
</ANTIGRAVITY_SLASH_COMMANDS>

<ANTIGRAVITY_WORKFLOW>
1. RESEARCH & INSPECTION PHASE:
   - View `apps/backend/src/modules/eta-tax/payload-builder.ts` (lines 135–150).
   - View `apps/backend/src/modules/gemini-ai/client.ts` (lines 70–105).
   - View `apps/backend/src/api/admin/ai/generate-copy/route.ts` (lines 55–75).
   - View `apps/backend/medusa-config.ts` (lines 50–65).

2. IMPLEMENTATION PHASE:
   - **Bug 11: ETA ISO Date Without Milliseconds** (`payload-builder.ts:L142`):
     ```typescript
     // BEFORE:
     dateTimeIssued: (input.issuedDate || new Date()).toISOString(),

     // AFTER:
     dateTimeIssued: (input.issuedDate || new Date()).toISOString().replace(/\.\d{3}Z$/, "Z"),
     ```
     *Rationale*: Conforms to strict ETA XML/JSON schema validation requiring `YYYY-MM-DDTHH:mm:ssZ` without fractional milliseconds.

   - **Bug 12: Gemini AI `keyFeatures` Interpolation** (`gemini-ai/client.ts:L79`):
     Update `buildPromptText()` in `client.ts` to append `keyFeatures` when present:
     ```typescript
     let prompt = `اسم المنتج: ${safeTitle}\nالفئة: ${safeCategory}\n`;
     if (input.keyFeatures && input.keyFeatures.length > 0) {
       prompt += `المميزات الرئيسية:\n${input.keyFeatures.map((f) => `- ${f}`).join("\n")}\n`;
     }
     ```
     *Rationale*: Merchant-provided product selling points are no longer dropped from the LLM prompt.

   - **Bug 13: Admin AI Rate Limiter Actor Keying** (`generate-copy/route.ts:L65`):
     ```typescript
     // BEFORE:
     const rateLimitKey = "ratelimit:ai:" + clientIp;

     // AFTER:
     const actorId = (req as any).auth_context?.actor_id;
     const rateLimitKey = "ratelimit:ai:" + (actorId || clientIp);
     ```
     *Rationale*: Prevents multiple store operators on the same corporate VPN from exhausting a shared rate limit.

   - **Bug 14: Clean Secret Configuration in Production** (`medusa-config.ts`):
     Ensure production checks strictly enforce `process.env.JWT_SECRET` and `process.env.COOKIE_SECRET` presence without relying on insecure development strings.

3. EMPIRICAL VERIFICATION & TESTING PHASE:
   - Run backend typecheck: `cd apps/backend && npx tsc --noEmit`
   - Run backend build verification: `cd apps/backend && npm run build`

4. PROCESS CLEANUP & LEARNING DIRECTIVE (CRITICAL):
   - Terminate any running subagents, background dev servers, or processes before completing turn.
</ANTIGRAVITY_WORKFLOW>

<ACCEPTANCE_CRITERIA>
- [ ] Subagents delegated for date format, AI prompt, and rate limit inspection.
- [ ] `payload-builder.ts` formats `dateTimeIssued` without millisecond fraction (`.replace(/\.\d{3}Z$/, "Z")`).
- [ ] `gemini-ai/client.ts` interpolates `keyFeatures` into prompt.
- [ ] `generate-copy/route.ts` keys rate limit on `actor_id || clientIp`.
- [ ] Backend build completes with exit code 0.
- [ ] All subagents and background tasks cleanly terminated.
</ACCEPTANCE_CRITERIA>
```

---

## Part 4: Storefront Search & Provisioning Hardening (Prompt 4)

---
### Developer Prompt 4: Fix Storefront Dynamic Search Catalog & Hardened Multi-Tenant Provisioning Script

```markdown
/goal

<TASK>
Resolve remaining Storefront & DevOps defects:
1. Replace hardcoded 4-product sample array in `apps/storefront/src/modules/search/components/smart-search-bar.tsx:L34-L39` with dynamic search support or prop-driven product catalog.
2. In `infrastructure/scripts/provision-tenant.sh`, remove positional secret CLI arguments, set `NEXT_PUBLIC_MEDUSA_BACKEND_URL=https://${CUSTOM_DOMAIN}` for custom domains, and prompt for real `ETA_TAX_REGISTRATION_NUMBER`.
</TASK>

<SUBAGENT_DELEGATION_DIRECTIVE>
- Use `invoke_subagent` to inspect `smart-search-bar.tsx` search handling and `provision-tenant.sh` environment generation lines.
</SUBAGENT_DELEGATION_DIRECTIVE>

<ANTIGRAVITY_SLASH_COMMANDS>
- /goal: Execute autonomously until storefront search accepts live product data and provisioning generates production-safe environment files.
- /learn: Persist storefront dynamic search and DevOps secret provisioning rules to .gemini/rules.
</ANTIGRAVITY_SLASH_COMMANDS>

<ANTIGRAVITY_WORKFLOW>
1. RESEARCH & INSPECTION PHASE:
   - View `apps/storefront/src/modules/search/components/smart-search-bar.tsx` (lines 25–60).
   - View `infrastructure/scripts/provision-tenant.sh` (lines 1–85).

2. IMPLEMENTATION PHASE:
   - **Bug 10: Storefront Dynamic Search Bar** (`smart-search-bar.tsx:L34-L39`):
     Update `SmartSearchBar` component to accept `initialProducts?: SearchResultItem[]` as an optional prop with fallback, or query `/api/products` dynamically on input change, so searching queries the live Medusa catalog rather than 4 hardcoded static dummy items.

   - **Bug 9 & 15: Provisioning Script Hardening** (`provision-tenant.sh`):
     - Remove plaintext positional CLI argument defaults for keys (`PAYMOB_API_KEY="${1:-...}"`). Read from existing environment variables or prompt securely.
     - Set `ETA_TAX_REGISTRATION_NUMBER="${ETA_TAX_REGISTRATION_NUMBER:-}"` and validate presence before writing to `.env`.
     - When `CUSTOM_DOMAIN` is set (e.g. `store.example.com`), write `NEXT_PUBLIC_MEDUSA_BACKEND_URL="https://${CUSTOM_DOMAIN}"` instead of hardcoded `http://localhost:9000`.

3. EMPIRICAL VERIFICATION & TESTING PHASE:
   - Run storefront typecheck: `cd apps/storefront && npx tsc --noEmit`
   - Run storefront build: `cd apps/storefront && npm run build`
   - Run shell syntax check: `bash -n infrastructure/scripts/provision-tenant.sh`

4. PROCESS CLEANUP & LEARNING DIRECTIVE (CRITICAL):
   - Terminate any running subagents, background dev servers, or processes before completing turn.
</ANTIGRAVITY_WORKFLOW>

<ACCEPTANCE_CRITERIA>
- [ ] Subagents delegated for search bar and provisioning script inspection.
- [ ] `smart-search-bar.tsx` supports dynamic product catalog search.
- [ ] `provision-tenant.sh` handles custom domain URLs (`https://${CUSTOM_DOMAIN}`) and avoids CLI secret leaks.
- [ ] Storefront build and shell script syntax pass with exit code 0.
- [ ] All subagents and background tasks cleanly terminated.
</ACCEPTANCE_CRITERIA>
```

---

## Part 5: Complete Monorepo 100% Verification (Prompt 5)

---
### Developer Prompt 5: Full Monorepo End-to-End Build & Deployment Verification

```markdown
/goal

<TASK>
Execute full monorepo typechecks, builds, test suites, and Docker config validations across all packages (`@dtc/shared-types`, `apps/backend`, `apps/storefront`, `infrastructure/`) to empirically prove 100% Deployment Readiness.
</TASK>

<SUBAGENT_DELEGATION_DIRECTIVE>
- Use `invoke_subagent` (Role: "Build & Release Specialist", TypeName: "research") to run TypeScript checks and production builds in parallel across all packages.
</SUBAGENT_DELEGATION_DIRECTIVE>

<ANTIGRAVITY_SLASH_COMMANDS>
- /goal: Execute autonomously until all packages build cleanly with exit code 0.
</ANTIGRAVITY_SLASH_COMMANDS>

<ANTIGRAVITY_WORKFLOW>
1. VERIFICATION SEQUENCE:
   - Shared Types Build: `cd packages/shared-types && npm run build`
   - Backend Typecheck: `cd apps/backend && npx tsc --noEmit`
   - Backend Medusa Build: `cd apps/backend && npm run build`
   - Storefront Typecheck: `cd apps/storefront && npx tsc --noEmit`
   - Storefront Production Build: `cd apps/storefront && npm run build`
   - Provisioning Script Syntax: `bash -n infrastructure/scripts/provision-tenant.sh`
   - Caddy Router Script Syntax: `bash -n infrastructure/scripts/caddy-domain-router.sh`

2. ACCEPTANCE VERIFICATION:
   - Verify 0 TypeScript compilation errors in all workspaces.
   - Verify backend bundles Medusa core + admin dashboard cleanly.
   - Verify Next.js storefront compiles all static and dynamic routes.
   - Verify all 15 defects have zero regressions.

3. PROCESS CLEANUP (CRITICAL):
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
