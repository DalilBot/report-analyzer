# Master 42-Defect Forensic Remediation & 10.0 Production Readiness Prompt Pack (`PROMPT_SEQUENCE_42_DEFECTS_MASTER_REMEDIATION.md`)

This prompt pack contains **5 sequentially executable developer prompts** engineered for **Google Antigravity Agentic IDE** to systematically resolve all **42 forensic defects, 180+ rogue hex tokens, payment flow disconnections, and backend subscriber gaps** cataloged in the finalized forensic audit across `apps/storefront` and `apps/backend`:

- **Prompt 1 (Step 1 — Payment, Checkout & Paymob Gateway Remediation)**:
  - Create `/api/checkout/init-payment/route.ts` to create Medusa Payment Collections and initiate live Paymob payment sessions.
  - In `paymob-modal.tsx`, render real 3DS iframes (eliminate mock completion bypass button) and wire real Mobile Wallet OTP.
  - Eliminate synthetic Kiosk `REF-${orderId.slice(-8)}` and return authentic `bill_reference`.
  - In `/api/orders/create/route.ts`, map the customer's governorate to the live Bosta shipping option (eliminate blind `options[0].id`).
- **Prompt 2 (Step 2 — Cart, Promotions, Price Normalization & Context Sync)**:
  - Eliminate corrupting `rawPrice > 10000 ? rawPrice / 100 : rawPrice` heuristic in `cart-context.tsx`.
  - Store full synchronized `StoreCart` object in React Context, hydrating `subtotal`, `tax_total`, `discount_total`, and `total` from Medusa.
  - In `cart-template.tsx`, pass `cartId` to `validateStoreCouponAsync` to evaluate promotions via `POST /store/carts/:id/promotions`.
  - Eliminate hardcoded coupon dictionary in `promotions.ts`.
- **Prompt 3 (Step 3 — Dynamic Catalog, Categories, Reviews & Variant Matrix)**:
  - Add `fetchStorefrontCategories()` & `fetchStorefrontCollections()` in `products.ts` querying live Medusa APIs.
  - In `catalog-template.tsx` and `home-client-view.tsx`, filter by Medusa Category IDs (eliminate title regex substring matching).
  - In `product-variant-selector.tsx`, remove ghost Size pills (`S, M, L, XL`) when `options` is empty.
  - In `product-detail-view.tsx`, pass `productId={product.id}` to `ProductReviews` and persist reviews.
  - Remove duplicate `<Header>` and `<Footer>` wrappers in `collections/[handle]/page.tsx`.
- **Prompt 4 (Step 4 — Global 180+ Rogue Hex Purge, Subpages & Theme Decoupling)**:
  - Replace all 180+ hardcoded hex classes (`#0F4C5C`, `#C86D51`, `#0A5C36`, `#EDE8E1`, `#FDFBF7`) across all 42 files with canonical Tailwind theme tokens (`bg-primary`, `text-accent`, `bg-emerald`, `border-border`, `bg-surface-muted`).
  - Fix hero stats locale rendering (`{isRtl ? stat.valueAr : stat.valueEn}`) in `home-client-view.tsx`.
  - In `contact/page.tsx`, connect form to live `POST /api/contact` route.
  - Dynamically localize `not-found.tsx` and `error.tsx` (remove hardcoded RTL & Arabic strings).
  - Move announcement bar to `Header` or `[countryCode]/layout.tsx` for global visibility.
  - Wire `footer.tsx` to `siteConfig.footer.links` and move `MEGA_MENU_CATEGORIES` into `site-config.json`.
- **Prompt 5 (Step 5 — Backend Admin Sync, Event Subscribers & Build Sign-Off)**:
  - In `apps/backend/src/subscribers/product-revalidate.ts`, listen to Medusa product/inventory events and dispatch on-demand revalidation to `POST /api/revalidate?tag=products`.
  - Align `/api/orders/track/route.ts` response payload with `track-order/page.tsx` (`{ found: true, order: { ...order, steps, items } }`).
  - Execute full monorepo typecheck and Next.js production build verification across all packages with exit code 0.

---

## 💳 PROMPT 1: Payment, Checkout & Paymob Gateway Remediation (Step 1)

```markdown
/goal

<TASK>
Eliminate all payment, checkout, and shipping gaps (Defects #2, #3, #4, #5, #6, #7):
1. Create `apps/storefront/src/app/api/checkout/init-payment/route.ts` that receives `cartId` and `providerId`, initializes a Medusa Payment Collection (`POST /store/payment-collections`), initiates a Payment Session (`POST /store/payment-collections/:id/payment-sessions`), and returns `{ success: true, paymentSession, iframeUrl, clientSecret }`.
2. In `apps/storefront/src/modules/checkout/components/paymob-modal.tsx`:
   - Render the live Paymob 3DS Iframe using dynamic `iframeUrl` when available.
   - Delete the mock bypass button (`triggers onSuccess() immediately`).
   - For Mobile Wallets, integrate with the live Paymob Wallet API (`payWithWallet`) and handle OTP verification.
3. In `apps/storefront/src/modules/checkout/components/checkout-view.tsx`:
   - Call `/api/checkout/init-payment` upon selecting Paymob Card/Wallet/Kiosk to obtain the live session and iframeUrl before opening the modal.
   - Retrieve and display the authentic `bill_reference` code for `paymob_kiosk` (eliminate synthetic fallback `REF-${orderId.slice(-8)}`).
4. In `apps/storefront/src/app/api/orders/create/route.ts`:
   - Match the selected customer governorate with the corresponding Medusa shipping option ID (`so_bosta_...`) from `GET /store/shipping-options?cart_id=${activeCartId}` instead of blindly defaulting to `options[0].id`.
   - Complete the cart (`POST /store/carts/:id/complete`) only after confirmed payment authorization.
</TASK>

<SUBAGENT_DELEGATION_DIRECTIVE>
- Use `invoke_subagent` (Role: "Payment & Checkout Systems Lead", TypeName: "research") to inspect `src/modules/checkout/components/checkout-view.tsx`, `paymob-modal.tsx`, and `apps/storefront/src/app/api/orders/create/route.ts`.
</SUBAGENT_DELEGATION_DIRECTIVE>

<ANTIGRAVITY_SLASH_COMMANDS>
- /goal: Execute autonomously until live Paymob 3DS sessions, authentic Kiosk bill references, and dynamic Bosta shipping option matching are fully wired.
- /learn: Persist Medusa payment collection initialization and Paymob 3DS session lifecycle standards to .gemini/rules.
</ANTIGRAVITY_SLASH_COMMANDS>

<ANTIGRAVITY_WORKFLOW>
1. RESEARCH & INSPECTION PHASE:
   - View `apps/storefront/src/modules/checkout/components/checkout-view.tsx` (lines 300–320, 790–820).
   - View `apps/storefront/src/modules/checkout/components/paymob-modal.tsx` (lines 40–60, 170–200).
   - View `apps/storefront/src/app/api/orders/create/route.ts` (lines 145–210).

2. IMPLEMENTATION PHASE:
   - **Create Payment Init Route** (`api/checkout/init-payment/route.ts`):
     ```typescript
     import { NextRequest, NextResponse } from "next/server";
     export async function POST(req: NextRequest) {
       const { cartId, providerId } = await req.json();
       const backendUrl = process.env.NEXT_PUBLIC_MEDUSA_BACKEND_URL || "http://localhost:9000";
       const pubKey = process.env.NEXT_PUBLIC_MEDUSA_PUBLISHABLE_KEY || "";

       // 1. Create Payment Collection
       const pcRes = await fetch(`${backendUrl}/store/payment-collections`, {
         method: "POST",
         headers: { "Content-Type": "application/json", "x-publishable-key": pubKey },
         body: JSON.stringify({ cart_id: cartId }),
       });
       const { payment_collection } = await pcRes.json();

       // 2. Create Payment Session
       const psRes = await fetch(`${backendUrl}/store/payment-collections/${payment_collection.id}/payment-sessions`, {
         method: "POST",
         headers: { "Content-Type": "application/json", "x-publishable-key": pubKey },
         body: JSON.stringify({ provider_id: providerId }),
       });
       const { payment_session } = await psRes.json();
       return NextResponse.json({
         success: true,
         paymentCollectionId: payment_collection.id,
         paymentSessionId: payment_session.id,
         iframeUrl: payment_session.data?.iframe_url || payment_session.data?.payment_token ? `https://accept.paymob.com/api/acceptance/iframes/${process.env.NEXT_PUBLIC_PAYMOB_IFRAME_ID || "888888"}?payment_token=${payment_session.data.payment_token}` : undefined,
         billReference: payment_session.data?.bill_reference,
       });
     }
     ```
   - **Update `paymob-modal.tsx`**:
     Remove mock completion bypass button. Render authentic `iframe` with `src={iframeUrl}`. For wallet, call backend wallet charge endpoint and verify OTP.
   - **Update `checkout-view.tsx`**:
     Trigger `/api/checkout/init-payment` before popping `PaymobModal`. Use returned `billReference` for Kiosk payments.
   - **Dynamic Shipping Matching** (`api/orders/create/route.ts`):
     Query `/store/shipping-options?cart_id=${cartId}` and select option matching `governorateId` / tier.

3. EMPIRICAL VERIFICATION:
   - Run `cd apps/storefront && npx tsc --noEmit`.
   - Test checkout with Card -> Verify `/api/checkout/init-payment` creates payment session and returns live iframeUrl.
   - Test checkout with Kiosk -> Verify real `bill_reference` is returned (zero `REF-${Math.random()}`).

4. PROCESS CLEANUP:
   - Terminate any running subagents or processes before completing turn.
</ANTIGRAVITY_WORKFLOW>

<ACCEPTANCE_CRITERIA>
- [ ] Subagents delegated for payment init and checkout inspection.
- [ ] `/api/checkout/init-payment` creates Payment Collection and initiates Paymob session.
- [ ] `PaymobModal` renders live 3DS iframe without mock bypass buttons.
- [ ] Authentic `bill_reference` displayed for Paymob Kiosk.
- [ ] Governorate dynamically maps to corresponding Bosta shipping option.
- [ ] Storefront builds cleanly with exit code 0.
- [ ] All subagents cleanly terminated.
</ACCEPTANCE_CRITERIA>
```

---

## 🛒 PROMPT 2: Cart, Promotions, Price Normalization & Context Sync (Step 2)

```markdown
/goal

<TASK>
Eliminate cart calculation flaws, pricing heuristics, and promotion decoupling (Defects #8, #9, #10, #11, #12):
1. In `apps/storefront/src/lib/context/cart-context.tsx`:
   - Delete the flawed price heuristic `rawPrice > 10000 ? rawPrice / 100 : rawPrice` (lines 37–38). Standardize all price representations using Medusa v2 minor units / currency decimal definitions.
   - When creating a new cart (`sdk.store.cart.create`), pass `region_id` or `currency_code: "egp"`.
   - Store the complete, synchronized `StoreCart` object in React Context. Hydrate `subtotal`, `tax_total`, `discount_total`, and `total` directly from the Medusa Cart object after every cart mutation (lines 495–516).
2. In `apps/storefront/src/modules/cart/templates/cart-template.tsx`:
   - Pass the active `cartId` into `validateStoreCouponAsync(couponCode, totalEgp, cartId)` (line 78).
   - Apply promotions using Medusa's native `/store/carts/:id/promotions` workflow.
3. In `apps/storefront/src/lib/data/promotions.ts`:
   - Remove the hardcoded client coupon array fallback (`EGYPT10`, `SAVE10`, `MEDUSA10`) from `site-config.json`.
   - Delegate all promotion validation strictly to the Medusa Promotions Engine and surface authentic backend error messages.
</TASK>

<SUBAGENT_DELEGATION_DIRECTIVE>
- Use `invoke_subagent` (Role: "Cart & Promotions Engine Specialist", TypeName: "research") to inspect `src/lib/context/cart-context.tsx`, `src/modules/cart/templates/cart-template.tsx`, and `src/lib/data/promotions.ts`.
</SUBAGENT_DELEGATION_DIRECTIVE>

<ANTIGRAVITY_SLASH_COMMANDS>
- /goal: Execute autonomously until cart prices, subtotal/tax/discount calculations, and promotion validations are 100% hydrated from Medusa v2 APIs.
- /learn: Persist Medusa cart state synchronization and promotion validation rules to .gemini/rules.
</ANTIGRAVITY_SLASH_COMMANDS>

<ANTIGRAVITY_WORKFLOW>
1. RESEARCH & INSPECTION PHASE:
   - View `apps/storefront/src/lib/context/cart-context.tsx` (lines 30–60, 480–520).
   - View `apps/storefront/src/modules/cart/templates/cart-template.tsx` (lines 70–95).
   - View `apps/storefront/src/lib/data/promotions.ts`.

2. IMPLEMENTATION PHASE:
   - **Fix Cart Context Price Normalization** (`cart-context.tsx`):
     Remove `rawPrice > 10000 ? rawPrice / 100 : rawPrice`.
     Pass `currency_code: "egp"` to `sdk.store.cart.create`.
     Synchronize `cart` state from Medusa API response after `addLineItem`, `updateLineItem`, `deleteLineItem`.
   - **Cart Template Promotions** (`cart-template.tsx`):
     Update `handleApplyCoupon` to pass `cartId`.
     Call `POST /store/carts/${cartId}/promotions` with `{ promo_codes: [couponCode] }`.
   - **Promotions Data Layer** (`promotions.ts`):
     Remove hardcoded static coupon dictionary. Call Medusa promotion endpoints directly.

3. EMPIRICAL VERIFICATION:
   - Run `cd apps/storefront && npx tsc --noEmit`.
   - Test adding 2 items to cart -> Verify subtotal, 14% VAT, and total match Medusa Cart API totals.
   - Test applying promotion code `EGYPT10` -> Verify live Medusa discount calculation.

4. PROCESS CLEANUP:
   - Terminate any running subagents or processes before completing turn.
</ANTIGRAVITY_WORKFLOW>

<ACCEPTANCE_CRITERIA>
- [ ] Subagents delegated for cart and promotions inspection.
- [ ] Price division heuristic (`> 10000`) completely deleted.
- [ ] Full `StoreCart` object synchronized in React Context.
- [ ] Cart template passes `cartId` and binds promotions via Medusa Promotions API.
- [ ] Static coupon array removed from `promotions.ts`.
- [ ] Storefront builds cleanly with exit code 0.
- [ ] All subagents cleanly terminated.
</ACCEPTANCE_CRITERIA>
```

---

## 🛍️ PROMPT 3: Dynamic Catalog, Categories, Reviews & Variant Matrix (Step 3)

```markdown
/goal

<TASK>
Eliminate catalog mocks, keyword substring filtering heuristics, and ghost variant options (Defects #1, #13, #14, #15, #16, #17, #18, #19, #20, #21, #22, #24, #26, #27, #28, #37, #41):
1. In `apps/storefront/src/lib/data/products.ts`:
   - Implement `fetchStorefrontCategories()` and `fetchStorefrontCollections()` querying live Medusa `/store/product-categories` and `/store/collections`.
   - Ensure live Medusa `/store/products` is the primary source with `region_id` and `currency_code: "egp"`.
   - Remove fallback price `350 EGP` and fallback stock `25` (set `price: 0`, `inStock: false` if unpriced/unmanaged).
   - In `titleArMap`, retrieve Arabic titles dynamically from product `metadata.title_ar` or `subtitle`.
   - Fetch default region ID dynamically from `GET /store/regions` (remove hardcoded `DEFAULT_REGION_ID = "reg_01KYH..."`).
2. In `apps/storefront/src/modules/products/templates/catalog-template.tsx` and `apps/storefront/src/modules/home/components/home-client-view.tsx`:
   - Filter products by Medusa Category IDs (`product.categories.some(c => c.id === catId)`) or Collection handles instead of title keyword substring matching (`title.includes("قميص")`).
3. In `apps/storefront/src/modules/products/components/product-variant-selector.tsx`:
   - Remove fallback ghost sizes (`S, M, L, XL`) when `options` is empty. Render single Add-to-Cart CTA for unconfigurable products.
4. In `apps/storefront/src/modules/products/components/product-detail-view.tsx` and `product-reviews.tsx`:
   - Pass `productId={product.id}` to `<ProductReviews />`.
   - Connect reviews to a persistent reviews API route scoped by `productId`.
5. In `apps/storefront/src/app/[countryCode]/collections/[handle]/page.tsx`:
   - Query Medusa `/store/collections?handle=${handle}` and fetch products by `collection_id` (remove hardcoded `COLLECTIONS_MAP`).
   - Remove duplicate `<Header>` and `<Footer>` wrappers.
6. In `apps/storefront/src/modules/layout/components/mega-menu.tsx`:
   - Extract static 200-line `MEGA_MENU_CATEGORIES` into `site-config.json` under `megaMenu` and populate dynamically.
7. In `apps/storefront/src/modules/products/components/product-json-ld.tsx`:
   - Read brand name from `siteConfig.brand.name` and canonical URL from `siteConfig.seo.canonicalBaseUrl` (remove `https://egyptbrand.com`).
</TASK>

<SUBAGENT_DELEGATION_DIRECTIVE>
- Use `invoke_subagent` (Role: "Catalog & Merchandising Specialist", TypeName: "research") to inspect `src/lib/data/products.ts`, `catalog-template.tsx`, `product-variant-selector.tsx`, `collections/[handle]/page.tsx`, and `mega-menu.tsx`.
</SUBAGENT_DELEGATION_DIRECTIVE>

<ANTIGRAVITY_SLASH_COMMANDS>
- /goal: Execute autonomously until catalog, categories, collections, reviews, and mega-menu are dynamically driven by Medusa APIs and JSON config.
- /learn: Persist Medusa category filtering and dynamic collection page architecture to .gemini/rules.
</ANTIGRAVITY_SLASH_COMMANDS>

<ANTIGRAVITY_WORKFLOW>
1. RESEARCH & INSPECTION PHASE:
   - View `apps/storefront/src/lib/data/products.ts`.
   - View `apps/storefront/src/modules/products/templates/catalog-template.tsx`.
   - View `apps/storefront/src/app/[countryCode]/collections/[handle]/page.tsx`.
   - View `apps/storefront/src/modules/layout/components/mega-menu.tsx`.

2. IMPLEMENTATION PHASE:
   - **Dynamic Categories & Collections** (`products.ts`):
     Add `fetchStorefrontCategories` (`/store/product-categories`) and `fetchStorefrontCollections` (`/store/collections`).
     Remove hardcoded region ID, 350 EGP fallback, and 25 stock fallback.
   - **Category-ID Filtering** (`catalog-template.tsx` & `home-client-view.tsx`):
     Filter by `category_id` / `collection_id` instead of title string matching.
   - **Clean Variant Selector** (`product-variant-selector.tsx`):
     Remove ghost Size pills (`S, M, L, XL`).
   - **Reviews Product Scoping** (`product-detail-view.tsx`):
     Pass `productId={product.id}`.
   - **Fix Collection Page** (`collections/[handle]/page.tsx`):
     Query live collection by handle. Remove outer `<Header>` and `<Footer>`.
   - **Dynamic Mega-Menu** (`mega-menu.tsx` & `site-config.json`):
     Move schema to `site-config.json` under `megaMenu` and iterate dynamically.

3. EMPIRICAL VERIFICATION:
   - Run `cd apps/storefront && npx tsc --noEmit`.
   - Navigate to `/eg/collections/hoodies` -> Verify live collection products render without double headers.
   - Test category filtering in `/eg/products` -> Verify filtering uses Medusa category IDs.

4. PROCESS CLEANUP:
   - Terminate any running subagents or processes before completing turn.
</ANTIGRAVITY_WORKFLOW>

<ACCEPTANCE_CRITERIA>
- [ ] Subagents delegated for catalog, categories, and collection page inspection.
- [ ] Live categories and collections fetched from Medusa API.
- [ ] Title keyword substring filtering replaced with category ID matching.
- [ ] Ghost sizes removed from unconfigurable products.
- [ ] Duplicate Header/Footer removed from collection page.
- [ ] MegaMenu populated dynamically from `site-config.json`.
- [ ] Storefront builds cleanly with exit code 0.
- [ ] All subagents cleanly terminated.
</ACCEPTANCE_CRITERIA>
```

---

## 🎨 PROMPT 4: Global 180+ Rogue Hex Purge, Subpages & Theme Decoupling (Step 4)

```markdown
/goal

<TASK>
Eliminate all 180+ rogue hardcoded hex classes, fix subpages, and decouple theme/i18n tokens (Defects #23, #25, #36, #38, #39, #40, #42, Section 3.1 & 3.2):
1. In `apps/storefront/src/app/globals.css`, register all color variables inside `@theme inline`:
   ```css
   @theme inline {
     --color-background: var(--background);
     --color-foreground: var(--foreground);
     --color-primary: var(--primary);
     --color-primary-hover: var(--primary-hover);
     --color-primary-light: var(--primary-light, #E8F1F3);
     --color-accent: var(--accent);
     --color-accent-hover: var(--accent-hover);
     --color-accent-light: var(--accent-light, #FAF0EC);
     --color-emerald: var(--emerald);
     --color-emerald-light: var(--emerald-light, #E7F4ED);
     --color-amber: var(--amber);
     --color-surface: var(--surface);
     --color-surface-muted: var(--surface-muted);
     --color-surface-elevated: var(--surface-elevated);
     --color-border: var(--border);
     --color-border-muted: var(--border-muted);
     --color-text-primary: var(--text-primary);
     --color-text-secondary: var(--text-secondary);
     --color-text-muted: var(--text-muted);
   }
   ```
2. Refactor all 180+ hardcoded hex occurrences across all 42 storefront files and subpages (`about`, `contact`, `faq`, `privacy`, `returns`, `shipping`, `terms`, `wishlist`, `not-found`, `error`, `header`, `footer`, `cart-drawer`, `checkout-view`, `home-client-view`):
   - Replace `#0F4C5C` -> `primary` (`bg-primary`, `text-primary`, `border-primary`)
   - Replace `#0C3C49` -> `primary-hover` (`bg-primary-hover`)
   - Replace `#C86D51` -> `accent` (`bg-accent`, `text-accent`)
   - Replace `#FAF0EC` -> `accent-light` (`bg-accent-light`)
   - Replace `#0A5C36` -> `emerald` (`bg-emerald`, `text-emerald`)
   - Replace `#EDE8E1` / `#E8E2D8` -> `border` (`border-border`)
   - Replace `#FDFBF7` / `#FAF8F5` -> `surface-muted` / `surface-elevated`
   - Replace `#1A202C` / `#718096` -> `text-primary` / `text-muted`
3. In `apps/storefront/src/modules/home/components/home-client-view.tsx`:
   - Fix hero stats locale bug: `{isRtl ? stat.valueAr : stat.valueEn}` and `{isRtl ? stat.labelAr : stat.labelEn}` (lines 213–216).
   - Remove dummy login item `prod_saved_fav`.
4. In `apps/storefront/src/app/[countryCode]/contact/page.tsx`:
   - Create `apps/storefront/src/app/api/contact/route.ts` and connect the contact form to dispatch real inquiries (eliminate `setTimeout(800)` simulation).
5. In `apps/storefront/src/app/not-found.tsx` and `apps/storefront/src/app/error.tsx`:
   - Dynamically bind locale direction (`dir="rtl"` vs `dir="ltr"`) and localized strings (eliminate hardcoded Arabic-only UI).
6. In `apps/storefront/src/modules/layout/components/footer.tsx`:
   - Dynamically iterate over `siteConfig.footer.links.about`, `customerCare`, and `legal`.
7. In `apps/storefront/src/modules/layout/components/header.tsx` or `[countryCode]/layout.tsx`:
   - Render the announcement bar globally across all pages.
</TASK>

<SUBAGENT_DELEGATION_DIRECTIVE>
- Use `invoke_subagent` (Role: "Design System & Theme Lead", TypeName: "research") to inspect `globals.css`, `home-client-view.tsx`, `contact/page.tsx`, `not-found.tsx`, `error.tsx`, and `footer.tsx`.
</SUBAGENT_DELEGATION_DIRECTIVE>

<ANTIGRAVITY_SLASH_COMMANDS>
- /goal: Execute autonomously until all 180+ rogue hexes are refactored to theme tokens, subpages are fully wired, and locale/footer/announcement bars are decoupled.
- /learn: Persist design system token refactoring and dynamic footer rendering rules to .gemini/rules.
</ANTIGRAVITY_SLASH_COMMANDS>

<ANTIGRAVITY_WORKFLOW>
1. RESEARCH & INSPECTION PHASE:
   - View `apps/storefront/src/app/globals.css`.
   - View `apps/storefront/src/modules/home/components/home-client-view.tsx`.
   - View `apps/storefront/src/app/[countryCode]/contact/page.tsx`.
   - View `apps/storefront/src/app/not-found.tsx` and `src/app/error.tsx`.

2. IMPLEMENTATION PHASE:
   - **Update `globals.css` `@theme inline`**: Register all canonical theme color variables.
   - **Global Hex Refactor**: Replace all 180+ occurrences of hardcoded hexes with semantic Tailwind classes across all 42 files.
   - **Fix Stats Locale** (`home-client-view.tsx`): Render localized `value` and `label`. Remove `prod_saved_fav`.
   - **Live Contact Form** (`contact/page.tsx` & `api/contact/route.ts`): Create API route and submit real form data.
   - **Dynamic 404 & Error** (`not-found.tsx`, `error.tsx`): Bind to active locale dictionary and use theme tokens.
   - **Dynamic Footer & Global Announcement**: Map `footer.tsx` to `siteConfig.footer.links`. Render announcement bar in `Header`.

3. EMPIRICAL VERIFICATION:
   - Run `cd apps/storefront && npx tsc --noEmit`.
   - Verify changing `primary` color in `site-config.json` updates all buttons across home, catalog, PDP, and checkout without CSS edits.
   - Test `/en` on homepage -> Verify hero stats render in English.
   - Run `cd apps/storefront && npm run build`.

4. PROCESS CLEANUP:
   - Terminate any running subagents or processes before completing turn.
</ANTIGRAVITY_WORKFLOW>

<ACCEPTANCE_CRITERIA>
- [ ] Subagents delegated for theme refactor and subpage inspection.
- [ ] All 180+ rogue hardcoded hex occurrences refactored to semantic Tailwind theme classes.
- [ ] Hero stats render correctly in both Arabic (`/eg`) and English (`/en`).
- [ ] Contact form dispatches to live `POST /api/contact`.
- [ ] 404 and Error pages dynamically localized and styled with theme tokens.
- [ ] Footer renders dynamically from `siteConfig.footer.links`.
- [ ] Storefront builds cleanly with exit code 0.
- [ ] All subagents cleanly terminated.
</ACCEPTANCE_CRITERIA>
```

---

## 🚀 PROMPT 5: Backend Admin Sync, Event Subscribers & Build Sign-Off (Step 5)

```markdown
/goal

<TASK>
Eliminate backend sync gaps and execute full monorepo production build verification (Defects #29, #30, #31, #32, #33, #34, #35, Section 4.1 & 4.2):
1. In `apps/backend/src/subscribers/product-revalidate.ts`:
   - Create a Medusa event subscriber listening to `product.created`, `product.updated`, `product.deleted`, `product-variant.created`, `product-variant.updated`, and `inventory-level.updated`.
   - Dispatch an on-demand revalidation request to `${storefrontUrl}/api/revalidate?tag=products` with `x-revalidate-secret` to immediately update storefront ISR cached data upon admin changes.
2. In `apps/storefront/src/app/api/orders/track/route.ts`:
   - Return `{ found: true, order: { ...order, steps, items } }` matching the data contract expected by `apps/storefront/src/app/[countryCode]/track-order/page.tsx` (lines 54, 230).
3. In `apps/storefront/src/app/api/auth/customer/route.ts`:
   - In `POST` (register), return explicit HTTP 400 if Medusa registration fails (eliminate fake `cust_tok_*`).
   - In `GET`, verify the JWT token against `GET ${backendUrl}/store/customers/me` before returning customer session.
4. In `apps/storefront/src/app/api/customer/orders/route.ts` and `apps/storefront/src/app/api/customer/returns/route.ts`:
   - Query orders strictly from Medusa `/store/orders` using customer JWT (eliminate cookie fallback).
   - Wire customer returns to Medusa return workflow (`POST /store/returns`).
5. In `apps/storefront/src/modules/account/components/address-book.tsx`:
   - Remove masked empty `catch {}` blocks. Surface toast errors on failure and mutate state only on HTTP 200 OK from Medusa DB.
6. Execute full monorepo typecheck and production build verification across all workspaces (`@dtc/shared-types`, `apps/backend`, `apps/storefront`).
</TASK>

<SUBAGENT_DELEGATION_DIRECTIVE>
- Use `invoke_subagent` (Role: "Backend Sync & Release Specialist", TypeName: "research") to inspect `apps/backend/src/subscribers/`, `src/app/api/orders/track/route.ts`, and `src/app/api/auth/customer/route.ts`.
</SUBAGENT_DELEGATION_DIRECTIVE>

<ANTIGRAVITY_SLASH_COMMANDS>
- /goal: Execute autonomously until backend revalidation subscribers are active, tracking contracts match, customer auth is verified, and all workspaces pass production builds with exit code 0.
</ANTIGRAVITY_SLASH_COMMANDS>

<ANTIGRAVITY_WORKFLOW>
1. IMPLEMENTATION PHASE:
   - **Create Revalidation Subscriber** (`apps/backend/src/subscribers/product-revalidate.ts`):
     ```typescript
     import { SubscriberArgs, SubscriberConfig } from "@medusajs/medusa";

     export default async function productRevalidateHandler({ event, container }: SubscriberArgs<any>) {
       const storefrontUrl = process.env.STOREFRONT_URL || "http://localhost:3000";
       const revalidateSecret = process.env.REVALIDATE_SECRET || "supersecret_revalidate_token";
       try {
         await fetch(`${storefrontUrl}/api/revalidate?tag=products`, {
           method: "POST",
           headers: { "x-revalidate-secret": revalidateSecret },
         });
       } catch (err) {
         console.warn("[Subscriber] Storefront revalidation failed:", err);
       }
     }

     export const config: SubscriberConfig = {
       event: [
         "product.created",
         "product.updated",
         "product.deleted",
         "product-variant.updated",
         "inventory-level.updated",
       ],
     };
     ```
   - **Align Tracking API Payload** (`api/orders/track/route.ts`):
     Format response to return `{ found: true, order: { id, display_id, status, fulfillment_status, steps: generateTrackingSteps(order), items: order.items } }`.
   - **Strict Customer Auth Verification** (`api/auth/customer/route.ts`):
     Verify JWT with `/store/customers/me` on `GET`. Return 400 on register failure.
   - **Live Address & Return Workflows** (`address-book.tsx`, `api/customer/returns/route.ts`):
     Surface live toast errors on address CRUD failures. Wire returns to Medusa return workflow.

2. FULL MONOREPO VERIFICATION:
   - Shared Types Build: `cd packages/shared-types && npm run build`
   - Backend Typecheck: `cd apps/backend && npx tsc --noEmit`
   - Backend Build: `cd apps/backend && npm run build`
   - Storefront Typecheck: `cd apps/storefront && npx tsc --noEmit`
   - Storefront Production Build: `cd apps/storefront && npm run build`

3. PROCESS CLEANUP:
   - Terminate any running subagents or processes before completing turn.
</ANTIGRAVITY_WORKFLOW>

<ACCEPTANCE_CRITERIA>
- [ ] Subagents delegated for backend subscriber and auth verification.
- [ ] `product-revalidate.ts` subscriber dispatches on-demand ISR revalidation on product/stock updates.
- [ ] `/api/orders/track` payload aligns with `track-order/page.tsx` schema.
- [ ] Customer JWT verified against `/store/customers/me`.
- [ ] Address book surfaces real backend errors and mutates only on DB success.
- [ ] All workspaces (`shared-types`, `backend`, `storefront`) compile and build cleanly with exit code 0.
- [ ] All 42 cataloged forensic defects resolved.
- [ ] All subagents cleanly terminated.
</ACCEPTANCE_CRITERIA>
```
