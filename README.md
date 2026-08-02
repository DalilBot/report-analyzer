# Final Production Polish Developer Prompt Pack (`PROMPT_SEQUENCE_FINAL_ENHANCEMENTS.md`)

This prompt pack contains **the final 3 developer prompts** to implement the next-stage CI/CD, OpenTelemetry metrics, and Caddyfile backup infrastructure enhancements identified in the 9.8/10 audit report.

> [!IMPORTANT]
> **Subagent Directive**: Send these 3 prompts sequentially (Prompt 1 through Prompt 3) to your developer Antigravity instance. Every prompt explicitly instructs the agent to delegate research or sub-tasks to subagents (`invoke_subagent`) to maintain clean context and maximize execution speed.

---

### Developer Prompt 1: GitHub Actions CI/CD Integration Test Pipeline (`.github/workflows/ci.yml`)

```markdown
/goal

<TASK>
Create a GitHub Actions CI pipeline `.github/workflows/ci.yml` that provisions PostgreSQL 15 & Redis 7 containers, builds the monorepo, and executes automated integration tests.
</TASK>

<SUBAGENT_DELEGATION_DIRECTIVE>
- Use `invoke_subagent` (Role: "Codebase Researcher", TypeName: "research") to inspect monorepo build scripts across `package.json`, `apps/backend`, and `apps/storefront`.
</SUBAGENT_DELEGATION_DIRECTIVE>

<ANTIGRAVITY_SLASH_COMMANDS>
- /goal: Execute autonomously until GitHub Actions workflow file passes YAML syntax validation.
- /learn: Persist GitHub Actions CI/CD pipeline configuration patterns to .gemini/rules.
</ANTIGRAVITY_SLASH_COMMANDS>

<ANTIGRAVITY_WORKFLOW>
1. RESEARCH & INSPECTION PHASE:
   - View root `package.json`, `apps/backend/package.json`, and `apps/storefront/package.json`.

2. IMPLEMENTATION PHASE:
   - Target file: `.github/workflows/ci.yml`
   - Configure a GitHub Actions workflow triggered on `push` and `pull_request` to `main`:
     - Service Containers: `postgres:15-alpine` (database `medusa-db`) and `redis:7-alpine`.
     - Job Steps: Node.js 20 setup, dependency installation (`npm ci`), workspace build (`npm run build`), TypeScript typecheck (`npx tsc --noEmit`), and test suite execution (`npm run test`).

3. EMPIRICAL VERIFICATION & TESTING PHASE:
   - Verify YAML file creation: Check `.github/workflows/ci.yml` structure.

4. PROCESS CLEANUP & LEARNING DIRECTIVE (CRITICAL):
   - Execute `/learn` to store CI/CD pipeline rules.
   - Terminate any running subagents or processes before completing turn.
</ANTIGRAVITY_WORKFLOW>

<ACCEPTANCE_CRITERIA>
- [ ] Subagents delegated for monorepo package script inspection.
- [ ] `.github/workflows/ci.yml` includes PostgreSQL 15 and Redis 7 service containers.
- [ ] Workflow steps execute workspace build, TypeScript check, and test commands.
- [ ] All subagents and background tasks are cleanly terminated.
</ACCEPTANCE_CRITERIA>
```

---

### Developer Prompt 2: OpenTelemetry & Prometheus Metrics Instrumentation (`apps/backend/src/instrumentation.ts`)

```markdown
/goal

<TASK>
Implement OpenTelemetry SDK metrics exporter in `apps/backend/src/instrumentation.ts` tracking Paymob payment gateway API latencies, Bosta rate cache hits/misses, and ETA tax submission DLQ error counts.
</TASK>

<SUBAGENT_DELEGATION_DIRECTIVE>
- Use `invoke_subagent` to research OpenTelemetry Node.js SDK instrumentation patterns for Medusa v2.
</SUBAGENT_DELEGATION_DIRECTIVE>

<ANTIGRAVITY_SLASH_COMMANDS>
- /goal: Execute autonomously until OpenTelemetry metrics instrumentation compiles cleanly.
- /learn: Persist OpenTelemetry telemetry patterns to .gemini/rules.
</ANTIGRAVITY_SLASH_COMMANDS>

<ANTIGRAVITY_WORKFLOW>
1. RESEARCH & INSPECTION PHASE:
   - View `apps/backend/src/instrumentation.ts` (or create if missing) and inspect OpenTelemetry metrics imports (`@opentelemetry/sdk-metrics`, `@opentelemetry/api`).

2. IMPLEMENTATION PHASE:
   - Target file: `apps/backend/src/instrumentation.ts`
   - Register OpenTelemetry Meter Provider exporting Prometheus/OTLP metrics.
   - Create custom counters and histograms:
     - `paymob_request_duration_seconds` (Histogram tracking Paymob API latency).
     - `bosta_rate_cache_hits_total` / `bosta_rate_cache_misses_total` (Counters tracking shipping cache performance).
     - `eta_tax_dlq_errors_total` (Counter tracking failed ETA tax submissions).

3. EMPIRICAL VERIFICATION & TESTING PHASE:
   - Run TypeScript check: `cd apps/backend && npx tsc --noEmit`
   - Run backend build verification: `cd apps/backend && npm run build`

4. PROCESS CLEANUP & LEARNING DIRECTIVE (CRITICAL):
   - Execute `/learn` to store OpenTelemetry metrics rules.
   - Terminate any running subagents, background dev servers, or processes before completing turn.
</ANTIGRAVITY_WORKFLOW>

<ACCEPTANCE_CRITERIA>
- [ ] Subagents delegated for OpenTelemetry SDK pattern research.
- [ ] `apps/backend/src/instrumentation.ts` exports Prometheus/OTLP metrics for Paymob, Bosta, and ETA Tax.
- [ ] Backend build completes with exit code 0.
- [ ] All subagents, background tasks, and dev servers are cleanly terminated.
</ACCEPTANCE_CRITERIA>
```

---

### Developer Prompt 3: Automated Caddyfile & Dynamic Tenant Domain Backup Cron Script (`infrastructure/scripts/backup-caddyfile.sh`)

```markdown
/goal

<TASK>
Create automated backup script `infrastructure/scripts/backup-caddyfile.sh` backing up Caddy configurations to timestamped tar.gz archives with automated rotation pruning.
</TASK>

<SUBAGENT_DELEGATION_DIRECTIVE>
- Delegate bash tar compression and pruning logic verification to a subagent via `invoke_subagent`.
</SUBAGENT_DELEGATION_DIRECTIVE>

<ANTIGRAVITY_SLASH_COMMANDS>
- /goal: Execute autonomously until Caddyfile backup script passes bash syntax check.
- /learn: Persist backup cron script patterns to .gemini/rules.
</ANTIGRAVITY_SLASH_COMMANDS>

<ANTIGRAVITY_WORKFLOW>
1. RESEARCH & INSPECTION PHASE:
   - View `infrastructure/scripts/caddy-domain-router.sh` and inspect Caddy config directory paths (`/etc/caddy/Caddyfile`, `/etc/caddy/tenants/`).

2. IMPLEMENTATION PHASE:
   - Target file: `infrastructure/scripts/backup-caddyfile.sh`
   - Create bash script that archives `/etc/caddy/Caddyfile` and `/etc/caddy/tenants/*.caddy` into `/var/backups/caddy/caddy_backup_$(date +%Y%m%d_%H%M%S).tar.gz`.
   - Include automated rotation pruning retaining the last 30 daily backup archives (`find /var/backups/caddy -name "*.tar.gz" -mtime +30 -delete`).

3. EMPIRICAL VERIFICATION & TESTING PHASE:
   - Run bash syntax check: `bash -n infrastructure/scripts/backup-caddyfile.sh`

4. PROCESS CLEANUP & LEARNING DIRECTIVE (CRITICAL):
   - Execute `/learn` to store backup script rules.
   - Terminate any running subagents or shell tasks before completing turn.
</ANTIGRAVITY_WORKFLOW>

<ACCEPTANCE_CRITERIA>
- [ ] Subagents delegated for bash syntax check.
- [ ] `infrastructure/scripts/backup-caddyfile.sh` creates timestamped tar.gz backups of Caddy configs.
- [ ] Includes 30-day rotation pruning logic.
- [ ] Script passes `bash -n` syntax check cleanly.
- [ ] All subagents and background tasks are cleanly terminated.
</ACCEPTANCE_CRITERIA>
```
