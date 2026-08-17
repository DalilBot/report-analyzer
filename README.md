# Consolidated QA Report Remediation Prompt Pack (`PROMPT_SEQUENCE_CONSOLIDATED_QA_REMEDIATION.md`)

This prompt pack contains **6 targeted developer prompts** engineered for **Google Antigravity Agentic IDE** to systematically resolve all findings and defects cataloged in the All-Phases Consolidated QA Report (P0 Blockers, P1 High Priority, and P2 UX/Friction), raising the system from **6.0/10.0 to 10.0/10.0 Production Readiness**:

- **Prompt 1 (P0 Core Checkout & Shipping Options)**: Seed Egypt shipping options (`so_bosta_standard`, `so_bosta_express`), initiate payment collection before `/complete`, and wire live Bosta pricing into checkout so orders can be placed.
- **Prompt 2 (P0/P1 Redis Resilience & In-Memory Fallbacks)**: Implement safe in-memory/mock fallback for BullMQ, idempotency locks, and cache stampede when Redis is offline (prevents 503 errors and unblocks local dev/CI).
- **Prompt 3 (P1 Rate Parity, Promotions & `/en` Locale)**: Fix Qalyubia (EG-04) rate parity (60 EGP), fix tax-inclusive discount base calculation, and fix `/en` route (dynamic `<html lang/dir>`, Inter font, English hero).
- **Prompt 4 (P1 Cart UX, Stepper, Deletion & Local Persistence)**: Add quantity stepper (+/-) and remove button to cart drawer, persist cart state to `localStorage` (reloads on `/checkout` don't wipe cart), and fix multi-tab race condition.
- **Prompt 5 (P1/P2 PDP Enhancements, ValU, Kiosk & Customer Auth)**: Implement ValU installment calculator, dual EGP pricing with discount badge, Kiosk/Aman bill reference in checkout UI, and customer login modal with guest cart merge.
- **Prompt 6 (Full Monorepo Build & E2E Validation)**: Comprehensive typecheck, build, and checkout order placement verification across all workspaces.

> [!IMPORTANT]
> **Subagent Directive**: Send these 6 prompts sequentially (Prompt 1 through Prompt 6) to your developer Antigravity instance. Every prompt explicitly instructs the agent to delegate research or sub-tasks to subagents (`invoke_subagent`).

---

## Part 1: Core Checkout, Shipping Options & Redis Resilience (Prompts 1–2)

---
### Developer Prompt 1: Seed Egypt Shipping Options, Wire Backend Payment Collection & Authoritative Bosta Pricing into Checkout

```markdown
/goal

<TASK>
Resolve the P0 Checkout Blocker:
1. Ensure the Egypt region (`reg_01KYH...` / `eg`) has active shipping options seeded (`so_bosta_standard`, `so_bosta_express`) in `apps/backend/src/scripts/seed-egypt-region.ts` and `initial-data-seed.ts`.
2. In `apps/storefront/src/modules/checkout/components/checkout-view.tsx`, ensure the checkout flow creates a payment collection (`POST /store/payment-collections`), selects the payment session, and adds the shipping method (`POST /store/carts/:id/shipping-methods`) before calling `POST /store/carts/:id/complete`.
3. Wire authoritative Bosta rate calculation from the backend into the checkout view rather than relying purely on client-side static tier approximations.
</TASK>

<SUBAGENT_DELEGATION_DIRECTIVE>
- Use `invoke_subagent` (Role: "Checkout & Fulfillment Specialist", TypeName: "research") to inspect `seed-egypt-region.ts`, `apps/storefront/src/modules/checkout/components/checkout-view.tsx`, and Medusa v2 Store API cart completion documentation.
</SUBAGENT_DELEGATION_DIRECTIVE>

<ANTIGRAVITY_SLASH_COMMANDS>
- /goal: Execute autonomously until checkout successfully places real orders with shipping methods and payment sessions.
- /learn: Persist Medusa v2 checkout payment collection and shipping method rules to .gemini/rules.
</ANTIGRAVITY_SLASH_COMMANDS>

<ANTIGRAVITY_WORKFLOW>
1. RESEARCH & INSPECTION PHASE:
   - View `apps/backend/src/scripts/seed-egypt-region.ts` (check shipping option creation).
   - View `apps/storefront/src/modules/checkout/components/checkout-view.tsx` (inspect why `/complete` fails with "Payment collection has not been initiated").

2. IMPLEMENTATION PHASE:
   - Target files: `apps/backend/src/scripts/seed-egypt-region.ts`, `apps/storefront/src/modules/checkout/components/checkout-view.tsx`
   - **Seed Shipping Options** (`seed-egypt-region.ts`):
     Ensure the seed script uses Medusa v2 `createShippingOptionsWorkflow` to attach Bosta Standard (`so_bosta_standard`) and Bosta Express (`so_bosta_express`) to the Egypt fulfillment set and service zone.
   - **Storefront Checkout Flow Alignment** (`checkout-view.tsx`):
     Update the submission handler:
     1. Add shipping address: `POST /store/carts/${cartId}` with `shipping_address`.
     2. Add shipping method: `POST /store/carts/${cartId}/shipping-methods` with `{ option_id: selectedShippingOptionId, data: { governorateId, weightKg } }`.
     3. Initialize payment collection: `POST /store/payment-collections` with `{ cart_id: cartId }`.
     4. Initialize payment session: `POST /store/payment-collections/${paymentCollectionId}/payment-sessions` with `{ provider_id: selectedPaymentProviderId }`.
     5. Complete cart: `POST /store/carts/${cartId}/complete`.
     6. Receive live order response (`order.id`, `order.display_id`) and render confirmation screen.

3. EMPIRICAL VERIFICATION & TESTING PHASE:
   - Run seed script: `cd apps/backend && npx medusa exec ./src/scripts/seed-egypt-region.ts`
   - Run storefront typecheck: `cd apps/storefront && npx tsc --noEmit`
   - Run storefront build: `cd apps/storefront && npm run build`

4. PROCESS CLEANUP & LEARNING DIRECTIVE (CRITICAL):
   - Terminate any running subagents, background dev servers, or processes before completing turn.
</ANTIGRAVITY_WORKFLOW>

<ACCEPTANCE_CRITERIA>
- [ ] Subagents delegated for seed script and checkout flow inspection.
- [ ] Egypt region has active Bosta shipping options linked to fulfillment sets.
- [ ] Checkout view initializes payment collection and shipping method before completion.
- [ ] Order placement completes without 400 "Payment collection not initiated" errors.
- [ ] Storefront build completes with exit code 0.
- [ ] All subagents and background tasks cleanly terminated.
</ACCEPTANCE_CRITERIA>
```

---
### Developer Prompt 2: Add Resilient In-Memory Fallbacks for Redis Outages (Queue, Webhook Lock & Mutex Stampede)

```markdown
/goal

<TASK>
Resolve the P0 Redis Dependency Blocker:
1. In `apps/backend/src/api/hooks/paymob/route.ts:L38`, when Redis is unreachable in development/staging (or when Redis is not running locally), allow the webhook idempotency lock to fall back to an in-memory LRU/Map lock instead of returning HTTP 503.
2. In `apps/backend/src/jobs/background-queue.ts`, add graceful in-memory processing fallback when Redis connection fails so `enqueueBackgroundJob` does not throw or fail silently in environments without local Redis.
3. In `apps/backend/src/modules/bosta/service.ts`, ensure `acquireLock` uses in-memory mutex fallback when Redis is absent.
</TASK>

<SUBAGENT_DELEGATION_DIRECTIVE>
- Use `invoke_subagent` to inspect `apps/backend/src/api/hooks/paymob/route.ts`, `apps/backend/src/jobs/background-queue.ts`, and `apps/backend/src/modules/bosta/service.ts`.
</SUBAGENT_DELEGATION_DIRECTIVE>

<ANTIGRAVITY_SLASH_COMMANDS>
- /goal: Execute autonomously until webhook idempotency, queue dispatch, and rate locking operate gracefully in standalone environments without Redis.
- /learn: Persist Redis graceful fallback and in-memory lock rules to .gemini/rules.
</ANTIGRAVITY_SLASH_COMMANDS>

<ANTIGRAVITY_WORKFLOW>
1. RESEARCH & INSPECTION PHASE:
   - View `apps/backend/src/api/hooks/paymob/route.ts` (lines 20–55).
   - View `apps/backend/src/jobs/background-queue.ts` (lines 40–90).
   - View `apps/backend/src/modules/bosta/service.ts` (lines 80–125).

2. IMPLEMENTATION PHASE:
   - **Webhook In-Memory Fallback** (`paymob/route.ts`):
     ```typescript
     // Memory fallback lock map:
     const memoryLockMap = new Map<string, number>();

     async function acquireIdempotencyLock(key: string, ttlSeconds: number, redisClient?: any): Promise<boolean> {
       if (redisClient && redisClient.status === "ready") {
         try {
           const result = await redisClient.set(key, "locked", "EX", ttlSeconds, "NX");
           return result === "OK";
         } catch (e) {
           console.warn("[PaymobWebhook] Redis lock failed, falling back to memory:", e);
         }
       }
       // In-memory fallback:
       const now = Date.now();
       const existingExpiry = memoryLockMap.get(key);
       if (existingExpiry && existingExpiry > now) return false;
       memoryLockMap.set(key, now + ttlSeconds * 1000);
       return true;
     }
     ```
     In production (`NODE_ENV === "production"`), keep strict fail-closed 503 semantics unless explicitly configured.

   - **Queue In-Memory Fallback** (`background-queue.ts`):
     When Redis is unreachable, process background jobs immediately in-process with `setImmediate()` rather than dropping them.

   - **Bosta Mutex In-Memory Fallback** (`bosta/service.ts`):
     Use a process-level `Map` for rate lock keys when `cacheService_` or Redis client is unavailable.

3. EMPIRICAL VERIFICATION & TESTING PHASE:
   - Run backend typecheck: `cd apps/backend && npx tsc --noEmit`
   - Run backend build verification: `cd apps/backend && npm run build`

4. PROCESS CLEANUP & LEARNING DIRECTIVE (CRITICAL):
   - Terminate any running subagents, background dev servers, or processes before completing turn.
</ANTIGRAVITY_WORKFLOW>

<ACCEPTANCE_CRITERIA>
- [ ] Subagents delegated for Redis fallback inspection.
- [ ] Paymob webhook processes successfully with in-memory lock when Redis is offline in dev/staging.
- [ ] Background queue runs in-process fallback when Redis is absent.
- [ ] Backend build completes with exit code 0.
- [ ] All subagents and background tasks cleanly terminated.
</ACCEPTANCE_CRITERIA>
```

---

## Part 2: Rate Parity, Promotions & Locale Fixes (Prompt 3)

---
### Developer Prompt 3: Fix Qalyubia (EG-04) Rate Parity, Tax-Inclusive Discount Calculation, & `/en` Locale Rendering

```markdown
/goal

<TASK>
Resolve P1 Defects:
1. Fix Qalyubia (EG-04) rate parity: Update `apps/backend/src/modules/bosta/rate-calculator.ts` so `EG-04` is in the Delta tier (**60 EGP**) matching `apps/storefront/src/lib/data/governorates.ts` (eliminating the 15 EGP rate mismatch).
2. Fix tax-inclusive discount base calculation in `apps/backend/src/modules/eta-tax/payload-builder.ts` and checkout display so discount values report on the tax-exclusive base.
3. Fix `/en` storefront route in `apps/storefront/src/app/layout.tsx`, `apps/storefront/src/app/[countryCode]/layout.tsx`, and `apps/storefront/src/modules/home/components/home-client-view.tsx` so `/en` dynamically sets `<html lang="en" dir="ltr">`, renders Inter font (`--font-inter`), and initializes English UI strings.
</TASK>

<SUBAGENT_DELEGATION_DIRECTIVE>
- Use `invoke_subagent` to inspect `rate-calculator.ts` lines 40–55, `governorates.ts`, `layout.tsx`, and `home-client-view.tsx` language initialization.
</SUBAGENT_DELEGATION_DIRECTIVE>

<ANTIGRAVITY_SLASH_COMMANDS>
- /goal: Execute autonomously until Qalyubia rates match 60 EGP, discounts calculate cleanly, and /en displays English LTR with Inter typography.
- /learn: Persist Egyptian shipping rate tiers and Next.js bilingual locale routing rules to .gemini/rules.
</ANTIGRAVITY_SLASH_COMMANDS>

<ANTIGRAVITY_WORKFLOW>
1. RESEARCH & INSPECTION PHASE:
   - View `apps/backend/src/modules/bosta/rate-calculator.ts` (check `GREATER_CAIRO_GOVS` array).
   - View `apps/storefront/src/app/layout.tsx` and `apps/storefront/src/app/[countryCode]/layout.tsx`.
   - View `apps/storefront/src/modules/home/components/home-client-view.tsx` (`lang` state).

2. IMPLEMENTATION PHASE:
   - **Qalyubia Rate Parity** (`rate-calculator.ts`):
     ```typescript
     // BEFORE:
     const GREATER_CAIRO_GOVS = ["EG-01", "EG-02", "EG-04"]; // Qalyubia was 45 EGP

     // AFTER:
     const GREATER_CAIRO_GOVS = ["EG-01", "EG-02"]; // Cairo & Giza: 45 EGP
     // EG-04 (Qalyubia) falls into DELTA_CANAL_GOVS: 60 EGP (100% parity with storefront)
     ```

   - **Dynamic `/en` Locale & Typography** (`layout.tsx` & `home-client-view.tsx`):
     In `apps/storefront/src/app/[countryCode]/layout.tsx`:
     Extract `countryCode` from `await params`. Compute `isRtl = countryCode === "eg" || countryCode === "ar"`.
     Pass `lang={isRtl ? "ar" : "en"}` and `dir={isRtl ? "rtl" : "ltr"}` to the root HTML or body wrapper.
     In `globals.css`: Apply `font-family: var(--font-inter)` when `[dir="ltr"]` and `font-family: var(--font-cairo)` when `[dir="rtl"]`.
     In `home-client-view.tsx`: Initialize `const [lang, setLang] = useState<"ar" | "en">(countryCode === "en" ? "en" : "ar")`.

3. EMPIRICAL VERIFICATION & TESTING PHASE:
   - Run backend typecheck: `cd apps/backend && npx tsc --noEmit`
   - Run storefront typecheck: `cd apps/storefront && npx tsc --noEmit`
   - Run storefront build: `cd apps/storefront && npm run build`

4. PROCESS CLEANUP & LEARNING DIRECTIVE (CRITICAL):
   - Terminate any running subagents, background dev servers, or processes before completing turn.
</ANTIGRAVITY_WORKFLOW>

<ACCEPTANCE_CRITERIA>
- [ ] Subagents delegated for rate tiers and layout locale inspection.
- [ ] Qalyubia (EG-04) returns 60 EGP in both backend rate calculator and storefront dropdown.
- [ ] Navigating to `/en` renders English text, `dir="ltr"`, and Inter font.
- [ ] Storefront build completes with exit code 0.
- [ ] All subagents and background tasks cleanly terminated.
</ACCEPTANCE_CRITERIA>
```

---

## Part 3: Storefront Cart UX, Deletion & Local Persistence (Prompt 4)

---
### Developer Prompt 4: Add Cart Quantity Stepper, Item Deletion, LocalStorage Persistence & Multi-Tab Conflict Safety

```markdown
/goal

<TASK>
Resolve P1 Cart & UX Gaps:
1. In `apps/storefront/src/modules/home/components/home-client-view.tsx` and cart drawer, implement interactive quantity steppers (`+` and `-` buttons) and an item removal button (`✕` or trash icon) using `updateQuantity` and `removeItem` from `CartProvider`.
2. In `apps/storefront/src/lib/context/cart-context.tsx`, persist the cart state (`items`) to `localStorage` (with fallback to React state) so a full page reload on `/eg/checkout` preserves items.
3. Enhance `BroadcastChannel` multi-tab synchronization with a timestamp/version check to prevent last-write-wins full-array overwrite races during simultaneous multi-tab edits.
</TASK>

<SUBAGENT_DELEGATION_DIRECTIVE>
- Use `invoke_subagent` (Role: "Cart & State Specialist", TypeName: "research") to inspect `cart-context.tsx` and the slide-over cart drawer markup in `home-client-view.tsx`.
</SUBAGENT_DELEGATION_DIRECTIVE>

<ANTIGRAVITY_SLASH_COMMANDS>
- /goal: Execute autonomously until cart drawer has working quantity steppers, item deletion, and cart survives browser refreshes.
- /learn: Persist cart local persistence and conflict-safe multi-tab sync rules to .gemini/rules.
</ANTIGRAVITY_SLASH_COMMANDS>

<ANTIGRAVITY_WORKFLOW>
1. RESEARCH & INSPECTION PHASE:
   - View `apps/storefront/src/lib/context/cart-context.tsx` (lines 50–160).
   - View `apps/storefront/src/modules/home/components/home-client-view.tsx` (cart drawer rendering).

2. IMPLEMENTATION PHASE:
   - Target files: `apps/storefront/src/lib/context/cart-context.tsx`, `apps/storefront/src/modules/home/components/home-client-view.tsx`
   - **Cart Drawer Stepper & Deletion UI** (`home-client-view.tsx`):
     In the cart drawer item list:
     ```tsx
     <div className="flex items-center gap-2 mt-2">
       <button
         onClick={() => updateQuantity(item.id, Math.max(1, item.quantity - 1))}
         className="w-6 h-6 rounded bg-neutral-200 hover:bg-neutral-300 dark:bg-neutral-700 flex items-center justify-center font-bold text-xs"
       >
         -
       </button>
       <span className="text-xs font-semibold px-2">{item.quantity}</span>
       <button
         onClick={() => updateQuantity(item.id, item.quantity + 1)}
         className="w-6 h-6 rounded bg-neutral-200 hover:bg-neutral-300 dark:bg-neutral-700 flex items-center justify-center font-bold text-xs"
       >
         +
       </button>
       <button
         onClick={() => removeItem(item.id)}
         className="text-red-500 hover:text-red-700 text-xs ms-auto flex items-center gap-1"
       >
         حذف
       </button>
     </div>
     ```

   - **LocalStorage Persistence** (`cart-context.tsx`):
     Initialize state from `localStorage.getItem("medusa_cart_items")` and save on every mutation.
     When navigating or refreshing `/eg/checkout`, restore cart items seamlessly.

   - **Conflict-Safe Multi-Tab Sync** (`cart-context.tsx`):
     Include `timestamp: Date.now()` in `BroadcastChannel` messages. Only accept updates if `message.timestamp > localLastUpdated`.

3. EMPIRICAL VERIFICATION & TESTING PHASE:
   - Run storefront typecheck: `cd apps/storefront && npx tsc --noEmit`
   - Run storefront build: `cd apps/storefront && npm run build`

4. PROCESS CLEANUP & LEARNING DIRECTIVE (CRITICAL):
   - Terminate any running subagents, background dev servers, or processes before completing turn.
</ANTIGRAVITY_WORKFLOW>

<ACCEPTANCE_CRITERIA>
- [ ] Subagents delegated for cart drawer and context state inspection.
- [ ] Cart drawer displays working `+`, `-`, and remove buttons for each item.
- [ ] Refreshing `/eg/checkout` preserves cart items from `localStorage`.
- [ ] BroadcastChannel multi-tab sync includes timestamp validation.
- [ ] Storefront build completes with exit code 0.
- [ ] All subagents and background tasks cleanly terminated.
</ACCEPTANCE_CRITERIA>
```

---

## Part 4: PDP Polish, ValU Widget, Kiosk UI & Customer Auth (Prompt 5)

---
### Developer Prompt 5: Add ValU Installment Calculator, Dual Pricing / Discount Badge, Kiosk UI, & Customer Login Modal with Cart Merge

```markdown
/goal

<TASK>
Resolve P1/P2 Storefront Features:
1. In `apps/storefront/src/app/[countryCode]/products/[handle]/page.tsx`, implement the **ValU Installment Calculator** widget (calculating 6/12/24/36 month installments starting from `price / 12` EGP/month), dual price display (original strikethrough vs discounted price with percentage badge), and product image thumbnail gallery.
2. In `apps/storefront/src/modules/checkout/components/checkout-view.tsx`, add the **Aman / Masary / Fawry Kiosk** payment option and render the generated `bill_reference` code on the success screen.
3. In `apps/storefront/src/modules/home/components/home-client-view.tsx`, implement category filter pills (الكل, إلكترونيات, أزياء, منزل, طعام) and a customer login modal that calls `mergeGuestCartOnLogin`.
</TASK>

<SUBAGENT_DELEGATION_DIRECTIVE>
- Use `invoke_subagent` to inspect product details page components, checkout view payment options, and category filtering in `home-client-view.tsx`.
</SUBAGENT_DELEGATION_DIRECTIVE>

<ANTIGRAVITY_SLASH_COMMANDS>
- /goal: Execute autonomously until PDP features ValU calculator, checkout shows Kiosk codes, and category pills filter live catalog.
- /learn: Persist ValU calculator formula and Kiosk payment UI rules to .gemini/rules.
</ANTIGRAVITY_SLASH_COMMANDS>

<ANTIGRAVITY_WORKFLOW>
1. RESEARCH & INSPECTION PHASE:
   - View `apps/storefront/src/app/[countryCode]/products/[handle]/page.tsx`.
   - View `apps/storefront/src/modules/checkout/components/checkout-view.tsx`.
   - View `apps/storefront/src/modules/home/components/home-client-view.tsx`.

2. IMPLEMENTATION PHASE:
   - **ValU Calculator & Dual Price** (`products/[handle]/page.tsx`):
     ```tsx
     // Dual Price:
     <div className="flex items-center gap-3 my-4">
       <span className="text-2xl font-bold text-emerald-600">{priceEgp} ج.م</span>
       {originalPriceEgp && (
         <>
           <span className="text-lg text-neutral-400 line-through">{originalPriceEgp} ج.م</span>
           <span className="bg-red-100 text-red-700 text-xs px-2 py-0.5 rounded-full font-bold">
             خصم {Math.round(((originalPriceEgp - priceEgp) / originalPriceEgp) * 100)}%
           </span>
         </>
       )}
     </div>

     // ValU Widget:
     <div className="bg-amber-50 dark:bg-amber-950/30 border border-amber-200 dark:border-amber-800 p-3 rounded-xl flex items-center gap-3 my-4">
       <div className="font-bold text-amber-600 text-sm">ڤاليو (ValU)</div>
       <div className="text-xs text-neutral-700 dark:text-neutral-300">
         قسط على 12 شهر بقسط شهري يبدأ من <strong className="text-amber-600">{Math.round(priceEgp / 12)} ج.م/شهر</strong>
       </div>
     </div>
     ```

   - **Kiosk / Aman Option** (`checkout-view.tsx`):
     Add radio option for Kiosk / Aman / Masary cash collection. When selected and order completes, display:
     `"رقم الدفع في أمان / مصاري / فوري: ${bill_reference || 'BILL-1002948'}"`.

   - **Category Filter Pills** (`home-client-view.tsx`):
     Wire the category pills to filter the live product list by `product.collection` or `category`.

3. EMPIRICAL VERIFICATION & TESTING PHASE:
   - Run storefront typecheck: `cd apps/storefront && npx tsc --noEmit`
   - Run storefront build: `cd apps/storefront && npm run build`

4. PROCESS CLEANUP & LEARNING DIRECTIVE (CRITICAL):
   - Terminate any running subagents, background dev servers, or processes before completing turn.
</ANTIGRAVITY_WORKFLOW>

<ACCEPTANCE_CRITERIA>
- [ ] Subagents delegated for PDP, checkout, and category UI inspection.
- [ ] PDP renders dual EGP prices, discount % badge, and ValU installment box.
- [ ] Checkout supports Kiosk payment and displays `bill_reference`.
- [ ] Category pills filter catalog on homepage.
- [ ] Storefront build completes with exit code 0.
- [ ] All subagents and background tasks cleanly terminated.
</ACCEPTANCE_CRITERIA>
```

---

## Part 5: Full Monorepo End-to-End Build & Validation (Prompt 6)

---
### Developer Prompt 6: Full Monorepo End-to-End Build & Order Placement Verification

```markdown
/goal

<TASK>
Execute full monorepo typechecks, builds, test suites, and order placement verifications across all packages (`@dtc/shared-types`, `apps/backend`, `apps/storefront`, `infrastructure/`) to empirically prove 100% Production Readiness.
</TASK>

<SUBAGENT_DELEGATION_DIRECTIVE>
- Use `invoke_subagent` (Role: "Build & Release Specialist", TypeName: "research") to run TypeScript checks and production builds in parallel across all packages.
</SUBAGENT_DELEGATION_DIRECTIVE>

<ANTIGRAVITY_SLASH_COMMANDS>
- /goal: Execute autonomously until all packages build cleanly with exit code 0 and order flow is fully verified.
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
   - Verify all P0, P1, and P2 defects from the consolidated report have zero regressions.

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
