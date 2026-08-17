# 🏛️ ULTIMATE MASTER DEVELOPER EXECUTION SUITE (`FINAL_MASTER_DEVELOPER_EXECUTION_SUITE.md`)

This is the **complete, unified, copy-pasteable execution prompt sequence** for your developer agent in Google Antigravity. It merges:
1. **The Definitive Backend & Checkout Fixes** (P0 order completion, seed shipping options, tax-exclusive discount math).
2. **The 100% Arabic-First Luxury UI & Jargon Purge** (Zero English default, zero developer text like `(Paymob/Bosta)`).
3. **The Granular Dynamic Animations Engine** (Full JSON customizability of speeds, easings, and transitions for every component).
4. **The Ranked Multi-Armed Bandits (R-MAB) + NLP Semantic Search Engine** (Stemming, Egyptian colloquial synonyms, typo tolerance, Thompson Sampling learning-to-rank).

---

## 📋 Execution Roadmap (4 Sequential Phases)

| Phase | Focus Area | Technical Scope | Target Deliverables |
| :--- | :--- | :--- | :--- |
| **Phase 1** | **Backend Core, Seed & Checkout Wiring** | Link shipping options to Egypt service zone, initiate payment collections, fix discount base math | Real orders succeed end-to-end, zero 400 errors |
| **Phase 2** | **Ranked Bandits (R-MAB) & NLP AI Search** | Plural stemming (`shirts` ↔ `shirt`), Egyptian dialect graph (`كوتشي`), Thompson Sampling R-MAB ranking | Instant intelligent search with zero dead ends |
| **Phase 3** | **Luxury UI, 100% Arabic Default & Jargon Purge** | Porcelain/Nile Teal/Emerald palette, purge all `(Paymob/Bosta)`, 100% Arabic defaults everywhere | Luxury aesthetic, zero English letters by default |
| **Phase 4** | **Configurable Dynamic Animation Engine & Final Build** | `site-config.json` motion engine, hover scale, cart drawer slide, and monorepo build sign-off | Fluid 60fps micro-animations, 100% clean builds |

---

# 🚀 PHASE 1: Backend Core, Seed & Checkout Wiring

```markdown
/goal

# TASK: Fix Egypt Shipping Options, Checkout Payment Collection & Promotions Discount Math

Resolve the last remaining backend and order placement blockers:
1. In `apps/backend/src/scripts/seed-egypt-region.ts`, ensure that the fulfillment set and service zone covering Egypt (`countries: ["eg"]`) are properly created, linked to the stock location and the Default Sales Channel, and that the 2 shipping options (`Bosta Standard Delivery` and `Bosta Express Delivery`) are created inside this service zone with valid EGP prices (`amount: 4500` / `amount: 6000`) so `GET /store/shipping-options?cart_id=:id` returns both options for any cart created in the Egypt region (`reg_01KYH...`).
2. In `apps/storefront/src/modules/checkout/components/checkout-view.tsx`, update the checkout submission sequence before calling `/store/carts/:id/complete`:
   - Step A: Add shipping method: `POST /store/carts/${cart.id}/shipping-methods` with `{ option_id: selectedShippingOptionId }`.
   - Step B: Create payment collection: `POST /store/payment-collections` with `{ cart_id: cart.id }`.
   - Step C: Create payment session: `POST /store/payment-collections/${paymentCollectionId}/payment-sessions` with `{ provider_id: selectedPaymentProviderId || "pp_system_default" }`.
   - Step D: Complete cart: `POST /store/carts/${cart.id}/complete`.
3. In `apps/backend/src/modules/eta-tax/payload-builder.ts` and checkout display, ensure percentage discounts (e.g. `EGYPT10` 10% off) calculate and report against the **tax-exclusive subtotal base** (e.g., subtotal 51800 piastres -> 10% discount = **5180 piastres / 51.80 EGP**, instead of the tax-inflated 5905.2 piastres).

<SUBAGENT_DELEGATION_DIRECTIVE>
- Use `invoke_subagent` to inspect `seed-egypt-region.ts`, `checkout-view.tsx`, and `payload-builder.ts` before editing.
</SUBAGENT_DELEGATION_DIRECTIVE>

<ANTIGRAVITY_SLASH_COMMANDS>
- /goal: Execute autonomously until live order placement succeeds end-to-end and discount calculation is exact.
- /learn: Persist Medusa v2 fulfillment service zone and tax-exclusive discount rules to .gemini/rules.
</ANTIGRAVITY_SLASH_COMMANDS>

<ANTIGRAVITY_WORKFLOW>
1. RESEARCH & INSPECTION:
   - View `apps/backend/src/scripts/seed-egypt-region.ts`.
   - View `apps/storefront/src/modules/checkout/components/checkout-view.tsx`.
   - View `apps/backend/src/modules/eta-tax/payload-builder.ts`.

2. IMPLEMENTATION:
   - Update `seed-egypt-region.ts` using `createLocationFulfillmentSetWorkflow`, `createServiceZonesWorkflow`, and `createShippingOptionsWorkflow`.
   - Update `checkout-view.tsx` to sequentialize shipping method addition -> payment collection -> payment session -> cart complete.
   - Fix discount calculation in `payload-builder.ts` to compute against net subtotal before VAT.

3. EMPIRICAL VERIFICATION:
   - Run seed script: `cd apps/backend && npx medusa exec ./src/scripts/seed-egypt-region.ts`
   - Run typecheck: `cd apps/backend && npx tsc --noEmit`
   - Run storefront build: `cd apps/storefront && npm run build`
   - Confirm order placement completes with HTTP 200 and live `order.id`.

4. PROCESS CLEANUP:
   - Terminate any running subagents, background dev servers, or processes before completing turn.
</ANTIGRAVITY_WORKFLOW>

<ACCEPTANCE_CRITERIA>
- [ ] Egypt service zone covers `countries: ["eg"]` and is linked to the Default Sales Channel.
- [ ] `GET /store/shipping-options?cart_id=:id` returns Bosta shipping options.
- [ ] Checkout initializes payment collection and payment session before `/complete`.
- [ ] Order placement completes cleanly emitting a real `order.id`.
- [ ] 10% discount on 51800 subtotal reports exactly 5180 piastres.
- [ ] All subagents and background tasks cleanly terminated.
</ACCEPTANCE_CRITERIA>
```

---

# 🧠 PHASE 2: Ranked Multi-Armed Bandits (R-MAB) & NLP Semantic Search

```markdown
/goal

# TASK: Implement Ranked Multi-Armed Bandits (R-MAB) + NLP Morphological Search Engine

Replace the rigid `.includes()` search in `apps/storefront/src/modules/search/components/smart-search-bar.tsx` with an industry-grade **Two-Stage Intelligent Search Engine**:
- **Stage 1 (High-Recall Candidate Retrieval)**:
  - English & Arabic Stemming: `shirts` ↔ `shirt`, `t-shirt` ↔ `تيشيرت`, `watches` ↔ `ساعة`, `hoodies` ↔ `هودي`.
  - Egyptian Dialect & Colloquial Synonyms: `كوتشي` / `شوز` ↔ `shoes`, `شيميز` / `فانلة` ↔ `shirt`, `برفان` / `عود` ↔ `perfume`.
  - Damerau-Levenshtein Typo Distance $\le 2$: `shrt` -> `shirt`, `تيشرط` -> `تيشرت`.
- **Stage 2 (Learning-to-Rank via Ranked Multi-Armed Bandits - R-MAB)**:
  - Implement **Thompson Sampling with Beta Distribution** $\text{Beta}(\alpha_{\text{clicks}} + 1, \beta_{\text{impressions}} - \alpha_{\text{clicks}} + 1)$ to re-rank search results dynamically based on user click conversions and position discounting.
  - Add instant click telemetry recording into local bandit state.

<SUBAGENT_DELEGATION_DIRECTIVE>
- Use `invoke_subagent` to research Thompson Sampling Beta draw algorithms, Arabic morphological normalization, and Levenshtein distance matching.
</SUBAGENT_DELEGATION_DIRECTIVE>

<ANTIGRAVITY_SLASH_COMMANDS>
- /goal: Execute autonomously until searching "shirts", "كوتشي", or "shrt" returns accurate, bandit-ranked products.
- /learn: Persist Ranked Multi-Armed Bandits (R-MAB) and NLP search rules to .gemini/rules.
</ANTIGRAVITY_SLASH_COMMANDS>

<ANTIGRAVITY_WORKFLOW>
1. RESEARCH & INSPECTION:
   - View `apps/storefront/src/modules/search/components/smart-search-bar.tsx` (lines 85–115).

2. IMPLEMENTATION:
   - **Create NLP Stemmer & Synonym Graph** (`apps/storefront/src/lib/search/nlp-stemmer.ts`):
     Include bilingual synonym maps, Arabic normalizer (`[أإآء] -> ا`, `ة -> ه`), English suffix stemmer (`s`, `es`, `ing`), and Levenshtein typo matcher.
   - **Create Ranked Bandit Engine** (`apps/storefront/src/lib/search/ranked-bandits.ts`):
     Include Thompson Sampling Beta random draws, position discounting, and `recordBanditClick(productId, query, position)` telemetry.
   - **Create Search API Route** (`apps/storefront/src/app/api/search/route.ts`):
     Connect Stage 1 candidate retrieval + Stage 2 R-MAB scoring.
   - **Update `SmartSearchBar` Component** (`smart-search-bar.tsx`):
     Wire debounced 150ms search with `useTransition`, click tracking, "هل تقصد؟" typo pills, and zero-result fallback recommendations.

3. EMPIRICAL VERIFICATION:
   - Test `shirts` -> Returns `Egyptian Cotton T-Shirt` / `تيشرت قطن مصري`.
   - Test `كوتشي` -> Returns footwear products.
   - Test `shrt` (typo) -> Matches target shirt product.
   - Run typecheck: `cd apps/storefront && npx tsc --noEmit`.
   - Run build: `cd apps/storefront && npm run build`.

4. PROCESS CLEANUP:
   - Terminate any running subagents, background dev servers, or processes before completing turn.
</ANTIGRAVITY_WORKFLOW>

<ACCEPTANCE_CRITERIA>
- [ ] Searching `shirts` returns all `shirt` / `t-shirt` products (stemming active).
- [ ] Searching with typos (`shrt`, `تيشرط`) matches target items (fuzzy tolerance active).
- [ ] Egyptian dialect terms (`كوتشي`, `شيميز`, `ساعة`) match respective products.
- [ ] Ranked Multi-Armed Bandit (R-MAB) dynamically ranks items based on click conversions.
- [ ] Storefront builds cleanly with exit code 0.
- [ ] All subagents and background tasks cleanly terminated.
</ACCEPTANCE_CRITERIA>
```

---

# 🎨 PHASE 3: Luxury UI, 100% Arabic Default & Jargon Purge

```markdown
/goal

# TASK: 100% Arabic-First Luxury E-Commerce Transformation & Developer Jargon Purge

Execute a complete aesthetic and linguistic overhaul across both the storefront and admin panels:
1. **Abolish Cheap AI Clichés**: Eliminate dark neon borders, generic purple glow, pulsing biscuit dots, and icon-stuffed bento boxes.
2. **Luxury Color Palette**: Implement warm porcelain white (`#FFFFFF`), warm linen/cream surfaces (`#FDFBF7`, `#F8F6F0`), Deep Nile Teal (`#0F4C5C`), Imperial Emerald (`#0A5C36`), and Terracotta Amber (`#D97706`).
3. **100% Arabic-First Default (Zero English Leakage)**:
   - Ensure every button, label, dropdown, input placeholder, banner, order confirmation, and admin card is **100% authentic Arabic by default**.
   - Not a single English letter appears anywhere (`EGP` -> `ج.م`, `SKU` -> `رمز المنتج`, `Total` -> `الإجمالي`, `Tax` -> `الضريبة`). English is strictly hidden unless explicitly toggled by the user.
4. **Purge All Technical/Developer Jargon**:
   - Strip all API/gateway/courier references from customer and employee views (`(Paymob / Bosta)`, `(شامل 14% ضريبة)`, `(Powered by Medusa)`). Replace with clean, decisive copy (`إتمام الطلب`, `أضف إلى السلة`, `تأكيد الشراء`).
5. **JSON Configuration**: Extract all branding, colors, trust banners, announcement ribbons, and category definitions into `apps/storefront/src/config/site-config.json`.

<SUBAGENT_DELEGATION_DIRECTIVE>
- Use `invoke_subagent` to inspect `apps/storefront/src/app/globals.css`, `home-client-view.tsx`, `cart-context.tsx`, `checkout-view.tsx`, and admin widgets for English leaks and jargon.
</SUBAGENT_DELEGATION_DIRECTIVE>

<ANTIGRAVITY_SLASH_COMMANDS>
- /goal: Execute autonomously until site is 100% Arabic by default, luxury styled, and free of developer jargon.
- /learn: Persist luxury e-commerce styling and Arabic-first localization rules to .gemini/rules.
</ANTIGRAVITY_SLASH_COMMANDS>

<ANTIGRAVITY_WORKFLOW>
1. RESEARCH & INSPECTION:
   - Search for English strings and jargon like "Paymob", "Bosta", "EGP", "SKU" across `apps/storefront` and `apps/backend/src/admin`.

2. IMPLEMENTATION:
   - **Create `site-config.json`** (`apps/storefront/src/config/site-config.json`): Define complete color tokens, announcement text, and trust banners.
   - **Update `globals.css`**: Define luxury CSS variables, smooth scrollbars, and Cairo/Inter font rules.
   - **Overhaul Components**:
     - `Header`: Glassmorphic floating navigation with live cart badge pulse and clean Arabic links.
     - `HeroBanner`: High-impact luxury typography with clean CTA (`تسوق الآن`).
     - `ProductCard`: Clean 1:1 image layout, dual pricing (`350 ج.م` vs `450 ج.م`), discount badge (`وفر 22%`), and floating quick-add button.
     - `CheckoutView`: Clean 1-page checkout with native Arabic payment cards and zero developer jargon.
     - `Admin Widgets`: Localized Egyptian Arabic labels and clean status badges.

3. EMPIRICAL VERIFICATION:
   - Open browser on `http://localhost:3000/eg` -> Verify zero English characters, luxury styling, and clean Arabic copy.
   - Run typecheck: `cd apps/storefront && npx tsc --noEmit`.
   - Run build: `cd apps/storefront && npm run build`.

4. PROCESS CLEANUP:
   - Terminate any running subagents, background dev servers, or processes before completing turn.
</ANTIGRAVITY_WORKFLOW>

<ACCEPTANCE_CRITERIA>
- [ ] 100% Arabic-first default across every screen, button, badge, and modal (zero English characters by default).
- [ ] All developer jargon (`(using Paymob/Bosta)`, `(شامل 14% ضريبة)`) completely deleted.
- [ ] Bright luxury palette with Nile Teal / Emerald / Terracotta accents and porcelain/linen surfaces.
- [ ] All branding and visual tokens customizable via `site-config.json`.
- [ ] Storefront and backend build cleanly with exit code 0.
- [ ] All subagents and background tasks cleanly terminated.
</ACCEPTANCE_CRITERIA>
```

---

# 🎬 PHASE 4: Configurable Dynamic Animations Engine & Final Monorepo Build

```markdown
/goal

# TASK: Granular Dynamic Animation Engine & Full Monorepo Build Verification

Implement a rich, fully customizable motion system across the entire storefront:
1. **Dynamic Motion Engine in `site-config.json`**:
   - Allow merchants to configure animation presets (`"luxury-smooth"`, `"playful-spring"`, `"snappy-minimal"`, `"cinematic-fade"`) or customize individual component animations, durations (ms), and cubic-bezier easing curves directly in `site-config.json`:
     - **Product Card Hover**: Lift scale (`scale(1.025)`), duration (`250ms`), and soft diffuse shadow.
     - **Cart Drawer**: Spring slide-in from right (`350ms`), backdrop blur (`8px`).
     - **Quantity Stepper**: Tactile micro-bounce on `+`/`-` (`scale: 1.35 -> 1.0`).
     - **Item Removal**: Smooth exit swipe with height collapse (`opacity: 0, height: 0`).
     - **Checkout Steps**: Smooth accordion/cross-fade transitions between delivery and payment.
     - **Order Success**: Animated SVG checkmark draw with particle confetti burst.
2. **Full Monorepo Build & Quality Verification**:
   - Execute end-to-end verification across `@dtc/shared-types`, `apps/backend`, and `apps/storefront` to guarantee 100% zero-error compilation and zero layout shift (CLS = 0).

<SUBAGENT_DELEGATION_DIRECTIVE>
- Use `invoke_subagent` (Role: "Motion & Release Specialist", TypeName: "research") to verify animation CSS variables, component motion props, and full monorepo build tasks.
</SUBAGENT_DELEGATION_DIRECTIVE>

<ANTIGRAVITY_SLASH_COMMANDS>
- /goal: Execute autonomously until animation engine is fully customizable via JSON and all packages build cleanly.
- /learn: Persist dynamic CSS motion variables and Next.js micro-animation rules to .gemini/rules.
</ANTIGRAVITY_SLASH_COMMANDS>

<ANTIGRAVITY_WORKFLOW>
1. RESEARCH & INSPECTION:
   - View `apps/storefront/src/config/site-config.json` and `globals.css`.

2. IMPLEMENTATION:
   - Add `motion` configuration block to `site-config.json` with presets, easings, and component parameters.
   - Expose CSS motion tokens in `globals.css` (`--motion-duration-card`, `--motion-ease-luxury`, etc.).
   - Wire animations in `ProductCard`, `CartDrawer`, `CheckoutView`, and `Header` to read from motion tokens.
   - Add interactive celebratory checkmark on order confirmation screen.

3. EMPIRICAL VERIFICATION:
   - Shared Types Build: `cd packages/shared-types && npm run build`
   - Backend Typecheck & Build: `cd apps/backend && npx tsc --noEmit && npm run build`
   - Storefront Typecheck & Build: `cd apps/storefront && npx tsc --noEmit && npm run build`
   - Shell Script Syntax Check: `bash -n infrastructure/scripts/provision-tenant.sh`

4. PROCESS CLEANUP:
   - Terminate any active subagents, background worker loops, or dev server processes.
</ANTIGRAVITY_WORKFLOW>

<ACCEPTANCE_CRITERIA>
- [ ] Every component animation (type, duration, easing, hover scale) is 100% configurable via `site-config.json`.
- [ ] Product cards, cart drawer, quantity steppers, and checkout transitions animate smoothly with 0 layout shift (CLS = 0).
- [ ] All workspaces (`@dtc/shared-types`, `apps/backend`, `apps/storefront`) pass typecheck and build with exit code 0.
- [ ] System is 100% production ready.
- [ ] All subagents and background tasks cleanly terminated.
</ACCEPTANCE_CRITERIA>
```
