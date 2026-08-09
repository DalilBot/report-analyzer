# Dedicated 6.4 Report Remediation Prompt Pack (`PROMPT_SEQUENCE_64_AUDIT_FIXES.md`)

This prompt pack contains **7 targeted developer prompts** engineered for **Google Antigravity Agentic IDE** to resolve the exact new defects, DI container bypasses, weight math unit errors, ETA document type mismatches, Gemini auth header bugs, storefront cart SDK calls, and infrastructure Sentinel port collisions identified in the 6.4/10 evaluation report. Zero older problems are included.

> [!IMPORTANT]
> **Subagent Directive**: Send these 7 prompts sequentially (Prompt 1 through Prompt 7) to your developer Antigravity instance. Every prompt explicitly instructs the agent to delegate research or sub-tasks to subagents (`invoke_subagent`) to maintain clean context and maximize execution speed.

---

## Part 1: Backend Architecture & Integration Fixes (Prompts 1–4)

---
### Developer Prompt 1: Backend DI Container Dependency Resolution & Paymob Integration ID Fix

```markdown
/goal

<TASK>
Resolve `geminiAi` via Medusa DI container in `api/admin/ai/generate-copy/route.ts` and dynamically select Paymob integration IDs in `paymob/service.ts`.
</TASK>

<SUBAGENT_DELEGATION_DIRECTIVE>
- Use `invoke_subagent` (Role: "Codebase Researcher", TypeName: "research") to inspect Medusa 2.0 container resolution (`req.scope.resolve`) and Paymob session config options.
</SUBAGENT_DELEGATION_DIRECTIVE>

<ANTIGRAVITY_SLASH_COMMANDS>
- /goal: Execute autonomously until DI container resolution and Paymob integration ID selection pass build checks.
- /learn: Persist Medusa v2 DI container resolution rules to .gemini/rules.
</ANTIGRAVITY_SLASH_COMMANDS>

<ANTIGRAVITY_WORKFLOW>
1. RESEARCH & INSPECTION PHASE:
   - View `apps/backend/src/api/admin/ai/generate-copy/route.ts` (line 62) and `apps/backend/src/modules/paymob/service.ts` (line 110).

2. IMPLEMENTATION PHASE:
   - Target files: `apps/backend/src/api/admin/ai/generate-copy/route.ts`, `apps/backend/src/modules/paymob/service.ts`
   - **`route.ts:L62`**: Replace `new GeminiAIStudioClient()` direct instantiation with Medusa DI container resolution `req.scope.resolve("geminiAi")`.
   - **`paymob/service.ts:L110`**: Update `initiatePayment()` to inspect payment session context/data and dynamically choose between `cardIntegrationId`, `walletIntegrationId`, or `valuIntegrationId` instead of hardcoding `cardIntegrationId`.

3. EMPIRICAL VERIFICATION & TESTING PHASE:
   - Run TypeScript check: `cd apps/backend && npx tsc --noEmit`
   - Run backend build verification: `cd apps/backend && npm run build`

4. PROCESS CLEANUP & LEARNING DIRECTIVE (CRITICAL):
   - Execute `/learn` to store Medusa DI container resolution rules.
   - Terminate any running subagents, background dev servers, or processes before completing turn.
</ANTIGRAVITY_WORKFLOW>

<ACCEPTANCE_CRITERIA>
- [ ] Subagents delegated for Medusa DI container pattern research.
- [ ] `generate-copy/route.ts` resolves `geminiAi` via `req.scope.resolve`.
- [ ] `paymob/service.ts` dynamically selects Paymob integration IDs for cards, wallets, and ValU.
- [ ] Backend build completes with exit code 0.
- [ ] All subagents and background tasks are cleanly terminated.
</ACCEPTANCE_CRITERIA>
```

---
### Developer Prompt 2: Bosta Weight Unit Conversion (Grams to Kg Math) & Workflow Container Injection

```markdown
/goal

<TASK>
Fix Bosta weight unit conversion (grams to kg) in `bosta/service.ts` and use container service resolution in `bosta-fulfillment-workflow.ts`.
</TASK>

<SUBAGENT_DELEGATION_DIRECTIVE>
- Delegate Bosta weight calculation formulas and workflow step container context resolution to a subagent via `invoke_subagent`.
</SUBAGENT_DELEGATION_DIRECTIVE>

<ANTIGRAVITY_SLASH_COMMANDS>
- /goal: Execute autonomously until Bosta weight calculations and workflow container resolution compile clean.
- /learn: Persist fulfillment weight calculation rules to .gemini/rules.
</ANTIGRAVITY_SLASH_COMMANDS>

<ANTIGRAVITY_WORKFLOW>
1. RESEARCH & INSPECTION PHASE:
   - View `apps/backend/src/modules/bosta/service.ts` (lines 170–186) and `apps/backend/src/workflows/bosta-fulfillment-workflow.ts` (line 60).

2. IMPLEMENTATION PHASE:
   - Target files: `apps/backend/src/modules/bosta/service.ts`, `apps/backend/src/workflows/bosta-fulfillment-workflow.ts`
   - **`bosta/service.ts:L170-186`**: Check if input item weight is provided in grams (`weight > 50`); divide by `1000.0` to convert to kilograms before computing excess weight surcharges to prevent incorrect +4,980 EGP overcharges.
   - **`bosta-fulfillment-workflow.ts:L60`**: Replace raw `new BostaClient()` instantiation with container service resolution (`container.resolve("bostaFulfillment")`).

3. EMPIRICAL VERIFICATION & TESTING PHASE:
   - Run TypeScript check: `cd apps/backend && npx tsc --noEmit`
   - Run backend build verification: `cd apps/backend && npm run build`

4. PROCESS CLEANUP & LEARNING DIRECTIVE (CRITICAL):
   - Execute `/learn` to store fulfillment unit conversion rules.
   - Terminate any running subagents, background dev servers, or processes before completing turn.
</ANTIGRAVITY_WORKFLOW>

<ACCEPTANCE_CRITERIA>
- [ ] Subagents delegated for weight unit conversion math inspection.
- [ ] Grams to kg conversion (`weight > 50 ? weight / 1000 : weight`) prevents excess rate overcharges.
- [ ] `bosta-fulfillment-workflow.ts` resolves Bosta fulfillment service via container context.
- [ ] Backend build completes with exit code 0.
- [ ] All subagents and background tasks are cleanly terminated.
</ACCEPTANCE_CRITERIA>
```

---
### Developer Prompt 3: ETA Tax Payload Document Type `"S"` & Property `dateTimeIssued` Fix

```markdown
/goal

<TASK>
Set document type `"S"` and property `dateTimeIssued` in `eta-tax/payload-builder.ts`, and wire the ETA retry worker case in `background-queue.ts`.
</TASK>

<SUBAGENT_DELEGATION_DIRECTIVE>
- Use `invoke_subagent` to inspect Egyptian Tax Authority (ETA) e-Receipt v1.0 schema specification for receipts submission.
</SUBAGENT_DELEGATION_DIRECTIVE>

<ANTIGRAVITY_SLASH_COMMANDS>
- /goal: Execute autonomously until ETA tax payload builder and background queue retry worker pass schema checks.
- /browser: Verify ETA Portal e-Receipt `/receipts/submission` document type and timestamp property requirements.
- /learn: Persist ETA tax e-Receipt schema rules to .gemini/rules.
</ANTIGRAVITY_SLASH_COMMANDS>

<ANTIGRAVITY_WORKFLOW>
1. RESEARCH & INSPECTION PHASE:
   - View `apps/backend/src/modules/eta-tax/payload-builder.ts` (lines 70, 194) and `apps/backend/src/jobs/background-queue.ts` (lines 128–130).

2. IMPLEMENTATION PHASE:
   - Target files: `apps/backend/src/modules/eta-tax/payload-builder.ts`, `apps/backend/src/jobs/background-queue.ts`
   - **`payload-builder.ts:L194`**: Set `documentType: "S"` (Sales Receipt) for submissions to `/receipts/submission` instead of `"I"` (Invoice).
   - **`payload-builder.ts:L70`**: Rename property `dateTimeIssuer` to official ETA schema property `dateTimeIssued`.
   - **`background-queue.ts:L128-130`**: Replace NO-OP log string in `ETA_SUBMISSION_RETRY` worker case with live execution of `etaTaxModuleService.submitAndAuditReceipt()`.

3. EMPIRICAL VERIFICATION & TESTING PHASE:
   - Run TypeScript check: `cd apps/backend && npx tsc --noEmit`
   - Run backend build verification: `cd apps/backend && npm run build`

4. PROCESS CLEANUP & LEARNING DIRECTIVE (CRITICAL):
   - Execute `/learn` to store ETA e-Receipt schema rules.
   - Terminate any running subagents, background dev servers, or processes before completing turn.
</ANTIGRAVITY_WORKFLOW>

<ACCEPTANCE_CRITERIA>
- [ ] Subagents delegated for ETA e-Receipt schema research.
- [ ] `payload-builder.ts` sets `documentType: "S"` and `dateTimeIssued`.
- [ ] `background-queue.ts` executes `submitAndAuditReceipt()` inside retry worker case.
- [ ] Backend build completes with exit code 0.
- [ ] All subagents and background tasks are cleanly terminated.
</ACCEPTANCE_CRITERIA>
```

---
### Developer Prompt 4: Gemini AI Authentication Header `x-goog-api-key`, Model Name, & Redis Task Store

```markdown
/goal

<TASK>
Fix Google AI Studio authentication header in `gemini-ai/client.ts`, update default model in `gemini-ai/service.ts`, and store worker task states in Redis.
</TASK>

<SUBAGENT_DELEGATION_DIRECTIVE>
- Use `invoke_subagent` to inspect Google AI Studio SDK header specs and Redis worker task state storage.
</SUBAGENT_DELEGATION_DIRECTIVE>

<ANTIGRAVITY_SLASH_COMMANDS>
- /goal: Execute autonomously until Gemini AI client authentication and AI copywriter worker Redis task store compile clean.
- /learn: Persist Google AI Studio authentication rules to .gemini/rules.
</ANTIGRAVITY_SLASH_COMMANDS>

<ANTIGRAVITY_WORKFLOW>
1. RESEARCH & INSPECTION PHASE:
   - View `apps/backend/src/modules/gemini-ai/client.ts` (line 79), `apps/backend/src/modules/gemini-ai/service.ts` (line 16), and `apps/backend/src/jobs/ai-copywriter-worker.ts` (line 37).

2. IMPLEMENTATION PHASE:
   - Target files: `apps/backend/src/modules/gemini-ai/client.ts`, `apps/backend/src/modules/gemini-ai/service.ts`, `apps/backend/src/jobs/ai-copywriter-worker.ts`
   - **`client.ts:L79`**: Change HTTP header from `Authorization: Bearer ${key}` to Google AI Studio's required header `x-goog-api-key: ${key}` to resolve 401 Unauthorized errors.
   - **`service.ts:L16`**: Update default model target identifier from non-existent `"gemma-4-31b-it"` to `"gemini-1.5-flash"`.
   - **`ai-copywriter-worker.ts:L37`**: Replace local in-memory `taskResultsStore` Map with Redis key-value storage (`gemini_task_${productId}`) so polling returns correct status in multi-pod deployments.

3. EMPIRICAL VERIFICATION & TESTING PHASE:
   - Run TypeScript check: `cd apps/backend && npx tsc --noEmit`
   - Run backend build verification: `cd apps/backend && npm run build`

4. PROCESS CLEANUP & LEARNING DIRECTIVE (CRITICAL):
   - Execute `/learn` to store Google AI Studio header rules.
   - Terminate any running subagents, background dev servers, or processes before completing turn.
</ANTIGRAVITY_WORKFLOW>

<ACCEPTANCE_CRITERIA>
- [ ] Subagents delegated for Google AI Studio header research.
- [ ] `client.ts` passes `x-goog-api-key` header.
- [ ] `service.ts` targets valid model `"gemini-1.5-flash"`.
- [ ] `ai-copywriter-worker.ts` stores task results in Redis.
- [ ] Backend build completes with exit code 0.
- [ ] All subagents and background tasks are cleanly terminated.
</ACCEPTANCE_CRITERIA>
```

---

## Part 2: Storefront & Infrastructure Enhancements (Prompts 5–7)

---
### Developer Prompt 5: Storefront Real Medusa Cart SDK Initialization (`sdk.store.cart.create()`)

```markdown
/goal

<TASK>
Replace local fake cart string initialization in `apps/storefront/src/lib/context/cart-context.tsx` with live Medusa SDK API call `sdk.store.cart.create()`.
</TASK>

<SUBAGENT_DELEGATION_DIRECTIVE>
- Delegate Medusa JS SDK store cart initialization inspection to a subagent via `invoke_subagent`.
</SUBAGENT_DELEGATION_DIRECTIVE>

<ANTIGRAVITY_SLASH_COMMANDS>
- /goal: Execute autonomously until Storefront Cart Context creates valid server-side cart instances via Medusa SDK.
- /learn: Persist Medusa SDK storefront cart initialization rules to .gemini/rules.
</ANTIGRAVITY_SLASH_COMMANDS>

<ANTIGRAVITY_WORKFLOW>
1. RESEARCH & INSPECTION PHASE:
   - View `apps/storefront/src/lib/context/cart-context.tsx` (lines 88–93).

2. IMPLEMENTATION PHASE:
   - Target file: `apps/storefront/src/lib/context/cart-context.tsx`
   - Remove fake cart string initialization (`"cart_172..."`).
   - Call `sdk.store.cart.create({ region_id: currentRegionId })` to generate a valid server-side Medusa cart ID, saving the returned cart ID to cookie storage (`medusa_cart_id`) so line item mutations succeed without 404 errors.

3. EMPIRICAL VERIFICATION & TESTING PHASE:
   - Run storefront build verification: `cd apps/storefront && npm run build`

4. PROCESS CLEANUP & LEARNING DIRECTIVE (CRITICAL):
   - Terminate any running subagents, background dev servers (e.g. `next dev`) before completing turn.
</ANTIGRAVITY_WORKFLOW>

<ACCEPTANCE_CRITERIA>
- [ ] Subagents delegated for Medusa SDK cart method research.
- [ ] `cart-context.tsx` initializes guest carts via `sdk.store.cart.create()`.
- [ ] Zero fake cart strings (`cart_172...`) in codebase.
- [ ] Storefront build completes with exit code 0.
- [ ] All subagents, background tasks, and dev servers are cleanly terminated.
</ACCEPTANCE_CRITERIA>
```

---
### Developer Prompt 6: Storefront Cairo Font Link in `globals.css` & PDP Add-to-Cart Client Component Wrapper

```markdown
/goal

<TASK>
Link `--font-cairo` variable in `apps/storefront/src/app/globals.css` and wrap PDP Add-to-Cart button in a interactive Client Component in `products/[handle]/page.tsx`.
</TASK>

<SUBAGENT_DELEGATION_DIRECTIVE>
- Use `invoke_subagent` to inspect Next.js font variable CSS attachments and PDP Client Component event handling.
</SUBAGENT_DELEGATION_DIRECTIVE>

<ANTIGRAVITY_SLASH_COMMANDS>
- /goal: Execute autonomously until Cairo Arabic font renders correctly and PDP Add-to-Cart button handles clicks.
</ANTIGRAVITY_SLASH_COMMANDS>

<ANTIGRAVITY_WORKFLOW>
1. RESEARCH & INSPECTION PHASE:
   - View `apps/storefront/src/app/globals.css` (line 11) and `apps/storefront/src/app/[countryCode]/products/[handle]/page.tsx` (line 94).

2. IMPLEMENTATION PHASE:
   - Target files: `apps/storefront/src/app/globals.css`, `apps/storefront/src/app/[countryCode]/products/[handle]/page.tsx`, `apps/storefront/src/modules/products/components/add-to-cart-button.tsx`
   - **`globals.css:L11`**: Attach `--font-cairo` to CSS `--font-sans` variable and `body` rules so Egyptian Arabic typography renders as intended.
   - **`products/[handle]/page.tsx:L94`**: Replace inert button inside async Server Component with interactive Client Component (`AddToCartButton`) that connects to `useCart()` with an `onClick` handler.

3. EMPIRICAL VERIFICATION & TESTING PHASE:
   - Run storefront build verification: `cd apps/storefront && npm run build`

4. PROCESS CLEANUP & LEARNING DIRECTIVE (CRITICAL):
   - Terminate any running subagents, background dev servers, or processes before completing turn.
</ANTIGRAVITY_WORKFLOW>

<ACCEPTANCE_CRITERIA>
- [ ] Subagents delegated for font CSS and Client Component research.
- [ ] `globals.css` links `--font-cairo` font family to body typography.
- [ ] Product detail page Add-to-Cart button wraps in an interactive Client Component using `useCart()`.
- [ ] Storefront build completes with exit code 0.
- [ ] All subagents, background tasks, and dev servers are cleanly terminated.
</ACCEPTANCE_CRITERIA>
```

---
### Developer Prompt 7: Infrastructure Dynamic Sentinel Ports, Script Secret Preservation, & Shared Types Docker COPY

```markdown
/goal

<TASK>
Use dynamic `PORT_OFFSET` for Sentinel ports in `docker-compose.tenant.yml`, preserve existing credentials in `provision-tenant.sh`, and copy shared-types in `Dockerfile.backend`.
</TASK>

<SUBAGENT_DELEGATION_DIRECTIVE>
- Use `invoke_subagent` to inspect multi-tenant Docker Compose port offsets and shell environment secret sourcing.
</SUBAGENT_DELEGATION_DIRECTIVE>

<ANTIGRAVITY_SLASH_COMMANDS>
- /goal: Execute autonomously until multi-tenant Redis Sentinel ports, provisioning secret preservation, and Dockerfile builds pass tests.
- /learn: Persist multi-tenant shell automation rules to .gemini/rules.
</ANTIGRAVITY_SLASH_COMMANDS>

<ANTIGRAVITY_WORKFLOW>
1. RESEARCH & INSPECTION PHASE:
   - View `infrastructure/docker/docker-compose.tenant.yml` (line 79), `infrastructure/scripts/provision-tenant.sh` (lines 48–75), and `infrastructure/docker/Dockerfile.backend`.

2. IMPLEMENTATION PHASE:
   - Target files: `infrastructure/docker/docker-compose.tenant.yml`, `infrastructure/scripts/provision-tenant.sh`, `infrastructure/docker/Dockerfile.backend`
   - **`docker-compose.tenant.yml:L79`**: Calculate Redis Sentinel ports dynamically using `PORT_OFFSET` variables (`REDIS_SENTINEL_1_PORT`) to prevent port collisions across multi-tenant stacks on the same host.
   - **`provision-tenant.sh:L48-75`**: Source existing `.env` credentials if present before generating new passwords to prevent breaking authentication on re-runs.
   - **`Dockerfile.backend`**: Copy `/app/packages/shared-types` build output into runner stage.

3. EMPIRICAL VERIFICATION & TESTING PHASE:
   - Run Docker compose config validation: `docker compose -f infrastructure/docker/docker-compose.tenant.yml config`
   - Run bash syntax check: `bash -n infrastructure/scripts/provision-tenant.sh`

4. PROCESS CLEANUP & LEARNING DIRECTIVE (CRITICAL):
   - Terminate any active subagents or background tasks before completing turn.
</ANTIGRAVITY_WORKFLOW>

<ACCEPTANCE_CRITERIA>
- [ ] Subagents delegated for Docker multi-tenant port inspection.
- [ ] Redis Sentinel ports use dynamic `PORT_OFFSET` variables.
- [ ] `provision-tenant.sh` preserves existing `.env` secrets on script re-runs.
- [ ] `Dockerfile.backend` copies `/app/packages/shared-types` build artifacts.
- [ ] Docker Compose config and bash script pass validation.
- [ ] All subagents and background tasks are cleanly terminated.
</ACCEPTANCE_CRITERIA>
```
