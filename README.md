# Dedicated 96% -> 100% Final Remediation Prompt Pack (`PROMPT_SEQUENCE_FINAL_100_PERCENT.md`)

This prompt pack contains **4 targeted developer prompts** engineered for **Google Antigravity Agentic IDE** to address the exact 5 remaining items accounting for the remaining **4.0%**, bringing the monorepo to a **100.0% Deployment Readiness Index**:
1. **ETA Client Constructor Parameter Misalignment (-1.5%)**
2. **Workflow Step 3 Redundant Double Hardware Signing (-1.0%)**
3. **Composite Multi-Tax Totals Omission in Audit Logs (-0.5%)**
4. **Missing Kiosk / Aman Integration IDs in `medusa-config.ts` (-0.5%)**
5. **AI Copywriter Worker `forceRefresh` Cache Bypass Flag (-0.5%)**

> [!IMPORTANT]
> **Subagent Directive**: Send these 4 prompts sequentially (Prompt 1 through Prompt 4) to your developer Antigravity instance. Every prompt explicitly instructs the agent to delegate research or sub-tasks to subagents (`invoke_subagent`).

---

## Part 1: ETA Tax Client & Workflow Signing Fixes (Prompts 1–2)

---
### Developer Prompt 1: Unify `EtaClient` Constructor Options Interface & Guard Against Double HSM Signing

```markdown
/goal

<TASK>
Align `apps/backend/src/modules/eta-tax/service.ts:L27` with `apps/backend/src/modules/eta-tax/client.ts:L49-54` by unifying constructor arguments into an options interface (`EtaClientOptions`), and add an `if (!r.signatures?.length)` guard in `client.ts:L186-188` to prevent duplicate hardware token re-signing during workflow Step 3.
</TASK>

<SUBAGENT_DELEGATION_DIRECTIVE>
- Use `invoke_subagent` (Role: "ETA Architecture Specialist", TypeName: "research") to inspect `service.ts` line 27, `client.ts` lines 45–60 and 180–195, and `eta-tax-workflow.ts` lines 75–95.
</SUBAGENT_DELEGATION_DIRECTIVE>

<ANTIGRAVITY_SLASH_COMMANDS>
- /goal: Execute autonomously until EtaClient constructor takes an options object and client.submitReceipts avoids redundant HSM re-signing.
- /learn: Persist ETA client constructor and HSM signature deduplication rules to .gemini/rules.
</ANTIGRAVITY_SLASH_COMMANDS>

<ANTIGRAVITY_WORKFLOW>
1. RESEARCH & INSPECTION PHASE:
   - View `apps/backend/src/modules/eta-tax/service.ts` (lines 20–35).
   - View `apps/backend/src/modules/eta-tax/client.ts` (lines 45–60 and 180–195).
   - Check `apps/backend/src/workflows/eta-tax-workflow.ts` (Step 2 and Step 3).

2. IMPLEMENTATION PHASE:
   - Target files: `apps/backend/src/modules/eta-tax/client.ts`, `apps/backend/src/modules/eta-tax/service.ts`
   - **Unify `EtaClient` Constructor Interface** (`client.ts` & `service.ts`):
     Define and export an options interface in `client.ts`:
     ```typescript
     export interface EtaClientOptions {
       clientId?: string;
       clientSecret?: string;
       environment?: "preprod" | "production" | string;
       hsmProxyUrl?: string;
       accessToken?: string;
       isProduction?: boolean;
     }
     ```
     Update `EtaClient` constructor in `client.ts`:
     ```typescript
     constructor(
       options: EtaClientOptions = {},
       container?: EtaClientDependencies
     ) {
       this.clientId = options.clientId || process.env.ETA_CLIENT_ID || "";
       this.clientSecret = options.clientSecret || process.env.ETA_CLIENT_SECRET || "";
       this.environment = options.environment || (process.env.NODE_ENV === "production" ? "production" : "preprod");
       this.isProduction = options.isProduction ?? (this.environment === "production" || process.env.NODE_ENV === "production");
       this.hsmSigner = container?.resolve?.("hsmSigner") || new EtaHsmSigner({
         hsmProxyUrl: options.hsmProxyUrl || process.env.ETA_HSM_PROXY_URL,
         environment: this.environment,
       });
       this.container = container;
     }
     ```
     Update `service.ts:L27`:
     ```typescript
     this.etaClient_ = new EtaClient(
       {
         clientId: this.options_.clientId,
         clientSecret: this.options_.clientSecret,
         environment: this.options_.environment,
         hsmProxyUrl: this.options_.hsmProxyUrl,
       },
       this.container_
     );
     ```
     *Rationale*: Eliminates the positional parameter bug where `clientId` was assigned as `accessToken` and string `clientSecret` coerced `isProduction` to `true`.

   - **Prevent Redundant Double Hardware Signing** (`client.ts:L186-188`):
     ```typescript
     async submitReceipts(receipts: (EtaReceiptPayload | EtaSignedReceiptPayload)[]): Promise<EtaSubmissionResponse> {
       const signedReceipts: EtaSignedReceiptPayload[] = await Promise.all(
         receipts.map(async (r) => {
           // If already signed by workflow Step 2 (signEtaReceiptHsmStep), do not re-sign:
           if ("signatures" in r && Array.isArray(r.signatures) && r.signatures.length > 0) {
             return r as EtaSignedReceiptPayload;
           }
           return this.hsmSigner.signReceipt(r as EtaReceiptPayload);
         })
       );
       ...
     ```
     *Rationale*: Prevents unnecessary physical USB token roundtrips and latency during Step 3 submission.

3. EMPIRICAL VERIFICATION & TESTING PHASE:
   - Run TypeScript check: `cd apps/backend && npx tsc --noEmit`
   - Run backend build verification: `cd apps/backend && npm run build`

4. PROCESS CLEANUP & LEARNING DIRECTIVE (CRITICAL):
   - Execute `/learn` to store unified constructor options and signature idempotency rules.
   - Terminate any running subagents, background dev servers, or processes before completing turn.
</ANTIGRAVITY_WORKFLOW>

<ACCEPTANCE_CRITERIA>
- [ ] Subagents delegated for ETA client and service parameter inspection.
- [ ] `EtaClient` constructor accepts `EtaClientOptions` object.
- [ ] `service.ts` instantiates `EtaClient` passing `{ clientId, clientSecret, environment, hsmProxyUrl }`.
- [ ] `client.submitReceipts` skips hardware signing if payload already contains valid `signatures`.
- [ ] Backend build completes with exit code 0.
- [ ] All subagents and background tasks cleanly terminated.
</ACCEPTANCE_CRITERIA>
```

---
### Developer Prompt 2: Fix Composite Multi-Tax Totals Summation in ETA Audit Log & Service

```markdown
/goal

<TASK>
Update `apps/backend/src/modules/eta-tax/service.ts:L77` to calculate `totalVatCents` by summing all elements of `payload.taxTotals` array rather than reading only index `[0]`.
</TASK>

<SUBAGENT_DELEGATION_DIRECTIVE>
- Use `invoke_subagent` to inspect `service.ts` lines 70–90 and check `EtaReceiptAudit` model fields for tax logging.
</SUBAGENT_DELEGATION_DIRECTIVE>

<ANTIGRAVITY_SLASH_COMMANDS>
- /goal: Execute autonomously until audit log correctly captures the sum of composite tax totals.
- /learn: Persist composite tax summation rules to .gemini/rules.
</ANTIGRAVITY_SLASH_COMMANDS>

<ANTIGRAVITY_WORKFLOW>
1. RESEARCH & INSPECTION PHASE:
   - View `apps/backend/src/modules/eta-tax/service.ts` (lines 65–90).

2. IMPLEMENTATION PHASE:
   - Target file: `apps/backend/src/modules/eta-tax/service.ts`
   - **Composite Multi-Tax Totals Summation** (`service.ts:L77`):
     ```typescript
     // BEFORE:
     const totalVatCents = Math.round(payload.taxTotals[0]?.amount * 100 || 0);

     // AFTER:
     const totalVatCents = Math.round(
       (payload.taxTotals || []).reduce((sum, item) => sum + (Number(item.amount) || 0), 0) * 100
     );
     ```
     *Rationale*: Captures the full tax sum in `eta_receipt_audit` when orders have composite Egyptian taxes (e.g. 14% T1 VAT + 1% T4 Withholding Tax or Table Tax), rather than dropping secondary tax amounts.

3. EMPIRICAL VERIFICATION & TESTING PHASE:
   - Run TypeScript check: `cd apps/backend && npx tsc --noEmit`
   - Run backend build verification: `cd apps/backend && npm run build`

4. PROCESS CLEANUP & LEARNING DIRECTIVE (CRITICAL):
   - Terminate any running subagents, background dev servers, or processes before completing turn.
</ANTIGRAVITY_WORKFLOW>

<ACCEPTANCE_CRITERIA>
- [ ] Subagents delegated for ETA service audit total inspection.
- [ ] `totalVatCents` sums all items in `payload.taxTotals` array with `reduce`.
- [ ] Backend build completes with exit code 0.
- [ ] All subagents and background tasks cleanly terminated.
</ACCEPTANCE_CRITERIA>
```

---

## Part 2: Configuration & Worker Cache Controls (Prompts 3–4)

---
### Developer Prompt 3: Add `kioskIntegrationId` & `amanIntegrationId` to `medusa-config.ts` Paymob Provider Options

```markdown
/goal

<TASK>
Add `kioskIntegrationId` and `amanIntegrationId` to the Paymob provider options object in `apps/backend/medusa-config.ts:L75-81` to guarantee pure dependency-injected options isolation.
</TASK>

<SUBAGENT_DELEGATION_DIRECTIVE>
- Use `invoke_subagent` to inspect `medusa-config.ts` lines 70–90 and compare against `PaymobModuleOptions` in `src/modules/paymob/types.ts`.
</SUBAGENT_DELEGATION_DIRECTIVE>

<ANTIGRAVITY_SLASH_COMMANDS>
- /goal: Execute autonomously until medusa-config.ts explicitly injects kiosk and aman integration IDs into Paymob module options.
- /learn: Persist Paymob DI options completeness rules to .gemini/rules.
</ANTIGRAVITY_SLASH_COMMANDS>

<ANTIGRAVITY_WORKFLOW>
1. RESEARCH & INSPECTION PHASE:
   - View `apps/backend/medusa-config.ts` (lines 70–95).
   - View `apps/backend/src/modules/paymob/types.ts` (`PaymobModuleOptions`).

2. IMPLEMENTATION PHASE:
   - Target file: `apps/backend/medusa-config.ts`
   - **Inject Kiosk & Aman Options** (`medusa-config.ts`):
     ```typescript
     providers: [
       {
         resolve: "./src/modules/paymob",
         id: "paymob",
         options: {
           apiKey: process.env.PAYMOB_API_KEY,
           hmacSecret: process.env.PAYMOB_HMAC_SECRET,
           cardIntegrationId: process.env.PAYMOB_CARD_INTEGRATION_ID,
           walletIntegrationId: process.env.PAYMOB_WALLET_INTEGRATION_ID,
           valuIntegrationId: process.env.PAYMOB_VALU_INTEGRATION_ID,
           souhoolaIntegrationId: process.env.PAYMOB_SOUHOOLA_INTEGRATION_ID,
           symplIntegrationId: process.env.PAYMOB_SYMPL_INTEGRATION_ID,
           kioskIntegrationId: process.env.PAYMOB_KIOSK_INTEGRATION_ID,
           amanIntegrationId: process.env.PAYMOB_AMAN_INTEGRATION_ID,
         },
       },
     ],
     ```
     *Rationale*: Guarantees pure dependency injection without requiring fallback to global `process.env` lookups within service methods.

3. EMPIRICAL VERIFICATION & TESTING PHASE:
   - Run TypeScript check: `cd apps/backend && npx tsc --noEmit`
   - Run backend build verification: `cd apps/backend && npm run build`

4. PROCESS CLEANUP & LEARNING DIRECTIVE (CRITICAL):
   - Terminate any running subagents, background dev servers, or processes before completing turn.
</ANTIGRAVITY_WORKFLOW>

<ACCEPTANCE_CRITERIA>
- [ ] Subagents delegated for Paymob configuration options inspection.
- [ ] `medusa-config.ts` injects `kioskIntegrationId` and `amanIntegrationId`.
- [ ] Backend build completes with exit code 0.
- [ ] All subagents and background tasks cleanly terminated.
</ACCEPTANCE_CRITERIA>
```

---
### Developer Prompt 4: Add `forceRefresh` Cache Bypass Flag to AI Copywriter Worker & Admin Widget

```markdown
/goal

<TASK>
Add an optional `forceRefresh?: boolean` parameter to `apps/backend/src/jobs/ai-copywriter-worker.ts:L83-89`, `apps/backend/src/jobs/background-queue.ts`, and `apps/backend/src/admin/widgets/ai-copywriter.tsx` to allow administrators to regenerate copy on-demand without 24-hour cache locks.
</TASK>

<SUBAGENT_DELEGATION_DIRECTIVE>
- Use `invoke_subagent` to inspect `ai-copywriter-worker.ts` lines 75–100, `background-queue.ts` job types, and `ai-copywriter.tsx` generation dispatch.
</SUBAGENT_DELEGATION_DIRECTIVE>

<ANTIGRAVITY_SLASH_COMMANDS>
- /goal: Execute autonomously until AI copywriter worker respects forceRefresh to bypass stale 24h cache when requested.
- /learn: Persist worker cache bypass rules to .gemini/rules.
</ANTIGRAVITY_SLASH_COMMANDS>

<ANTIGRAVITY_WORKFLOW>
1. RESEARCH & INSPECTION PHASE:
   - View `apps/backend/src/jobs/ai-copywriter-worker.ts` (lines 75–105).
   - View `apps/backend/src/jobs/background-queue.ts` (`AiCopywriterJobData` interface).
   - View `apps/backend/src/admin/widgets/ai-copywriter.tsx` (request payload).

2. IMPLEMENTATION PHASE:
   - Target files: `apps/backend/src/jobs/background-queue.ts`, `apps/backend/src/jobs/ai-copywriter-worker.ts`, `apps/backend/src/admin/widgets/ai-copywriter.tsx`
   - **Add `forceRefresh` to Job Interface** (`background-queue.ts`):
     ```typescript
     export interface AiCopywriterJobData {
       productId: string;
       title: string;
       description?: string;
       category?: string;
       forceRefresh?: boolean;
     }
     ```
   - **Respect `forceRefresh` in Worker** (`ai-copywriter-worker.ts:L83-89`):
     ```typescript
     const existingResult = await getAiCopywriterTaskResult(productId);
     if (!job.data.forceRefresh && existingResult && existingResult.status === "COMPLETED") {
       console.log(`[AiWorker] Returning cached copy for product ${productId}`);
       return existingResult;
     }
     ```
   - **Pass `forceRefresh` from Admin Widget** (`ai-copywriter.tsx`):
     Add a "Regenerate" toggle or checkbox (`forceRefresh: true`) when the user clicks the "Regenerate Copy" button.

3. EMPIRICAL VERIFICATION & TESTING PHASE:
   - Run backend typecheck: `cd apps/backend && npx tsc --noEmit`
   - Run backend Medusa build: `cd apps/backend && npm run build`
   - Run storefront build: `cd apps/storefront && npm run build`

4. PROCESS CLEANUP & LEARNING DIRECTIVE (CRITICAL):
   - Terminate any running subagents, background dev servers, or processes before completing turn.
</ANTIGRAVITY_WORKFLOW>

<ACCEPTANCE_CRITERIA>
- [ ] Subagents delegated for AI worker job interface and cache logic inspection.
- [ ] `AiCopywriterJobData` includes `forceRefresh?: boolean`.
- [ ] `ai-copywriter-worker.ts` checks `!job.data.forceRefresh` before returning cached results.
- [ ] Admin widget can dispatch `forceRefresh: true`.
- [ ] Full monorepo compiles clean with 0 errors (`shared-types`, `backend`, `storefront`).
- [ ] All subagents and background tasks cleanly terminated.
</ACCEPTANCE_CRITERIA>
```
