# New Findings Remediation Prompt Pack (`PROMPT_SEQUENCE_NEW_68_AUDIT_FIXES.md`)

This prompt pack contains **6 newly identified developer prompts** engineered for **Google Antigravity Agentic IDE** to fix the brand new architectural gaps, CommonJS leaks, Paymob ID ambiguities, volumetric weight calculations, Gemini native JSON schemas, and Docker multi-tenant volume collisions discovered in the 6.8/10 evaluation report.

> [!IMPORTANT]
> **Subagent Directive**: Send these 6 prompts sequentially (Prompt 1 through Prompt 6) to your developer Antigravity instance. Every prompt explicitly instructs the agent to delegate research or sub-tasks to subagents (`invoke_subagent`) to maintain clean context and maximize execution speed.

---

### Developer Prompt 1: Fix CommonJS `module.exports` Leak & Cloud Managed Postgres SSL Settings in `medusa-config.ts`

```markdown
/goal

<TASK>
Fix CommonJS syntax leak on line 17 of `apps/backend/medusa-config.ts` (convert `module.exports` to `export default`) and configure managed cloud PostgreSQL SSL driver options.
</TASK>

<SUBAGENT_DELEGATION_DIRECTIVE>
- Use `invoke_subagent` (Role: "Codebase Researcher", TypeName: "research") to inspect Node16 ES module export conventions and Medusa v2 `databaseDriverOptions` SSL configurations.
</SUBAGENT_DELEGATION_DIRECTIVE>

<ANTIGRAVITY_SLASH_COMMANDS>
- /goal: Execute autonomously until medusa-config.ts uses ESM export default and cloud PostgreSQL SSL settings compile clean.
- /learn: Persist Medusa v2 ESM config and database driver rules to .gemini/rules.
</ANTIGRAVITY_SLASH_COMMANDS>

<ANTIGRAVITY_WORKFLOW>
1. RESEARCH & INSPECTION PHASE:
   - View `apps/backend/medusa-config.ts` (lines 15–25).

2. IMPLEMENTATION PHASE:
   - Target file: `apps/backend/medusa-config.ts`
   - **Line 17**: Replace `module.exports = defineConfig(...)` with `export default defineConfig(...)` to fix CommonJS syntax leaks in ESM Node16 module contexts.
   - **Database Config**: Add `databaseDriverOptions` SSL configuration supporting managed PostgreSQL services (Supabase, Neon, AWS RDS):
     ```typescript
     databaseDriverOptions: process.env.NODE_ENV === "production" ? {
       connection: {
         ssl: process.env.DB_SSL === "false" ? false : { rejectUnauthorized: false }
       }
     } : {}
     ```

3. EMPIRICAL VERIFICATION & TESTING PHASE:
   - Run TypeScript check: `cd apps/backend && npx tsc --noEmit`
   - Run backend build verification: `cd apps/backend && npm run build`

4. PROCESS CLEANUP & LEARNING DIRECTIVE (CRITICAL):
   - Execute `/learn` to store Medusa ESM config rules.
   - Terminate any running subagents, background dev servers, or processes before completing turn.
</ANTIGRAVITY_WORKFLOW>

<ACCEPTANCE_CRITERIA>
- [ ] Subagents delegated for ESM export syntax inspection.
- [ ] `medusa-config.ts` uses `export default defineConfig(...)`.
- [ ] `databaseDriverOptions` configures `connection.ssl` for cloud PostgreSQL compatibility.
- [ ] Backend build completes with exit code 0.
- [ ] All subagents and background tasks are cleanly terminated.
</ACCEPTANCE_CRITERIA>
```

---

### Developer Prompt 2: Fix Paymob Order ID vs. Transaction ID Resolution Ambiguity in `paymob/service.ts`

```markdown
/goal

<TASK>
Fix ID resolution ambiguity in `capturePayment()` and `refundPayment()` in `apps/backend/src/modules/paymob/service.ts` so API calls pass live Paymob Transaction IDs instead of Order IDs.
</TASK>

<SUBAGENT_DELEGATION_DIRECTIVE>
- Use `invoke_subagent` to inspect Paymob payment data payload resolution in `service.ts` to prevent 404 API rejections.
</SUBAGENT_DELEGATION_DIRECTIVE>

<ANTIGRAVITY_SLASH_COMMANDS>
- /goal: Execute autonomously until Paymob capture and refund calls reliably resolve Paymob Transaction IDs.
- /learn: Persist Paymob transaction ID resolution rules to .gemini/rules.
</ANTIGRAVITY_SLASH_COMMANDS>

<ANTIGRAVITY_WORKFLOW>
1. RESEARCH & INSPECTION PHASE:
   - View `apps/backend/src/modules/paymob/service.ts` (capturePayment and refundPayment methods).

2. IMPLEMENTATION PHASE:
   - Target file: `apps/backend/src/modules/paymob/service.ts`
   - Ensure capture and refund methods explicitly resolve `paymob_transaction_id` (e.g. `paymentData.paymob_transaction_id || paymentData.transaction_id || paymentData.id`) instead of passing `paymob_order_id` to `/acceptance/capture` or `/acceptance/void_refund/refund`.
   - Throw a descriptive Error if `paymob_transaction_id` is missing instead of returning silent mock objects (`{ simulated: true }`).

3. EMPIRICAL VERIFICATION & TESTING PHASE:
   - Run TypeScript check: `cd apps/backend && npx tsc --noEmit`
   - Run backend build verification: `cd apps/backend && npm run build`

4. PROCESS CLEANUP & LEARNING DIRECTIVE (CRITICAL):
   - Execute `/learn` to store Paymob ID resolution rules.
   - Terminate any running subagents, background dev servers, or processes before completing turn.
</ANTIGRAVITY_WORKFLOW>

<ACCEPTANCE_CRITERIA>
- [ ] Subagents delegated for Paymob transaction ID payload inspection.
- [ ] `capturePayment()` and `refundPayment()` pass live Paymob Transaction IDs to API endpoints.
- [ ] Missing credentials throw explicit Errors instead of returning `{ simulated: true }`.
- [ ] Backend build completes with exit code 0.
- [ ] All subagents and background tasks are cleanly terminated.
</ACCEPTANCE_CRITERIA>
```

---

### Developer Prompt 3: Implement Bosta Volumetric Weight Formula & Fix Redis Cache Key Float Quantization

```markdown
/goal

<TASK>
Implement chargeable volumetric weight formula `Math.max(actualWeight, (L*W*H)/5000)` and fix float quantization cache collisions in `apps/backend/src/modules/bosta/service.ts`.
</TASK>

<SUBAGENT_DELEGATION_DIRECTIVE>
- Delegate Bosta dimensional weight calculations and Redis cache key format checks to a subagent via `invoke_subagent`.
</SUBAGENT_DELEGATION_DIRECTIVE>

<ANTIGRAVITY_SLASH_COMMANDS>
- /goal: Execute autonomously until Bosta volumetric weight formula and Redis cache keys compile clean.
- /learn: Persist logistics rate calculation and caching rules to .gemini/rules.
</ANTIGRAVITY_SLASH_COMMANDS>

<ANTIGRAVITY_WORKFLOW>
1. RESEARCH & INSPECTION PHASE:
   - View `apps/backend/src/modules/bosta/service.ts` (lines 41–135).

2. IMPLEMENTATION PHASE:
   - Target file: `apps/backend/src/modules/bosta/service.ts`
   - **Volumetric Weight Formula**: Calculate volumetric dimensional weight `volumetricWeight = (length * width * height) / 5000`; set `chargeableWeight = Math.max(actualWeight, volumetricWeight)`.
   - **Redis Cache Key Float Quantization**: Replace `Math.round(weight)` with 1-decimal float formatting `chargeableWeight.toFixed(1)` (e.g. `BOSTA_RATE_${cityId}_W${chargeableWeight.toFixed(1)}`) to eliminate weight collision bugs across carrier billing tiers.

3. EMPIRICAL VERIFICATION & TESTING PHASE:
   - Run TypeScript check: `cd apps/backend && npx tsc --noEmit`
   - Run backend build verification: `cd apps/backend && npm run build`

4. PROCESS CLEANUP & LEARNING DIRECTIVE (CRITICAL):
   - Execute `/learn` to store volumetric weight calculation rules.
   - Terminate any running subagents, background dev servers, or processes before completing turn.
</ANTIGRAVITY_WORKFLOW>

<ACCEPTANCE_CRITERIA>
- [ ] Subagents delegated for volumetric weight formula inspection.
- [ ] Chargeable weight uses `Math.max(actualWeight, (L*W*H)/5000)`.
- [ ] Redis cache key formats weight with `toFixed(1)` to eliminate float quantization collisions.
- [ ] Backend build completes with exit code 0.
- [ ] All subagents and background tasks are cleanly terminated.
</ACCEPTANCE_CRITERIA>
```

---

### Developer Prompt 4: Use Gemini Native `responseMimeType: "application/json"` Structured Output in `gemini-ai/client.ts`

```markdown
/goal

<TASK>
Replace regex string stripping (`replace(/```json/g, "")`) with Gemini native `responseMimeType: "application/json"` structured schema generation in `apps/backend/src/modules/gemini-ai/client.ts`.
</TASK>

<SUBAGENT_DELEGATION_DIRECTIVE>
- Use `invoke_subagent` to inspect Google AI Studio SDK `responseMimeType` and `responseSchema` options.
</SUBAGENT_DELEGATION_DIRECTIVE>

<ANTIGRAVITY_SLASH_COMMANDS>
- /goal: Execute autonomously until Gemini AI client generates structured JSON via native Google AI Studio SDK configs.
- /learn: Persist LLM structured JSON output rules to .gemini/rules.
</ANTIGRAVITY_SLASH_COMMANDS>

<ANTIGRAVITY_WORKFLOW>
1. RESEARCH & INSPECTION PHASE:
   - View `apps/backend/src/modules/gemini-ai/client.ts` (lines 40–85).

2. IMPLEMENTATION PHASE:
   - Target file: `apps/backend/src/modules/gemini-ai/client.ts`
   - Configure `generationConfig` with `responseMimeType: "application/json"` when invoking Gemini AI model.
   - Parse returned structured JSON directly with `JSON.parse(response.text())` without relying on fragile markdown codeblock regex string replacements.

3. EMPIRICAL VERIFICATION & TESTING PHASE:
   - Run TypeScript check: `cd apps/backend && npx tsc --noEmit`
   - Run backend build verification: `cd apps/backend && npm run build`

4. PROCESS CLEANUP & LEARNING DIRECTIVE (CRITICAL):
   - Execute `/learn` to store structured LLM output rules.
   - Terminate any running subagents, background dev servers, or processes before completing turn.
</ANTIGRAVITY_WORKFLOW>

<ACCEPTANCE_CRITERIA>
- [ ] Subagents delegated for Gemini structured JSON SDK research.
- [ ] `gemini-ai/client.ts` configures `responseMimeType: "application/json"`.
- [ ] Direct `JSON.parse()` executes safely without regex codeblock stripping.
- [ ] Backend build completes with exit code 0.
- [ ] All subagents and background tasks are cleanly terminated.
</ACCEPTANCE_CRITERIA>
```

---

### Developer Prompt 5: Prevent Multi-Tenant Docker Compose Volume Collisions (`-p tenant_${TENANT_ID}`) in `provision-tenant.sh`

```markdown
/goal

<TASK>
Update `infrastructure/scripts/provision-tenant.sh` to include `-p tenant_${TENANT_ID}` in all Docker Compose commands to prevent multi-tenant database volume overwrites.
</TASK>

<SUBAGENT_DELEGATION_DIRECTIVE>
- Delegate Docker Compose project naming (`-p`) and multi-tenant container isolation checks to a subagent via `invoke_subagent`.
</SUBAGENT_DELEGATION_DIRECTIVE>

<ANTIGRAVITY_SLASH_COMMANDS>
- /goal: Execute autonomously until tenant provisioning script isolates multi-tenant Docker compose project namespaces.
- /learn: Persist Docker multi-tenant isolation rules to .gemini/rules.
</ANTIGRAVITY_SLASH_COMMANDS>

<ANTIGRAVITY_WORKFLOW>
1. RESEARCH & INSPECTION PHASE:
   - View `infrastructure/scripts/provision-tenant.sh`.

2. IMPLEMENTATION PHASE:
   - Target file: `infrastructure/scripts/provision-tenant.sh`
   - Update all `docker compose` invocations to include `-p "tenant_${TENANT_ID}"`:
     ```bash
     docker compose -p "tenant_${TENANT_ID}" --env-file "${TENANT_DIR}/.env" -f "${TENANT_DIR}/infrastructure/docker/docker-compose.tenant.yml" up -d --build
     ```
   - Ensure PostgreSQL database volumes and network namespaces are scoped strictly per tenant ID.

3. EMPIRICAL VERIFICATION & TESTING PHASE:
   - Run bash syntax check: `bash -n infrastructure/scripts/provision-tenant.sh`

4. PROCESS CLEANUP & LEARNING DIRECTIVE (CRITICAL):
   - Terminate any running subagents or shell tasks before completing turn.
</ANTIGRAVITY_WORKFLOW>

<ACCEPTANCE_CRITERIA>
- [ ] Subagents delegated for shell script inspection.
- [ ] All `docker compose` invocations in `provision-tenant.sh` include `-p "tenant_${TENANT_ID}"`.
- [ ] Script passes `bash -n` syntax check cleanly.
- [ ] All subagents and background tasks are cleanly terminated.
</ACCEPTANCE_CRITERIA>
```

---

### Developer Prompt 6: Bind Container Application Ports to `127.0.0.1:${PORT}` in Infrastructure Scripts

```markdown
/goal

<TASK>
Update `infrastructure/docker/docker-compose.tenant.yml` and `infrastructure/scripts/provision-tenant.sh` so container application ports bind to `127.0.0.1:${PORT}` instead of `0.0.0.0:${PORT}`.
</TASK>

<SUBAGENT_DELEGATION_DIRECTIVE>
- Use `invoke_subagent` to inspect Docker Compose port binding security guidelines and Caddy reverse proxy routing.
</SUBAGENT_DELEGATION_DIRECTIVE>

<ANTIGRAVITY_SLASH_COMMANDS>
- /goal: Execute autonomously until application containers bind exclusively to 127.0.0.1 localhost interfaces.
- /learn: Persist host interface binding security rules to .gemini/rules.
</ANTIGRAVITY_SLASH_COMMANDS>

<ANTIGRAVITY_WORKFLOW>
1. RESEARCH & INSPECTION PHASE:
   - View `infrastructure/docker/docker-compose.tenant.yml` and `infrastructure/scripts/provision-tenant.sh`.

2. IMPLEMENTATION PHASE:
   - Target files: `infrastructure/docker/docker-compose.tenant.yml`, `infrastructure/scripts/provision-tenant.sh`
   - Update port mapping definitions from `${PORT}:${PORT}` to `127.0.0.1:${PORT}:${PORT}` for backend and storefront container services.
   - Ensures direct public requests cannot bypass Caddy reverse proxy rate limits and dynamic SSL routing.

3. EMPIRICAL VERIFICATION & TESTING PHASE:
   - Run Docker compose config validation: `docker compose -f infrastructure/docker/docker-compose.tenant.yml config`
   - Run bash syntax check: `bash -n infrastructure/scripts/provision-tenant.sh`

4. PROCESS CLEANUP & LEARNING DIRECTIVE (CRITICAL):
   - Terminate any active subagents or background tasks before completing turn.
</ANTIGRAVITY_WORKFLOW>

<ACCEPTANCE_CRITERIA>
- [ ] Subagents delegated for Docker security inspection.
- [ ] Container application ports bind to `127.0.0.1:${PORT}`.
- [ ] Docker Compose config and bash script pass validation tests.
- [ ] All subagents and background tasks are cleanly terminated.
</ACCEPTANCE_CRITERIA>
```
