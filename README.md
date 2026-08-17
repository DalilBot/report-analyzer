# Master UI/UX & Design Transformation Prompt (`PROMPT_MASTER_LUXURY_UI_TRANSFORMATION.md`)

This prompt is engineered for **Google Antigravity Agentic IDE** to perform a complete, top-tier aesthetic, linguistic, and architectural transformation across both the Next.js Storefront and Medusa Admin dashboard.

---

```markdown
/goal

# 🏛️ MISSION: 100% Arabic-First Luxury E-Commerce Transformation & Cognitive Design Overhaul

You are a Principal Product Designer and Staff Frontend/UI Engineer with mastery in high-conversion luxury e-commerce (think Apple, Stripe, Linear, SSENSE, Farfetch Arabia).

Your mission is to completely redesign and reshape the UI/UX across the entire `medusa-eg` monorepo (`apps/storefront` and `apps/backend/src/admin`). You must eliminate all cheap-looking generic starter elements, abolish "AI-generated" visual clichés, strip developer jargon and technical clutter from customer and admin eyes, build a clean, bright, eye-grabbing, comfortable, and lively design system with buttery-smooth micro-animations, make the entire UI configurable via simple JSON theme files, and enforce a **100% Arabic-first experience** where not a single English letter appears anywhere unless explicitly toggled by the user.

---

## 🎨 PART 1: CORE DESIGN PHILOSOPHY & AESTHETIC DIRECTIVES

### 1. Abolish Cheap "AI Clichés" & Generic Defaults:
- ❌ **NO cheap neon gradients, purple-on-dark glow, or generic crypto/AI dark theme gimmicks**.
- ❌ **NO icon-stuffed bento boxes, pulsing biscuit pills with glowing dots, or raw border outlines**.
- ❌ **NO developer jargon or unnecessary technical words**:
  - Delete `(Paymob / Bosta)`, `(شامل 14% ضريبة)`, `(Powered by Medusa v2)`, `(Accept Paymob Gateway)`. Customers do NOT care what API courier or payment provider processes their order.
  - Simplify CTAs: Replace clunky text with clean, decisive Arabic copy (e.g. `إتمام الطلب`, `أضف للسلة`, `تأكيد الشراء`, `متابعة`).
- ✅ **Lively, Bright, Eye-Grabbing & Ultra-Comfortable Palette**:
  - Warm luxury neutrals: Crisp porcelain white (`#FFFFFF`), warm cream/linen surfaces (`#FDFBF7`, `#F8F6F0`), subtle cashmere borders (`#EDE8E1`).
  - Sophisticated Egyptian accent palette: Deep Nile Teal (`#0F4C5C`), Imperial Emerald (`#0A5C36`), Warm Terracotta / Sand Amber (`#C86D51`, `#D97706`), Velvet Slate for typography (`#1A202C`, `#2D3748`).
  - Organic depth: Subtle layered elevations (`box-shadow: 0 4px 20px -2px rgba(0, 0, 0, 0.05)`), glassmorphism frosted blurs (`backdrop-blur-md bg-white/80`), tactile active states.

### 2. Micro-Animations & Fluid Responsiveness:
- Implement tactile hover states, spring physics, smooth cart drawer slides, interactive image thumbnail cross-fades, and snappy optimistic quantity steppers.
- Use CSS cubic-bezier transitions (`cubic-bezier(0.16, 1, 0.3, 1)`) for buttery smoothness with zero layout shift (CLS = 0).

### 3. 100% Arabic-First Default (Zero English Leakage):
- Every single screen, button, badge, header, placeholder, toast notification, error message, footer, invoice, and metadata tag must be **100% native Arabic by default**.
- **Not a single English character or foreign abbreviation may appear anywhere** on any customer or employee screen (e.g., `EGP` -> `ج.م`, `SKU` -> `رمز المنتج`, `Tax` -> `الضريبة`, `Total` -> `الإجمالي`, `Discount` -> `الخصم`).
- Arabic numerals or localized digits applied consistently.
- English is strictly hidden until a user explicitly changes their language preference to English in their profile.

### 4. Full UI Easy JSON Customizability (`theme.json` / `site-config.json`):
- Extract all branding, colors, typography tokens, trust banners, announcement bars, navigation links, and category definitions into a centralized, editable JSON configuration file (e.g. `apps/storefront/src/config/theme.json` and `site-content.json`).
- Store owners should be able to re-theme the entire platform (colors, banners, promotions, hero slogans) simply by editing this JSON without touching JSX code.

---

## 🛠️ PART 2: COMPONENT-BY-COMPONENT IMPLEMENTATION BLUEPRINT

### 1. Unified Theme Configuration (`apps/storefront/src/config/site-config.json`)
Create a comprehensive JSON configuration file controlling all visual tokens and content:
```json
{
  "theme": {
    "colors": {
      "primary": "#0F4C5C",
      "primaryHover": "#0C3C49",
      "accent": "#D97706",
      "accentLight": "#FEF3C7",
      "surface": "#FFFFFF",
      "surfaceMuted": "#FDFBF7",
      "border": "#EDE8E1",
      "textPrimary": "#1A202C",
      "textSecondary": "#718096"
    },
    "borderRadius": "16px",
    "fontFamily": "var(--font-cairo)"
  },
  "announcement": {
    "enabled": true,
    "textAr": "✨ توصيل سريع لجميع محافظات مصر | دفع عند الاستلام أو بالتقسيط",
    "textEn": "✨ Express delivery across Egypt | Cash on delivery or installments"
  },
  "trustBadges": [
    { "id": "shipping", "titleAr": "شحن سريع لكافة المحافظات", "descAr": "توصيل خلال 24-48 ساعة لجميع مدن مصر" },
    { "id": "payment", "titleAr": "دفع آمن ومتعدد الخيارات", "descAr": "بطاقات بنكية، محافظ إلكترونية، كاش، وتقسيط" },
    { "id": "quality", "titleAr": "ضمان الجودة المصرية", "descAr": "منتجات أصلية 100% مع إمكانية الإرجاع السهل" }
  ]
}
```

### 2. Storefront Layout & Header (`apps/storefront/src/app/layout.tsx` & Header)
- **Top Announcement Bar**: Subtle warm gold/linen banner with animated marquee or smooth fade for current promotions.
- **Floating Glassmorphic Header**: Clean logo, live search with BiDi auto-detection, category navigation, language/currency indicator, and an interactive floating Cart pill with real-time badge count pulse.
- **Typography**: Google Cairo loaded with optimal weight distribution (400, 500, 600, 700, 800) with `display: swap`.

### 3. Homepage & Catalog Showcase (`home-client-view.tsx`)
- **Luxury Hero Banner**: Clean, high-impact typography with subtle parallax, smooth CTA buttons (`تسوق الآن`), and zero cluttered badges.
- **Category Filter Rail**: Modern horizontal scrolling pills with tactile active indicators (`الكل`, `إلكترونيات`, `أزياء`, `منزل وديكور`, `عناية وجمال`, `عروض حصرية`).
- **Product Card Masterpiece**:
  - Image ratio 1:1 or 4:5 with smooth hover zoom.
  - Clean localized pricing: `350 ج.م` with original strikethrough `450 ج.م` and subtle terracotta badge (`وفر 22%`).
  - Floating Quick-Add button (`+`) that triggers optimistic cart drawer opening with haptic feedback.
  - Zero developer text (delete all mentions of Bosta, Paymob, VAT percentages).

### 4. Slide-Over Cart Drawer (`cart-drawer.tsx`)
- Buttery-smooth slide-in from right (in RTL) with backdrop blur.
- Clean item rows with high-res thumbnails, variant badges (`مقاس: كبير`, `لون: أسود`), interactive quantity stepper (`-` `1` `+`), and instant trash icon removal.
- Free shipping progress bar (e.g. `أضف 150 ج.م إضافية للحصول على شحن مجاني!`).
- Clean Checkout Button: `إتمام الطلب • [الإجمالي] ج.م` (Full width, bold, high-contrast Nile Teal / Emerald).

### 5. Frictionless 1-Page Checkout (`checkout-view.tsx`)
- **Visual Progress Stepper**: `1. بيانات التوصيل` -> `2. خيارات الدفع` -> `3. تأكيد الطلب`.
- **Address & Governorate Selector**:
  - Clean tiered Egyptian governorate selector displaying delivery cost transparently (e.g. `القاهرة والجيزة - 45 ج.م`, `الإسكندرية والدلتا - 60 ج.م`).
  - Egyptian phone input with carrier auto-badge (Vodafone, Orange, Etisalat, WE).
- **Payment Method Cards (Clean & Visual)**:
  - `الدفع عند الاستلام (كاش)`
  - `بطاقة بنكية (فيزا / ماستركارد / ميزة)`
  - `المحافظ الإلكترونية (فودافون كاش، أورنج، اتصالات، وي)`
  - `تقسيط ڤاليو (ValU) أو سهولة`
  - `الدفع في منافذ أمان / فوري / مصاري`
- **Total Summary Box**: Clear breakdown of `المجموع الفرعي`, `الشحن والتوصيل`, and `الإجمالي النهائي`.

### 6. Medusa Admin & Employee Portal (`apps/backend/src/admin/`)
- Inject Egyptian Arabic localized dashboard labels, clean status pills (`مكتمل`, `قيد التجهيز`, `في الطريق`, `تم الإلغاء`), and rich order action drawers.
- Streamline AI Copywriter widget into a sleek, one-click Egyptian marketing assistant (`توليد وصف جذاب بالعامية المصرية`).

---

## 📋 STEP-BY-STEP IMPLEMENTATION WORKFLOW

1. **Phase 1: Design Tokens & JSON Theme Foundation**:
   - Create `apps/storefront/src/config/site-config.json` with all theme tokens and Arabic copy.
   - Update `apps/storefront/src/app/globals.css` with luxury color variables, custom scrollbars, animations, and typography rules.

2. **Phase 2: Storefront Components Overhaul**:
   - Redesign `Header`, `HeroBanner`, `ProductCard`, `CategoryPills`, and `Footer`.
   - Ensure all strings are 100% Arabic with zero English text leakage.
   - Strip all technical provider references (`Paymob`, `Bosta`, `Medusa`).

3. **Phase 3: Interactive Cart & Checkout Transformation**:
   - Redesign `CartDrawer` with quantity steppers, delete animations, and free shipping tracker.
   - Streamline `CheckoutView` into a modern, frictionless 1-page checkout with native Arabic payment cards and live Bosta tariff calculation.

4. **Phase 4: Admin Extension & Widget Polish**:
   - Restyle Admin AI Copywriter widget to match luxury aesthetics with clean Arabic copy.

5. **Phase 5: Build & Verification**:
   - Verify `tsc --noEmit` on backend and storefront.
   - Verify production build `npm run build` on both packages.
   - Confirm complete visual beauty, 100% Arabic default, and zero console errors.

---

## 🎯 ACCEPTANCE CRITERIA

- [ ] Zero cheap "AI dark-mode" clichés, neon borders, or icon-stuffed boxes.
- [ ] Bright, luxury, eye-grabbing color palette with Nile Teal / Emerald / Terracotta accents and warm linen backgrounds.
- [ ] 100% Arabic-first experience across every screen, button, badge, and modal (zero English letters by default).
- [ ] All developer jargon (`(using Paymob/Bosta)`, `(شامل 14% ضريبة)`) completely purged from customer and employee view.
- [ ] All visual tokens, banners, and copy are easily customizable via `site-config.json`.
- [ ] Micro-animations on buttons, cart drawer, and product cards with 0 layout shift.
- [ ] Storefront and backend build cleanly with exit code 0.
```
