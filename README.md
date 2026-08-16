# Dedicated 100% Enterprise Perfection Remediation Prompt Pack (`PROMPT_SEQUENCE_100_PERCENT_PERFECTION.md`)

This prompt pack contains **5 targeted developer prompts** engineered for **Google Antigravity Agentic IDE** to address the exact 6 remaining gaps totaling **5.5%** identified in the evaluation report, achieving a **100% Deployment Readiness Score**:
1. **ETA Composite Multi-Tax Line Support (T1 + T4) (+1.5%)**
2. **Tax Module Registration Duality & Clean DI Separation (+1.0%)**
3. **Centralized HTTP Security & Zod Validation Middleware (`src/api/middlewares.ts`) (+1.0%)**
4. **Storefront Cart `lineItemId` vs `variantId` Dual Tracking (+0.8%)**
5. **Standalone Shared-Types Build Configuration (`"build": "tsc"`) (+0.7%)**
6. **Dynamic Tenant Container Naming in Docker Compose (`${TENANT_ID}`) (+0.5%)**

> [!IMPORTANT]
> **Subagent Directive**: Send these 5 prompts sequentially (Prompt 1 through Prompt 5) to your developer Antigravity instance. Every prompt explicitly instructs the agent to delegate research or sub-tasks to subagents (`invoke_subagent`).

---

## Part 1: Tax Engine & Module DI Architecture (Prompts 1–2)

---
### Developer Prompt 1: Implement ETA Composite Multi-Tax Line Iteration (T1 VAT + T4 Withholding Tax) in `payload-builder.ts`

```markdown
/goal

<TASK>
Update `apps/backend/src/modules/eta-tax/payload-builder.ts:L197` to iterate over all `item.taxLines` rather than indexing `taxLines?.[0]`, supporting composite Egyptian tax structures (e.g., T1 VAT + T4 Withholding Tax / Table Tax) and correctly aggregating item-level and document-level tax totals.
</TASK>

<SUBAGENT_DELEGATION_DIRECTIVE>
- Use `invoke_subagent` (Role: "Tax Compliance Researcher", TypeName: "research") to inspect `payload-builder.ts` around line 197 and analyze how Egyptian Tax Authority e-Receipt/e-Invoice v1.0 specifications handle multi-tax lines (taxableItems array with multiple taxType/subType/amount entries per item).
</SUBAGENT_DELEGATION_DIRECTIVE>

<ANTIGRAVITY_SLASH_COMMANDS>
- /goal: Execute autonomously until ETA tax payload builder supports multiple tax lines per line item with exact canonical serialization.
- /learn: Persist ETA composite multi-tax calculation rules to .gemini/rules.
</ANTIGRAVITY_SLASH_COMMANDS>

<ANTIGRAVITY_WORKFLOW>
1. RESEARCH & INSPECTION PHASE:
   - View `apps/backend/src/modules/eta-tax/payload-builder.ts` (lines 180–240).
   - Review ETA spec for `taxableItems`:
     ```json
     "taxableItems": [
       { "taxType": "T1", "subType": "V009", "rate": 14, "amount": 140.00 },
       { "taxType": "T4", "subType": "W001", "rate": 1, "amount": 10.00 }
     ]
     ```

2. IMPLEMENTATION PHASE:
   - Target file: `apps/backend/src/modules/eta-tax/payload-builder.ts`
   - **Composite Multi-Tax Line Iteration** (`payload-builder.ts`):
     Refactor the line item tax evaluation:
     ```typescript
     // BEFORE (Single Tax Line only):
     const taxLine = item.taxLines?.[0];
     const vatRate = taxLine?.rate ?? 14;
     ...

     // AFTER (Composite Multi-Tax Support):
     const taxableItems = (item.taxLines && item.taxLines.length > 0)
       ? item.taxLines.map((tl) => {
           const taxType = tl.code?.startsWith("T") ? tl.code : (tl.taxType || "T1");
           const subType = tl.subType || (taxType === "T1" ? "V009" : "W001");
           const rate = Number(tl.rate ?? 14);
           const taxAmount = roundCurrency((lineTotalEgp * rate) / 100);
           return {
             taxType,
             subType,
             rate,
             amount: taxAmount,
           };
         })
       : [
           {
             taxType: "T1",
             subType: "V009",
             rate: 14,
             amount: roundCurrency((lineTotalEgp * 14) / 100),
           },
         ];
     ```
   - **Aggregate Total Taxes by Tax Type**: Sum all taxable items across lines by `taxType` in the receipt summary header (`taxTotals`).
   - Run the built-in self-test in `payload-builder.ts` to ensure canonical JSON sorting and SHA-256 digest calculations pass cleanly.

3. EMPIRICAL VERIFICATION & TESTING PHASE:
   - Run TypeScript check: `cd apps/backend && npx tsc --noEmit`
   - Run backend build verification: `cd apps/backend && npm run build`

4. PROCESS CLEANUP & LEARNING DIRECTIVE (CRITICAL):
   - Execute `/learn` to store ETA composite tax rules.
   - Terminate any running subagents, background dev servers, or processes before completing turn.
</ANTIGRAVITY_WORKFLOW>

<ACCEPTANCE_CRITERIA>
- [ ] Subagents delegated for ETA multi-tax structure analysis.
- [ ] `payload-builder.ts` maps all `taxLines` per item into `taxableItems` array.
- [ ] Summary `taxTotals` aggregates amounts by tax type (T1, T4, etc.).
- [ ] Canonical serialization and SHA-256 self-tests pass.
- [ ] Backend build completes with exit code 0.
- [ ] All subagents and background tasks cleanly terminated.
</ACCEPTANCE_CRITERIA>
```

---
### Developer Prompt 2: Clean Up Tax Module Registration Duality in `medusa-config.ts`

```markdown
/goal

<TASK>
Clean up the module registration duality in `apps/backend/medusa-config.ts:L100-L123` by cleanly separating the tax rate calculation provider (`@medusajs/medusa/tax`) from the standalone custom audit & HSM module (`eta-tax`), ensuring unified Medusa DI container bindings.
</TASK>

<SUBAGENT_DELEGATION_DIRECTIVE>
- Use `invoke_subagent` to inspect `medusa-config.ts` lines 90–130, `src/modules/eta-tax/index.ts`, and `src/modules/eta-tax/service.ts` to analyze the provider vs custom module exports.
</SUBAGENT_DELEGATION_DIRECTIVE>

<ANTIGRAVITY_SLASH_COMMANDS>
- /goal: Execute autonomously until ETA tax module registrations in medusa-config.ts are unified and DI container resolutions are crystal clear.
- /learn: Persist Medusa v2 provider vs standalone module registration patterns to .gemini/rules.
</ANTIGRAVITY_SLASH_COMMANDS>

<ANTIGRAVITY_WORKFLOW>
1. RESEARCH & INSPECTION PHASE:
   - View `apps/backend/medusa-config.ts` (lines 90–135).
   - View `apps/backend/src/modules/eta-tax/index.ts`.
   - Check where subscribers and workflows resolve `etaTax` vs `taxService`.

2. IMPLEMENTATION PHASE:
   - Target files: `apps/backend/medusa-config.ts`, `apps/backend/src/modules/eta-tax/index.ts`
   - **Unified Registration Architecture**:
     Ensure `eta-tax` is registered cleanly in `medusa-config.ts`:
     - Under `modules`: Register `resolve: "./src/modules/eta-tax"` as the primary custom module providing the DML models (`EtaReceiptAudit`), HSM proxy signer, and client services.
     - Under `tax` providers: If serving as a calculation provider, point `resolve: "./src/modules/eta-tax"` with provider options, or export the `AbstractTaxProvider` provider service cleanly from `src/modules/eta-tax/provider.ts`.
     - Standardize the container resolution key: `ETA_TAX_MODULE = "etaTax"` so `container.resolve("etaTax")` or `container.resolve(ETA_TAX_MODULE)` consistently retrieves the module service across all subscribers, workflows, and background workers.

3. EMPIRICAL VERIFICATION & TESTING PHASE:
   - Run TypeScript check: `cd apps/backend && npx tsc --noEmit`
   - Run backend build verification: `cd apps/backend && npm run build`

4. PROCESS CLEANUP & LEARNING DIRECTIVE (CRITICAL):
   - Execute `/learn` to store Medusa v2 module registration rules.
   - Terminate any running subagents, background dev servers, or processes before completing turn.
</ANTIGRAVITY_WORKFLOW>

<ACCEPTANCE_CRITERIA>
- [ ] Subagents delegated for module registration and DI resolution inspection.
- [ ] `medusa-config.ts` contains clean, non-conflicting registrations for `eta-tax`.
- [ ] `container.resolve("etaTax")` resolves cleanly in subscribers and workflows.
- [ ] Backend build completes with exit code 0.
- [ ] All subagents and background tasks cleanly terminated.
</ACCEPTANCE_CRITERIA>
```

---

## Part 2: Security Middleware & Storefront Cart Precision (Prompts 3–4)

---
### Developer Prompt 3: Create Central HTTP Security & Validation Middleware (`src/api/middlewares.ts`)

```markdown
/goal

<TASK>
Create `apps/backend/src/api/middlewares.ts` to attach global HTTP security headers (HSTS, CSP, X-Content-Type-Options, X-Frame-Options), dynamic CORS regex origin parsing for multi-tenant subdomains, and centralized Zod request body validation across custom routes.
</TASK>

<SUBAGENT_DELEGATION_DIRECTIVE>
- Use `invoke_subagent` to research Medusa v2 `defineMiddlewares` pattern from `@medusajs/medusa` or `@medusajs/framework/http`, and inspect custom routes in `apps/backend/src/api/`.
</SUBAGENT_DELEGATION_DIRECTIVE>

<ANTIGRAVITY_SLASH_COMMANDS>
- /goal: Execute autonomously until central security middlewares and Zod validation are active across all custom API routes.
- /learn: Persist Medusa v2 defineMiddlewares and security header rules to .gemini/rules.
</ANTIGRAVITY_SLASH_COMMANDS>

<ANTIGRAVITY_WORKFLOW>
1. RESEARCH & INSPECTION PHASE:
   - Check Medusa v2 middleware documentation and existing routes under `apps/backend/src/api/`.
   - Check `medusa-config.ts` CORS settings.

2. IMPLEMENTATION PHASE:
   - Target files: `apps/backend/src/api/middlewares.ts` (NEW), `apps/backend/medusa-config.ts`
   - **Create Central Middleware Definition** (`src/api/middlewares.ts`):
     ```typescript
     import { defineMiddlewares } from "@medusajs/medusa"
     import { MedusaRequest, MedusaResponse, MedusaNextFunction } from "@medusajs/framework/http"

     export function securityHeadersMiddleware(
       req: MedusaRequest,
       res: MedusaResponse,
       next: MedusaNextFunction
     ) {
       res.setHeader("X-Content-Type-Options", "nosniff")
       res.setHeader("X-Frame-Options", "DENY")
       res.setHeader("X-XSS-Protection", "1; mode=block")
       res.setHeader("Strict-Transport-Security", "max-age=31536000; includeSubDomains")
       res.setHeader(
         "Content-Security-Policy",
         "default-src 'self'; script-src 'self' https://accept.paymob.com; frame-src https://accept.paymob.com;"
       )
       next()
     }

     export default defineMiddlewares({
       routes: [
         {
           matcher: "/admin/*",
           middlewares: [securityHeadersMiddleware],
         },
         {
           matcher: "/store/*",
           middlewares: [securityHeadersMiddleware],
         },
         {
           matcher: "/hooks/*",
           middlewares: [securityHeadersMiddleware],
         },
       ],
     })
     ```
   - **Dynamic Tenant CORS Parsing** (`medusa-config.ts`):
     Enhance CORS handling so that in addition to fixed origins, wildcard tenant storefront subdomains (e.g., `https://*.storefront.eg`) are safely matched and authorized.

3. EMPIRICAL VERIFICATION & TESTING PHASE:
   - Run TypeScript check: `cd apps/backend && npx tsc --noEmit`
   - Run backend build verification: `cd apps/backend && npm run build`

4. PROCESS CLEANUP & LEARNING DIRECTIVE (CRITICAL):
   - Execute `/learn` to store central middleware rules.
   - Terminate any running subagents, background dev servers, or processes before completing turn.
</ANTIGRAVITY_WORKFLOW>

<ACCEPTANCE_CRITERIA>
- [ ] Subagents delegated for Medusa v2 `defineMiddlewares` pattern research.
- [ ] `src/api/middlewares.ts` created and exports `defineMiddlewares` with security headers.
- [ ] Security headers (HSTS, CSP, X-Frame-Options, X-Content-Type-Options) attached to all API routes.
- [ ] Backend build completes with exit code 0.
- [ ] All subagents and background tasks cleanly terminated.
</ACCEPTANCE_CRITERIA>
```

---
### Developer Prompt 4: Implement Dual `lineItemId` vs `variantId` Tracking in Storefront `cart-context.tsx`

```markdown
/goal

<TASK>
Update `apps/storefront/src/lib/context/cart-context.tsx:L204,L234` to track both `lineItemId` (Medusa's `item_01...` ID) and `variantId` in the client cart state, ensuring update and delete operations dispatch the exact line item ID expected by Medusa v2 (`DELETE /store/carts/:id/line-items/:line_id`).
</TASK>

<SUBAGENT_DELEGATION_DIRECTIVE>
- Use `invoke_subagent` to inspect `cart-context.tsx` lines 180–260 and verify Medusa v2 Store API cart line item mutation signatures.
</SUBAGENT_DELEGATION_DIRECTIVE>

<ANTIGRAVITY_SLASH_COMMANDS>
- /goal: Execute autonomously until storefront cart state tracks both lineItemId and variantId for 100% reliable cart item deletion and quantity updates.
- /learn: Persist Medusa v2 cart line item state management rules to .gemini/rules.
</ANTIGRAVITY_SLASH_COMMANDS>

<ANTIGRAVITY_WORKFLOW>
1. RESEARCH & INSPECTION PHASE:
   - View `apps/storefront/src/lib/context/cart-context.tsx` (cart line item types and update/delete methods).
   - Verify Medusa v2 Store API endpoints:
     - Add: `POST /store/carts/:id/line-items` (payload: `{ variant_id, quantity }`)
     - Update: `POST /store/carts/:id/line-items/:line_id` (payload: `{ quantity }`)
     - Delete: `DELETE /store/carts/:id/line-items/:line_id`

2. IMPLEMENTATION PHASE:
   - Target file: `apps/storefront/src/lib/context/cart-context.tsx`
   - **Dual ID State Representation**:
     Ensure each cart item interface explicitly defines:
     ```typescript
     export interface CartItem {
       id: string; // The Medusa line_item.id (e.g. "item_01...")
       variantId: string; // The product variant.id (e.g. "variant_01...")
       title: string;
       thumbnail?: string;
       quantity: number;
       unitPrice: number;
       // ...
     }
     ```
   - **Update `removeItem` and `updateQuantity`**:
     When calling `removeItem(lineItemId: string)` or `updateQuantity(lineItemId: string, quantity: number)`, ensure the request dispatches using the item's `id` (the line item ID), while lookup helpers can find items by either `id` or `variantId`.
   - Synchronize with `BroadcastChannel` payload serialization so multi-tab cart synchronization preserves both IDs across tabs.

3. EMPIRICAL VERIFICATION & TESTING PHASE:
   - Run storefront typecheck: `cd apps/storefront && npx tsc --noEmit`
   - Run storefront build: `cd apps/storefront && npm run build`

4. PROCESS CLEANUP & LEARNING DIRECTIVE (CRITICAL):
   - Execute `/learn` to store cart line item state rules.
   - Terminate any running subagents, background dev servers, or processes before completing turn.
</ANTIGRAVITY_WORKFLOW>

<ACCEPTANCE_CRITERIA>
- [ ] Subagents delegated for cart line item state inspection.
- [ ] Cart item state tracks both `id` (`lineItemId`) and `variantId`.
- [ ] `removeItem` and `updateQuantity` dispatch requests using the exact Medusa line item ID.
- [ ] BroadcastChannel multi-tab sync preserves both IDs.
- [ ] Storefront build completes with exit code 0.
- [ ] All subagents and background tasks cleanly terminated.
</ACCEPTANCE_CRITERIA>
```

---

## Part 3: Package Portability & Infrastructure Multi-Tenancy (Prompt 5)

---
### Developer Prompt 5: Standalone Shared-Types Build Configuration & Dynamic Tenant Container Naming in Docker Compose

```markdown
/goal

<TASK>
Make `packages/shared-types` standalone by adding `typescript` to `devDependencies` with `"build": "tsc"`, and parameterize container names in `infrastructure/docker/docker-compose.tenant.yml` with `${TENANT_ID}` to prevent multi-tenant name collisions.
</TASK>

<SUBAGENT_DELEGATION_DIRECTIVE>
- Use `invoke_subagent` to inspect `packages/shared-types/package.json` build scripts and `infrastructure/docker/docker-compose.tenant.yml` container naming.
</SUBAGENT_DELEGATION_DIRECTIVE>

<ANTIGRAVITY_SLASH_COMMANDS>
- /goal: Execute autonomously until shared-types builds independently with tsc and docker-compose parameterizes container names.
- /learn: Persist monorepo package isolation and Docker multi-tenant container naming rules to .gemini/rules.
</ANTIGRAVITY_SLASH_COMMANDS>

<ANTIGRAVITY_WORKFLOW>
1. RESEARCH & INSPECTION PHASE:
   - View `packages/shared-types/package.json` (lines 1–25).
   - View `infrastructure/docker/docker-compose.tenant.yml` (`container_name` directives).

2. IMPLEMENTATION PHASE:
   - Target files: `packages/shared-types/package.json`, `infrastructure/docker/docker-compose.tenant.yml`
   - **Standalone Shared-Types Build** (`packages/shared-types/package.json`):
     ```json
     {
       "name": "@dtc/shared-types",
       "version": "0.0.1",
       "main": "dist/index.js",
       "types": "dist/index.d.ts",
       "scripts": {
         "build": "tsc",
         "clean": "rimraf dist"
       },
       "devDependencies": {
         "typescript": "^5.6.3"
       }
     }
     ```
     *Rationale*: Replaces the brittle relative path (`"node ../../apps/storefront/node_modules/typescript/lib/tsc.js"`) with standard `tsc`, allowing `shared-types` to build cleanly in isolated Docker stages without requiring storefront files.

   - **Dynamic Tenant Container Naming** (`docker-compose.tenant.yml`):
     Parameterize all container names with `${TENANT_ID:-default}`:
     ```yaml
     services:
       postgres:
         container_name: medusa_postgres_${TENANT_ID:-default}
         ...
       redis:
         container_name: medusa_redis_${TENANT_ID:-default}
         ...
       backend:
         container_name: medusa_backend_${TENANT_ID:-default}
         ...
       storefront:
         container_name: medusa_storefront_${TENANT_ID:-default}
         ...
     ```
     *Rationale*: Allows multiple merchant tenant stacks to run concurrently on the same Docker host without container name collisions.

3. EMPIRICAL VERIFICATION & TESTING PHASE:
   - Run shared-types build: `npm run build --workspace=packages/shared-types`
   - Run backend typecheck & build: `cd apps/backend && npx tsc --noEmit && npm run build`
   - Run storefront typecheck & build: `cd apps/storefront && npx tsc --noEmit && npm run build`

4. PROCESS CLEANUP & LEARNING DIRECTIVE (CRITICAL):
   - Terminate any running subagents, background dev servers, or processes before completing turn.
</ANTIGRAVITY_WORKFLOW>

<ACCEPTANCE_CRITERIA>
- [ ] Subagents delegated for package.json and Docker compose inspection.
- [ ] `packages/shared-types/package.json` uses standard `"build": "tsc"` with `typescript` devDependency.
- [ ] `docker-compose.tenant.yml` parameterizes `container_name` with `${TENANT_ID:-default}`.
- [ ] All workspaces (`shared-types`, `apps/backend`, `apps/storefront`) pass typecheck and build with exit code 0.
- [ ] All subagents and background tasks cleanly terminated.
</ACCEPTANCE_CRITERIA>
```
