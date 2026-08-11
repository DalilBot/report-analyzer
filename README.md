# Dedicated 8.6 Report & Multi-LLM Provider Prompt Pack (`PROMPT_SEQUENCE_86_FINAL_REPORT_FIXES.md`)

This prompt pack contains **5 targeted developer prompts** engineered for **Google Antigravity Agentic IDE** to resolve the exact new defects identified in the latest 8.6/10 evaluation report: migrating fake "BullMQ" to real `bullmq` with `BRPOPLPUSH`/ atomic pops, eliminating `any` container resolution casts with `MedusaContainer`, fixing DI bypass in ETA workflow fallback, injecting CORS in `provision-tenant.sh`, replacing `alert()` with a toast library, adding OpenRouter API & Hack Club AI API support to Gemini AI client, fixing hardcoded storefront product data, and memory leak cleanups. Zero older problems are included.

> [!IMPORTANT]
> **Subagent Directive**: Send these 5 prompts sequentially (Prompt 1 through Prompt 5) to your developer Antigravity instance. Every prompt explicitly instructs the agent to delegate research or sub-tasks to subagents (`invoke_subagent`).

---

## Part 1: Background Queue Reliability & LLM Multi-Provider Support (Prompts 1–2)

---
### Developer Prompt 1: Replace Fake Redis Queue with Real `bullmq` (Atomic Pops & Lock Recovery) & Eliminate `any` Container Resolutions

```markdown
/goal

<TASK>
Migrate `apps/backend/src/jobs/background-queue.ts` from custom `rpush`/`blpop` to the official `bullmq` npm package (with atomic pops, stalled job recovery, and job visibility timeouts), eliminate `any` container resolution casts using proper `MedusaContainer<T>` types across all jobs/subscribers, and fix brittle fallback resolution chains.
</TASK>

<SUBAGENT_DELEGATION_DIRECTIVE>
- Use `invoke_subagent` (Role: "Queue Architecture Researcher", TypeName: "research") to inspect `apps/backend/src/jobs/background-queue.ts` and catalog all custom Redis pop logic and missing BullMQ worker configurations.
- Use a second `invoke_subagent` to search the backend for all `container.resolve<any>()` and `(container as any).resolve()` calls to build a complete replacement list.
</SUBAGENT_DELEGATION_DIRECTIVE>

<ANTIGRAVITY_SLASH_COMMANDS>
- /goal: Execute autonomously until background queue uses official BullMQ with stalled job recovery and all container resolutions are typed with MedusaContainer.
- /learn: Persist BullMQ worker lifecycle and typed container resolution rules to .gemini/rules.
</ANTIGRAVITY_SLASH_COMMANDS>

<ANTIGRAVITY_WORKFLOW>
1. RESEARCH & INSPECTION PHASE:
   - View `apps/backend/src/jobs/background-queue.ts` (full file).
   - View `apps/backend/src/jobs/ai-copywriter-worker.ts`.
   - Search for `resolve<any>` across `apps/backend/src/`.

2. IMPLEMENTATION PHASE:
   - Target files: `apps/backend/src/jobs/background-queue.ts`, `apps/backend/src/jobs/ai-copywriter-worker.ts`, subscriber & job files
   - **Migrate to Real `bullmq`**: Replace custom `rpush`/`blpop` with official `Queue` and `Worker` instances from the `bullmq` package. Ensure job visibility timeouts, stalled job recovery (using `stalledInterval`), and atomic pops (`BRPOPLPUSH`/`BLMOVE` under the hood) are active to guarantee zero job loss on worker crash.
   - **Typed Container Resolutions**: Replace `req.scope.resolve<any>(...)`, `container.resolve<any>(...)`, and `(container as any).resolve(...)` with properly typed resolutions using `MedusaContainer`:
     ```typescript
     import { MedusaContainer } from "@medusajs/framework/types"
     const etaService = container.resolve<EtaTaxModuleService>("etaTax")
     ```
   - **Fix Brittle Fallbacks**: Replace `resolve("etaTaxModuleService") || resolve("eta-tax")` chains with direct, typed module resolution keys (`ETA_TAX_MODULE` constant).
   - **Lazy Connection**: Move Redis client instantiation inside `startWorker()` so importing the module does not create dangling connections.

3. EMPIRICAL VERIFICATION & TESTING PHASE:
   - Run TypeScript check: `cd apps/backend && npx tsc --noEmit`
   - Run backend build verification: `cd apps/backend && npm run build`

4. PROCESS CLEANUP & LEARNING DIRECTIVE (CRITICAL):
   - Execute `/learn` to store BullMQ worker lifecycle rules.
   - Terminate any running subagents, background dev servers, or processes before completing turn.
</ANTIGRAVITY_WORKFLOW>

<ACCEPTANCE_CRITERIA>
- [ ] 2 subagents delegated for queue catalog and container resolution scan.
- [ ] `background-queue.ts` uses official `bullmq` `Queue` and `Worker` classes.
- [ ] Zero `resolve<any>` or `(container as any)` calls in jobs/subscribers — all typed with `MedusaContainer`.
- [ ] Redis connection lazy-loaded inside `startWorker()`.
- [ ] Backend build completes with exit code 0.
- [ ] All subagents and background tasks are cleanly terminated.
</ACCEPTANCE_CRITERIA>
```

---
### Developer Prompt 2: Add Multi-Provider LLM Support (OpenRouter API & Hack Club AI API) to Gemini AI Client

```markdown
/goal

<TASK>
Extend `apps/backend/src/modules/gemini-ai/client.ts` and configuration to support **OpenRouter API** (`https://openrouter.ai/api/v1`) and **Hack Club AI API** (`https://ai.hackclub.com/v1`) alongside native Gemini API studio, with provider fallback and structured JSON output preservation.
</TASK>

<SUBAGENT_DELEGATION_DIRECTIVE>
- Use `invoke_subagent` to inspect the Gemini AI client implementation and research the Hack Club AI endpoint specification (`https://docs.ai.hackclub.com/`) and OpenRouter OpenAI-compatible chat completions interface.
</SUBAGENT_DELEGATION_DIRECTIVE>

<ANTIGRAVITY_SLASH_COMMANDS>
- /goal: Execute autonomously until Gemini AI module supports OpenRouter and Hack Club AI APIs with automatic provider failover.
- /learn: Persist multi-provider LLM integration rules to .gemini/rules.
</ANTIGRAVITY_SLASH_COMMANDS>

<ANTIGRAVITY_WORKFLOW>
1. RESEARCH & INSPECTION PHASE:
   - View `apps/backend/src/modules/gemini-ai/client.ts`.
   - View `apps/backend/src/modules/gemini-ai/service.ts`.
   - View `apps/backend/medusa-config.ts` (Gemini options block).

2. IMPLEMENTATION PHASE:
   - Target files: `apps/backend/src/modules/gemini-ai/client.ts`, `apps/backend/src/modules/gemini-ai/service.ts`, `apps/backend/medusa-config.ts`
   - **Configure Provider Strategy**: Update module options to accept `LLM_PROVIDER` ("gemini" | "openrouter" | "hackclub"), `OPENROUTER_API_KEY`, and `HACKCLUB_API_KEY`.
   - **OpenRouter Endpoint**: Implement OpenRouter OpenAI-compatible `/v1/chat/completions` dispatch when `LLM_PROVIDER === "openrouter"` or as secondary fallback:
     - Endpoint: `https://openrouter.ai/api/v1/chat/completions`
     - Headers: `Authorization: Bearer ${OPENROUTER_API_KEY}`, `HTTP-Referer: https://medusa-eg.com`, `X-Title: Medusa EG AI`
     - Response Format: `{ type: "json_object" }`
   - **Hack Club AI Endpoint**: Implement Hack Club AI proxy dispatch (`https://ai.hackclub.com/v1/chat/completions`) per Hack Club docs (`https://docs.ai.hackclub.com/`):
     - Endpoint: `https://ai.hackclub.com/v1/chat/completions`
     - Headers: `Authorization: Bearer ${HACKCLUB_API_KEY}`
     - Model: `meta-llama/llama-3.3-70b-instruct` or specified model
   - **Structured Output & Prompt Sanitization**: Ensure prompt injection sanitization (`sanitizePromptInput`) and structured JSON schema validation apply consistently regardless of whether native Gemini, OpenRouter, or Hack Club AI is serving the request.
   - **Provider Fallback Cascade**: If the primary provider fails with a transient error (timeout, 5xx, 429), cascade automatically: Native Gemini → OpenRouter → Hack Club AI before failing over to hardcoded template.

3. EMPIRICAL VERIFICATION & TESTING PHASE:
   - Run TypeScript check: `cd apps/backend && npx tsc --noEmit`
   - Run backend build verification: `cd apps/backend && npm run build`

4. PROCESS CLEANUP & LEARNING DIRECTIVE (CRITICAL):
   - Execute `/learn` to store multi-LLM provider rules.
   - Terminate any running subagents, background dev servers, or processes before completing turn.
</ANTIGRAVITY_WORKFLOW>

<ACCEPTANCE_CRITERIA>
- [ ] Subagents delegated for OpenRouter and Hack Club AI API research.
- [ ] Client supports native Gemini, OpenRouter (`openrouter.ai/api/v1`), and Hack Club AI (`ai.hackclub.com/v1`).
- [ ] Provider fallback cascade (Gemini → OpenRouter → Hack Club AI) active for transient errors.
- [ ] Structured JSON enforcement & prompt sanitization preserved across all providers.
- [ ] Backend build completes with exit code 0.
- [ ] All subagents and background tasks are cleanly terminated.
</ACCEPTANCE_CRITERIA>
```

---

## Part 2: Module Refactoring & Provisioning Fixes (Prompts 3–4)

---
### Developer Prompt 3: Fix ETA Workflow DI Fallback Container Injection, Type Webhook Paymob/Bosta Payloads, & Inject CORS in Provisioning Script

```markdown
/goal

<TASK>
Fix DI container injection in `eta-tax-workflow.ts` fallback, create explicit TypeScript interfaces for Paymob/Bosta webhook payloads, and update `provision-tenant.sh` to generate `STORE_CORS` and `ADMIN_CORS`.
</TASK>

<SUBAGENT_DELEGATION_DIRECTIVE>
- Use `invoke_subagent` to inspect ETA workflow container resolution fallback, Paymob/Bosta webhook route types, and `provision-tenant.sh` environment variable generation.
</SUBAGENT_DELEGATION_DIRECTIVE>

<ANTIGRAVITY_SLASH_COMMANDS>
- /goal: Execute autonomously until ETA workflow fallback receives container, webhooks have typed payloads, and provisioning generates CORS env vars.
- /learn: Persist workflow container fallback and provisioning CORS rules to .gemini/rules.
</ANTIGRAVITY_SLASH_COMMANDS>

<ANTIGRAVITY_WORKFLOW>
1. RESEARCH & INSPECTION PHASE:
   - View `apps/backend/src/workflows/eta-tax-workflow.ts` (line 49 fallback).
   - View `apps/backend/src/api/hooks/paymob/route.ts` & `apps/backend/src/api/hooks/bosta/route.ts`.
   - View `infrastructure/scripts/provision-tenant.sh` (lines 50–68 `.env` generation).

2. IMPLEMENTATION PHASE:
   - Target files: `apps/backend/src/workflows/eta-tax-workflow.ts`, `apps/backend/src/modules/paymob/types.ts`, `apps/backend/src/modules/bosta/types.ts`, `apps/backend/src/api/hooks/paymob/route.ts`, `apps/backend/src/api/hooks/bosta/route.ts`, `infrastructure/scripts/provision-tenant.sh`
   - **ETA Workflow DI Fallback** (`eta-tax-workflow.ts:L49`): Replace `new EtaClient()` fallback (which lacks container context, breaking Redis OAuth2 token caching) with proper container resolution: `const client = container.resolve<EtaTaxModuleService>("etaTax")?.getClient() || new EtaClient(options, container)`. Always pass `container` if instantiating directly.
   - **Typed Webhook Payloads**: Define `PaymobWebhookPayload` and `BostaWebhookPayload` interfaces in their respective module `types.ts` files. Update webhook route handlers to type incoming bodies (`req.body as PaymobWebhookPayload`) instead of `any`.
   - **Provisioning CORS Injection** (`provision-tenant.sh`): Update the `.env` template generation section in `provision-tenant.sh` to dynamically derive and write `STORE_CORS`, `ADMIN_CORS`, and `AUTH_CORS` using the tenant's `CUSTOM_DOMAIN` (e.g., `STORE_CORS=https://${CUSTOM_DOMAIN},http://localhost:8000`).

3. EMPIRICAL VERIFICATION & TESTING PHASE:
   - Run TypeScript check: `cd apps/backend && npx tsc --noEmit`
   - Run backend build verification: `cd apps/backend && npm run build`
   - Run bash syntax check: `bash -n infrastructure/scripts/provision-tenant.sh`

4. PROCESS CLEANUP & LEARNING DIRECTIVE (CRITICAL):
   - Execute `/learn` to store provisioning CORS rules.
   - Terminate any running subagents, background dev servers, or processes before completing turn.
</ANTIGRAVITY_WORKFLOW>

<ACCEPTANCE_CRITERIA>
- [ ] Subagents delegated for ETA workflow fallback, webhook types, and provisioning script inspection.
- [ ] `EtaClient` fallback receives container context — Redis token cache preserved.
- [ ] Paymob and Bosta webhook route handlers use typed payload interfaces (zero `any` on body).
- [ ] `provision-tenant.sh` generates `STORE_CORS`, `ADMIN_CORS`, and `AUTH_CORS` matching tenant domain.
- [ ] All builds and script validations pass cleanly.
- [ ] All subagents and background tasks are cleanly terminated.
</ACCEPTANCE_CRITERIA>
```

---

## Part 3: Storefront UX & Code Polish (Prompt 5)

---
### Developer Prompt 4 (Storefront): Replace Browser `alert()` with Toast Library, Connect Live Medusa Data on Product Pages, & Fix `setTimeout` Memory Leaks

```markdown
/goal

<TASK>
Replace native browser `alert()` with `react-hot-toast` / `sonner` in cart context and checkout, connect live Medusa SDK product data in `app/[countryCode]/products/[handle]/page.tsx`, and add cleanup to `setTimeout` in `add-to-cart-button.tsx`.
</TASK>

<SUBAGENT_DELEGATION_DIRECTIVE>
- Use `invoke_subagent` to inspect all `alert()` call sites in storefront, product handle page data fetching, and `add-to-cart-button.tsx` animation timers.
</SUBAGENT_DELEGATION_DIRECTIVE>

<ANTIGRAVITY_SLASH_COMMANDS>
- /goal: Execute autonomously until storefront uses non-blocking toasts, product pages fetch live Medusa data, and timers clean up on unmount.
- /learn: Persist storefront error handling and memory leak prevention rules to .gemini/rules.
</ANTIGRAVITY_SLASH_COMMANDS>

<ANTIGRAVITY_WORKFLOW>
1. RESEARCH & INSPECTION PHASE:
   - View `apps/storefront/src/lib/context/cart-context.tsx` (line 185 `alert()`).
   - View `apps/storefront/src/modules/checkout/components/checkout-view.tsx` (line 90 `alert()`).
   - View `apps/storefront/src/app/[countryCode]/products/[handle]/page.tsx` (lines 26–34 dummy data).
   - View `apps/storefront/src/modules/products/components/add-to-cart-button.tsx` (line 49 `setTimeout`).

2. IMPLEMENTATION PHASE:
   - Target files: `apps/storefront/src/lib/context/cart-context.tsx`, `apps/storefront/src/modules/checkout/components/checkout-view.tsx`, `apps/storefront/src/app/[countryCode]/products/[handle]/page.tsx`, `apps/storefront/src/modules/products/components/add-to-cart-button.tsx`
   - **Replace `alert()` with Toasts**: Import `toast` from `react-hot-toast` or `sonner`. Replace native `alert(error.message)` with `toast.error(error.message)` in `cart-context.tsx` and `checkout-view.tsx` for non-blocking, accessible notifications.
   - **Live Medusa Product Fetching** (`products/[handle]/page.tsx`): Replace static dummy product data (L26–34) with live API fetching:
     ```typescript
     const product = await getProductByHandle(handle, region.id)
     if (!product) notFound()
     ```
   - **`setTimeout` Memory Leak Fix** (`add-to-cart-button.tsx`): Wrap the "Added to cart" state timer in `useEffect` with return cleanup:
     ```typescript
     useEffect(() => {
       if (!isAdded) return
       const timer = setTimeout(() => setIsAdded(false), 2000)
       return () => clearTimeout(timer)
     }, [isAdded])
     ```

3. EMPIRICAL VERIFICATION & TESTING PHASE:
   - Run storefront build verification: `cd apps/storefront && npm run build`

4. PROCESS CLEANUP & LEARNING DIRECTIVE (CRITICAL):
   - Terminate any running subagents, background dev servers (e.g. `next dev`) before completing turn.
</ANTIGRAVITY_WORKFLOW>

<ACCEPTANCE_CRITERIA>
- [ ] Subagents delegated for alert call sites, product data fetching, and timer inspection.
- [ ] Native `alert()` calls replaced with toast notifications (`toast.error()`).
- [ ] Product handle page fetches live Medusa SDK product data (returns `notFound()` if missing).
- [ ] `add-to-cart-button.tsx` `setTimeout` cleans up on unmount.
- [ ] Storefront build completes with exit code 0.
- [ ] All subagents and background tasks are cleanly terminated.
</ACCEPTANCE_CRITERIA>
```

---
### Developer Prompt 5: Workspace Protocol Fix, Storefront Dedicated Health Endpoint, & Final Monorepo Verification

```markdown
/goal

<TASK>
Update `apps/backend/package.json` to use npm workspace protocol (`"*"`) for `@dtc/shared-types`, create a dedicated `/api/health` endpoint in storefront for Docker healthchecks, and run full monorepo verification.
</TASK>

<SUBAGENT_DELEGATION_DIRECTIVE>
- Use `invoke_subagent` to inspect `apps/backend/package.json` workspace dependencies, Docker Compose storefront healthcheck config, and trigger full monorepo build verification.
</SUBAGENT_DELEGATION_DIRECTIVE>

<ANTIGRAVITY_SLASH_COMMANDS>
- /goal: Execute autonomously until workspace dependencies use npm workspace protocol, storefront has /api/health, and full monorepo compiles clean.
</ANTIGRAVITY_SLASH_COMMANDS>

<ANTIGRAVITY_WORKFLOW>
1. RESEARCH & INSPECTION PHASE:
   - View `apps/backend/package.json` (line 35 `"file:..."`).
   - View `infrastructure/docker/docker-compose.tenant.yml` (storefront healthcheck line).
   - Check for `apps/storefront/src/app/api/health/route.ts`.

2. IMPLEMENTATION PHASE:
   - Target files: `apps/backend/package.json`, `apps/storefront/src/app/api/health/route.ts` (NEW), `infrastructure/docker/docker-compose.tenant.yml`
   - **Workspace Protocol**: Change `"@dtc/shared-types": "file:../../packages/shared-types"` to `"@dtc/shared-types": "*"` in `apps/backend/package.json` so npm workspace linking works consistently in CI and local dev without duplicate packages.
   - **Dedicated Health Route**: Create `apps/storefront/src/app/api/health/route.ts`:
     ```typescript
     import { NextResponse } from "next/server"
     export async function GET() {
       return NextResponse.json({ status: "healthy", timestamp: new Date().toISOString() })
     }
     ```
   - **Update Docker Healthcheck**: Change storefront healthcheck in `docker-compose.tenant.yml` from polling `/` to polling `/api/health` — avoiding false failures from homepage redirects or auth guards.

3. EMPIRICAL VERIFICATION & TESTING PHASE:
   - Run shared-types build: `npm run build --workspace=packages/shared-types`
   - Run backend typecheck & build: `cd apps/backend && npx tsc --noEmit && npm run build`
   - Run storefront typecheck & build: `cd apps/storefront && npx tsc --noEmit && npm run build`

4. PROCESS CLEANUP & LEARNING DIRECTIVE (CRITICAL):
   - Execute `/learn` to store workspace protocol and healthcheck rules.
   - Terminate any running subagents, background dev servers, or processes before completing turn.
</ANTIGRAVITY_WORKFLOW>

<ACCEPTANCE_CRITERIA>
- [ ] Subagents delegated for package.json dependencies and healthcheck inspection.
- [ ] `@dtc/shared-types` uses workspace protocol `"*"`.
- [ ] Storefront route `/api/health` exists and returns HTTP 200 `{ status: "healthy" }`.
- [ ] Docker Compose healthcheck updated to target `/api/health`.
- [ ] Monorepo workspaces compile with zero errors (exit code 0 across all 3 packages).
- [ ] All subagents and background tasks are cleanly terminated.
</ACCEPTANCE_CRITERIA>
```
