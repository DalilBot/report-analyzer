# Antigravity Master Developer Prompt Sequence: Egyptian MedusaJS v2 Platform (Prompts 1–37)

This prompt pack contains **37 atomic, step-by-step developer prompts** tailored for **Google Antigravity Agentic IDE** with native `/goal`, `/browser`, and `/learn` slash command triggers.

---

## Phase 1: Project Scaffolding & Setup

---
### Developer Prompt 1: Initialize MedusaJS v2 Backend Project

```markdown
/goal

<TASK>
Initialize the core MedusaJS v2 backend application scaffold in `apps/backend`.
</TASK>

<ANTIGRAVITY_SLASH_COMMANDS>
- /goal: Execute autonomously until project scaffolding and build verification pass.
- /learn: Save MedusaJS v2 module directory structure into .gemini/rules upon success.
</ANTIGRAVITY_SLASH_COMMANDS>

<ANTIGRAVITY_WORKFLOW>
1. RESEARCH & INSPECTION PHASE:
   - Inspect workspace root using `list_dir`.
   - Verify Node.js and npm version compatibility (`node -v && npm -v`).

2. IMPLEMENTATION PHASE:
   - Target files: `apps/backend/package.json`, `apps/backend/medusa-config.ts`
   - Execute: `npx -y create-medusa-app@latest ./` inside `apps/backend`.
   - Verify `medusa-config.ts` configures PostgreSQL connection and Redis cache.

3. EMPIRICAL VERIFICATION & TESTING PHASE:
   - Run build verification command: `cd apps/backend && npm run build`
   - Ensure build completes with exit code 0.

4. PROCESS CLEANUP & LEARNING DIRECTIVE (CRITICAL):
   - Execute `/learn` to store backend module paths for future tasks.
   - Terminate any running background dev servers, processes, or occupied ports before completing your turn.
</ANTIGRAVITY_WORKFLOW>

<ACCEPTANCE_CRITERIA>
- [ ] `apps/backend/medusa-config.ts` exists and compiles cleanly.
- [ ] Backend build completes with exit code 0.
- [ ] All background tasks and dev servers are cleanly terminated.
</ACCEPTANCE_CRITERIA>
```

---
### Developer Prompt 2: Initialize Next.js Storefront App Router Project

```markdown
/goal

<TASK>
Initialize the Next.js Storefront application scaffold in `apps/storefront`.
</TASK>

<ANTIGRAVITY_SLASH_COMMANDS>
- /goal: Execute autonomously until Next.js app router scaffold and SDK installation pass build checks.
- /learn: Persist Storefront component directory structure to .gemini/rules.
</ANTIGRAVITY_SLASH_COMMANDS>

<ANTIGRAVITY_WORKFLOW>
1. RESEARCH & INSPECTION PHASE:
   - Inspect `apps/` directory using `list_dir`.
   - Review `@medusajs/js-sdk` setup requirements.

2. IMPLEMENTATION PHASE:
   - Target files: `apps/storefront/package.json`, `apps/storefront/next.config.js`, `apps/storefront/tailwind.config.js`
   - Execute: `npx -y create-next-app@latest ./ --typescript --tailwind --app --eslint` inside `apps/storefront`.
   - Install SDK: `cd apps/storefront && npm install @medusajs/js-sdk @medusajs/types lucide-react`.

3. EMPIRICAL VERIFICATION & TESTING PHASE:
   - Run build verification command: `cd apps/storefront && npm run build`

4. PROCESS CLEANUP & LEARNING DIRECTIVE (CRITICAL):
   - Terminate any running background dev servers (e.g., stop `next dev`), background processes, or open ports before ending your turn.
</ANTIGRAVITY_WORKFLOW>

<ACCEPTANCE_CRITERIA>
- [ ] Next.js storefront app router scaffolding compiles cleanly.
- [ ] `@medusajs/js-sdk` installed and configured in `package.json`.
- [ ] All background tasks and dev servers are cleanly terminated.
</ACCEPTANCE_CRITERIA>
```

---
### Developer Prompt 3: Configure Root Workspace & Environment Variables Wiring

```markdown
/goal

<TASK>
Establish root workspace template environment variables for Backend and Storefront.
</TASK>

<ANTIGRAVITY_SLASH_COMMANDS>
- /goal: Execute autonomously until all environment templates are created and verified.
</ANTIGRAVITY_SLASH_COMMANDS>

<ANTIGRAVITY_WORKFLOW>
1. RESEARCH & INSPECTION PHASE:
   - Inspect `.env` requirements for Medusa v2, Paymob API v2, Bosta Logistics, and ETA e-Receipt API.

2. IMPLEMENTATION PHASE:
   - Target files: `.env.example`, `apps/backend/.env.template`, `apps/storefront/.env.template`
   - Create `.env.example` at root containing keys for DB, Redis, Paymob, Bosta, and ETA.
   - Create `apps/backend/.env.template` containing backend secrets (`DATABASE_URL`, `REDIS_URL`, `PAYMOB_API_KEY`, `PAYMOB_HMAC_SECRET`, `BOSTA_API_KEY`).
   - Create `apps/storefront/.env.template` with `NEXT_PUBLIC_MEDUSA_BACKEND_URL` and `NEXT_PUBLIC_DEFAULT_REGION`.

3. EMPIRICAL VERIFICATION & TESTING PHASE:
   - Execute verification test: `test -f .env.example && test -f apps/backend/.env.template && test -f apps/storefront/.env.template`

4. PROCESS CLEANUP & LEARNING DIRECTIVE (CRITICAL):
   - Terminate any active background tasks before ending turn.
</ANTIGRAVITY_WORKFLOW>

<ACCEPTANCE_CRITERIA>
- [ ] `.env.example` and module templates created with comprehensive variable keys.
- [ ] Verification command passes cleanly.
- [ ] All background tasks are cleanly terminated.
</ACCEPTANCE_CRITERIA>
```

---

## Phase 2: Egyptian Localization Core

---
### Developer Prompt 4: Configure Tailwind CSS RTL Logical Properties & Direction Helpers

```markdown
/goal

<TASK>
Configure Tailwind CSS in `apps/storefront` with RTL logical properties and Bidi direction utilities.
</TASK>

<ANTIGRAVITY_SLASH_COMMANDS>
- /goal: Execute autonomously until Tailwind CSS RTL build compiles with zero errors.
</ANTIGRAVITY_SLASH_COMMANDS>

<ANTIGRAVITY_WORKFLOW>
1. RESEARCH & INSPECTION PHASE:
   - View `apps/storefront/tailwind.config.js` and `apps/storefront/src/app/globals.css`.
   - Inspect Tailwind RTL logical property utilities (`ms-*`, `me-*`, `ps-*`, `pe-*`).

2. IMPLEMENTATION PHASE:
   - Target files: `apps/storefront/tailwind.config.js`, `apps/storefront/src/app/globals.css`
   - Configure Tailwind RTL plugins and logical spacing rules.
   - Add `.rtl-flip` utility CSS class to mirror icons when `[dir="rtl"]` is active.

3. EMPIRICAL VERIFICATION & TESTING PHASE:
   - Run verification command: `cd apps/storefront && npm run build`

4. PROCESS CLEANUP & LEARNING DIRECTIVE (CRITICAL):
   - Kill any running dev servers or tasks before completing turn.
</ANTIGRAVITY_WORKFLOW>

<ACCEPTANCE_CRITERIA>
- [ ] Storefront builds with RTL logical utility classes enabled.
- [ ] Icon mirroring helper `.rtl-flip` defined in `globals.css`.
- [ ] All background processes are cleanly terminated.
</ACCEPTANCE_CRITERIA>
```

---
### Developer Prompt 5: Implement Egyptian Arabic & English i18n Translation Dictionary

```markdown
/goal

<TASK>
Implement bilingual translation dictionaries for Egyptian Arabic (Ammiya fallback) and English.
</TASK>

<ANTIGRAVITY_SLASH_COMMANDS>
- /goal: Execute autonomously until i18n dictionaries are created and type-checked.
</ANTIGRAVITY_SLASH_COMMANDS>

<ANTIGRAVITY_WORKFLOW>
1. RESEARCH & INSPECTION PHASE:
   - Inspect requirements for Egyptian e-Commerce terms ("سلة الشراء", "تأكيد الطلب", "مصاريف الشحن", "الدفع كاش عند الاستلام").

2. IMPLEMENTATION PHASE:
   - Target files: `apps/storefront/src/lib/i18n/ar.json`, `apps/storefront/src/lib/i18n/en.json`, `apps/storefront/src/lib/i18n/index.ts`
   - Create `ar.json` with natural Egyptian terminology.
   - Create `en.json` with matching English keys.
   - Create i18n helper module in `index.ts` for dynamic language switching.

3. EMPIRICAL VERIFICATION & TESTING PHASE:
   - Run TypeScript check: `cd apps/storefront && npx tsc --noEmit`

4. PROCESS CLEANUP & LEARNING DIRECTIVE (CRITICAL):
   - Terminate any running tasks before ending turn.
</ANTIGRAVITY_WORKFLOW>

<ACCEPTANCE_CRITERIA>
- [ ] `ar.json` includes Egyptian Arabic e-commerce terminology.
- [ ] TypeScript compilation passes cleanly.
- [ ] All background tasks are cleanly terminated.
</ACCEPTANCE_CRITERIA>
```

---
### Developer Prompt 6: Configure Medusa EGP Region, 14% VAT Tax Rate, and Currency Settings

```markdown
/goal

<TASK>
Create seeding script to configure Egypt Region with EGP currency and 14% VAT rate.
</TASK>

<ANTIGRAVITY_SLASH_COMMANDS>
- /goal: Execute autonomously until Egypt EGP 14% VAT region is seeded and verified.
</ANTIGRAVITY_SLASH_COMMANDS>

<ANTIGRAVITY_WORKFLOW>
1. RESEARCH & INSPECTION PHASE:
   - Search Medusa v2 region and tax rate service methods.

2. IMPLEMENTATION PHASE:
   - Target file: `apps/backend/src/scripts/seed-egypt-region.ts`
   - Write typescript script checking if "Egypt" region exists; if not, create it with `currency_code: "egp"`, `name: "Egypt"`, and `tax_rate: 14.0`.

3. EMPIRICAL VERIFICATION & TESTING PHASE:
   - Run verification: `cd apps/backend && npx ts-node src/scripts/seed-egypt-region.ts`

4. PROCESS CLEANUP & LEARNING DIRECTIVE (CRITICAL):
   - Kill any background processes or test scripts before completing turn.
</ANTIGRAVITY_WORKFLOW>

<ACCEPTANCE_CRITERIA>
- [ ] Seed script executes and creates/verifies Egypt EGP 14% VAT region.
- [ ] All background tasks are cleanly terminated.
</ACCEPTANCE_CRITERIA>
```

---
### Developer Prompt 7: Implement 27 Egyptian Governorates & District Data Structure

```markdown
/goal

<TASK>
Create structured lookup dataset and utility functions for all 27 Egyptian Governorates and Bosta city codes.
</TASK>

<ANTIGRAVITY_SLASH_COMMANDS>
- /goal: Execute autonomously until governorate data structure passes test scripts.
</ANTIGRAVITY_SLASH_COMMANDS>

<ANTIGRAVITY_WORKFLOW>
1. RESEARCH & INSPECTION PHASE:
   - Inspect Bosta governorate and city ID mappings for Cairo, Alexandria, Delta, Upper Egypt, Canal, and Sinai zones.

2. IMPLEMENTATION PHASE:
   - Target files: `packages/shared-types/src/egypt-governorates.json`, `packages/shared-types/src/governorate-utils.ts`
   - Create JSON data file containing all 27 governorates in Arabic and English with Bosta IDs.
   - Implement utility methods `getGovernorates()`, `getDistricts(id)`, and `getBostaCityId(id)`.

3. EMPIRICAL VERIFICATION & TESTING PHASE:
   - Run verification test: `npx ts-node packages/shared-types/src/governorate-utils.ts`

4. PROCESS CLEANUP & LEARNING DIRECTIVE (CRITICAL):
   - Kill any background processes before completing turn.
</ANTIGRAVITY_WORKFLOW>

<ACCEPTANCE_CRITERIA>
- [ ] Dataset contains all 27 Egyptian Governorates with Bosta city mappings.
- [ ] Utility functions pass execution tests.
- [ ] All background tasks are cleanly terminated.
</ACCEPTANCE_CRITERIA>
```

---
### Developer Prompt 8: Implement Egyptian Phone Number Validation & E.164 Normalization Utility

```markdown
/goal

<TASK>
Build phone validation and E.164 normalization utilities tailored for Egyptian mobile networks.
</TASK>

<ANTIGRAVITY_SLASH_COMMANDS>
- /goal: Execute autonomously until phone normalization regex tests pass.
</ANTIGRAVITY_SLASH_COMMANDS>

<ANTIGRAVITY_WORKFLOW>
1. RESEARCH & INSPECTION PHASE:
   - Inspect Egyptian mobile operator prefixes (`010` Vodafone, `011` Etisalat, `012` Orange, `015` WE).

2. IMPLEMENTATION PHASE:
   - Target file: `packages/shared-types/src/phone-utils.ts`
   - Implement regex: `^(\+20|0)?1[0125]\d{8}$`.
   - Implement `normalizeEgyptianPhone(phone: string): string` outputting `+201XXXXXXXXX`.

3. EMPIRICAL VERIFICATION & TESTING PHASE:
   - Run verification script test: `npx ts-node packages/shared-types/src/phone-utils.ts`

4. PROCESS CLEANUP & LEARNING DIRECTIVE (CRITICAL):
   - Terminate any running processes before ending turn.
</ANTIGRAVITY_WORKFLOW>

<ACCEPTANCE_CRITERIA>
- [ ] Phone regex accurately validates all Egyptian mobile operator prefixes.
- [ ] Normalization output matches E.164 format `+201XXXXXXXXX`.
- [ ] All background tasks are cleanly terminated.
</ACCEPTANCE_CRITERIA>
```

---

## Phase 3: Custom Medusa v2 Paymob Module

---
### Developer Prompt 9: Scaffold Custom Paymob Payment Module Architecture

```markdown
/goal

<TASK>
Scaffold custom Paymob payment module structure in Medusa v2 backend.
</TASK>

<ANTIGRAVITY_SLASH_COMMANDS>
- /goal: Execute autonomously until Paymob module scaffolding compiles without errors.
- /browser: Use browser search if Medusa v2 AbstractPaymentProvider documentation needs verification.
- /learn: Persist Paymob module interface patterns to .gemini/rules.
</ANTIGRAVITY_SLASH_COMMANDS>

<ANTIGRAVITY_WORKFLOW>
1. RESEARCH & INSPECTION PHASE:
   - Search Medusa v2 documentation or use `/browser` to inspect `AbstractPaymentProvider` patterns.

2. IMPLEMENTATION PHASE:
   - Target files: `apps/backend/src/modules/paymob/index.ts`, `apps/backend/src/modules/paymob/service.ts`
   - Create module directory and service class extending `AbstractPaymentProvider`.
   - Export module definition.

3. EMPIRICAL VERIFICATION & TESTING PHASE:
   - Run build check: `cd apps/backend && npm run build`

4. PROCESS CLEANUP & LEARNING DIRECTIVE (CRITICAL):
   - Execute `/learn` to store Paymob payment provider interface details.
   - Kill background tasks/servers before ending turn.
</ANTIGRAVITY_WORKFLOW>

<ACCEPTANCE_CRITERIA>
- [ ] Paymob module scaffold compiles under Medusa v2 framework.
- [ ] All background tasks are cleanly terminated.
</ACCEPTANCE_CRITERIA>
```

---
### Developer Prompt 10: Implement Paymob Token Auth & Order Registration Client

```markdown
/goal

<TASK>
Implement HTTP API client for Paymob auth token exchange and order registration in piastres.
</TASK>

<ANTIGRAVITY_SLASH_COMMANDS>
- /goal: Execute autonomously until Paymob API client functions pass TypeScript compilation.
- /browser: Verify Paymob REST API v2 auth and order endpoints if needed.
</ANTIGRAVITY_SLASH_COMMANDS>

<ANTIGRAVITY_WORKFLOW>
1. RESEARCH & INSPECTION PHASE:
   - Inspect Paymob API v2 endpoints (`POST /api/auth/tokens`, `POST /api/ecommerce/orders`).

2. IMPLEMENTATION PHASE:
   - Target file: `apps/backend/src/modules/paymob/client.ts`
   - Implement `authenticate(apiKey)` returning auth token.
   - Implement `registerOrder(token, amountCents, currency)` converting EGP to piastres (`amount * 100`).

3. EMPIRICAL VERIFICATION & TESTING PHASE:
   - Run TypeScript check: `cd apps/backend && npx tsc --noEmit`

4. PROCESS CLEANUP & LEARNING DIRECTIVE (CRITICAL):
   - Kill any active processes before ending turn.
</ANTIGRAVITY_WORKFLOW>

<ACCEPTANCE_CRITERIA>
- [ ] API client functions convert EGP to piastres accurately.
- [ ] TypeScript compilation passes cleanly.
- [ ] All background tasks are cleanly terminated.
</ACCEPTANCE_CRITERIA>
```

---
### Developer Prompt 11: Implement Paymob Payment Key & Iframe Token Generator

```markdown
/goal

<TASK>
Implement Payment Key request generator for Cards, Mobile Wallets, and ValU.
</TASK>

<ANTIGRAVITY_SLASH_COMMANDS>
- /goal: Execute autonomously until payment key generator formats billing payloads correctly.
</ANTIGRAVITY_SLASH_COMMANDS>

<ANTIGRAVITY_WORKFLOW>
1. RESEARCH & INSPECTION PHASE:
   - Review Paymob API v2 `/api/acceptance/payment_keys` payload requirements.

2. IMPLEMENTATION PHASE:
   - Target files: `apps/backend/src/modules/paymob/client.ts`, `apps/backend/src/modules/paymob/service.ts`
   - Implement `generatePaymentKey(token, orderId, amountCents, integrationId, billingData)`.
   - Wire `initiatePayment` method in service to return iframe URL or wallet token.

3. EMPIRICAL VERIFICATION & TESTING PHASE:
   - Run TypeScript check: `cd apps/backend && npx tsc --noEmit`

4. PROCESS CLEANUP & LEARNING DIRECTIVE (CRITICAL):
   - Kill any active processes before ending turn.
</ANTIGRAVITY_WORKFLOW>

<ACCEPTANCE_CRITERIA>
- [ ] Payment key generator formats billing payload accurately.
- [ ] All background tasks are cleanly terminated.
</ACCEPTANCE_CRITERIA>
```

---
### Developer Prompt 12: Implement Paymob Webhook Controller & SHA-512 HMAC Verification

```markdown
/goal

<TASK>
Build webhook route controller with SHA-512 HMAC signature verification.
</TASK>

<ANTIGRAVITY_SLASH_COMMANDS>
- /goal: Execute autonomously until SHA-512 HMAC calculator and webhook route pass tests.
- /learn: Persist HMAC signature calculation algorithm to .gemini/rules.
</ANTIGRAVITY_SLASH_COMMANDS>

<ANTIGRAVITY_WORKFLOW>
1. RESEARCH & INSPECTION PHASE:
   - Inspect 20 required Paymob callback fields for SHA-512 HMAC calculation.

2. IMPLEMENTATION PHASE:
   - Target files: `apps/backend/src/api/hooks/paymob/route.ts`, `apps/backend/src/modules/paymob/hmac.ts`
   - Implement `verifyPaymobHmac(payload, secret): boolean` sorting 20 attributes alphabetically.
   - Create route `POST /api/hooks/paymob` verifying HMAC and capturing payment on success.

3. EMPIRICAL VERIFICATION & TESTING PHASE:
   - Run TypeScript check: `cd apps/backend && npx tsc --noEmit`

4. PROCESS CLEANUP & LEARNING DIRECTIVE (CRITICAL):
   - Execute `/learn` to store Paymob HMAC verification logic.
   - Kill any background servers before ending turn.
</ANTIGRAVITY_WORKFLOW>

<ACCEPTANCE_CRITERIA>
- [ ] HMAC calculator sorts attributes alphabetically and generates SHA-512 hash.
- [ ] Webhook route handles valid/invalid signatures correctly.
- [ ] All background tasks are cleanly terminated.
</ACCEPTANCE_CRITERIA>
```

---
### Developer Prompt 13: Wire Paymob Mobile Wallets, Credit Cards, and ValU BNPL Integration Keys

```markdown
/goal

<TASK>
Register Paymob integration options in Medusa configuration.
</TASK>

<ANTIGRAVITY_SLASH_COMMANDS>
- /goal: Execute autonomously until Medusa backend builds cleanly with Paymob options.
</ANTIGRAVITY_SLASH_COMMANDS>

<ANTIGRAVITY_WORKFLOW>
1. RESEARCH & INSPECTION PHASE:
   - View `apps/backend/medusa-config.ts`.

2. IMPLEMENTATION PHASE:
   - Target files: `apps/backend/src/modules/paymob/types.ts`, `apps/backend/medusa-config.ts`
   - Define options type: `cardIntegrationId`, `walletIntegrationId`, `valuIntegrationId`, `iframeId`, `hmacSecret`.
   - Register module in `medusa-config.ts`.

3. EMPIRICAL VERIFICATION & TESTING PHASE:
   - Run backend build: `cd apps/backend && npm run build`

4. PROCESS CLEANUP & LEARNING DIRECTIVE (CRITICAL):
   - Kill background dev servers or processes before completing turn.
</ANTIGRAVITY_WORKFLOW>

<ACCEPTANCE_CRITERIA>
- [ ] Medusa config includes registered Paymob module options.
- [ ] All background tasks are cleanly terminated.
</ACCEPTANCE_CRITERIA>
```

---

## Phase 4: Custom Medusa v2 Bosta Fulfillment Module

---
### Developer Prompt 14: Scaffold Custom Bosta Fulfillment Module Architecture

```markdown
/goal

<TASK>
Scaffold Bosta fulfillment module extending Medusa v2 AbstractFulfillmentProvider.
</TASK>

<ANTIGRAVITY_SLASH_COMMANDS>
- /goal: Execute autonomously until Bosta fulfillment module compiles clean.
- /learn: Persist Bosta fulfillment module patterns to .gemini/rules.
</ANTIGRAVITY_SLASH_COMMANDS>

<ANTIGRAVITY_WORKFLOW>
1. RESEARCH & INSPECTION PHASE:
   - Inspect Medusa v2 `AbstractFulfillmentProvider` specification.

2. IMPLEMENTATION PHASE:
   - Target files: `apps/backend/src/modules/bosta/index.ts`, `apps/backend/src/modules/bosta/service.ts`
   - Create module directory and service class. Export module in `index.ts`.

3. EMPIRICAL VERIFICATION & TESTING PHASE:
   - Run backend build: `cd apps/backend && npm run build`

4. PROCESS CLEANUP & LEARNING DIRECTIVE (CRITICAL):
   - Execute `/learn` to store Bosta fulfillment provider interface details.
   - Kill any running tasks before completing turn.
</ANTIGRAVITY_WORKFLOW>

<ACCEPTANCE_CRITERIA>
- [ ] Bosta fulfillment module scaffold compiles cleanly.
- [ ] All background tasks are cleanly terminated.
</ACCEPTANCE_CRITERIA>
```

---
### Developer Prompt 15: Implement Bosta Governorate ID to Location Code Mapper

```markdown
/goal

<TASK>
Implement mapping helper translating Egyptian Governorates to Bosta location codes.
</TASK>

<ANTIGRAVITY_SLASH_COMMANDS>
- /goal: Execute autonomously until location mapper handles all 27 governorates.
</ANTIGRAVITY_SLASH_COMMANDS>

<ANTIGRAVITY_WORKFLOW>
1. RESEARCH & INSPECTION PHASE:
   - Review Bosta API governorate city ID keys.

2. IMPLEMENTATION PHASE:
   - Target file: `apps/backend/src/modules/bosta/location-mapper.ts`
   - Build lookup table mapping all 27 governorates to Bosta city codes with fallback handling.

3. EMPIRICAL VERIFICATION & TESTING PHASE:
   - Run TypeScript check: `cd apps/backend && npx tsc --noEmit`

4. PROCESS CLEANUP & LEARNING DIRECTIVE (CRITICAL):
   - Kill active processes before ending turn.
</ANTIGRAVITY_WORKFLOW>

<ACCEPTANCE_CRITERIA>
- [ ] Location mapper covers all 27 governorates.
- [ ] All background tasks are cleanly terminated.
</ACCEPTANCE_CRITERIA>
```

---
### Developer Prompt 16: Implement Bosta Delivery Creation API & Airway Bill (AWB) Label Generator

```markdown
/goal

<TASK>
Implement `createFulfillment` API call making Bosta delivery requests and receiving AWB tracking labels.
</TASK>

<ANTIGRAVITY_SLASH_COMMANDS>
- /goal: Execute autonomously until Bosta delivery creation payload passes type checks.
- /browser: Verify Bosta REST API delivery endpoint `/api/v2/deliveries` schema if needed.
</ANTIGRAVITY_SLASH_COMMANDS>

<ANTIGRAVITY_WORKFLOW>
1. RESEARCH & INSPECTION PHASE:
   - Inspect Bosta REST API `/api/v2/deliveries` payload requirements.

2. IMPLEMENTATION PHASE:
   - Target files: `apps/backend/src/modules/bosta/client.ts`, `apps/backend/src/modules/bosta/service.ts`
   - Implement `createBostaDelivery(payload): Promise<{ trackingNumber, waybillUrl }>`.
   - Connect to `BostaFulfillmentModuleService.createFulfillment()`.

3. EMPIRICAL VERIFICATION & TESTING PHASE:
   - Run TypeScript check: `cd apps/backend && npx tsc --noEmit`

4. PROCESS CLEANUP & LEARNING DIRECTIVE (CRITICAL):
   - Kill any active processes before ending turn.
</ANTIGRAVITY_WORKFLOW>

<ACCEPTANCE_CRITERIA>
- [ ] Delivery creation returns tracking number and waybill URL structure.
- [ ] All background tasks are cleanly terminated.
</ACCEPTANCE_CRITERIA>
```

---
### Developer Prompt 17: Implement Bosta Tracking Callback Webhook Handler & Status Sync

```markdown
/goal

<TASK>
Create webhook endpoint handling Bosta status callbacks (`DELIVERED`, `CANCELLED`).
</TASK>

<ANTIGRAVITY_SLASH_COMMANDS>
- /goal: Execute autonomously until Bosta webhook route passes TypeScript check.
</ANTIGRAVITY_SLASH_COMMANDS>

<ANTIGRAVITY_WORKFLOW>
1. RESEARCH & INSPECTION PHASE:
   - Review Bosta webhook status payloads.

2. IMPLEMENTATION PHASE:
   - Target file: `apps/backend/src/api/hooks/bosta/route.ts`
   - Create route `POST /api/hooks/bosta`.
   - Update Medusa order fulfillment & COD status upon delivery callbacks.

3. EMPIRICAL VERIFICATION & TESTING PHASE:
   - Run TypeScript check: `cd apps/backend && npx tsc --noEmit`

4. PROCESS CLEANUP & LEARNING DIRECTIVE (CRITICAL):
   - Kill background servers or processes before completing turn.
</ANTIGRAVITY_WORKFLOW>

<ACCEPTANCE_CRITERIA>
- [ ] Webhook route processes Bosta delivery status updates dynamically.
- [ ] All background tasks are cleanly terminated.
</ACCEPTANCE_CRITERIA>
```

---

## Phase 5: Egyptian Tax Authority (ETA) Compliance Subscriber

---
### Developer Prompt 18: Implement ETA Compliance Module & Database Audit Schema

```markdown
/goal

<TASK>
Create module and database schema for ETA e-Receipt submission audit logs.
</TASK>

<ANTIGRAVITY_SLASH_COMMANDS>
- /goal: Execute autonomously until ETA audit database schema compiles clean.
</ANTIGRAVITY_SLASH_COMMANDS>

<ANTIGRAVITY_WORKFLOW>
1. RESEARCH & INSPECTION PHASE:
   - Review database requirements for ETA e-Receipt logging.

2. IMPLEMENTATION PHASE:
   - Target files: `apps/backend/src/modules/eta-tax/index.ts`, `apps/backend/src/modules/eta-tax/models/eta-audit.ts`
   - Define entity `EtaReceiptAudit` with fields `id`, `orderId`, `receiptUuid`, `taxRegistrationNumber`, `totalVatCents`, `status`.

3. EMPIRICAL VERIFICATION & TESTING PHASE:
   - Run backend build: `cd apps/backend && npm run build`

4. PROCESS CLEANUP & LEARNING DIRECTIVE (CRITICAL):
   - Kill active processes before ending turn.
</ANTIGRAVITY_WORKFLOW>

<ACCEPTANCE_CRITERIA>
- [ ] ETA audit database schema registered in Medusa v2.
- [ ] All background tasks are cleanly terminated.
</ACCEPTANCE_CRITERIA>
```

---
### Developer Prompt 19: Implement `order.placed` Event Subscriber for Tax Payload Transformation

```markdown
/goal

<TASK>
Create event subscriber listening to `order.placed` for ETA tax processing.
</TASK>

<ANTIGRAVITY_SLASH_COMMANDS>
- /goal: Execute autonomously until order.placed subscriber passes type checks.
</ANTIGRAVITY_SLASH_COMMANDS>

<ANTIGRAVITY_WORKFLOW>
1. RESEARCH & INSPECTION PHASE:
   - Search Medusa v2 event subscriber patterns.

2. IMPLEMENTATION PHASE:
   - Target file: `apps/backend/src/subscribers/order-placed-eta.ts`
   - Create subscriber handling `order.placed` and passing order payload to ETA module.

3. EMPIRICAL VERIFICATION & TESTING PHASE:
   - Run TypeScript check: `cd apps/backend && npx tsc --noEmit`

4. PROCESS CLEANUP & LEARNING DIRECTIVE (CRITICAL):
   - Kill active tasks before completing turn.
</ANTIGRAVITY_WORKFLOW>

<ACCEPTANCE_CRITERIA>
- [ ] Subscriber listens to `order.placed` event.
- [ ] All background tasks are cleanly terminated.
</ACCEPTANCE_CRITERIA>
```

---
### Developer Prompt 20: Implement EGS/GS1 Tax Taxonomy Mapper & 14% VAT Payload Builder

```markdown
/goal

<TASK>
Implement tax payload builder formatting e-Receipt JSON according to ETA standards.
</TASK>

<ANTIGRAVITY_SLASH_COMMANDS>
- /goal: Execute autonomously until ETA tax payload builder output matches schema specs.
- /browser: Verify ETA Portal JSON e-Receipt schema if needed.
</ANTIGRAVITY_SLASH_COMMANDS>

<ANTIGRAVITY_WORKFLOW>
1. RESEARCH & INSPECTION PHASE:
   - Inspect ETA e-Receipt JSON payload schema specifications.

2. IMPLEMENTATION PHASE:
   - Target file: `apps/backend/src/modules/eta-tax/payload-builder.ts`
   - Construct ETA JSON body with documentType (`I`), 14% VAT calculations (`T1`/`V009`), and canonical UUID v4.

3. EMPIRICAL VERIFICATION & TESTING PHASE:
   - Run TypeScript check: `cd apps/backend && npx tsc --noEmit`

4. PROCESS CLEANUP & LEARNING DIRECTIVE (CRITICAL):
   - Kill background tasks before completing turn.
</ANTIGRAVITY_WORKFLOW>

<ACCEPTANCE_CRITERIA>
- [ ] Payload builder constructs ETA-compliant e-Receipt JSON structures.
- [ ] All background tasks are cleanly terminated.
</ACCEPTANCE_CRITERIA>
```

---
### Developer Prompt 21: Implement ETA e-Receipt Portal Submission Client & Audit Logger

```markdown
/goal

<TASK>
Implement HTTP client transmitting receipts to ETA Portal and writing audit logs.
</TASK>

<ANTIGRAVITY_SLASH_COMMANDS>
- /goal: Execute autonomously until ETA submission client passes type check.
</ANTIGRAVITY_SLASH_COMMANDS>

<ANTIGRAVITY_WORKFLOW>
1. RESEARCH & INSPECTION PHASE:
   - Inspect ETA API submission endpoint `/api/v1/receipts/submission`.

2. IMPLEMENTATION PHASE:
   - Target files: `apps/backend/src/modules/eta-tax/client.ts`, `apps/backend/src/modules/eta-tax/service.ts`
   - Implement `submitReceipt(payload)` and record status (`FILED` / `PENDING_TAX_ID`) in `EtaReceiptAudit`.

3. EMPIRICAL VERIFICATION & TESTING PHASE:
   - Run TypeScript check: `cd apps/backend && npx tsc --noEmit`

4. PROCESS CLEANUP & LEARNING DIRECTIVE (CRITICAL):
   - Kill active processes before ending turn.
</ANTIGRAVITY_WORKFLOW>

<ACCEPTANCE_CRITERIA>
- [ ] ETA client submits payloads and records database audit logs.
- [ ] All background tasks are cleanly terminated.
</ACCEPTANCE_CRITERIA>
```

---

## Phase 6: AI Studio Extensions

---
### Developer Prompt 22: Implement Admin Widget for AI Arabic Product Copywriter & SEO Generator

```markdown
/goal

<TASK>
Build Medusa Admin Extension widget for 1-click Arabic/English description & SEO generation.
</TASK>

<ANTIGRAVITY_SLASH_COMMANDS>
- /goal: Execute autonomously until Admin widget compiles clean without UI errors.
</ANTIGRAVITY_SLASH_COMMANDS>

<ANTIGRAVITY_WORKFLOW>
1. RESEARCH & INSPECTION PHASE:
   - Inspect Medusa Admin Widget extension API.

2. IMPLEMENTATION PHASE:
   - Target file: `apps/backend/src/admin/widgets/ai-copywriter.tsx`
   - Create React widget UI invoking LLM API to generate Egyptian Arabic descriptions, English translations, and SEO metadata.

3. EMPIRICAL VERIFICATION & TESTING PHASE:
   - Run backend build: `cd apps/backend && npm run build`

4. PROCESS CLEANUP & LEARNING DIRECTIVE (CRITICAL):
   - Kill background servers or processes before completing turn.
</ANTIGRAVITY_WORKFLOW>

<ACCEPTANCE_CRITERIA>
- [ ] Admin widget compiles clean without UI build errors.
- [ ] All background tasks are cleanly terminated.
</ACCEPTANCE_CRITERIA>
```

---
### Developer Prompt 23: Implement AI Theme Customizer (Logo Palette Extractor & Arabic Google Fonts)

```markdown
/goal

<TASK>
Build AI Theme assistant helper analyzing logo palettes and suggesting Arabic Google Fonts.
</TASK>

<ANTIGRAVITY_SLASH_COMMANDS>
- /goal: Execute autonomously until Theme assistant outputs valid theme.json token mappings.
</ANTIGRAVITY_SLASH_COMMANDS>

<ANTIGRAVITY_WORKFLOW>
1. RESEARCH & INSPECTION PHASE:
   - View `apps/storefront/src/lib/theme/ai-theme-assistant.ts`.

2. IMPLEMENTATION PHASE:
   - Target file: `apps/storefront/src/lib/theme/ai-theme-assistant.ts`
   - Implement color extraction function mapping logo tones to `theme.json` CSS variables and pairing fonts (*Cairo*, *Tajawal*, *Alexandria*, *Readex Pro*).

3. EMPIRICAL VERIFICATION & TESTING PHASE:
   - Run TypeScript check: `cd apps/storefront && npx tsc --noEmit`

4. PROCESS CLEANUP & LEARNING DIRECTIVE (CRITICAL):
   - Kill active processes before completing turn.
</ANTIGRAVITY_WORKFLOW>

<ACCEPTANCE_CRITERIA>
- [ ] Theme assistant outputs valid `theme.json` CSS variable mappings.
- [ ] All background tasks are cleanly terminated.
</ACCEPTANCE_CRITERIA>
```

---
### Developer Prompt 24: Implement Redis Vector AI Smart Search Bar with `dir="auto"` BiDi Fix

```markdown
/goal

<TASK>
Build Storefront Search component with typo tolerance, dialect understanding, and BiDi text isolate fix.
</TASK>

<ANTIGRAVITY_SLASH_COMMANDS>
- /goal: Execute autonomously until Smart Search Bar component compiles cleanly.
</ANTIGRAVITY_SLASH_COMMANDS>

<ANTIGRAVITY_WORKFLOW>
1. RESEARCH & INSPECTION PHASE:
   - Research `dir="auto"` and CSS `unicode-bidi: plaintext` for mixed RTL/LTR input fields.

2. IMPLEMENTATION PHASE:
   - Target file: `apps/storefront/src/modules/search/components/smart-search-bar.tsx`
   - Create React search bar component with `dir="auto"` and `unicode-bidi: plaintext` styling.
   - Connect input to vector/fuzzy search API.

3. EMPIRICAL VERIFICATION & TESTING PHASE:
   - Run storefront build: `cd apps/storefront && npm run build`

4. PROCESS CLEANUP & LEARNING DIRECTIVE (CRITICAL):
   - Kill background dev servers or processes before completing turn.
</ANTIGRAVITY_WORKFLOW>

<ACCEPTANCE_CRITERIA>
- [ ] Search input handles mixed Arabic/English text without visual scrambling or cursor jumps.
- [ ] Storefront build passes cleanly.
- [ ] All background tasks are cleanly terminated.
</ACCEPTANCE_CRITERIA>
```

---
### Developer Prompt 25: Implement Storefront 30-Day Cross-Tab Synchronized Cart Engine

```markdown
/goal

<TASK>
Build React Cart state context using `BroadcastChannel` API and 30-day persistent cookies.
</TASK>

<ANTIGRAVITY_SLASH_COMMANDS>
- /goal: Execute autonomously until Cart context passes storefront build verification.
- /learn: Persist BroadcastChannel cart sync patterns to .gemini/rules.
</ANTIGRAVITY_SLASH_COMMANDS>

<ANTIGRAVITY_WORKFLOW>
1. RESEARCH & INSPECTION PHASE:
   - Research JavaScript `BroadcastChannel('medusa_cart')` API for real-time tab state synchronization.

2. IMPLEMENTATION PHASE:
   - Target file: `apps/storefront/src/lib/context/cart-context.tsx`
   - Implement Cart Context listening to cross-tab mutations and updating UI drawer/badge state instantly without page reloads.
   - Ensure guest cart items merge seamlessly on customer login.

3. EMPIRICAL VERIFICATION & TESTING PHASE:
   - Run storefront build: `cd apps/storefront && npm run build`

4. PROCESS CLEANUP & LEARNING DIRECTIVE (CRITICAL):
   - Execute `/learn` to store cross-tab cart synchronization patterns.
   - Kill background dev servers or processes before completing turn.
</ANTIGRAVITY_WORKFLOW>

<ACCEPTANCE_CRITERIA>
- [ ] Cart updates synchronize across tabs in real time.
- [ ] Guest cart merges into customer account upon login without data loss.
- [ ] All background tasks are cleanly terminated.
</ACCEPTANCE_CRITERIA>
```

---

## Phase 7: Multi-Tenant SaaS Provisioning Automation

---
### Developer Prompt 26: Scaffold Single-Tenant Docker Compose Infrastructure Templates

```markdown
/goal

<TASK>
Create Docker Compose templates for single-tenant merchant container isolation.
</TASK>

<ANTIGRAVITY_SLASH_COMMANDS>
- /goal: Execute autonomously until Docker Compose template passes validation.
</ANTIGRAVITY_SLASH_COMMANDS>

<ANTIGRAVITY_WORKFLOW>
1. RESEARCH & INSPECTION PHASE:
   - Review Docker Compose service structures for Medusa v2 + Next.js + PostgreSQL + Redis.

2. IMPLEMENTATION PHASE:
   - Target files: `infrastructure/docker/docker-compose.tenant.yml`, `infrastructure/docker/Dockerfile.backend`, `infrastructure/docker/Dockerfile.storefront`
   - Create Dockerfiles and compose configuration for tenant isolation.

3. EMPIRICAL VERIFICATION & TESTING PHASE:
   - Run docker validation: `docker compose -f infrastructure/docker/docker-compose.tenant.yml config`

4. PROCESS CLEANUP & LEARNING DIRECTIVE (CRITICAL):
   - Kill active background tasks before completing turn.
</ANTIGRAVITY_WORKFLOW>

<ACCEPTANCE_CRITERIA>
- [ ] Docker Compose template validates without syntax or port errors.
- [ ] All background tasks are cleanly terminated.
</ACCEPTANCE_CRITERIA>
```

---
### Developer Prompt 27: Implement Master Dashboard Central Tenant Provisioning Agent

```markdown
/goal

<TASK>
Build provisioning shell script for deploying new tenant instances on local VPS nodes.
</TASK>

<ANTIGRAVITY_SLASH_COMMANDS>
- /goal: Execute autonomously until provisioning shell script passes syntax check.
</ANTIGRAVITY_SLASH_COMMANDS>

<ANTIGRAVITY_WORKFLOW>
1. RESEARCH & INSPECTION PHASE:
   - Review bash automation steps for Git cloning, `.env` generation, DB migrations, and Docker startup.

2. IMPLEMENTATION PHASE:
   - Target file: `infrastructure/scripts/provision-tenant.sh`
   - Implement shell script executing tenant directory creation, env generation, `medusa db:migrate`, and docker compose startup.

3. EMPIRICAL VERIFICATION & TESTING PHASE:
   - Run syntax check: `bash -n infrastructure/scripts/provision-tenant.sh`

4. PROCESS CLEANUP & LEARNING DIRECTIVE (CRITICAL):
   - Kill background processes before completing turn.
</ANTIGRAVITY_WORKFLOW>

<ACCEPTANCE_CRITERIA>
- [ ] Provisioning script passes bash syntax check (`bash -n`).
- [ ] All background tasks are cleanly terminated.
</ACCEPTANCE_CRITERIA>
```

---
### Developer Prompt 28: Implement Subscription Paymob Listener & Soft-Suspension Engine

```markdown
/goal

<TASK>
Implement subscription listener toggling soft-suspension on tenant instances upon payment failure.
</TASK>

<ANTIGRAVITY_SLASH_COMMANDS>
- /goal: Execute autonomously until subscription listener passes type checks.
- /learn: Persist soft-suspension lifecycle and DB preservation rules to .gemini/rules.
</ANTIGRAVITY_SLASH_COMMANDS>

<ANTIGRAVITY_WORKFLOW>
1. RESEARCH & INSPECTION PHASE:
   - Review subscription lifecycle rules: 3-day grace period, warning banner, soft-suspension, indefinite DB preservation.

2. IMPLEMENTATION PHASE:
   - Target file: `apps/backend/src/subscribers/subscription-listener.ts`
   - Create subscriber toggling tenant environment to `SOFT_SUSPENDED` upon lapsed subscription payments without touching database tables.

3. EMPIRICAL VERIFICATION & TESTING PHASE:
   - Run TypeScript check: `cd apps/backend && npx tsc --noEmit`

4. PROCESS CLEANUP & LEARNING DIRECTIVE (CRITICAL):
   - Execute `/learn` to store soft-suspension lifecycle rules.
   - Terminate any running background dev servers, processes, or background tasks before completing turn.
</ANTIGRAVITY_WORKFLOW>

<ACCEPTANCE_CRITERIA>
- [ ] Soft-suspension listener updates tenant state while preserving PostgreSQL database intact.
- [ ] All background tasks, processes, and dev servers are cleanly terminated upon completion.
</ACCEPTANCE_CRITERIA>
```

---

## Phase 8: Production Hardening & Performance Polish

---
### Developer Prompt 29: Implement Paymob Webhook Idempotency (Redis Lock) & Strict Production HMAC Enforcement

```markdown
/goal

<TASK>
Implement Redis-backed webhook idempotency deduplication and strict production HMAC signature enforcement in Paymob webhook controller.
</TASK>

<ANTIGRAVITY_SLASH_COMMANDS>
- /goal: Execute autonomously until Paymob webhook idempotency and strict HMAC enforcement pass build tests.
- /learn: Persist Redis webhook deduplication pattern to .gemini/rules.
</ANTIGRAVITY_SLASH_COMMANDS>

<ANTIGRAVITY_WORKFLOW>
1. RESEARCH & INSPECTION PHASE:
   - View `apps/backend/src/api/hooks/paymob/route.ts` and inspect Redis container access in Medusa v2.

2. IMPLEMENTATION PHASE:
   - Target file: `apps/backend/src/api/hooks/paymob/route.ts`
   - Add Redis key check `paymob_tx_<transactionId>` with a 24-hour TTL (86,400s). If key exists, return HTTP `200 OK` with `{ deduplicated: true }`.
   - In production (`process.env.NODE_ENV === "production"`), strictly reject requests with HTTP `401 Unauthorized` if `PAYMOB_HMAC_SECRET` is missing or signature verification fails.

3. EMPIRICAL VERIFICATION & TESTING PHASE:
   - Run TypeScript check: `cd apps/backend && npx tsc --noEmit`
   - Run backend build verification: `cd apps/backend && npm run build`

4. PROCESS CLEANUP & LEARNING DIRECTIVE (CRITICAL):
   - Execute `/learn` to store Paymob webhook deduplication logic.
   - Terminate any running background dev servers, processes, or background tasks before completing turn.
</ANTIGRAVITY_WORKFLOW>

<ACCEPTANCE_CRITERIA>
- [ ] Paymob webhook route checks Redis key `paymob_tx_<id>` to prevent duplicate transaction processing.
- [ ] Production environment strictly rejects non-verified HMAC webhooks with HTTP 401.
- [ ] Backend build completes with exit code 0.
- [ ] All background tasks and processes are cleanly terminated.
</ACCEPTANCE_CRITERIA>
```

---
### Developer Prompt 30: Implement Bosta Shipping Rate Redis Caching per Governorate

```markdown
/goal

<TASK>
Implement Redis caching for Bosta governorate shipping rate calculations to optimize cart drawer performance.
</TASK>

<ANTIGRAVITY_SLASH_COMMANDS>
- /goal: Execute autonomously until Bosta shipping rate Redis caching compiles clean.
</ANTIGRAVITY_SLASH_COMMANDS>

<ANTIGRAVITY_WORKFLOW>
1. RESEARCH & INSPECTION PHASE:
   - View `apps/backend/src/modules/bosta/service.ts`.

2. IMPLEMENTATION PHASE:
   - Target file: `apps/backend/src/modules/bosta/service.ts`
   - In `calculatePrice()`, check Redis for cache key `bosta_rate_<governorate_id>`.
   - If cache hit: Return cached shipping price immediately.
   - If cache miss: Calculate price, store result in Redis with 1-hour TTL (3,600s), and return amount.

3. EMPIRICAL VERIFICATION & TESTING PHASE:
   - Run TypeScript check: `cd apps/backend && npx tsc --noEmit`
   - Run backend build verification: `cd apps/backend && npm run build`

4. PROCESS CLEANUP & LEARNING DIRECTIVE (CRITICAL):
   - Terminate any running background processes or dev servers before ending turn.
</ANTIGRAVITY_WORKFLOW>

<ACCEPTANCE_CRITERIA>
- [ ] Bosta shipping rate calculation uses Redis caching with 1-hour TTL per governorate.
- [ ] Backend build completes with exit code 0.
- [ ] All background tasks and processes are cleanly terminated.
</ACCEPTANCE_CRITERIA>
```

---
### Developer Prompt 31: Add Google Fonts Preconnect & Font-Display Swap in Next.js Storefront Layout

```markdown
/goal

<TASK>
Add Google Fonts preconnect headers and font-display swap rules for sub-second Arabic text rendering.
</TASK>

<ANTIGRAVITY_SLASH_COMMANDS>
- /goal: Execute autonomously until Next.js layout builds cleanly with font preconnect tags.
</ANTIGRAVITY_SLASH_COMMANDS>

<ANTIGRAVITY_WORKFLOW>
1. RESEARCH & INSPECTION PHASE:
   - View `apps/storefront/src/app/layout.tsx`.

2. IMPLEMENTATION PHASE:
   - Target file: `apps/storefront/src/app/layout.tsx`
   - Add `<link rel="preconnect" href="https://fonts.googleapis.com">` and `<link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="anonymous">`.
   - Add Google Fonts stylesheet link for Arabic fonts (*Cairo*, *Tajawal*, *Alexandria*, *Readex Pro*) with `display=swap`.

3. EMPIRICAL VERIFICATION & TESTING PHASE:
   - Run storefront build verification: `cd apps/storefront && npm run build`

4. PROCESS CLEANUP & LEARNING DIRECTIVE (CRITICAL):
   - Terminate any running background dev servers (e.g. stop `next dev`) or processes before completing turn.
</ANTIGRAVITY_WORKFLOW>

<ACCEPTANCE_CRITERIA>
- [ ] Next.js storefront layout includes Google Fonts preconnect links and Arabic font swap definitions.
- [ ] Storefront build completes with exit code 0.
- [ ] All background tasks and dev servers are cleanly terminated.
</ACCEPTANCE_CRITERIA>
```

---
### Developer Prompt 32: Implement Schema.org Arabic JSON-LD Structured Data Component for Product Pages

```markdown
/goal

<TASK>
Create React JSON-LD component generating Schema.org Product structured data in EGP currency and Egyptian Arabic.
</TASK>

<ANTIGRAVITY_SLASH_COMMANDS>
- /goal: Execute autonomously until Product JSON-LD component builds cleanly.
- /learn: Persist Schema.org EGP e-commerce SEO patterns to .gemini/rules.
</ANTIGRAVITY_SLASH_COMMANDS>

<ANTIGRAVITY_WORKFLOW>
1. RESEARCH & INSPECTION PHASE:
   - Inspect Schema.org `Product` and `Offer` specifications for multi-currency EGP e-commerce.

2. IMPLEMENTATION PHASE:
   - Target files: `apps/storefront/src/modules/products/components/product-json-ld.tsx`, `apps/storefront/src/app/[countryCode]/products/[handle]/page.tsx`
   - Create `ProductJsonLd` component outputting `<script type="application/ld+json">` with `@type: "Product"`, `name`, `description` (Arabic), `offers`: `{ "@type": "Offer", "priceCurrency": "EGP", "price": amount, "availability": "https://schema.org/InStock" }`.
   - Embed component in product detail page route.

3. EMPIRICAL VERIFICATION & TESTING PHASE:
   - Run storefront build verification: `cd apps/storefront && npm run build`

4. PROCESS CLEANUP & LEARNING DIRECTIVE (CRITICAL):
   - Execute `/learn` to store Schema.org EGP structured data patterns.
   - Terminate any running background dev servers or processes before completing turn.
</ANTIGRAVITY_WORKFLOW>

<ACCEPTANCE_CRITERIA>
- [ ] Product JSON-LD component generates compliant Schema.org structured data snippets.
- [ ] Storefront build completes with exit code 0.
- [ ] All background tasks and dev servers are cleanly terminated.
</ACCEPTANCE_CRITERIA>
```

---

## Phase 9: Perfect 10/10 Enterprise Hardening Pack

---
### Developer Prompt 33: Implement Redis Transaction Idempotency Lock for Paymob Webhooks

```markdown
/goal

<TASK>
Implement Redis atomic transaction idempotency locking in Paymob webhook route to prevent duplicate callback processing.
</TASK>

<ANTIGRAVITY_SLASH_COMMANDS>
- /goal: Execute autonomously until Paymob webhook idempotency lock passes build checks.
- /learn: Persist Redis transaction locking patterns to .gemini/rules.
</ANTIGRAVITY_SLASH_COMMANDS>

<ANTIGRAVITY_WORKFLOW>
1. RESEARCH & INSPECTION PHASE:
   - View `apps/backend/src/api/hooks/paymob/route.ts` and inspect Redis container access in Medusa v2.

2. IMPLEMENTATION PHASE:
   - Target file: `apps/backend/src/api/hooks/paymob/route.ts`
   - Use Redis client to set atomic key `paymob_tx_<transactionId>` with `NX` (only if not exists) and 24-hour TTL (86,400s).
   - If key already exists, return HTTP `200 OK` immediately with `{ deduplicated: true, message: "Transaction already processed" }`.

3. EMPIRICAL VERIFICATION & TESTING PHASE:
   - Run TypeScript check: `cd apps/backend && npx tsc --noEmit`
   - Run backend build verification: `cd apps/backend && npm run build`

4. PROCESS CLEANUP & LEARNING DIRECTIVE (CRITICAL):
   - Execute `/learn` to record Redis transaction idempotency patterns.
   - Terminate any running background dev servers, processes, or background tasks before completing turn.
</ANTIGRAVITY_WORKFLOW>

<ACCEPTANCE_CRITERIA>
- [ ] Paymob webhook route uses atomic Redis `NX` lock on `paymob_tx_<id>` to prevent duplicate executions.
- [ ] Backend build completes with exit code 0.
- [ ] All background tasks and processes are cleanly terminated.
</ACCEPTANCE_CRITERIA>
```

---
### Developer Prompt 34: Implement Redis Rate Caching for Bosta Governorate Shipping Fees

```markdown
/goal

<TASK>
Implement Redis rate caching for Bosta governorate shipping fee calculations to eliminate REST API latency during peak flash sales.
</TASK>

<ANTIGRAVITY_SLASH_COMMANDS>
- /goal: Execute autonomously until Bosta shipping fee Redis caching compiles cleanly.
</ANTIGRAVITY_SLASH_COMMANDS>

<ANTIGRAVITY_WORKFLOW>
1. RESEARCH & INSPECTION PHASE:
   - View `apps/backend/src/modules/bosta/service.ts`.

2. IMPLEMENTATION PHASE:
   - Target file: `apps/backend/src/modules/bosta/service.ts`
   - In `calculatePrice()`, query Redis for cache key `BOSTA_RATE_<governorate_id>`.
   - On cache hit: Return cached shipping price immediately.
   - On cache miss: Calculate price from Bosta API/rules, store in Redis with 1-hour TTL (3,600s), and return result.

3. EMPIRICAL VERIFICATION & TESTING PHASE:
   - Run TypeScript check: `cd apps/backend && npx tsc --noEmit`
   - Run backend build verification: `cd apps/backend && npm run build`

4. PROCESS CLEANUP & LEARNING DIRECTIVE (CRITICAL):
   - Terminate any running background processes or dev servers before completing turn.
</ANTIGRAVITY_WORKFLOW>

<ACCEPTANCE_CRITERIA>
- [ ] Bosta shipping fee calculation queries and populates Redis cache key `BOSTA_RATE_<id>` with 1-hour TTL.
- [ ] Backend build completes with exit code 0.
- [ ] All background tasks and dev servers are cleanly terminated.
</ACCEPTANCE_CRITERIA>
```

---
### Developer Prompt 35: Implement PKCS#11 Hardware Token REST Proxy Client for Real-Time ETA e-Receipt Signing

```markdown
/goal

<TASK>
Implement PKCS#11 REST proxy signing client for physical USB HSM hardware tokens (Egypt Trust / MICS certificates) in ETA Tax module.
</TASK>

<ANTIGRAVITY_SLASH_COMMANDS>
- /goal: Execute autonomously until ETA PKCS#11 HSM signing client passes build tests.
- /browser: Verify ETA Portal PKCS#11 signature structure if needed.
- /learn: Persist ETA hardware signing patterns to .gemini/rules.
</ANTIGRAVITY_SLASH_COMMANDS>

<ANTIGRAVITY_WORKFLOW>
1. RESEARCH & INSPECTION PHASE:
   - View `apps/backend/src/modules/eta-tax/client.ts` and `apps/backend/src/modules/eta-tax/payload-builder.ts`.

2. IMPLEMENTATION PHASE:
   - Target files: `apps/backend/src/modules/eta-tax/client.ts`, `apps/backend/src/modules/eta-tax/hsm-signer.ts`
   - Create `hsm-signer.ts` client that connects to local PKCS#11 REST proxy daemon (`http://localhost:8585/sign`).
   - Sign canonical e-Receipt JSON payload with CAdES-BES / ES-BES signature structure before transmitting payload to ETA submission API.

3. EMPIRICAL VERIFICATION & TESTING PHASE:
   - Run TypeScript check: `cd apps/backend && npx tsc --noEmit`
   - Run backend build verification: `cd apps/backend && npm run build`

4. PROCESS CLEANUP & LEARNING DIRECTIVE (CRITICAL):
   - Execute `/learn` to store ETA PKCS#11 HSM signing patterns.
   - Terminate any running background dev servers or processes before completing turn.
</ANTIGRAVITY_WORKFLOW>

<ACCEPTANCE_CRITERIA>
- [ ] ETA tax client supports PKCS#11 REST proxy integration for physical USB HSM hardware token signing.
- [ ] Backend build completes with exit code 0.
- [ ] All background tasks and processes are cleanly terminated.
</ACCEPTANCE_CRITERIA>
```

---
### Developer Prompt 36: Implement Automated Caddy / Coolify Proxy Orchestrator for Self-Serve Custom Domains

```markdown
/goal

<TASK>
Implement automated Caddy reverse-proxy script for self-serve merchant custom domain routing and auto-SSL provisioning.
</TASK>

<ANTIGRAVITY_SLASH_COMMANDS>
- /goal: Execute autonomously until Caddy domain router script passes bash syntax check.
</ANTIGRAVITY_SLASH_COMMANDS>

<ANTIGRAVITY_WORKFLOW>
1. RESEARCH & INSPECTION PHASE:
   - Inspect `infrastructure/scripts/provision-tenant.sh` and Caddy REST API `/config/apps/http/servers`.

2. IMPLEMENTATION PHASE:
   - Target files: `infrastructure/scripts/caddy-domain-router.sh`, `infrastructure/scripts/provision-tenant.sh`
   - Create `caddy-domain-router.sh` accepting `TENANT_ID`, `CUSTOM_DOMAIN`, and `CONTAINER_PORT`.
   - Send API payload to Caddy REST API to provision dynamic reverse proxy route and automatic Let's Encrypt SSL certificate for merchant domain (`merchantbrand.com`).

3. EMPIRICAL VERIFICATION & TESTING PHASE:
   - Run bash syntax check: `bash -n infrastructure/scripts/caddy-domain-router.sh`
   - Run provisioning syntax check: `bash -n infrastructure/scripts/provision-tenant.sh`

4. PROCESS CLEANUP & LEARNING DIRECTIVE (CRITICAL):
   - Terminate any running background tasks or shell jobs before completing turn.
</ANTIGRAVITY_WORKFLOW>

<ACCEPTANCE_CRITERIA>
- [ ] `caddy-domain-router.sh` passes bash syntax check (`bash -n`) and provisions dynamic SSL reverse proxy routes.
- [ ] All background tasks are cleanly terminated.
</ACCEPTANCE_CRITERIA>
```

---
### Developer Prompt 37: Implement BullMQ Background Worker Queue for Asynchronous Admin AI Copywriter Jobs

```markdown
/goal

<TASK>
Implement BullMQ background worker queue for non-blocking asynchronous LLM copywriter generation in Medusa Admin.
</TASK>

<ANTIGRAVITY_SLASH_COMMANDS>
- /goal: Execute autonomously until BullMQ AI copywriter worker queue passes build verification.
- /learn: Persist BullMQ background worker patterns to .gemini/rules.
</ANTIGRAVITY_SLASH_COMMANDS>

<ANTIGRAVITY_WORKFLOW>
1. RESEARCH & INSPECTION PHASE:
   - Inspect `apps/backend/src/admin/widgets/ai-copywriter.tsx` and Redis connection options in Medusa v2.

2. IMPLEMENTATION PHASE:
   - Target files: `apps/backend/src/jobs/ai-copywriter-worker.ts`, `apps/backend/src/api/admin/ai-copywriter/route.ts`
   - Implement BullMQ queue `ai_copywriter_queue`.
   - API route dispatches copywriter job to queue; worker process handles LLM generation asynchronously and updates product metadata when complete.

3. EMPIRICAL VERIFICATION & TESTING PHASE:
   - Run TypeScript check: `cd apps/backend && npx tsc --noEmit`
   - Run backend build verification: `cd apps/backend && npm run build`

4. PROCESS CLEANUP & LEARNING DIRECTIVE (CRITICAL):
   - Execute `/learn` to store BullMQ background worker patterns.
   - Terminate any running background dev servers, processes, or background tasks before completing turn.
</ANTIGRAVITY_WORKFLOW>

<ACCEPTANCE_CRITERIA>
- [ ] Admin AI Copywriter dispatches tasks to BullMQ queue for asynchronous background execution.
- [ ] Backend build completes with exit code 0.
- [ ] All background tasks and dev servers are cleanly terminated.
</ACCEPTANCE_CRITERIA>
```

