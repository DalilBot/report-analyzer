# Final 9.78 Production Hardening Developer Prompt Pack (`PROMPT_SEQUENCE_978_ENHANCEMENTS.md`)

This prompt pack contains **4 dedicated developer prompts** engineered for **Google Antigravity Agentic IDE** to implement the final production hardening, BNPL provider extensions, JSON-LD metadata fixes, SDK fetch consolidation, and Bosta rate cache pre-warming scheduled jobs identified in the 9.78/10 report.

> [!IMPORTANT]
> **Subagent Directive**: Send these 4 prompts sequentially (Prompt 1 through Prompt 4) to your developer Antigravity instance. Every prompt explicitly instructs the agent to delegate research or sub-tasks to subagents (`invoke_subagent`) to maintain clean context and maximize execution speed.

---

## Part 1: Backend Module & Integration Extensions (Prompts 1–2)

---
### Developer Prompt 1: Extend Paymob Integration Options (`souhoolaIntegrationId`, `symplIntegrationId`)

```markdown
/goal

<TASK>
Expose `souhoolaIntegrationId` and `symplIntegrationId` in `PaymobModuleOptions` in `apps/backend/src/modules/paymob/service.ts` and `medusa-config.ts`.
</TASK>

<SUBAGENT_DELEGATION_DIRECTIVE>
- Use `invoke_subagent` (Role: "Codebase Researcher", TypeName: "research") to inspect Paymob module options types and session configuration mappings.
</SUBAGENT_DELEGATION_DIRECTIVE>

<ANTIGRAVITY_SLASH_COMMANDS>
- /goal: Execute autonomously until Paymob module options support Souhoola and Sympl BNPL integration IDs cleanly.
- /learn: Persist Paymob multi-BNPL integration rules to .gemini/rules.
</ANTIGRAVITY_SLASH_COMMANDS>

<ANTIGRAVITY_WORKFLOW>
1. RESEARCH & INSPECTION PHASE:
   - View `apps/backend/src/modules/paymob/service.ts`, `apps/backend/src/modules/paymob/index.ts`, and `apps/backend/medusa-config.ts`.

2. IMPLEMENTATION PHASE:
   - Target files: `apps/backend/src/modules/paymob/service.ts`, `apps/backend/src/modules/paymob/index.ts`, `apps/backend/medusa-config.ts`
   - Update `PaymobModuleOptions` interface to support:
     ```typescript
     souhoolaIntegrationId?: string;
     symplIntegrationId?: string;
     ```
   - In `service.ts` (`initiatePayment`), dynamically resolve integration IDs for Souhoola (`souhoolaIntegrationId`) and Sympl (`symplIntegrationId`) based on payment session provider context.
   - Update `medusa-config.ts` to map `PAYMOB_SOUHOOLA_INTEGRATION_ID` and `PAYMOB_SYMPL_INTEGRATION_ID` from environment variables.

3. EMPIRICAL VERIFICATION & TESTING PHASE:
   - Run TypeScript check: `cd apps/backend && npx tsc --noEmit`
   - Run backend build verification: `cd apps/backend && npm run build`

4. PROCESS CLEANUP & LEARNING DIRECTIVE (CRITICAL):
   - Execute `/learn` to store Paymob BNPL options rules.
   - Terminate any running subagents, background dev servers, or processes before completing turn.
</ANTIGRAVITY_WORKFLOW>

<ACCEPTANCE_CRITERIA>
- [ ] Subagents delegated for Paymob module options interface research.
- [ ] `PaymobModuleOptions` includes `souhoolaIntegrationId` and `symplIntegrationId`.
- [ ] `medusa-config.ts` maps Souhoola and Sympl integration IDs from environment variables.
- [ ] Backend build completes with exit code 0.
- [ ] All subagents and background tasks are cleanly terminated.
</ACCEPTANCE_CRITERIA>
```

---
### Developer Prompt 2: Medusa Scheduled Job for Bosta Shipping Rate Cache Pre-Warming

```markdown
/goal

<TASK>
Create a Medusa scheduled job `apps/backend/src/jobs/prewarm-bosta-rates.ts` to pre-warm Redis shipping rate cache keys for high-volume Egyptian governorates.
</TASK>

<SUBAGENT_DELEGATION_DIRECTIVE>
- Delegate Medusa 2.0 scheduled job registration and Bosta rate calculation inspection to a subagent via `invoke_subagent`.
</SUBAGENT_DELEGATION_DIRECTIVE>

<ANTIGRAVITY_SLASH_COMMANDS>
- /goal: Execute autonomously until Bosta rate cache pre-warming scheduled job compiles and registers clean.
- /learn: Persist Medusa scheduled job rules to .gemini/rules.
</ANTIGRAVITY_SLASH_COMMANDS>

<ANTIGRAVITY_WORKFLOW>
1. RESEARCH & INSPECTION PHASE:
   - View `apps/backend/src/modules/bosta/service.ts` and inspect Medusa 2.0 scheduled job patterns (`@medusajs/framework/jobs`).

2. IMPLEMENTATION PHASE:
   - Target files: `apps/backend/src/jobs/prewarm-bosta-rates.ts`, `apps/backend/medusa-config.ts`
   - Create scheduled job `prewarm-bosta-rates.ts` running on cron schedule (e.g. `0 4 * * *` daily at 4:00 AM).
   - Pre-calculate shipping rates for high-volume governorates (`Cairo`, `Giza`, `Alexandria`) across standard and express options for base weights (1kg, 2kg, 5kg), storing results directly in Redis cache (`BOSTA_RATE_*`) with 24-hour TTL.

3. EMPIRICAL VERIFICATION & TESTING PHASE:
   - Run TypeScript check: `cd apps/backend && npx tsc --noEmit`
   - Run backend build verification: `cd apps/backend && npm run build`

4. PROCESS CLEANUP & LEARNING DIRECTIVE (CRITICAL):
   - Execute `/learn` to store Medusa scheduled job patterns.
   - Terminate any running subagents, background dev servers, or processes before completing turn.
</ANTIGRAVITY_WORKFLOW>

<ACCEPTANCE_CRITERIA>
- [ ] Subagents delegated for scheduled job registration research.
- [ ] `src/jobs/prewarm-bosta-rates.ts` created and registered on cron schedule.
- [ ] Pre-warms Redis shipping rate cache for Cairo, Giza, and Alexandria.
- [ ] Backend build completes with exit code 0.
- [ ] All subagents and background tasks are cleanly terminated.
</ACCEPTANCE_CRITERIA>
```

---

## Part 2: Storefront Metadata & SDK Consolidation (Prompts 3–4)

---
### Developer Prompt 3: Dynamic Storefront Base URL in Product JSON-LD Metadata

```markdown
/goal

<TASK>
Replace hardcoded `"https://localhost:3000"` fallback in `apps/storefront/src/modules/products/components/product-json-ld.tsx` with `process.env.NEXT_PUBLIC_STORE_URL`.
</TASK>

<SUBAGENT_DELEGATION_DIRECTIVE>
- Use `invoke_subagent` to inspect Storefront JSON-LD metadata components and environment variable resolution.
</SUBAGENT_DELEGATION_DIRECTIVE>

<ANTIGRAVITY_SLASH_COMMANDS>
- /goal: Execute autonomously until Product JSON-LD metadata dynamically uses NEXT_PUBLIC_STORE_URL.
</ANTIGRAVITY_SLASH_COMMANDS>

<ANTIGRAVITY_WORKFLOW>
1. RESEARCH & INSPECTION PHASE:
   - View `apps/storefront/src/modules/products/components/product-json-ld.tsx` and `apps/storefront/src/app/[countryCode]/products/[handle]/page.tsx`.

2. IMPLEMENTATION PHASE:
   - Target files: `apps/storefront/src/modules/products/components/product-json-ld.tsx`, `apps/storefront/src/app/[countryCode]/products/[handle]/page.tsx`
   - Replace fallback string `"https://localhost:3000"` in Product and Offer Schema.org JSON-LD objects with `process.env.NEXT_PUBLIC_STORE_URL || "https://egyptbrand.com"`.

3. EMPIRICAL VERIFICATION & TESTING PHASE:
   - Run storefront build verification: `cd apps/storefront && npm run build`

4. PROCESS CLEANUP & LEARNING DIRECTIVE (CRITICAL):
   - Terminate any running subagents, background dev servers (e.g. `next dev`) before completing turn.
</ANTIGRAVITY_WORKFLOW>

<ACCEPTANCE_CRITERIA>
- [ ] Subagents delegated for JSON-LD component research.
- [ ] `product-json-ld.tsx` reads `process.env.NEXT_PUBLIC_STORE_URL`.
- [ ] Storefront build completes with exit code 0.
- [ ] All subagents and background tasks are cleanly terminated.
</ACCEPTANCE_CRITERIA>
```

---
### Developer Prompt 4: Consolidate Storefront Data Fetching via Global Medusa JS SDK (`sdk.client.fetch`)

```markdown
/goal

<TASK>
Consolidate custom fetch wrappers in `apps/storefront/src/lib/data/products.ts` to use `sdk.client.fetch` from `@medusajs/js-sdk`.
</TASK>

<SUBAGENT_DELEGATION_DIRECTIVE>
- Delegate Medusa JS SDK client fetch API inspection to a subagent via `invoke_subagent`.
</SUBAGENT_DELEGATION_DIRECTIVE>

<ANTIGRAVITY_SLASH_COMMANDS>
- /goal: Execute autonomously until Storefront product data fetching uses global Medusa JS SDK client instance exclusively.
- /learn: Persist Medusa SDK fetch patterns to .gemini/rules.
</ANTIGRAVITY_SLASH_COMMANDS>

<ANTIGRAVITY_WORKFLOW>
1. RESEARCH & INSPECTION PHASE:
   - View `apps/storefront/src/lib/data/products.ts` and `apps/storefront/src/lib/medusa.ts`.

2. IMPLEMENTATION PHASE:
   - Target file: `apps/storefront/src/lib/data/products.ts`
   - Refactor custom `fetch()` calls to use `sdk.client.fetch()` from the central Medusa SDK instance (`src/lib/medusa.ts`) to ensure uniform header propagation, authentication, and error handling across all storefront requests.

3. EMPIRICAL VERIFICATION & TESTING PHASE:
   - Run storefront build verification: `cd apps/storefront && npm run build`

4. PROCESS CLEANUP & LEARNING DIRECTIVE (CRITICAL):
   - Terminate any running subagents, background dev servers, or processes before completing turn.
</ANTIGRAVITY_WORKFLOW>

<ACCEPTANCE_CRITERIA>
- [ ] Subagents delegated for Medusa SDK client fetch research.
- [ ] `src/lib/data/products.ts` uses `sdk.client.fetch()` exclusively.
- [ ] Storefront build completes with exit code 0.
- [ ] All subagents and background tasks are cleanly terminated.
</ACCEPTANCE_CRITERIA>
```
