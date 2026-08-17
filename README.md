# Turnkey White-Label Commercial Transformation Prompt Pack (`PROMPT_SEQUENCE_STOREFRONT_TURNKEY_TRANSFORMATION.md`)

This prompt pack contains **3 sequentially executable master developer prompts** engineered for **Google Antigravity Agentic IDE** to systematically resolve all 62 assessed features and defects cataloged in the `STOREFRONT_COMPREHENSIVE_GAP_AUDIT_REPORT.md`, elevating the storefront from a **6.5/10.0 prototype to a 10.0/10.0 turnkey white-label e-commerce product**:

- **Prompt 1 (Phase 1 — Core Commerce, Variant Matrix & Critical CRO)**:
  1. Dynamic multi-attribute variant selector (Size, Color, Capacity, Material) on PDP with live price/SKU updates.
  2. Mobile sticky bottom "Add to Cart" floating bar with `IntersectionObserver`.
  3. Resolve missing 404 routes (`/shipping`, `/returns`, `/collections/[handle]`).
  4. Redesign `not-found.tsx` and `error.tsx` to match the warm luxury palette (`#FDFBF7`, `#0F4C5C`).
  5. Apply `unicodeBidi: "plaintext"` to all checkout and form inputs.

- **Prompt 2 (Phase 2 — Customer Auth, Social Proof & Retention Portal)**:
  1. Dedicated customer authentication pages (`/login`, `/register`, `/forgot-password`) connected to Medusa Auth SDK (`/store/auth`).
  2. Customer Reviews & 5-Star Social Proof Engine with aggregate scorecards, verified buyer badges, and photo review gallery.
  3. Interactive multi-address book management (Add/Edit/Delete, Default Shipping vs Billing).
  4. Visual 4-stage courier order tracking timeline (`/account/orders/[id]`).
  5. Self-service customer return & refund request workflow (`/account/returns`).

- **Prompt 3 (Phase 3 — Merchandising, Mega-Menu & SEO Expansion)**:
  1. Hierarchical Mega-Menu dropdown with multi-level nested categories and thumbnail banners.
  2. Mobile bottom navigation dock (Home, Categories, Search, Cart, Account).
  3. "Frequently Bought Together" & Bundle Discount engine on PDP.
  4. Dynamic `sitemap.ts`, `robots.ts`, OpenGraph social cards, and `BreadcrumbList` JSON-LD schemas.
  5. Full monorepo typecheck and production build validation (`tsc` & `next build`).

---

## 🚀 PROMPT 1: Core Commerce, Variant Matrix, Mobile Sticky Bar & Route Fixes (Phase 1)

```markdown
/goal

<TASK>
Execute Phase 1 of the Turnkey Commercial Transformation:
1. Multi-Attribute Variant Matrix: In `apps/storefront/src/app/[countryCode]/products/[handle]/page.tsx` and product components, dynamically parse all product options (Size, Color, Storage Capacity, Material, Volume) from the Medusa payload. Render interactive pill/swatch selectors with out-of-stock disabled states, dynamically updating the active price, SKU, and variant ID sent to the Add-to-Cart button.
2. Mobile Sticky Bottom "Add to Cart" Bar: Implement an `IntersectionObserver`-driven floating bottom dock on mobile viewports featuring product thumbnail, selected variant price, and full-width "أضف للسلة" button when the main CTA scrolls out of view.
3. Missing Sub-Pages: Create `src/app/[countryCode]/shipping/page.tsx`, `src/app/[countryCode]/returns/page.tsx`, and `src/app/[countryCode]/collections/[handle]/page.tsx`.
4. Theme Harmonization in Error Boundaries: Redesign `src/app/not-found.tsx` and `src/app/error.tsx` to use the warm luxury palette (`#FDFBF7`, `#0F4C5C`), wrapping them in proper headers and footers with 100% Arabic default copy.
5. BiDi Form Input Isolation: Apply `dir="auto"` and `style={{ unicodeBidi: "plaintext", textAlign: "start" }}` across all inputs in `checkout-view.tsx` and contact forms.
</TASK>

<SUBAGENT_DELEGATION_DIRECTIVE>
- Use `invoke_subagent` (Role: "PDP & Layout Specialist", TypeName: "research") to inspect `src/app/[countryCode]/products/[handle]/page.tsx`, `not-found.tsx`, `error.tsx`, and `checkout-view.tsx`.
</SUBAGENT_DELEGATION_DIRECTIVE>

<ANTIGRAVITY_SLASH_COMMANDS>
- /goal: Execute autonomously until variant selection is fully dynamic, mobile sticky bar operates smoothly, and all 404 routes are resolved.
- /learn: Persist multi-attribute variant matrix and mobile sticky CTA patterns to .gemini/rules.
</ANTIGRAVITY_SLASH_COMMANDS>

<ANTIGRAVITY_WORKFLOW>
1. RESEARCH & INSPECTION PHASE:
   - View `apps/storefront/src/app/[countryCode]/products/[handle]/page.tsx` (inspect variant handling).
   - View `apps/storefront/src/app/not-found.tsx` and `src/app/error.tsx` (inspect dark mode classes).
   - View `apps/storefront/src/modules/checkout/components/checkout-view.tsx` (check input fields).

2. IMPLEMENTATION PHASE:
   - **Dynamic Variant Selector Component** (`src/modules/products/components/product-variant-selector.tsx`):
     ```tsx
     // Dynamically groups options (e.g. Size: S/M/L, Color: Black/White)
     // Manages selectedOptions state Record<string, string>
     // Finds matching variant: product.variants.find(v => matchesAllOptions)
     // Passes resolved variantId, price, and inventory status to AddToCartButton
     ```
   - **Mobile Sticky CTA Bar** (`src/modules/products/components/mobile-sticky-bar.tsx`):
     ```tsx
     // Uses IntersectionObserver targeting the main PDP AddToCart button
     // Slides up smoothly from bottom on mobile viewports (< 768px)
     // Displays thumbnail, active variant price, and Quick-Add CTA
     ```
   - **Missing Sub-Page Routes**:
     - `src/app/[countryCode]/shipping/page.tsx`: Shipping policy detailing 27-governorate delivery times and Bosta tracking.
     - `src/app/[countryCode]/returns/page.tsx`: 14-day statutory return & replacement policy under Consumer Protection Law.
     - `src/app/[countryCode]/collections/[handle]/page.tsx`: Dynamic collection landing page filtering products by collection handle.
   - **Harmonize 404 & Error Pages** (`not-found.tsx`, `error.tsx`):
     - Replace dark slate styling with warm linen (`bg-[#FDFBF7]`), Nile Teal CTA (`bg-[#0F4C5C]`), and Arabic typography.
   - **BiDi Isolation**:
     - Add `style={{ unicodeBidi: "plaintext", textAlign: "start" }}` to address and phone inputs.

3. EMPIRICAL VERIFICATION:
   - Run `cd apps/storefront && npx tsc --noEmit`.
   - Run `cd apps/storefront && npm run build`.
   - Verify `/eg/shipping`, `/eg/returns`, and `/eg/collections/featured` return HTTP 200.

4. PROCESS CLEANUP:
   - Terminate any running subagents or processes before completing turn.
</ANTIGRAVITY_WORKFLOW>

<ACCEPTANCE_CRITERIA>
- [ ] Subagents delegated for PDP and route inspection.
- [ ] PDP dynamically renders option selectors (Size, Color, etc.) with real-time price & variant ID switching.
- [ ] Mobile sticky bottom Add-to-Cart bar triggers on viewport scroll.
- [ ] `/shipping`, `/returns`, and `/collections/[handle]` routes are live (zero 404s).
- [ ] `not-found.tsx` and `error.tsx` match the warm luxury palette.
- [ ] Storefront builds cleanly with exit code 0.
- [ ] All subagents cleanly terminated.
</ACCEPTANCE_CRITERIA>
```

---

## 🔐 PROMPT 2: Customer Auth, Social Proof & Retention Portal (Phase 2)

```markdown
/goal

<TASK>
Execute Phase 2 of the Turnkey Commercial Transformation:
1. Dedicated Customer Authentication Routes: Create `src/app/[countryCode]/login/page.tsx`, `src/app/[countryCode]/register/page.tsx`, and `src/app/[countryCode]/forgot-password/page.tsx` integrated with Medusa customer auth endpoints (`/store/auth/customer/emailpass` and `/store/customers`).
2. Customer Reviews & 5-Star Social Proof Engine: In PDP (`/products/[handle]`), build an aggregate review scorecard (e.g. 4.8/5.0 with rating breakdown bars), verified buyer badges (`مشتري موثق`), review filter tabs, photo gallery, and an interactive "أضف تقييمك" review submission modal.
3. Multi-Address Book Management: In `/account`, build an interactive address manager allowing customers to Add New Address, Edit, Delete, and toggle Default Shipping vs Default Billing address.
4. Visual Courier Tracking Timeline: In `/account/orders/[id]`, implement a 4-stage tracking visualizer (`تم استلام الطلب` -> `قيد التجهيز في المستودع` -> `في الطريق مع المندوب` -> `تم التوصيل بنجاح`) with tracking code copy and Bosta AWB status details.
5. Self-Service Returns Workflow: In `src/app/[countryCode]/account/returns/page.tsx`, build a step-by-step return request form (select delivered item, reason for return, photo upload, pickup date confirmation).
</TASK>

<SUBAGENT_DELEGATION_DIRECTIVE>
- Use `invoke_subagent` (Role: "Auth & Customer Portal Specialist", TypeName: "research") to inspect Medusa auth client methods, account views in `src/modules/account/`, and customer review schemas.
</SUBAGENT_DELEGATION_DIRECTIVE>

<ANTIGRAVITY_SLASH_COMMANDS>
- /goal: Execute autonomously until customer authentication, reviews, address book, and visual tracking are fully interactive.
- /learn: Persist Medusa customer session management and visual courier tracking timeline rules to .gemini/rules.
</ANTIGRAVITY_SLASH_COMMANDS>

<ANTIGRAVITY_WORKFLOW>
1. RESEARCH & INSPECTION PHASE:
   - View `apps/storefront/src/modules/account/components/account-view.tsx`.
   - Check Medusa Auth API routes in `apps/backend/src/api/`.

2. IMPLEMENTATION PHASE:
   - **Auth Pages** (`src/app/[countryCode]/login`, `/register`, `/forgot-password`):
     - High-conversion luxury login/register cards with password visibility toggle, Egyptian phone number field, and smooth redirect to `/account` on success.
   - **Customer Reviews Engine** (`src/modules/products/components/product-reviews.tsx`):
     - Renders rating summary (e.g. ★ 4.9 / 5.0 بناءً على 124 تقييم).
     - Breakdown progress bars for 5, 4, 3, 2, 1 stars.
     - Review cards with verified buyer badge (`مشتري موثق`), date, star rating, verified feedback, and user photos.
     - Interactive review modal with star selector and image upload.
   - **Address Book Manager** (`src/modules/account/components/address-book.tsx`):
     - Interactive grid of saved addresses with "تعيين كعنوان افتراضي", "تعديل", and "حذف" actions.
   - **Visual Courier Tracking Timeline** (`src/app/[countryCode]/account/orders/[id]/page.tsx`):
     - Animated 4-step progress line with icons, current step highlighted in Nile Teal, estimated delivery date, and live Bosta AWB reference.
   - **Self-Service Returns Portal** (`src/app/[countryCode]/account/returns/page.tsx`):
     - Return request generator allowing customers to request item returns within 14 days under Consumer Protection Law.

3. EMPIRICAL VERIFICATION:
   - Test navigating to `/eg/login`, `/eg/register`, `/eg/account/orders/ord_123`, and `/eg/account/returns`.
   - Verify review component renders cleanly on PDP.
   - Run `cd apps/storefront && npx tsc --noEmit && npm run build`.

4. PROCESS CLEANUP:
   - Terminate any running subagents or processes before completing turn.
</ANTIGRAVITY_WORKFLOW>

<ACCEPTANCE_CRITERIA>
- [ ] Subagents delegated for auth and customer portal inspection.
- [ ] Dedicated `/login`, `/register`, and `/forgot-password` pages are live and functional.
- [ ] PDP features rich 5-star customer reviews, verified badges, and review modal.
- [ ] Address book allows adding, editing, and deleting customer addresses.
- [ ] Order detail page features 4-stage visual courier tracking timeline.
- [ ] Storefront builds cleanly with exit code 0.
- [ ] All subagents cleanly terminated.
</ACCEPTANCE_CRITERIA>
```

---

## 🛍️ PROMPT 3: Merchandising, Mega-Menu, Mobile Dock & SEO Expansion (Phase 3)

```markdown
/goal

<TASK>
Execute Phase 3 of the Turnkey Commercial Transformation:
1. Hierarchical Mega-Menu Navigation: In `src/modules/layout/components/header.tsx`, build a multi-level luxury mega-menu with rich dropdown panels for main categories (أزياء, إلكترونيات, منزل وديكور, عطور), sub-categories, featured brands, and promotional thumbnail banners.
2. Mobile Bottom Navigation Dock: Build a sticky bottom navigation dock for mobile screens (`< 768px`) with 5 tactile action tabs: `الرئيسية` (Home), `التصنيفات` (Categories), `البحث` (Search), `السلة` (Cart with badge), and `حسابي` (Account).
3. "Frequently Bought Together" & Bundle Engine: In PDP (`/products/[handle]`), implement a bundle cross-sell card ("اشترِ معاً ووفر 10%") that lets users add the main product + 1 compatible accessory to cart in a single click with bundle discount calculation.
4. Dynamic SEO & SERP Expansion:
   - Create `src/app/sitemap.ts` dynamically generating URLs for all products, categories, and static pages.
   - Create `src/app/robots.ts` with standard crawler directives.
   - Embed Schema.org `BreadcrumbList` and root `WebSite` with `SearchAction` JSON-LD schemas in `src/app/[countryCode]/layout.tsx`.
   - Add dynamic OpenGraph and Twitter card metadata generators on all product pages.
5. Monorepo Build & Turnkey Verification: Run full TypeScript compilation and Next.js production builds across all workspaces.
</TASK>

<SUBAGENT_DELEGATION_DIRECTIVE>
- Use `invoke_subagent` (Role: "Merchandising & SEO Specialist", TypeName: "research") to inspect header mega-menu markup, mobile layout triggers, and Next.js 15 Metadata/Sitemap APIs.
</SUBAGENT_DELEGATION_DIRECTIVE>

<ANTIGRAVITY_SLASH_COMMANDS>
- /goal: Execute autonomously until mega-menu, mobile dock, bundle engine, and SEO automation are fully implemented.
- /learn: Persist Next.js 15 sitemap automation and mega-menu navigation standards to .gemini/rules.
</ANTIGRAVITY_SLASH_COMMANDS>

<ANTIGRAVITY_WORKFLOW>
1. RESEARCH & INSPECTION PHASE:
   - View `apps/storefront/src/modules/layout/components/header.tsx`.
   - View `apps/storefront/src/app/[countryCode]/layout.tsx`.

2. IMPLEMENTATION PHASE:
   - **Hierarchical Mega-Menu** (`src/modules/layout/components/mega-menu.tsx`):
     - Hover-activated animated dropdowns featuring sub-category lists, trending tags, and promotional hero banners with CTAs.
   - **Mobile Bottom Navigation Dock** (`src/modules/layout/components/mobile-nav-dock.tsx`):
     - Fixed `bottom-0 start-0 end-0 z-40` glassmorphic dock with active tab indicators and real-time cart badge pulse.
   - **Frequently Bought Together Bundle Engine** (`src/modules/products/components/product-bundle-upsell.tsx`):
     - Checkbox-driven bundle builder calculating combined bundle price and instant 10% bundle savings.
   - **Automated Sitemap & Robots** (`src/app/sitemap.ts` & `src/app/robots.ts`):
     - Generates valid XML sitemap of all active localized routes (`/eg`, `/en`, `/products`, `/collections`, etc.).
   - **SERP BreadcrumbList & WebSite Schema** (`src/app/[countryCode]/layout.tsx`):
     - Embeds Schema.org `BreadcrumbList` and `SearchAction` for Google rich snippets.

3. EMPIRICAL VERIFICATION & BUILD:
   - Shared Types: `cd packages/shared-types && npm run build`
   - Storefront Typecheck: `cd apps/storefront && npx tsc --noEmit`
   - Storefront Build: `cd apps/storefront && npm run build`
   - Verify `http://localhost:3000/sitemap.xml` and `http://localhost:3000/robots.txt` respond with valid schema.

4. PROCESS CLEANUP:
   - Terminate any running subagents or processes before completing turn.
</ANTIGRAVITY_WORKFLOW>

<ACCEPTANCE_CRITERIA>
- [ ] Subagents delegated for mega-menu and SEO inspection.
- [ ] Header features rich multi-level category mega-menu.
- [ ] Mobile bottom navigation dock is responsive and active on mobile viewports.
- [ ] PDP features interactive "Frequently Bought Together" bundle builder.
- [ ] `sitemap.xml` and `robots.txt` dynamically generated.
- [ ] Entire storefront passes typecheck and production build with exit code 0.
- [ ] All subagents cleanly terminated.
</ACCEPTANCE_CRITERIA>
```
