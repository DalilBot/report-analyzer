# Dedicated Audit Line-Level Fix Prompts (`AUDIT_LINE_BY_LINE_PROMPTS_ONLY.md`)

This file contains **ONLY the 11 hyper-focused developer prompts** corresponding 1-to-1 with the **11 File Audit Defects** in your line-by-line audit report. Zero older or extraneous prompts are included.

> [!IMPORTANT]
> **Exact 1-to-1 Mapping**: Send these 11 prompts sequentially (Prompt 1 through Prompt 11) to your developer Antigravity instance. Every prompt starts with `/goal` and includes native `/browser`, `/learn`, `<SUBAGENT_DELEGATION_DIRECTIVE>`, and process cleanup rules.

---

### Developer Prompt 1: Fix `apps/backend/medusa-config.ts` (Lines 7–36)
**Fixes Audit File #1**

```markdown
/goal

<TASK>
Fix fallback secrets (Lines 7–14) and register missing `bosta` and `gemini-ai` custom modules (Lines 18–36) in `apps/backend/medusa-config.ts`.
</TASK>

<SUBAGENT_DELEGATION_DIRECTIVE>
- Use `invoke_subagent` (Role: "Codebase Researcher", TypeName: "research") if module path verification is needed to keep context clean.
</SUBAGENT_DELEGATION_DIRECTIVE>

<ANTIGRAVITY_SLASH_COMMANDS>
- /goal: Execute autonomously until medusa-config.ts compiles cleanly without fallback secrets.
- /learn: Persist Medusa v2 module configuration patterns to .gemini/rules.
</ANTIGRAVITY_SLASH_COMMANDS>

<ANTIGRAVITY_WORKFLOW>
1. RESEARCH & INSPECTION PHASE:
   - View `apps/backend/medusa-config.ts` (lines 7–36).

2. IMPLEMENTATION PHASE:
   - Target file: `apps/backend/medusa-config.ts`
   - **Line 7-14**: Remove hardcoded fallback secret strings (`"postgres://postgres:postgres@localhost:5432/medusa-db"` and `"supersecret_jwt_key_medusa_egypt_123"`). Require `process.env.DATABASE_URL` and `process.env.JWT_SECRET`.
   - **Line 18-36**: Add `bosta` and `gemini-ai` module declarations into the `modules` array so the Medusa v2 container injects their services.

3. EMPIRICAL VERIFICATION & TESTING PHASE:
   - Run TypeScript check: `cd apps/backend && npx tsc --noEmit`
   - Run backend build verification: `cd apps/backend && npm run build`

4. PROCESS CLEANUP & LEARNING DIRECTIVE (CRITICAL):
   - Execute `/learn` to store Medusa module registration rules.
   - Terminate any running subagents, background dev servers, or processes before completing turn.
</ANTIGRAVITY_WORKFLOW>

<ACCEPTANCE_CRITERIA>
- [ ] `medusa-config.ts` contains zero hardcoded fallback secret strings on lines 7–14.
- [ ] `bosta` and `gemini-ai` modules are registered in the `modules` array on lines 18–36.
- [ ] Backend build completes with exit code 0.
- [ ] All subagents, background tasks, and dev servers are cleanly terminated.
</ACCEPTANCE_CRITERIA>
```

---

### Developer Prompt 2: Fix `apps/backend/src/modules/paymob/service.ts` (Lines 57–91)
**Fixes Audit File #2**

```markdown
/goal

<TASK>
Remove silent mock response fallbacks (Lines 57–67) and map dynamic customer billing payload (Lines 86–91) in `apps/backend/src/modules/paymob/service.ts`.
</TASK>

<SUBAGENT_DELEGATION_DIRECTIVE>
- Use `invoke_subagent` to inspect customer context types or search Paymob billing specifications across the codebase.
</SUBAGENT_DELEGATION_DIRECTIVE>

<ANTIGRAVITY_SLASH_COMMANDS>
- /goal: Execute autonomously until Paymob service accurately maps customer billing payloads.
</ANTIGRAVITY_SLASH_COMMANDS>

<ANTIGRAVITY_WORKFLOW>
1. RESEARCH & INSPECTION PHASE:
   - View `apps/backend/src/modules/paymob/service.ts` (lines 57–91).

2. IMPLEMENTATION PHASE:
   - Target file: `apps/backend/src/modules/paymob/service.ts`
   - **Line 57-67**: In production (`process.env.NODE_ENV === "production"`), throw an Error if `apiKey` is missing instead of returning silent mock data.
   - **Line 86-91**: Replace hardcoded `billingData` (`"Customer"`, `"Order"`, `"customer@example.com"`, `"01000000000"`) with real customer context:
     ```typescript
     first_name: input.context?.customer?.first_name || "Guest",
     last_name: input.context?.customer?.last_name || "User",
     email: input.context?.customer?.email || "customer@example.com",
     phone_number: input.context?.customer?.phone || "000000000",
     ```

3. EMPIRICAL VERIFICATION & TESTING PHASE:
   - Run TypeScript check: `cd apps/backend && npx tsc --noEmit`
   - Run backend build verification: `cd apps/backend && npm run build`

4. PROCESS CLEANUP & LEARNING DIRECTIVE (CRITICAL):
   - Terminate any running subagents, background processes, or dev servers before completing turn.
</ANTIGRAVITY_WORKFLOW>

<ACCEPTANCE_CRITERIA>
- [ ] Paymob billing payload dynamically maps real customer first_name, last_name, email, and phone (Lines 86–91).
- [ ] Missing API key in production throws an explicit Error instead of returning silent mock objects (Lines 57–67).
- [ ] Backend build completes with exit code 0.
- [ ] All subagents, background tasks, and dev servers are cleanly terminated.
</ACCEPTANCE_CRITERIA>
```

---

### Developer Prompt 3: Fix `apps/backend/src/modules/bosta/service.ts` (Lines 12–18)
**Fixes Audit File #3**

```markdown
/goal

<TASK>
Replace local in-memory JavaScript `Map` (`rateCacheMap` on lines 12–18) in `apps/backend/src/modules/bosta/service.ts` with Medusa's distributed Redis caching service `@medusajs/caching`.
</TASK>

<SUBAGENT_DELEGATION_DIRECTIVE>
- Spawn a `research` subagent using `invoke_subagent` to research `@medusajs/caching` container resolution patterns in Medusa v2.
</SUBAGENT_DELEGATION_DIRECTIVE>

<ANTIGRAVITY_SLASH_COMMANDS>
- /goal: Execute autonomously until Bosta service uses distributed Redis rate caching.
</ANTIGRAVITY_SLASH_COMMANDS>

<ANTIGRAVITY_WORKFLOW>
1. RESEARCH & INSPECTION PHASE:
   - View `apps/backend/src/modules/bosta/service.ts` (lines 12–18).

2. IMPLEMENTATION PHASE:
   - Target file: `apps/backend/src/modules/bosta/service.ts`
   - Remove local `rateCacheMap` (lines 12–18).
   - Use Medusa `@medusajs/caching` container service or Redis client to store and retrieve `BOSTA_RATE_<governorate_id>` with a 1-hour (3,600s) TTL.

3. EMPIRICAL VERIFICATION & TESTING PHASE:
   - Run TypeScript check: `cd apps/backend && npx tsc --noEmit`
   - Run backend build verification: `cd apps/backend && npm run build`

4. PROCESS CLEANUP & LEARNING DIRECTIVE (CRITICAL):
   - Terminate any running subagents, background processes, or dev servers before completing turn.
</ANTIGRAVITY_WORKFLOW>

<ACCEPTANCE_CRITERIA>
- [ ] `bosta/service.ts` contains zero local `Map` instances on lines 12–18; utilizes distributed Redis caching.
- [ ] Backend build completes with exit code 0.
- [ ] All subagents, background tasks, and dev servers are cleanly terminated.
</ACCEPTANCE_CRITERIA>
```

---

### Developer Prompt 4: Fix `apps/backend/src/admin/widgets/ai-copywriter.tsx` (Line 4)
**Fixes Audit File #4**

```markdown
/goal

<TASK>
Fix browser import defect on line 4 of `apps/backend/src/admin/widgets/ai-copywriter.tsx` by creating an authenticated REST API route `/admin/ai/generate-copy`.
</TASK>

<SUBAGENT_DELEGATION_DIRECTIVE>
- Use `invoke_subagent` to delegate creation of the backend API route or inspection of admin widget API patterns to a subagent.
</SUBAGENT_DELEGATION_DIRECTIVE>

<ANTIGRAVITY_SLASH_COMMANDS>
- /goal: Execute autonomously until Admin UI widget fetches AI copy via HTTP REST API.
- /learn: Persist Admin UI REST communication rules to .gemini/rules.
</ANTIGRAVITY_SLASH_COMMANDS>

<ANTIGRAVITY_WORKFLOW>
1. RESEARCH & INSPECTION PHASE:
   - View `apps/backend/src/admin/widgets/ai-copywriter.tsx` (line 4).

2. IMPLEMENTATION PHASE:
   - Target files: `apps/backend/src/api/admin/ai/generate-copy/route.ts`, `apps/backend/src/admin/widgets/ai-copywriter.tsx`
   - Create authenticated Medusa Admin REST API route `POST /admin/ai/generate-copy`.
   - Remove `import { GeminiAIStudioClient } from "../../modules/gemini-ai/client";` on line 4 of `ai-copywriter.tsx`.
   - Refactor `ai-copywriter.tsx` to fetch copy via HTTP POST to `/admin/ai/generate-copy`.

3. EMPIRICAL VERIFICATION & TESTING PHASE:
   - Run backend build verification: `cd apps/backend && npm run build`

4. PROCESS CLEANUP & LEARNING DIRECTIVE (CRITICAL):
   - Execute `/learn` to store Admin widget REST API rules.
   - Terminate any running subagents, background dev servers, or processes before completing turn.
</ANTIGRAVITY_WORKFLOW>

<ACCEPTANCE_CRITERIA>
- [ ] Line 4 import `GeminiAIStudioClient` is removed from `ai-copywriter.tsx`.
- [ ] Admin widget fetches via authenticated `/admin/ai/generate-copy` HTTP endpoint.
- [ ] Backend build completes with exit code 0.
- [ ] All subagents, background tasks, and dev servers are cleanly terminated.
</ACCEPTANCE_CRITERIA>
```

---

### Developer Prompt 5: Fix `apps/storefront/src/app/page.tsx` (Lines 1–12)
**Fixes Audit File #5**

```markdown
/goal

<TASK>
Refactor `apps/storefront/src/app/page.tsx` (lines 1–12) into a React Server Component (RSC) by removing `"use client"`.
</TASK>

<SUBAGENT_DELEGATION_DIRECTIVE>
- Delegate identification of client-side interactive sub-components in `app/page.tsx` to a `research` subagent using `invoke_subagent`.
</SUBAGENT_DELEGATION_DIRECTIVE>

<ANTIGRAVITY_SLASH_COMMANDS>
- /goal: Execute autonomously until homepage compiles as a pure React Server Component.
</ANTIGRAVITY_SLASH_COMMANDS>

<ANTIGRAVITY_WORKFLOW>
1. RESEARCH & INSPECTION PHASE:
   - View `apps/storefront/src/app/page.tsx` (lines 1–12).

2. IMPLEMENTATION PHASE:
   - Target file: `apps/storefront/src/app/page.tsx`
   - Remove `"use client"` directive from line 1.
   - Extract interactive client widgets into separate `"use client"` components.
   - Convert `Home()` into an `async` React Server Component that fetches storefront data on the server.

3. EMPIRICAL VERIFICATION & TESTING PHASE:
   - Run storefront build verification: `cd apps/storefront && npm run build`

4. PROCESS CLEANUP & LEARNING DIRECTIVE (CRITICAL):
   - Terminate any running subagents, background dev servers (e.g. `next dev`) before completing turn.
</ANTIGRAVITY_WORKFLOW>

<ACCEPTANCE_CRITERIA>
- [ ] `app/page.tsx` line 1 does NOT contain `"use client"`.
- [ ] Homepage renders as an `async` React Server Component.
- [ ] Storefront build completes with exit code 0.
- [ ] All subagents, background tasks, and dev servers are cleanly terminated.
</ACCEPTANCE_CRITERIA>
```

---

### Developer Prompt 6: Fix `apps/storefront/src/lib/context/cart-context.tsx` (Lines 24–48)
**Fixes Audit File #6**

```markdown
/goal

<TASK>
Synchronize cart items with Medusa backend DB via JS SDK in `apps/storefront/src/lib/context/cart-context.tsx` (lines 24–48).
</TASK>

<SUBAGENT_DELEGATION_DIRECTIVE>
- Spawn a subagent via `invoke_subagent` to research `@medusajs/js-sdk` store cart methods (`sdk.store.carts.lineItems.create()`).
</SUBAGENT_DELEGATION_DIRECTIVE>

<ANTIGRAVITY_SLASH_COMMANDS>
- /goal: Execute autonomously until cart state syncs server-side with Medusa JS SDK.
</ANTIGRAVITY_SLASH_COMMANDS>

<ANTIGRAVITY_WORKFLOW>
1. RESEARCH & INSPECTION PHASE:
   - View `apps/storefront/src/lib/context/cart-context.tsx` (lines 24–48).

2. IMPLEMENTATION PHASE:
   - Target file: `apps/storefront/src/lib/context/cart-context.tsx`
   - Wire `addItem`, `removeItem`, and `updateQuantity` to call Medusa JS SDK endpoints (`sdk.store.carts.lineItems.create()`, `update()`, `delete()`).
   - Ensure cart ID is persisted server-side in Medusa database as well as 30-day persistent cookie.

3. EMPIRICAL VERIFICATION & TESTING PHASE:
   - Run storefront build verification: `cd apps/storefront && npm run build`

4. PROCESS CLEANUP & LEARNING DIRECTIVE (CRITICAL):
   - Terminate any running subagents, background dev servers, or processes before completing turn.
</ANTIGRAVITY_WORKFLOW>

<ACCEPTANCE_CRITERIA>
- [ ] Cart Context (lines 24–48) syncs line items with Medusa backend SDK endpoints.
- [ ] Storefront build completes with exit code 0.
- [ ] All subagents, background tasks, and dev servers are cleanly terminated.
</ACCEPTANCE_CRITERIA>
```

---

### Developer Prompt 7: Fix `apps/storefront/src/modules/home/components/home-client-view.tsx` (Line 168)
**Fixes Audit File #7**

```markdown
/goal

<TASK>
Replace standard HTML `<img>` tag on line 168 of `apps/storefront/src/modules/home/components/home-client-view.tsx` with Next.js `<Image />` component.
</TASK>

<SUBAGENT_DELEGATION_DIRECTIVE>
- Use `invoke_subagent` to search for any other unoptimized `<img>` tags across storefront modules.
</SUBAGENT_DELEGATION_DIRECTIVE>

<ANTIGRAVITY_SLASH_COMMANDS>
- /goal: Execute autonomously until all image elements use Next.js Image component.
</ANTIGRAVITY_SLASH_COMMANDS>

<ANTIGRAVITY_WORKFLOW>
1. RESEARCH & INSPECTION PHASE:
   - View `apps/storefront/src/modules/home/components/home-client-view.tsx` (line 168).

2. IMPLEMENTATION PHASE:
   - Target file: `apps/storefront/src/modules/home/components/home-client-view.tsx`
   - Replace standard HTML `<img>` tag on line 168 with `import Image from "next/image"`.
   - Provide proper `alt`, `width`, `height`, `sizes`, and `priority` props.

3. EMPIRICAL VERIFICATION & TESTING PHASE:
   - Run storefront build verification: `cd apps/storefront && npm run build`

4. PROCESS CLEANUP & LEARNING DIRECTIVE (CRITICAL):
   - Terminate any running subagents, background dev servers, or processes before completing turn.
</ANTIGRAVITY_WORKFLOW>

<ACCEPTANCE_CRITERIA>
- [ ] Line 168 of `home-client-view.tsx` uses Next.js `<Image />` component.
- [ ] Storefront build completes with exit code 0.
- [ ] All subagents, background tasks, and dev servers are cleanly terminated.
</ACCEPTANCE_CRITERIA>
```

---

### Developer Prompt 8: Fix `infrastructure/docker/Dockerfile.backend` (Line 45)
**Fixes Audit File #8**

```markdown
/goal

<TASK>
Fix process wrapping on line 45 of `infrastructure/docker/Dockerfile.backend` to ensure graceful OS signal handling.
</TASK>

<SUBAGENT_DELEGATION_DIRECTIVE>
- Use `invoke_subagent` if Dockerfile multi-stage optimizations require research.
</SUBAGENT_DELEGATION_DIRECTIVE>

<ANTIGRAVITY_SLASH_COMMANDS>
- /goal: Execute autonomously until Dockerfile CMD executes Node directly.
</ANTIGRAVITY_SLASH_COMMANDS>

<ANTIGRAVITY_WORKFLOW>
1. RESEARCH & INSPECTION PHASE:
   - View `infrastructure/docker/Dockerfile.backend` (line 45).

2. IMPLEMENTATION PHASE:
   - Target file: `infrastructure/docker/Dockerfile.backend`
   - Change line 45 from `CMD ["npm", "run", "start"]` to `CMD ["node", "dist/main.js"]` (or direct node entrypoint) so OS signals (`SIGTERM`, `SIGINT`) reach Node directly.

3. EMPIRICAL VERIFICATION & TESTING PHASE:
   - Run Docker compose config validation: `docker compose -f infrastructure/docker/docker-compose.tenant.yml config`

4. PROCESS CLEANUP & LEARNING DIRECTIVE (CRITICAL):
   - Terminate any active subagents or background tasks before completing turn.
</ANTIGRAVITY_WORKFLOW>

<ACCEPTANCE_CRITERIA>
- [ ] Line 45 of `Dockerfile.backend` executes Node directly (`CMD ["node", "dist/main.js"]`).
- [ ] Docker Compose config passes validation.
- [ ] All subagents and background tasks are cleanly terminated.
</ACCEPTANCE_CRITERIA>
```

---

### Developer Prompt 9: Fix `infrastructure/docker/docker-compose.tenant.yml` (Line 69)
**Fixes Audit File #9**

```markdown
/goal

<TASK>
Fix browser-inaccessible internal hostname on line 69 of `infrastructure/docker/docker-compose.tenant.yml`.
</TASK>

<SUBAGENT_DELEGATION_DIRECTIVE>
- Delegate environment variable resolution checks to a subagent using `invoke_subagent`.
</SUBAGENT_DELEGATION_DIRECTIVE>

<ANTIGRAVITY_SLASH_COMMANDS>
- /goal: Execute autonomously until NEXT_PUBLIC_MEDUSA_BACKEND_URL points to accessible tenant public URL.
</ANTIGRAVITY_SLASH_COMMANDS>

<ANTIGRAVITY_WORKFLOW>
1. RESEARCH & INSPECTION PHASE:
   - View `infrastructure/docker/docker-compose.tenant.yml` (line 69).

2. IMPLEMENTATION PHASE:
   - Target file: `infrastructure/docker/docker-compose.tenant.yml`
   - Change line 69 from `NEXT_PUBLIC_MEDUSA_BACKEND_URL=http://backend:9000` to point to dynamic tenant environment variable `${TENANT_PUBLIC_BACKEND_URL:-http://localhost:9000}`.

3. EMPIRICAL VERIFICATION & TESTING PHASE:
   - Run Docker compose config validation: `docker compose -f infrastructure/docker/docker-compose.tenant.yml config`

4. PROCESS CLEANUP & LEARNING DIRECTIVE (CRITICAL):
   - Terminate any active subagents or background tasks before completing turn.
</ANTIGRAVITY_WORKFLOW>

<ACCEPTANCE_CRITERIA>
- [ ] Line 69 of `docker-compose.tenant.yml` configures `NEXT_PUBLIC_MEDUSA_BACKEND_URL` for public browser resolution.
- [ ] Docker Compose config passes validation.
- [ ] All subagents and background tasks are cleanly terminated.
</ACCEPTANCE_CRITERIA>
```

---

### Developer Prompt 10: Fix `infrastructure/scripts/provision-tenant.sh` (Line 100)
**Fixes Audit File #10**

```markdown
/goal

<TASK>
Remove migration failure suppression `|| true` on line 100 of `infrastructure/scripts/provision-tenant.sh`.
</TASK>

<SUBAGENT_DELEGATION_DIRECTIVE>
- Use `invoke_subagent` if bash healthcheck polling loops need syntax verification.
</SUBAGENT_DELEGATION_DIRECTIVE>

<ANTIGRAVITY_SLASH_COMMANDS>
- /goal: Execute autonomously until tenant provisioning script aborts deployment on migration failure.
</ANTIGRAVITY_SLASH_COMMANDS>

<ANTIGRAVITY_WORKFLOW>
1. RESEARCH & INSPECTION PHASE:
   - View `infrastructure/scripts/provision-tenant.sh` (line 100).

2. IMPLEMENTATION PHASE:
   - Target file: `infrastructure/scripts/provision-tenant.sh`
   - Remove `|| true` from line 100 (`docker compose exec -T backend npx medusa db:migrate`).
   - Add error check ensuring script exits with non-zero status if database migration fails.

3. EMPIRICAL VERIFICATION & TESTING PHASE:
   - Run bash syntax check: `bash -n infrastructure/scripts/provision-tenant.sh`

4. PROCESS CLEANUP & LEARNING DIRECTIVE (CRITICAL):
   - Terminate any running subagents or shell tasks before completing turn.
</ANTIGRAVITY_WORKFLOW>

<ACCEPTANCE_CRITERIA>
- [ ] Line 100 of `provision-tenant.sh` does NOT contain `|| true`.
- [ ] Migration failure causes provisioning script to exit with error code.
- [ ] Script passes `bash -n` syntax check cleanly.
- [ ] All subagents and background tasks are cleanly terminated.
</ACCEPTANCE_CRITERIA>
```

---

### Developer Prompt 11: Fix `packages/shared-types/package.json` (Lines 5–8)
**Fixes Audit File #11**

```markdown
/goal

<TASK>
Fix TypeScript build and main entrypoint configuration in `packages/shared-types/package.json` (lines 5–8).
</TASK>

<SUBAGENT_DELEGATION_DIRECTIVE>
- Use `invoke_subagent` to test shared-types build outputs in clean subagent contexts.
</SUBAGENT_DELEGATION_DIRECTIVE>

<ANTIGRAVITY_SLASH_COMMANDS>
- /goal: Execute autonomously until packages/shared-types emits compiled JS and d.ts declaration files.
</ANTIGRAVITY_SLASH_COMMANDS>

<ANTIGRAVITY_WORKFLOW>
1. RESEARCH & INSPECTION PHASE:
   - View `packages/shared-types/package.json` (lines 5–8).

2. IMPLEMENTATION PHASE:
   - Target file: `packages/shared-types/package.json`
   - Update lines 5–8:
     ```json
     "main": "dist/index.js",
     "types": "dist/index.d.ts",
     "scripts": {
       "build": "tsc"
     }
     ```

3. EMPIRICAL VERIFICATION & TESTING PHASE:
   - Run build verification: `cd packages/shared-types && npm run build`
   - Verify `dist/index.js` and `dist/index.d.ts` are generated.

4. PROCESS CLEANUP & LEARNING DIRECTIVE (CRITICAL):
   - Terminate any running subagents or background tasks before completing turn.
</ANTIGRAVITY_WORKFLOW>

<ACCEPTANCE_CRITERIA>
- [ ] Lines 5–8 of `packages/shared-types/package.json` set `"main": "dist/index.js"` and `"types": "dist/index.d.ts"`.
- [ ] `npm run build` executes `tsc` and emits `dist/` build files.
- [ ] All subagents and background tasks are cleanly terminated.
</ACCEPTANCE_CRITERIA>
```
