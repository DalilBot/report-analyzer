# Dedicated 95% -> 100% Final Perfection Prompt Pack (`PROMPT_SEQUENCE_FINAL_5_PERCENT_PERFECTION.md`)

This prompt pack contains **4 targeted developer prompts** engineered for **Google Antigravity Agentic IDE** to address the exact 4 remaining gaps accounting for the final **5.0%** deduction identified in the audit report, bringing the monorepo to a **100.0% Deployment Readiness Index**:
1. **Storefront Cart Drawer Checkout Navigation Link (-1.5%)**
2. **ETA Tax: Dynamic GS1/EGS Coding, Workflow Audit Persistence & Registration Cleanup (-1.5%)**
3. **Gemini AI Worker: Forward Category Context & Retry-Safe Redis Caching (-1.0%)**
4. **Storefront CSS Font Variable Fallback & Robust Cookie Parsing (-1.0%)**

> [!IMPORTANT]
> **Subagent Directive**: Send these 4 prompts sequentially (Prompt 1 through Prompt 4) to your developer Antigravity instance. Every prompt explicitly instructs the agent to delegate research or sub-tasks to subagents (`invoke_subagent`).

---

## Part 1: Storefront Drawer Navigation & Frontend Edge Cases (Prompts 1–2)

---
### Developer Prompt 1: Fix Cart Drawer Checkout Navigation CTA in `home-client-view.tsx`

```markdown
/goal

<TASK>
In `apps/storefront/src/modules/home/components/home-client-view.tsx:L306-L311`, wrap the "Proceed to Checkout" (متابعة لإتمام الطلب) drawer button in a Next.js `<Link href={`/${countryCode || "eg"}/checkout`}>` (or attach an `onClick` router push handler) and ensure it closes the drawer upon navigation.
</TASK>

<SUBAGENT_DELEGATION_DIRECTIVE>
- Use `invoke_subagent` (Role: "Storefront UI Specialist", TypeName: "research") to inspect `home-client-view.tsx` lines 290–330 around the slide-over cart drawer CTA button.
</SUBAGENT_DELEGATION_DIRECTIVE>

<ANTIGRAVITY_SLASH_COMMANDS>
- /goal: Execute autonomously until cart drawer checkout button seamlessly navigates to the checkout page.
- /learn: Persist storefront navigation and drawer state management rules to .gemini/rules.
</ANTIGRAVITY_SLASH_COMMANDS>

<ANTIGRAVITY_WORKFLOW>
1. RESEARCH & INSPECTION PHASE:
   - View `apps/storefront/src/modules/home/components/home-client-view.tsx` (lines 295–325).
   - Check how `countryCode` is passed or derived in `home-client-view.tsx`.

2. IMPLEMENTATION PHASE:
   - Target file: `apps/storefront/src/modules/home/components/home-client-view.tsx`
   - **Wrap or Wire Drawer Checkout Button** (`home-client-view.tsx:L306-L311`):
     ```tsx
     // BEFORE:
     <button
       disabled={items.length === 0}
       className="w-full py-3 bg-amber-500 hover:bg-amber-600 disabled:opacity-50 text-white rounded-xl font-bold text-xs shadow-md transition-colors"
     >
       {isRtl ? "متابعة لإتمام الطلب" : "Proceed to Checkout"} (Paymob / Bosta)
     </button>

     // AFTER:
     <Link
       href={`/${countryCode || "eg"}/checkout`}
       onClick={() => setIsCartOpen(false)}
       className={`w-full block text-center py-3 bg-amber-500 hover:bg-amber-600 text-white rounded-xl font-bold text-xs shadow-md transition-colors ${
         items.length === 0 ? "pointer-events-none opacity-50" : ""
       }`}
     >
       {isRtl ? "متابعة لإتمام الطلب" : "Proceed to Checkout"} (Paymob / Bosta)
     </Link>
     ```
   - Ensure Next.js `Link` component is imported (`import Link from "next/link"`).

3. EMPIRICAL VERIFICATION & TESTING PHASE:
   - Run storefront typecheck: `cd apps/storefront && npx tsc --noEmit`
   - Run storefront build: `cd apps/storefront && npm run build`

4. PROCESS CLEANUP & LEARNING DIRECTIVE (CRITICAL):
   - Terminate any running subagents, background dev servers, or processes before completing turn.
</ANTIGRAVITY_WORKFLOW>

<ACCEPTANCE_CRITERIA>
- [ ] Subagents delegated for cart drawer CTA code inspection.
- [ ] Drawer "Proceed to Checkout" button is wrapped in `<Link href={`/${countryCode || "eg"}/checkout`}>`.
- [ ] Clicking checkout CTA closes the drawer and navigates to `/[countryCode]/checkout`.
- [ ] Storefront build completes with exit code 0.
- [ ] All subagents and background tasks cleanly terminated.
</ACCEPTANCE_CRITERIA>
```

---
### Developer Prompt 2: Fix Storefront Monospace Font Fallback in `globals.css` & Robust Regex Cookie Parsing in `cart-context.tsx`

```markdown
/goal

<TASK>
Add a fallback for `--font-geist-mono` in `apps/storefront/src/app/globals.css:L12` and replace brittle substring split cookie parsing with robust regex in `apps/storefront/src/lib/context/cart-context.tsx:L74-L77`.
</TASK>

<SUBAGENT_DELEGATION_DIRECTIVE>
- Use `invoke_subagent` to inspect `globals.css` line 12 and `cart-context.tsx` lines 70–85.
</SUBAGENT_DELEGATION_DIRECTIVE>

<ANTIGRAVITY_SLASH_COMMANDS>
- /goal: Execute autonomously until CSS monospace font variable has safe system fallbacks and cookie parsing is immune to substring collisions.
- /learn: Persist CSS font fallbacks and client cookie parsing rules to .gemini/rules.
</ANTIGRAVITY_SLASH_COMMANDS>

<ANTIGRAVITY_WORKFLOW>
1. RESEARCH & INSPECTION PHASE:
   - View `apps/storefront/src/app/globals.css` (lines 1–25).
   - View `apps/storefront/src/lib/context/cart-context.tsx` (lines 65–85).

2. IMPLEMENTATION PHASE:
   - Target files: `apps/storefront/src/app/globals.css`, `apps/storefront/src/lib/context/cart-context.tsx`
   - **Monospace Font Fallback** (`globals.css:L12`):
     ```css
     /* BEFORE */
     font-family: var(--font-geist-mono);

     /* AFTER */
     font-family: var(--font-geist-mono, ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace);
     ```
     *Rationale*: Prevents missing font variable warnings if `--font-geist-mono` is not defined in `layout.tsx`.

   - **Robust Cookie Parsing** (`cart-context.tsx:L74-L77`):
     ```typescript
     // BEFORE:
     const value = `; ${document.cookie}`;
     const parts = value.split(`; ${name}=`);
     if (parts.length === 2) return parts.pop()?.split(';').shift();

     // AFTER:
     const match = document.cookie.match(new RegExp(`(?:^|;\\s*)${name}=([^;]*)`));
     return match ? decodeURIComponent(match[1]) : undefined;
     ```
     *Rationale*: Prevents `parts.length === 2` checks from failing when multiple cookie keys share similar prefix substrings.

3. EMPIRICAL VERIFICATION & TESTING PHASE:
   - Run storefront typecheck: `cd apps/storefront && npx tsc --noEmit`
   - Run storefront build: `cd apps/storefront && npm run build`

4. PROCESS CLEANUP & LEARNING DIRECTIVE (CRITICAL):
   - Terminate any running subagents, background dev servers, or processes before completing turn.
</ANTIGRAVITY_WORKFLOW>

<ACCEPTANCE_CRITERIA>
- [ ] Subagents delegated for CSS font variables and cookie parsing inspection.
- [ ] `globals.css` provides system font fallbacks for monospace font stack.
- [ ] `cart-context.tsx` parses cookies using regex with `decodeURIComponent`.
- [ ] Storefront build completes with exit code 0.
- [ ] All subagents and background tasks cleanly terminated.
</ACCEPTANCE_CRITERIA>
```

---

## Part 2: ETA Tax Compliance & AI Worker Reliability (Prompts 3–4)

---
### Developer Prompt 3: ETA Dynamic GS1/EGS Coding, Workflow Audit Persistence Step & Module Class Field Declaration

```markdown
/goal

<TASK>
In `apps/backend/src/modules/eta-tax/payload-builder.ts:L242-L243`, dynamically assign `itemType: "GS1"` for 13-digit numeric GTINs and `"EGS"` otherwise; in `apps/backend/src/modules/eta-tax/service.ts:L16-L36`, explicitly declare `private hsmSigner_: EtaHsmSigner` on the class definition; and add a step in `apps/backend/src/workflows/eta-tax-workflow.ts` to persist successful submissions into the `EtaReceiptAudit` table.
</TASK>

<SUBAGENT_DELEGATION_DIRECTIVE>
- Use `invoke_subagent` (Role: "ETA Tax Compliance Specialist", TypeName: "research") to inspect `payload-builder.ts` line 242, `service.ts` line 36, and `eta-tax-workflow.ts` step pipeline.
</SUBAGENT_DELEGATION_DIRECTIVE>

<ANTIGRAVITY_SLASH_COMMANDS>
- /goal: Execute autonomously until ETA items support dynamic GS1/EGS codes, class fields are declared, and workflow persists audit records.
- /learn: Persist ETA item coding, audit recording, and class field declaration rules to .gemini/rules.
</ANTIGRAVITY_SLASH_COMMANDS>

<ANTIGRAVITY_WORKFLOW>
1. RESEARCH & INSPECTION PHASE:
   - View `apps/backend/src/modules/eta-tax/payload-builder.ts` (lines 235–255).
   - View `apps/backend/src/modules/eta-tax/service.ts` (lines 15–40).
   - View `apps/backend/src/workflows/eta-tax-workflow.ts` (lines 75–130).

2. IMPLEMENTATION PHASE:
   - Target files: `apps/backend/src/modules/eta-tax/payload-builder.ts`, `apps/backend/src/modules/eta-tax/service.ts`, `apps/backend/src/workflows/eta-tax-workflow.ts`
   - **Dynamic GS1 vs EGS Item Type** (`payload-builder.ts:L242-L243`):
     ```typescript
     // BEFORE:
     itemType: "EGS",

     // AFTER:
     itemType: /^\d{13}$/.test(item.itemCode || item.sku || "") ? "GS1" : "EGS",
     ```
     *Rationale*: 13-digit international numeric GTIN/EAN barcodes must be classified as `"GS1"`, while custom internal codes (`EG-TRN-SKU`) use `"EGS"`.

   - **Declare `hsmSigner_` Class Property** (`service.ts:L16-L36`):
     ```typescript
     export class EtaTaxModuleService extends MedusaService({
       EtaReceiptAudit,
     }) {
       protected options_: EtaTaxModuleOptions;
       protected container_: any;
       protected etaClient_: EtaClient;
       protected hsmSigner_: EtaHsmSigner; // <-- Explicit class property declaration
     ```

   - **Workflow Audit Record Persistence Step** (`eta-tax-workflow.ts`):
     Add `recordEtaAuditStep` after `submitEtaPortalReceiptStep` in `eta-tax-workflow.ts`:
     ```typescript
     export const recordEtaAuditStep = createStep(
       "record-eta-audit-step",
       async (input: { orderId: string; submissionUuid: string; totalVatCents: number; rawPayload: any; rawResponse: any }, { container }) => {
         const etaTaxService = container.resolve<EtaTaxModuleService>("etaTax");
         if (etaTaxService?.createEtaReceiptAudits) {
           await etaTaxService.createEtaReceiptAudits({
             order_id: input.orderId,
             submission_uuid: input.submissionUuid,
             total_vat_cents: input.totalVatCents,
             status: "ACCEPTED",
             raw_payload: input.rawPayload,
             raw_response: input.rawResponse,
           });
         }
         return new StepResponse({ status: "RECORDED" });
       }
     );
     ```

3. EMPIRICAL VERIFICATION & TESTING PHASE:
   - Run TypeScript check: `cd apps/backend && npx tsc --noEmit`
   - Run backend build verification: `cd apps/backend && npm run build`

4. PROCESS CLEANUP & LEARNING DIRECTIVE (CRITICAL):
   - Execute `/learn` to store ETA tax audit and coding rules.
   - Terminate any running subagents, background dev servers, or processes before completing turn.
</ANTIGRAVITY_WORKFLOW>

<ACCEPTANCE_CRITERIA>
- [ ] Subagents delegated for ETA payload, service, and workflow audit inspection.
- [ ] `payload-builder.ts` detects 13-digit numeric codes as `itemType: "GS1"`.
- [ ] `service.ts` explicitly declares `protected hsmSigner_: EtaHsmSigner`.
- [ ] `eta-tax-workflow.ts` persists successful submissions to `EtaReceiptAudit` table.
- [ ] Backend build completes with exit code 0.
- [ ] All subagents and background tasks cleanly terminated.
</ACCEPTANCE_CRITERIA>
```

---
### Developer Prompt 4: Forward Category Context to AI Copywriter & Prevent Premature "FAILED" Caching During Retries

```markdown
/goal

<TASK>
In `apps/backend/src/jobs/ai-copywriter-worker.ts:L102-L105`, forward `category` and `description` from the BullMQ job payload into `generateProductCopy()`, and in `L153-L165` ensure transient failure responses do not write permanent `status: "FAILED"` to Redis while BullMQ retry attempts are still pending.
</TASK>

<SUBAGENT_DELEGATION_DIRECTIVE>
- Use `invoke_subagent` (Role: "AI Queue Engineer", TypeName: "research") to inspect `ai-copywriter-worker.ts` lines 95–170.
</SUBAGENT_DELEGATION_DIRECTIVE>

<ANTIGRAVITY_SLASH_COMMANDS>
- /goal: Execute autonomously until AI worker forwards category context and intermediate retries do not set premature FAILED cache status.
- /learn: Persist BullMQ worker payload forwarding and retry caching rules to .gemini/rules.
</ANTIGRAVITY_SLASH_COMMANDS>

<ANTIGRAVITY_WORKFLOW>
1. RESEARCH & INSPECTION PHASE:
   - View `apps/backend/src/jobs/ai-copywriter-worker.ts` (lines 95–170).

2. IMPLEMENTATION PHASE:
   - Target file: `apps/backend/src/jobs/ai-copywriter-worker.ts`
   - **Forward Category & Description Context** (`ai-copywriter-worker.ts:L102-L105`):
     ```typescript
     // BEFORE:
     const copyResult = await geminiService.generateProductCopy(job.data.title);

     // AFTER:
     const copyResult = await geminiService.generateProductCopy(
       job.data.title,
       job.data.description || "",
       job.data.category || "عام"
     );
     ```
     *Rationale*: Preserves the category context (e.g. "إلكترونيات", "أزياء") and existing product description in asynchronous background copywriting tasks, avoiding falling back to generic copy.

   - **Condition "FAILED" Redis Caching on Final Retry Attempt** (`ai-copywriter-worker.ts:L153-L165`):
     ```typescript
     // In worker catch block:
     const isFinalAttempt = (job.attemptsMade + 1) >= (job.opts.attempts || 5);
     if (isFinalAttempt) {
       await setAiCopywriterTaskResult(productId, {
         status: "FAILED",
         error: error.message || "Failed after maximum retry attempts",
         failedAt: new Date().toISOString(),
       });
     }
     throw error; // Re-throw so BullMQ schedules the next exponential backoff retry
     ```
     *Rationale*: Prevents admin users polling the copywriting task status from seeing a transient "FAILED" status during intermediate BullMQ retries (e.g., attempt 1 of 5).

3. EMPIRICAL VERIFICATION & TESTING PHASE:
   - Run backend typecheck: `cd apps/backend && npx tsc --noEmit`
   - Run backend build: `cd apps/backend && npm run build`
   - Run storefront build: `cd apps/storefront && npm run build`

4. PROCESS CLEANUP & LEARNING DIRECTIVE (CRITICAL):
   - Terminate any running subagents, background dev servers, or processes before completing turn.
</ANTIGRAVITY_WORKFLOW>

<ACCEPTANCE_CRITERIA>
- [ ] Subagents delegated for AI worker context forwarding and retry caching inspection.
- [ ] `generateProductCopy` receives `job.data.title`, `job.data.description`, and `job.data.category`.
- [ ] Redis task result is only marked `FAILED` on the final retry attempt (`isFinalAttempt`).
- [ ] Full monorepo builds cleanly with exit code 0 (`packages/shared-types`, `apps/backend`, `apps/storefront`).
- [ ] All subagents and background tasks cleanly terminated.
</ACCEPTANCE_CRITERIA>
```
