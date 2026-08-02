# Master Production Remediation Developer Prompt Pack (`PROMPT_SEQUENCE_COMPLETE_REMEDIATION.md`)

This prompt pack contains **10 comprehensive developer prompts** engineered for **Google Antigravity Agentic IDE** to systematically resolve all 24 Critical Security/Financial Blockers, 47 Major Functional Bugs, and 31 Minor Issues identified in the full codebase evaluation report.

> [!IMPORTANT]
> **Subagent Directive**: Send these 10 prompts sequentially (Prompt 1 through Prompt 10) to your developer Antigravity instance. Every prompt explicitly instructs the agent to delegate research or sub-tasks to subagents (`invoke_subagent`) to maintain clean context and maximize execution speed.

---

## Part 1: Backend Core, Security & Configuration (Prompts 1–3)

---
### Developer Prompt 1: Backend Core Config Validation, Trailing Comma & OpenTelemetry Instrumentation

```markdown
/goal

<TASK>
Validate environment variables at startup in `medusa-config.ts`, fix JSON trailing comma in `tsconfig.json`, and configure OpenTelemetry instrumentation in `src/instrumentation.ts`.
</TASK>

<SUBAGENT_DELEGATION_DIRECTIVE>
- Use `invoke_subagent` (Role: "Codebase Researcher", TypeName: "research") to inspect backend configuration files and OpenTelemetry SDK initialization patterns.
</SUBAGENT_DELEGATION_DIRECTIVE>

<ANTIGRAVITY_SLASH_COMMANDS>
- /goal: Execute autonomously until config validation, tsconfig syntax, and OpenTelemetry instrumentation pass build tests.
- /learn: Persist startup config validation rules to .gemini/rules.
</ANTIGRAVITY_SLASH_COMMANDS>

<ANTIGRAVITY_WORKFLOW>
1. RESEARCH & INSPECTION PHASE:
   - View `apps/backend/medusa-config.ts` (lines 19–66), `tsconfig.json` (line 37), and `apps/backend/src/instrumentation.ts`.

2. IMPLEMENTATION PHASE:
   - Target files: `apps/backend/medusa-config.ts`, `tsconfig.json`, `apps/backend/src/instrumentation.ts`
   - **`medusa-config.ts`**: Add fail-fast validation throwing explicit startup errors if `DATABASE_URL`, `REDIS_URL`, `JWT_SECRET`, or `COOKIE_SECRET` are undefined. Validate `PAYMOB_API_KEY`, `BOSTA_API_KEY`, `ETA_TAX_REGISTRATION_NUMBER`, and `GEMINI_API_KEY`.
   - **`tsconfig.json`**: Fix JSON syntax error on line 37 by removing trailing comma.
   - **`instrumentation.ts`**: Uncomment OpenTelemetry SDK initialization with fallback exporter logging if primary OTLP collector is unreachable.

3. EMPIRICAL VERIFICATION & TESTING PHASE:
   - Run TypeScript check: `cd apps/backend && npx tsc --noEmit`
   - Run backend build verification: `cd apps/backend && npm run build`

4. PROCESS CLEANUP & LEARNING DIRECTIVE (CRITICAL):
   - Execute `/learn` to store backend startup validation patterns.
   - Terminate any running subagents, background dev servers, or processes before completing turn.
</ANTIGRAVITY_WORKFLOW>

<ACCEPTANCE_CRITERIA>
- [ ] Subagents delegated for config and OpenTelemetry research.
- [ ] `medusa-config.ts` validates all core database, redis, JWT, and provider API keys at startup.
- [ ] `tsconfig.json` trailing comma removed.
- [ ] `instrumentation.ts` initializes OpenTelemetry metrics cleanly.
- [ ] Backend build completes with exit code 0.
- [ ] All subagents and background tasks are cleanly terminated.
</ACCEPTANCE_CRITERIA>
```

---
### Developer Prompt 2: Paymob Client Error Sanitization, PCI-DSS HMAC PAN Masking & Integration Whitelisting

```markdown
/goal

<TASK>
Sanitize error messages in `paymob/client.ts`, mask PAN data in `paymob/hmac.ts`, validate integration ID whitelisting, and remove auth tokens from payment data in `paymob/service.ts`.
</TASK>

<SUBAGENT_DELEGATION_DIRECTIVE>
- Use `invoke_subagent` to inspect Paymob payment provider security and PCI-DSS compliance specifications.
</SUBAGENT_DELEGATION_DIRECTIVE>

<ANTIGRAVITY_SLASH_COMMANDS>
- /goal: Execute autonomously until Paymob client error handling and HMAC security comply with PCI-DSS guidelines.
- /learn: Persist PCI-DSS data masking and payment security rules to .gemini/rules.
</ANTIGRAVITY_SLASH_COMMANDS>

<ANTIGRAVITY_WORKFLOW>
1. RESEARCH & INSPECTION PHASE:
   - View `apps/backend/src/modules/paymob/client.ts` (lines 146–426), `hmac.ts` (lines 35–50), and `service.ts` (lines 87, 142).

2. IMPLEMENTATION PHASE:
   - Target files: `apps/backend/src/modules/paymob/client.ts`, `apps/backend/src/modules/paymob/hmac.ts`, `apps/backend/src/modules/paymob/service.ts`
   - **`client.ts`**: Replace verbose backend/API error string exposures (`throw new Error(...)`) in auth, order registration, capture, refund, and void methods with generic client-safe error messages while logging details internally.
   - **`hmac.ts`**: Mask/omit raw Primary Account Number (PAN) data from HMAC calculation logs to ensure PCI-DSS compliance.
   - **`service.ts`**: Validate `integrationId` against numeric whitelist; remove raw Paymob auth tokens from payment data objects before storing/caching.

3. EMPIRICAL VERIFICATION & TESTING PHASE:
   - Run TypeScript check: `cd apps/backend && npx tsc --noEmit`
   - Run backend build verification: `cd apps/backend && npm run build`

4. PROCESS CLEANUP & LEARNING DIRECTIVE (CRITICAL):
   - Execute `/learn` to store payment data security rules.
   - Terminate any running subagents, background dev servers, or processes before completing turn.
</ANTIGRAVITY_WORKFLOW>

<ACCEPTANCE_CRITERIA>
- [ ] Subagents delegated for PCI-DSS compliance inspection.
- [ ] Paymob client sanitizes internal error disclosures across auth, capture, refund, and void calls.
- [ ] HMAC logging contains zero unmasked PAN data.
- [ ] `integrationId` validated against numeric whitelist.
- [ ] Backend build completes with exit code 0.
- [ ] All subagents and background tasks are cleanly terminated.
</ACCEPTANCE_CRITERIA>
```

---
### Developer Prompt 3: Paymob Capture/Refund Idempotency Locks & Atomic Webhook Redis Deduplication

```markdown
/goal

<TASK>
Implement pre-state checks and idempotency keys in Paymob capture/refund methods, and enforce atomic Redis `NX` locking in `api/hooks/paymob/route.ts`.
</TASK>

<SUBAGENT_DELEGATION_DIRECTIVE>
- Delegate Redis transaction locking and payment idempotency pattern research to a subagent via `invoke_subagent`.
</SUBAGENT_DELEGATION_DIRECTIVE>

<ANTIGRAVITY_SLASH_COMMANDS>
- /goal: Execute autonomously until Paymob payment processing and webhook deduplication pass idempotency tests.
- /learn: Persist Redis payment idempotency rules to .gemini/rules.
</ANTIGRAVITY_SLASH_COMMANDS>

<ANTIGRAVITY_WORKFLOW>
1. RESEARCH & INSPECTION PHASE:
   - View `apps/backend/src/modules/paymob/service.ts` (lines 160–230) and `apps/backend/src/api/hooks/paymob/route.ts` (lines 66–105).

2. IMPLEMENTATION PHASE:
   - Target files: `apps/backend/src/modules/paymob/service.ts`, `apps/backend/src/api/hooks/paymob/route.ts`
   - **`service.ts`**: Add pre-capture state validation verifying order authorization status before capturing; attach unique idempotency keys (`paymob_rfnd_<order_id>`) to refund requests to prevent double-refunding.
   - **`paymob/route.ts`**: Remove in-process `activeLockSet` Map fallback; enforce atomic Redis `NX` lock (`paymob_tx_<id>`) across multi-pod deployments; reject unauthenticated/unsigned webhooks in production.

3. EMPIRICAL VERIFICATION & TESTING PHASE:
   - Run TypeScript check: `cd apps/backend && npx tsc --noEmit`
   - Run backend build verification: `cd apps/backend && npm run build`

4. PROCESS CLEANUP & LEARNING DIRECTIVE (CRITICAL):
   - Execute `/learn` to store payment idempotency patterns.
   - Terminate any running subagents, background dev servers, or processes before completing turn.
</ANTIGRAVITY_WORKFLOW>

<ACCEPTANCE_CRITERIA>
- [ ] Subagents delegated for Redis lock pattern research.
- [ ] Pre-capture authorization state check and refund idempotency keys active.
- [ ] Webhook route uses atomic Redis `NX` key lock exclusively.
- [ ] Backend build completes with exit code 0.
- [ ] All subagents and background tasks are cleanly terminated.
</ACCEPTANCE_CRITERIA>
```

---

## Part 2: Logistics, Tax & AI Security (Prompts 4–7)

---
### Developer Prompt 4: Bosta Governorate Whitelist, Weight NaN Guard, & E.164 Phone Validation

```markdown
/goal

<TASK>
Validate governorate codes in `bosta/client.ts`, sanitize package weight calculations in `bosta/service.ts`, and fix Arabic string normalization in `bosta/location-mapper.ts`.
</TASK>

<SUBAGENT_DELEGATION_DIRECTIVE>
- Use `invoke_subagent` to inspect Bosta API governorate city codes and Egyptian mobile phone format rules.
</SUBAGENT_DELEGATION_DIRECTIVE>

<ANTIGRAVITY_SLASH_COMMANDS>
- /goal: Execute autonomously until Bosta fulfillment service passes location and weight validation checks.
</ANTIGRAVITY_SLASH_COMMANDS>

<ANTIGRAVITY_WORKFLOW>
1. RESEARCH & INSPECTION PHASE:
   - View `apps/backend/src/modules/bosta/client.ts` (lines 23, 60–62), `service.ts` (lines 107–198), and `location-mapper.ts` (lines 87–145).

2. IMPLEMENTATION PHASE:
   - Target files: `apps/backend/src/modules/bosta/client.ts`, `apps/backend/src/modules/bosta/service.ts`, `apps/backend/src/modules/bosta/location-mapper.ts`
   - **`client.ts`**: Add governorate code whitelist validation (`EG-01` to `EG-27`); prevent mock tracking generation in production.
   - **`service.ts`**: Sanitize item weights (handling `NaN`/`null`/`0`/`-1`), providing safe fallback (`1.0` kg); complete rate tier logic for Sinai/Frontier governorates (`EG-15` to `EG-27`); reject dummy phone `"01000000000"`, requiring E.164 Egyptian mobile format (`+201XXXXXXXXX`).
   - **`location-mapper.ts`**: Add Arabic normalization for `ى` (alif maksura) and `ء` (hamza); enforce word boundaries in sub-district matching; log warning for unmapped cities instead of silent Cairo fallback.

3. EMPIRICAL VERIFICATION & TESTING PHASE:
   - Run TypeScript check: `cd apps/backend && npx tsc --noEmit`
   - Run backend build verification: `cd apps/backend && npm run build`

4. PROCESS CLEANUP & LEARNING DIRECTIVE (CRITICAL):
   - Terminate any running subagents, background dev servers, or processes before completing turn.
</ANTIGRAVITY_WORKFLOW>

<ACCEPTANCE_CRITERIA>
- [ ] Subagents delegated for governorate dataset research.
- [ ] Governorate whitelist and E.164 phone validation enforced.
- [ ] Item weight calculation handles `NaN` safely.
- [ ] Arabic normalization handles hamza and alif maksura with word boundaries.
- [ ] Backend build completes with exit code 0.
- [ ] All subagents and background tasks are cleanly terminated.
</ACCEPTANCE_CRITERIA>
```

---
### Developer Prompt 5: Bosta Workflow Webhook Synchronization & Exponential Backoff Compensation

```markdown
/goal

<TASK>
Implement Bosta status sync webhook, exponential backoff retries in workflow compensations, and fix COD amount fallbacks in `bosta-fulfillment-workflow.ts`.
</TASK>

<SUBAGENT_DELEGATION_DIRECTIVE>
- Delegate Bosta webhook status payload and workflow compensation saga inspection to a subagent via `invoke_subagent`.
</SUBAGENT_DELEGATION_DIRECTIVE>

<ANTIGRAVITY_SLASH_COMMANDS>
- /goal: Execute autonomously until Bosta workflow compensations and webhook status sync compile clean.
- /learn: Persist fulfillment workflow compensation patterns to .gemini/rules.
</ANTIGRAVITY_SLASH_COMMANDS>

<ANTIGRAVITY_WORKFLOW>
1. RESEARCH & INSPECTION PHASE:
   - View `apps/backend/src/workflows/bosta-fulfillment-workflow.ts` (lines 45–107) and `apps/backend/src/api/hooks/bosta/route.ts`.

2. IMPLEMENTATION PHASE:
   - Target files: `apps/backend/src/workflows/bosta-fulfillment-workflow.ts`, `apps/backend/src/api/hooks/bosta/route.ts`
   - **`bosta/route.ts`**: Implement webhook listener syncing Bosta delivery status (`DELIVERED`, `CANCELLED`, `RETURNED`) back to Medusa fulfillment state.
   - **`bosta-fulfillment-workflow.ts`**: Add exponential backoff retry loop (3s $\rightarrow$ 9s $\rightarrow$ 27s) for delivery cancellation compensations; fix COD amount calculation (`codAmount = isCod ? order.total : 0`); handle duplicate reference errors cleanly.

3. EMPIRICAL VERIFICATION & TESTING PHASE:
   - Run TypeScript check: `cd apps/backend && npx tsc --noEmit`
   - Run backend build verification: `cd apps/backend && npm run build`

4. PROCESS CLEANUP & LEARNING DIRECTIVE (CRITICAL):
   - Execute `/learn` to store fulfillment status sync rules.
   - Terminate any running subagents, background dev servers, or processes before completing turn.
</ANTIGRAVITY_WORKFLOW>

<ACCEPTANCE_CRITERIA>
- [ ] Subagents delegated for Bosta webhook status sync research.
- [ ] Bosta webhook syncs delivery status changes to Medusa fulfillment.
- [ ] Workflow compensation includes exponential backoff retry loop.
- [ ] COD amount calculation verified.
- [ ] Backend build completes with exit code 0.
- [ ] All subagents and background tasks are cleanly terminated.
</ACCEPTANCE_CRITERIA>
```

---
### Developer Prompt 6: Real ETA HSM Signing, Encrypted PIN, PII Encryption, & RFC 4122 UUID

```markdown
/goal

<TASK>
Enforce real HSM proxy signing in `hsm-signer.ts`, encrypt PII in audit logs, fix buyer type logic in `payload-builder.ts`, and format RFC 4122 receipt UUIDs.
</TASK>

<SUBAGENT_DELEGATION_DIRECTIVE>
- Use `invoke_subagent` to inspect ETA e-Receipt v1.0 standard schema and CAdES-BES signature requirements.
</SUBAGENT_DELEGATION_DIRECTIVE>

<ANTIGRAVITY_SLASH_COMMANDS>
- /goal: Execute autonomously until ETA Tax module complies with Egyptian Tax Authority e-Receipt v1.0 specifications.
- /browser: Verify ETA Portal RFC 4122 UUID and CAdES-BES signature requirements.
- /learn: Persist ETA tax compliance rules to .gemini/rules.
</ANTIGRAVITY_SLASH_COMMANDS>

<ANTIGRAVITY_WORKFLOW>
1. RESEARCH & INSPECTION PHASE:
   - View `apps/backend/src/modules/eta-tax/hsm-signer.ts` (lines 39–51), `payload-builder.ts` (lines 210–213), and `apps/backend/src/subscribers/order-placed-eta.ts` (lines 119–193).

2. IMPLEMENTATION PHASE:
   - Target files: `apps/backend/src/modules/eta-tax/hsm-signer.ts`, `apps/backend/src/modules/eta-tax/payload-builder.ts`, `apps/backend/src/subscribers/order-placed-eta.ts`
   - **`hsm-signer.ts`**: Remove mock Base64 signature fallback in production; require valid HSM proxy connection or throw an error; transmit token PIN over encrypted TLS channel only.
   - **`payload-builder.ts`**: Fix buyer type ternary logic on lines 210–213 to `type: buyer.nationalId ? "P" : "B"` so business buyers are correctly identified as `"B"`.
   - **`order-placed-eta.ts`**: Encrypt customer national ID and phone in `EtaReceiptAudit` log table; replace `ETA_${Date.now()}` with standard RFC 4122 UUID (`crypto.randomUUID()`); validate production Tax Registration Number (TRN).

3. EMPIRICAL VERIFICATION & TESTING PHASE:
   - Run TypeScript check: `cd apps/backend && npx tsc --noEmit`
   - Run backend build verification: `cd apps/backend && npm run build`

4. PROCESS CLEANUP & LEARNING DIRECTIVE (CRITICAL):
   - Execute `/learn` to store ETA e-Receipt schema rules.
   - Terminate any running subagents, background dev servers, or processes before completing turn.
</ANTIGRAVITY_WORKFLOW>

<ACCEPTANCE_CRITERIA>
- [ ] Subagents delegated for ETA e-Receipt schema research.
- [ ] HSM signer enforces production proxy signing without mock fallbacks.
- [ ] Buyer type correctly distinguishes Person (`P`) vs Business (`B`).
- [ ] Customer PII encrypted in audit log table.
- [ ] Receipt UUID follows RFC 4122 format.
- [ ] Backend build completes with exit code 0.
- [ ] All subagents and background tasks are cleanly terminated.
</ACCEPTANCE_CRITERIA>
```

---
### Developer Prompt 7: Gemini AI Key Vault Rotation, Prompt Injection Sanitization, & BullMQ DLQ

```markdown
/goal

<TASK>
Rotate Gemini API key to `process.env.GEMINI_API_KEY`, sanitize prompts against injection in `gemini-ai/client.ts`, and implement BullMQ job persistence & DLQ in `background-queue.ts`.
</TASK>

<SUBAGENT_DELEGATION_DIRECTIVE>
- Use `invoke_subagent` to inspect prompt injection sanitization patterns and BullMQ Redis persistent queue setup.
</SUBAGENT_DELEGATION_DIRECTIVE>

<ANTIGRAVITY_SLASH_COMMANDS>
- /goal: Execute autonomously until Gemini AI client and BullMQ job queue pass security and persistence tests.
- /learn: Persist LLM prompt injection defense rules to .gemini/rules.
</ANTIGRAVITY_SLASH_COMMANDS>

<ANTIGRAVITY_WORKFLOW>
1. RESEARCH & INSPECTION PHASE:
   - View `apps/backend/src/modules/gemini-ai/client.ts` (lines 24–80), `apps/backend/src/jobs/background-queue.ts` (lines 30–91), and `apps/backend/src/jobs/ai-copywriter-worker.ts`.

2. IMPLEMENTATION PHASE:
   - Target files: `apps/backend/src/modules/gemini-ai/client.ts`, `apps/backend/src/jobs/background-queue.ts`, `apps/backend/src/jobs/ai-copywriter-worker.ts`, `apps/backend/src/api/admin/ai/generate-copy/route.ts`
   - **`client.ts`**: Remove hardcoded API key string; require `process.env.GEMINI_API_KEY`; pass API key in `Authorization` header instead of URL query parameter; sanitize `productTitle` and `category` parameters against prompt injection; set 30s request timeout.
   - **`background-queue.ts`**: Replace in-memory `Map` with persistent Redis key-value store; add Dead-Letter Queue (DLQ) for failed jobs exceeding max retries; implement 24-hour job TTL.
   - **`route.ts`**: Add input validation and token bucket rate limiting on AI copy generation endpoints.

3. EMPIRICAL VERIFICATION & TESTING PHASE:
   - Run TypeScript check: `cd apps/backend && npx tsc --noEmit`
   - Run backend build verification: `cd apps/backend && npm run build`

4. PROCESS CLEANUP & LEARNING DIRECTIVE (CRITICAL):
   - Execute `/learn` to store LLM security rules.
   - Terminate any running subagents, background dev servers, or processes before completing turn.
</ANTIGRAVITY_WORKFLOW>

<ACCEPTANCE_CRITERIA>
- [ ] Subagents delegated for LLM security and BullMQ research.
- [ ] Zero hardcoded API keys in codebase; loaded via `process.env.GEMINI_API_KEY`.
- [ ] Prompt inputs sanitized against prompt injection.
- [ ] Background job queue persists tasks in Redis with DLQ and 24h TTL.
- [ ] Backend build completes with exit code 0.
- [ ] All subagents and background tasks are cleanly terminated.
</ACCEPTANCE_CRITERIA>
```

---

## Part 3: Storefront & Infrastructure Security (Prompts 8–10)

---
### Developer Prompt 8: Storefront SSRF Image Whitelist, Open Redirect Fix, & Paymob Iframe Validation

```markdown
/goal

<TASK>
Replace image wildcard in `next.config.ts`, fix open redirect in `checkout-view.tsx`, and validate Paymob iframe URL in `paymob-modal.tsx`.
</TASK>

<SUBAGENT_DELEGATION_DIRECTIVE>
- Delegate Next.js security headers and URL validation checks to a subagent via `invoke_subagent`.
</SUBAGENT_DELEGATION_DIRECTIVE>

<ANTIGRAVITY_SLASH_COMMANDS>
- /goal: Execute autonomously until storefront SSRF image whitelist, open redirect fix, and iframe validation pass build tests.
- /learn: Persist Next.js storefront security rules to .gemini/rules.
</ANTIGRAVITY_SLASH_COMMANDS>

<ANTIGRAVITY_WORKFLOW>
1. RESEARCH & INSPECTION PHASE:
   - View `apps/storefront/next.config.ts` (line 10), `apps/storefront/src/modules/checkout/components/checkout-view.tsx` (line 161), and `apps/storefront/src/modules/checkout/components/paymob-modal.tsx` (lines 105–110).

2. IMPLEMENTATION PHASE:
   - Target files: `apps/storefront/next.config.ts`, `apps/storefront/src/modules/checkout/components/checkout-view.tsx`, `apps/storefront/src/modules/checkout/components/paymob-modal.tsx`
   - **`next.config.ts`**: Replace wildcard `hostname: "**"` with explicit CDN domain whitelist (e.g. `res.cloudinary.com`, `accept.paymob.com`, `bosta.co`).
   - **`checkout-view.tsx`**: Validate `countryCode` parameter against ISO 3166-1 alpha-2 list (`eg`) before redirecting; add phone regex (`^(\+20|0)1[0125][0-9]{8}$`) and email format validation.
   - **`paymob-modal.tsx`**: Validate `iframeUrl` ensuring it begins with `https://accept.paymob.com/` before rendering iframe.

3. EMPIRICAL VERIFICATION & TESTING PHASE:
   - Run storefront build verification: `cd apps/storefront && npm run build`

4. PROCESS CLEANUP & LEARNING DIRECTIVE (CRITICAL):
   - Terminate any running subagents, background dev servers (e.g. `next dev`) before completing turn.
</ANTIGRAVITY_WORKFLOW>

<ACCEPTANCE_CRITERIA>
- [ ] Subagents delegated for Next.js security config inspection.
- [ ] `next.config.ts` replaces wildcard image hostname with explicit domain whitelist.
- [ ] Open redirect patched with ISO country code validation.
- [ ] Paymob iframe URL strictly validated against Paymob domain.
- [ ] Storefront build completes with exit code 0.
- [ ] All subagents, background tasks, and dev servers are cleanly terminated.
</ACCEPTANCE_CRITERIA>
```

---
### Developer Prompt 9: Storefront Cart Context Type Safety, Optimistic Race Fix, & Cairo Font Fallback

```markdown
/goal

<TASK>
Replace `any` annotations in `cart-context.tsx`, resolve optimistic update race conditions, and add typography fallback fonts in `layout.tsx`.
</TASK>

<SUBAGENT_DELEGATION_DIRECTIVE>
- Use `invoke_subagent` to inspect Storefront Cart Context TypeScript interfaces and font loading optimization.
</SUBAGENT_DELEGATION_DIRECTIVE>

<ANTIGRAVITY_SLASH_COMMANDS>
- /goal: Execute autonomously until Cart Context type safety and font loading pass build checks.
</ANTIGRAVITY_SLASH_COMMANDS>

<ANTIGRAVITY_WORKFLOW>
1. RESEARCH & INSPECTION PHASE:
   - View `apps/storefront/src/lib/context/cart-context.tsx` (lines 102–195) and `apps/storefront/src/app/layout.tsx` (lines 35–40).

2. IMPLEMENTATION PHASE:
   - Target files: `apps/storefront/src/lib/context/cart-context.tsx`, `apps/storefront/src/app/layout.tsx`
   - **`cart-context.tsx`**: Replace all 7x `any` type assertions with strict TypeScript interfaces (`StoreCart`, `StoreCartLineItem`); wrap optimistic cart update state mutations with mutex lock or queue to prevent race conditions during concurrent item additions.
   - **`layout.tsx`**: Configure font fallback array (`fallback: ['system-ui', 'arial']`) on Cairo and Inter font loaders; validate country code parameter cleanly.

3. EMPIRICAL VERIFICATION & TESTING PHASE:
   - Run storefront build verification: `cd apps/storefront && npm run build`

4. PROCESS CLEANUP & LEARNING DIRECTIVE (CRITICAL):
   - Terminate any running subagents, background dev servers, or processes before completing turn.
</ANTIGRAVITY_WORKFLOW>

<ACCEPTANCE_CRITERIA>
- [ ] Subagents delegated for Cart Context type definitions.
- [ ] Zero `any` type assertions in `cart-context.tsx`.
- [ ] Optimistic cart mutations protected against concurrent race conditions.
- [ ] Font loaders include fallback font families.
- [ ] Storefront build completes with exit code 0.
- [ ] All subagents, background tasks, and dev servers are cleanly terminated.
</ACCEPTANCE_CRITERIA>
```

---
### Developer Prompt 10: Docker Compose Host Port Isolation, Redis Authentication & Sentinel HA Fix

```markdown
/goal

<TASK>
Remove default plaintext passwords, bind DB/Redis ports to 127.0.0.1, configure Redis authentication, and fix Dockerfile file ownership.
</TASK>

<SUBAGENT_DELEGATION_DIRECTIVE>
- Use `invoke_subagent` to inspect Docker Compose security hardening and Redis Sentinel HA configuration.
</SUBAGENT_DELEGATION_DIRECTIVE>

<ANTIGRAVITY_SLASH_COMMANDS>
- /goal: Execute autonomously until Docker Compose template and Dockerfiles pass security validation.
- /learn: Persist Docker container security rules to .gemini/rules.
</ANTIGRAVITY_SLASH_COMMANDS>

<ANTIGRAVITY_WORKFLOW>
1. RESEARCH & INSPECTION PHASE:
   - View `infrastructure/docker/docker-compose.tenant.yml` (lines 10–57), `infrastructure/docker/Dockerfile.backend` (lines 41–48), and `infrastructure/docker/Dockerfile.storefront`.

2. IMPLEMENTATION PHASE:
   - Target files: `infrastructure/docker/docker-compose.tenant.yml`, `infrastructure/docker/Dockerfile.backend`, `infrastructure/docker/Dockerfile.storefront`
   - **`docker-compose.tenant.yml`**: Remove hardcoded fallback passwords (`POSTGRES_PASSWORD:-postgres`); bind PostgreSQL (`127.0.0.1:5432:5432`) and Redis (`127.0.0.1:6379:6379`) to localhost interfaces only; enable Redis authentication (`requirepass`); configure 3-node Redis Sentinel quorum with healthcheck probes (`HEALTHCHECK`); set CPU and memory resource limits per container.
   - **`Dockerfile.backend` & `Dockerfile.storefront`**: Add `--chown=node:node` to all `COPY` instructions in build stages; add `HEALTHCHECK` probe instruction to `Dockerfile.backend`.

3. EMPIRICAL VERIFICATION & TESTING PHASE:
   - Run Docker compose config validation: `docker compose -f infrastructure/docker/docker-compose.tenant.yml config`

4. PROCESS CLEANUP & LEARNING DIRECTIVE (CRITICAL):
   - Execute `/learn` to store Docker security patterns.
   - Terminate any active subagents or background tasks before completing turn.
</ANTIGRAVITY_WORKFLOW>

<ACCEPTANCE_CRITERIA>
- [ ] Subagents delegated for Docker security inspection.
- [ ] `docker-compose.tenant.yml` contains zero default plaintext passwords.
- [ ] Database and Redis ports bound to `127.0.0.1` localhost interface.
- [ ] Redis authentication enabled.
- [ ] Dockerfiles include `--chown=node:node` and `HEALTHCHECK` probes.
- [ ] Docker Compose config passes validation.
- [ ] All subagents and background tasks are cleanly terminated.
</ACCEPTANCE_CRITERIA>
```
