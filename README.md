# Master Storefront Feature & UX Fixes Prompt Pack (`PROMPT_SEQUENCE_STOREFRONT_NAVIGATION_PAGES_LOCALE.md`)

This prompt pack contains **4 targeted developer prompts** engineered for **Google Antigravity Agentic IDE** to implement the required missing core pages, interactive search submission, cross-tab synced animated locale switching, and a dedicated product catalog page.

---

## 📋 Prompt Sequence Overview

| Prompt | Target Scope | Key Technical Implementations |
| :--- | :--- | :--- |
| **Prompt 1** | **Search Submission & Dedicated Results Page** | Enter key & search icon navigation to `/[countryCode]/search?q=...`, dedicated search results page with filter drawer, sort options, and empty state. |
| **Prompt 2** | **Cross-Tab Synced & Animated Locale Switcher** | Animated directional layout flip (`dir` & font swap with smooth CSS opacity transition), 30-day cookie persistence, and `BroadcastChannel("medusa_locale_sync")` cross-tab live synchronization. |
| **Prompt 3** | **Dedicated Products Catalog & Filter Page** | `/[countryCode]/products/page.tsx` with category filters (الكل, أزياء, إلكترونيات, منزل), price range slider, sort dropdown (الأعلى تقييماً, الأقل سعراً), and pagination. |
| **Prompt 4** | **Content & Information Sub-Pages** | `/[countryCode]/about` (من نحن), `/[countryCode]/contact` (اتصل بنا مع نموذج تواصل), `/[countryCode]/faq` (الأسئلة الشائعة), `/[countryCode]/privacy` (سياسة الخصوصية), `/[countryCode]/terms` (الشروط والأحكام). |

---

## 🔍 PROMPT 1: Search Submission & Dedicated Results Page

```markdown
/goal

<TASK>
Implement search submission navigation on Enter key and search icon click in `SmartSearchBar`, and create a dedicated search results page at `apps/storefront/src/app/[countryCode]/search/page.tsx`.
</TASK>

<SUBAGENT_DELEGATION_DIRECTIVE>
- Use `invoke_subagent` (Role: "Storefront Search Specialist", TypeName: "research") to inspect `apps/storefront/src/modules/search/components/smart-search-bar.tsx` and check Next.js App Router query parameter routing patterns.
</SUBAGENT_DELEGATION_DIRECTIVE>

<ANTIGRAVITY_SLASH_COMMANDS>
- /goal: Execute autonomously until pressing Enter or clicking search icon navigates to the dedicated search results page.
- /learn: Persist search query routing and results page standards to .gemini/rules.
</ANTIGRAVITY_SLASH_COMMANDS>

<ANTIGRAVITY_WORKFLOW>
1. RESEARCH & INSPECTION PHASE:
   - View `apps/storefront/src/modules/search/components/smart-search-bar.tsx`.
   - Check existing search input handlers and form wrappers.

2. IMPLEMENTATION PHASE:
   - Target files: `apps/storefront/src/modules/search/components/smart-search-bar.tsx`, `apps/storefront/src/app/[countryCode]/search/page.tsx` (NEW), `apps/storefront/src/modules/search/templates/search-results-template.tsx` (NEW).
   - **Search Bar Submission Wiring** (`smart-search-bar.tsx`):
     Wrap the search input in a `<form onSubmit={handleFormSubmit}>` element:
     ```tsx
     const router = useRouter();
     const handleFormSubmit = (e: React.FormEvent) => {
       e.preventDefault();
       if (!query.trim()) return;
       setIsOpen(false);
       router.push(`/${countryCode || "eg"}/search?q=${encodeURIComponent(query.trim())}`);
     };
     ```
     Make the search icon inside the input clickable as a submit button (`type="submit"`).
   - **Dedicated Search Results Page** (`app/[countryCode]/search/page.tsx`):
     Create a Server Component that reads `searchParams.q`, fetches matching products from Medusa SDK or `/api/products`, and renders:
     - Header: "نتائج البحث عن: [Query]" / "Search results for: [Query]" with result count badge.
     - Product Grid: Responsive cards (2 cols mobile, 4 cols desktop) with dual EGP prices and Quick-Add.
     - Sort Dropdown: By Price (Low/High), Newest, and Best Selling.
     - Empty State: If 0 results, show "لم نجد نتائج مطابقة" with 4 trending recommended products.

3. EMPIRICAL VERIFICATION:
   - Run `cd apps/storefront && npx tsc --noEmit`.
   - Run `cd apps/storefront && npm run build`.
   - Test pressing Enter on query "تيشرت" -> Navigates to `/eg/search?q=%D8%AA%D9%8A%D8%B4%D8%B1%D8%AA`.

4. PROCESS CLEANUP:
   - Terminate any running subagents or processes before completing turn.
</ANTIGRAVITY_WORKFLOW>

<ACCEPTANCE_CRITERIA>
- [ ] Subagents delegated for search bar and route inspection.
- [ ] Pressing Enter or clicking search icon redirects to `/[countryCode]/search?q=...`.
- [ ] `app/[countryCode]/search/page.tsx` exists, renders search query, and displays matching products.
- [ ] Empty search state displays recommendations rather than blank screen.
- [ ] Storefront builds cleanly with exit code 0.
- [ ] All subagents cleanly terminated.
</ACCEPTANCE_CRITERIA>
```

---

## 🌐 PROMPT 2: Cross-Tab Synced & Animated Locale Switcher

```markdown
/goal

<TASK>
Create a smooth, animated Language/Locale Switcher that dynamically flips layout direction (`dir="rtl"` / `dir="ltr"`), transitions fonts (Cairo ↔ Inter) with an animated cross-fade, persists the choice to a 30-day cookie (`medusa_locale`), and synchronizes instantly across all open browser tabs via `BroadcastChannel("medusa_locale_sync")`.
</TASK>

<SUBAGENT_DELEGATION_DIRECTIVE>
- Use `invoke_subagent` (Role: "Localization & State Specialist", TypeName: "research") to inspect `apps/storefront/src/app/[countryCode]/layout.tsx`, `apps/storefront/src/lib/context/`, and cookie management in the storefront.
</SUBAGENT_DELEGATION_DIRECTIVE>

<ANTIGRAVITY_SLASH_COMMANDS>
- /goal: Execute autonomously until language switching is animated, persistent, and synchronizes across open tabs in real-time.
- /learn: Persist locale synchronization and directional animation rules to .gemini/rules.
</ANTIGRAVITY_SLASH_COMMANDS>

<ANTIGRAVITY_WORKFLOW>
1. RESEARCH & INSPECTION PHASE:
   - View `apps/storefront/src/app/[countryCode]/layout.tsx` and `apps/storefront/src/app/layout.tsx`.
   - View how locale is currently toggled in header/navbar components.

2. IMPLEMENTATION PHASE:
   - Target files: `apps/storefront/src/lib/context/locale-context.tsx` (NEW), `apps/storefront/src/modules/layout/components/locale-toggle.tsx` (NEW/UPDATE), `apps/storefront/src/app/[countryCode]/layout.tsx`, `apps/storefront/src/app/globals.css`.
   - **Locale Context & Cross-Tab Broadcast** (`locale-context.tsx`):
     ```typescript
     export const LocaleContext = createContext<...>(...);

     export function LocaleProvider({ children, initialLocale }: { children: React.ReactNode; initialLocale: string }) {
       const [locale, setLocale] = useState(initialLocale);
       const router = useRouter();
       const pathname = usePathname();

       useEffect(() => {
         const channel = new BroadcastChannel("medusa_locale_sync");
         channel.onmessage = (event) => {
           if (event.data?.locale && event.data.locale !== locale) {
             setLocale(event.data.locale);
             // Smoothly route to matching localized path in other tabs
             const segments = pathname.split("/");
             segments[1] = event.data.locale;
             router.push(segments.join("/"));
           }
         };
         return () => channel.close();
       }, [locale, pathname, router]);

       const changeLocale = (newLocale: "eg" | "en") => {
         document.cookie = `medusa_locale=${newLocale}; path=/; max-age=${30 * 24 * 60 * 60}; SameSite=Lax`;
         const channel = new BroadcastChannel("medusa_locale_sync");
         channel.postMessage({ locale: newLocale });
         channel.close();
         
         const segments = pathname.split("/");
         segments[1] = newLocale;
         router.push(segments.join("/"));
       };

       return (
         <LocaleContext.Provider value={{ locale, changeLocale, isRtl: locale === "eg" || locale === "ar" }}>
           {children}
         </LocaleContext.Provider>
       );
     }
     ```
   - **Smooth CSS Animation for Direction Flips** (`globals.css`):
     ```css
     .locale-transition-wrapper {
       transition: opacity 250ms cubic-bezier(0.16, 1, 0.3, 1), transform 250ms cubic-bezier(0.16, 1, 0.3, 1);
     }
     ```
   - **Interactive Language Toggle Button** (`locale-toggle.tsx`):
     Create a sleek floating or header pill (`العربية | English`) with tactile spring animation on toggle.

3. EMPIRICAL VERIFICATION:
   - Open Tab 1 (`http://localhost:3000/eg`) and Tab 2 (`http://localhost:3000/eg`).
   - Switch language to English in Tab 1 -> Tab 2 must automatically switch to `/en` with smooth transition.
   - Run `cd apps/storefront && npx tsc --noEmit && npm run build`.

4. PROCESS CLEANUP:
   - Terminate any running subagents or processes before completing turn.
</ANTIGRAVITY_WORKFLOW>

<ACCEPTANCE_CRITERIA>
- [ ] Subagents delegated for locale context and layout inspection.
- [ ] Switching language updates URL path, sets 30-day `medusa_locale` cookie, and flips `dir`/font.
- [ ] `BroadcastChannel("medusa_locale_sync")` syncs language change across all open tabs instantly.
- [ ] Transition between RTL and LTR has smooth CSS opacity/transform animation without jarring flickers.
- [ ] Storefront build completes with exit code 0.
- [ ] All subagents cleanly terminated.
</ACCEPTANCE_CRITERIA>
```

---

## 🛍️ PROMPT 3: Dedicated Products Catalog & Filter Page

```markdown
/goal

<TASK>
Create a full-featured, dedicated Product Catalog page at `apps/storefront/src/app/[countryCode]/products/page.tsx` with category filters, price range sliders, sorting, grid/list toggles, and responsive pagination.
</TASK>

<SUBAGENT_DELEGATION_DIRECTIVE>
- Use `invoke_subagent` (Role: "Catalog Architecture Specialist", TypeName: "research") to inspect product fetching in `apps/storefront/src/lib/data/products.ts` and Medusa v2 store products query parameters.
</SUBAGENT_DELEGATION_DIRECTIVE>

<ANTIGRAVITY_SLASH_COMMANDS>
- /goal: Execute autonomously until the dedicated products catalog page is live, interactive, and filterable.
- /learn: Persist product catalog layout and filtering standards to .gemini/rules.
</ANTIGRAVITY_SLASH_COMMANDS>

<ANTIGRAVITY_WORKFLOW>
1. RESEARCH & INSPECTION PHASE:
   - Check `apps/storefront/src/lib/data/products.ts`.
   - Check if `apps/storefront/src/app/[countryCode]/products/page.tsx` exists (currently only `[handle]/page.tsx` exists).

2. IMPLEMENTATION PHASE:
   - Target files: `apps/storefront/src/app/[countryCode]/products/page.tsx` (NEW), `apps/storefront/src/modules/products/templates/catalog-template.tsx` (NEW), `apps/storefront/src/modules/products/components/catalog-filters.tsx` (NEW).
   - **Catalog Page Implementation** (`app/[countryCode]/products/page.tsx`):
     - Server Component reading `searchParams` (`category`, `sort`, `minPrice`, `maxPrice`, `page`).
     - Fetches live products from Medusa SDK or fallback dataset.
     - Features:
       - **Category Sidebar & Mobile Drawer**: `الكل`, `أزياء وملابس`, `إلكترونيات`, `منزل وديكور`, `عطور وعناية`.
       - **Price Range Filter**: Interactive slider or min/max inputs in EGP (`ج.م`).
       - **Sort Select Dropdown**: `الأحدث وصولاً` (Newest), `السعر: من الأقل للأعلى` (Price: Low to High), `السعر: من الأعلى للأقل` (Price: High to Low), `الأعلى تقييماً` (Top Rated).
       - **Active Filter Pills**: Shows removable badge tags for active filters (e.g. `أزياء ✕`, `أقل من 500 ج.م ✕`).
       - **Product Grid**: Luxury responsive cards with hover zoom, discount badges, and Quick-Add button.
       - **Pagination / Load More**: Clean numeric pagination or smooth "عرض المزيد من المنتجات" button.

3. EMPIRICAL VERIFICATION:
   - Navigate to `http://localhost:3000/eg/products` -> Must load catalog grid with sidebar filters.
   - Filter by category and sort -> URL updates (`/eg/products?category=fashion&sort=price_asc`) and products filter accurately.
   - Run `cd apps/storefront && npx tsc --noEmit && npm run build`.

4. PROCESS CLEANUP:
   - Terminate any running subagents or processes before completing turn.
</ANTIGRAVITY_WORKFLOW>

<ACCEPTANCE_CRITERIA>
- [ ] Subagents delegated for catalog page and data fetching inspection.
- [ ] `app/[countryCode]/products/page.tsx` exists and serves the full catalog.
- [ ] Filtering by category, price, and sorting works without breaking URL state.
- [ ] Responsive filter drawer on mobile and sticky sidebar on desktop.
- [ ] Storefront build completes with exit code 0.
- [ ] All subagents cleanly terminated.
</ACCEPTANCE_CRITERIA>
```

---

## 📄 PROMPT 4: Complete Information & Content Sub-Pages (About, Contact, FAQ, Terms, Privacy)

```markdown
/goal

<TASK>
Implement all missing institutional and customer support sub-pages with luxury typography, 100% authentic Arabic copy, responsive layouts, and interactive contact forms:
1. `apps/storefront/src/app/[countryCode]/about/page.tsx` (من نحن - قصة المتجر والجودة المصرية)
2. `apps/storefront/src/app/[countryCode]/contact/page.tsx` (اتصل بنا - نموذج تواصل تفاعلي، بيانات الاتصال، وأوقات العمل)
3. `apps/storefront/src/app/[countryCode]/faq/page.tsx` (الأسئلة الشائعة - أكورديون تفاعلي للشحن، الدفع، والإرجاع)
4. `apps/storefront/src/app/[countryCode]/privacy/page.tsx` (سياسة الخصوصية وحماية البيانات)
5. `apps/storefront/src/app/[countryCode]/terms/page.tsx` (الشروط والأحكام وسياسة الإرجاع)
</TASK>

<SUBAGENT_DELEGATION_DIRECTIVE>
- Use `invoke_subagent` (Role: "Content & Sub-Pages Specialist", TypeName: "research") to check footer and navigation links across `apps/storefront`.
</SUBAGENT_DELEGATION_DIRECTIVE>

<ANTIGRAVITY_SLASH_COMMANDS>
- /goal: Execute autonomously until all 5 institutional sub-pages are created, styled, and linked in header/footer.
- /learn: Persist institutional sub-page templates and contact form standards to .gemini/rules.
</ANTIGRAVITY_SLASH_COMMANDS>

<ANTIGRAVITY_WORKFLOW>
1. RESEARCH & INSPECTION PHASE:
   - View footer links in `apps/storefront/src/modules/layout/components/footer.tsx` (or equivalent).
   - Identify all dead 404 links.

2. IMPLEMENTATION PHASE:
   - Target files:
     - `apps/storefront/src/app/[countryCode]/about/page.tsx` (NEW)
     - `apps/storefront/src/app/[countryCode]/contact/page.tsx` (NEW)
     - `apps/storefront/src/app/[countryCode]/faq/page.tsx` (NEW)
     - `apps/storefront/src/app/[countryCode]/privacy/page.tsx` (NEW)
     - `apps/storefront/src/app/[countryCode]/terms/page.tsx` (NEW)
     - `apps/storefront/src/modules/layout/components/footer.tsx` (Update links)
   - **About Page** (`about/page.tsx`):
     - Brand story celebrating authentic Egyptian craftsmanship, premium cotton, and local manufacturing.
     - Visual stat cards: "توصيل لـ 27 محافظة", "أكثر من 10,000 عميل سعيد", "جودة مصرية 100%".
   - **Contact Us Page** (`contact/page.tsx`):
     - Interactive form: Name, Email, Egyptian Phone Number (`010...`), Subject, and Message.
     - Direct WhatsApp quick-chat button (`تواصل فوري عبر واتساب`).
     - Egyptian support hours & location (Cairo, Egypt).
   - **FAQ Page** (`faq/page.tsx`):
     - Interactive collapsible accordion (الشحن والتوصيل، طرق الدفع والتقسيط، الاستبدال والاسترجاع خلال 14 يوم).
   - **Terms & Privacy Pages** (`privacy/page.tsx` & `terms/page.tsx`):
     - Formatted legal copy compliant with Egyptian e-commerce regulations and consumer protection law (قانون حماية المستهلك المصري رقم 181 لسنة 2018).
   - **Footer Navigation Update**:
     - Connect all footer and header links to these new routes so zero 404s exist across the entire site.

3. EMPIRICAL VERIFICATION:
   - Click every link in footer (`من نحن`, `اتصل بنا`, `الأسئلة الشائعة`, `سياسة الخصوصية`, `الشروط`) -> Confirm HTTP 200 on all.
   - Run `cd apps/storefront && npx tsc --noEmit && npm run build`.

4. PROCESS CLEANUP:
   - Terminate any running subagents or processes before completing turn.
</ANTIGRAVITY_WORKFLOW>

<ACCEPTANCE_CRITERIA>
- [ ] Subagents delegated for sub-pages and footer link inspection.
- [ ] All 5 sub-pages (`/about`, `/contact`, `/faq`, `/privacy`, `/terms`) created and render with luxury styling.
- [ ] Contact page features interactive form and direct WhatsApp CTA.
- [ ] FAQ page features animated collapsible accordion.
- [ ] Footer and header links connected with zero 404 dead links.
- [ ] Storefront build completes with exit code 0.
- [ ] All subagents cleanly terminated.
</ACCEPTANCE_CRITERIA>
```
