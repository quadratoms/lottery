# Django + React 1–99 Lottery System — Processes & Requirements (Nigeria/Africa)

## 0) Document purpose
A practical, implementation-ready specification to build an online number-based betting system (focus: **pick-1 from 1–99** and extensions), using **Django** (backend) and **React** (frontend). It includes: scope, functional & non-functional requirements, domain model, API design, RNG/draw mechanics, payout logic, integrations (Paystack/Flutterwave/Remita), security/compliance notes for Nigeria, DevOps, testing, and delivery plan.

---

## 1) Product scope & goals
- **Core value**: Let verified adults in Nigeria/Africa pick numbers (1–99), place bets securely, and receive instant/scheduled draw outcomes with fair, audited randomness, fast payouts, and transparent history.
- **MVP game**: Pick **1** number from **1–99**. If the drawn number matches, user wins based on a configurable odds multiplier. (Extensions below.)
- **Market fit**: Mobile-first, low-bandwidth UI; local payments; clear rules; strong trust signals (licence, audit, RNG certificate).

### Game extensions (post-MVP)
- **Pick-2 (ordered/unordered)**, **Pick-3 (digits)**, **hot/cold quick-pick**, **bundles** (multi-lines), **subscriptions** (multi-draw), **mini Keno** (e.g., pick up to N from 1–30), **raffle** draws.

---

## 2) User roles & permissions
- **Player**: register, KYC, deposit, pick numbers, place bets, view tickets/results, withdraw.
- **Agent** (optional): onboard players, assist deposits/withdrawals, earn commission.
- **Ops/Admin**: manage draws, odds, game configs, users, limits, payments, disputes, reports.
- **Auditor**: read-only access to RNG logs, draws, payouts, tamper-evident logs.

---

## 3) Functional requirements (FR)
**FR1 Registration & auth**
- Email/phone signup, passwordless or OTP login (SMS/email). 2FA optional.
- KYC: BVN/NIN verification (via provider), selfie + ID (later phase), date of birth (>=18), address.

**FR2 Wallet & payments**
- Deposit via **Paystack/Flutterwave/Remita**; webhooks to confirm.
- Withdraw to bank accounts (NIP) after KYC & risk checks; approval workflow & limits.
- Ledger with double-entry accounting: available, locked, bonus balances.

**FR3 Game play**
- Select number 1–99; choose stake (min/max, per user/day limits).
- Place bet for **next scheduled draw** or **instant draw** (if enabled).
- Display **implied odds/payout** before confirm; show T&Cs.
- Generate immutable **ticket** with ID, hash, placed_at, draw_id.

**FR4 Draws & results**
- **Scheduled draws** (e.g., every 5/10/15 minutes) via Celery beat.
- **RNG**: cryptographically secure PRNG with secure seeding; per-draw seed, seed hash pre-commit, post-reveal.
- Publish winning number, seed, proof; close wagering before draw lock time.

**FR5 Payouts**
- Auto-calc winnings by odds table; credit wallet; record taxes/withholding if applicable.
- Handle partial failures (idempotent payout tasks).

**FR6 History & transparency**
- Ticket history, bets, deposits/withdrawals, statements (CSV/PDF).
- Public results page: draw timeline, winning numbers, seed/commitment proofs.

**FR7 Limits, risk & RG**
- Session limits, daily loss limits, bet size caps; self-exclusion; cooldown.
- Velocity checks, unusual patterns flagged.

**FR8 Admin console**
- Manage users, limits, KYC, draws, odds, game configs, payment rails.
- Reconciliation reports; audit trails; role-based access.

**FR9 Notifications**
- Email/SMS/Push (web push) for wins, withdrawals, security alerts.

**FR10 Localization**
- NGN currency, time zone Africa/Lagos; i18n support for EN + local languages later.

---

## 4) Non-functional requirements (NFR)
- **Availability**: 99.5%+ monthly (MVP), 99.9%+ post-MVP.
- **Performance**: API p95 < 300ms under typical load; < 1s at p99.
- **Scale**: 50k DAU MVP; 1k RPS bursts at draw close.
- **Security**: TLS 1.2+, strong cipher suites; OWASP ASVS L2+; PCI-DSS scope minimization.
- **Compliance**: NLRC + state board licensing; KYC/AML (NFIU); data protection (NDPR); age gating.
- **Observability**: central logs, metrics, traces; alerting SLOs.

---

## 5) Domain model (ERD outline)
- **User**(id, email, phone, dob, kyc_status, …)
- **Wallet**(user_id, currency, available, locked, bonus)
- **LedgerEntry**(id, wallet_id, type, amount, balance_after, ref, meta)
- **Payment**(id, user_id, type=deposit/withdrawal, provider, status, amount, fees, external_ref)
- **GameConfig**(id, name, range_min=1, range_max=99, draw_interval_sec, lock_offset_sec, min_bet, max_bet, odds_scheme_id)
- **OddsScheme**(id, bet_type, payout_multiplier, tax_rate, active_from)
- **Draw**(id, game_id, scheduled_at, locked_at, status=pending/closed/resulted, seed_commit_hash, seed_reveal, winning_number)
- **Ticket**(id, user_id, draw_id, selection, stake, potential_payout, status=pending/won/lost/void, placed_at, ticket_hash)
- **Payout**(id, ticket_id, amount, tax_withheld, paid_at, status)
- **KycCheck**(id, user_id, provider, result, reference, created_at)
- **AuditLog**(id, actor_id, action, entity_type, entity_id, payload, ip, created_at)

---

## 6) Odds & payout design (Pick-1 from 1–99)
- **Raw probability**: 1 / 99 ≈ 1.0101%.
- **Fair payout**: ~99× stake (ignoring costs).
- **House edge**: choose **payout multiplier** M < 99 to achieve target margin.

**Example payout table (configurable):**
- Pick-1: **85×** multiplier ⇒ approx house margin ≈ (1 − 85/99) ≈ 14.1% (before fees & promos).
- (Optional) Tiered odds by draw type or time of day.

> Store multipliers in **OddsScheme** so you can A/B test and adjust without code changes. Always disclose odds.

---

## 7) RNG & fairness (commit–reveal)
1) Before each draw **D**, server generates **seed_reveal_D** (256-bit) and stores **seed_commit_hash_D = SHA-256(seed_reveal_D)** in DB; publish commit hash on results page ahead of time.
2) At draw time, generate winning number by `winning = (HMAC(seed_reveal_D, draw_nonce) mod 99) + 1`.
3) Publish **seed_reveal_D** after draw; anyone can hash it to match the pre-committed hash. Optionally, blend low-entropy beacon (e.g., block hash, time) into HMAC message (auditable) without affecting secrecy of seed.
4) External lab certification later (GLI/iTech). Keep deterministic, reproducible replay from stored inputs.

---

## 8) API design (REST, versioned /api/v1)
### Auth & user
- `POST /auth/register` {email/phone, password/otp}
- `POST /auth/login`
- `POST /auth/otp/send`, `POST /auth/otp/verify`
- `GET /me` (profile)
- `POST /me/kyc` (start), `GET /me/kyc/status`

### Wallet & payments
- `GET /wallet`
- `GET /wallet/statement?from=&to=`
- `POST /payments/deposit` {provider, amount}
- `POST /payments/withdraw` {amount, bank_account_id}
- `POST /payments/webhook/{provider}` (no auth; HMAC verify)

### Game & draws
- `GET /games` (range, min/max stake, intervals)
- `GET /draws/next?game_id=`
- `GET /draws/recent?limit=100`
- `GET /draws/{id}` (includes commit hash, reveal if completed)

### Tickets & payouts
- `POST /tickets` {game_id, draw_id, selection: int 1–99, stake}
- `GET /tickets?status=&page=`
- `GET /tickets/{id}`
- `GET /payouts?ticket_id=`

### Admin
- `GET/POST /admin/odds-schemes`
- `GET/POST /admin/games`
- `GET /admin/reports/reconciliation?date=`
- `POST /admin/users/{id}/limits` `POST /admin/users/{id}/ban`

**Conventions**: JWT Bearer auth; idempotency-key header for POST (payments, tickets); pagination; RFC 7807 error format; request/response schemas via OpenAPI.

---

## 9) Django implementation plan
**Apps**: `accounts`, `kyc`, `wallet`, `payments`, `games`, `draws`, `tickets`, `payouts`, `adminpanel`, `audit`, `notifications`.

**Key packages**
- Django 5.x, Django REST Framework (DRF), django-filter, drf-spectacular (OpenAPI), django-cors-headers
- Auth: django-allauth or custom OTP microservice; djangorestframework-simplejwt
- Celery + Redis (broker & beat), django-redis (cache)
- PostgreSQL, psycopg
- Payment SDKs (Paystack/Flutterwave/Remita) or plain HTTPS
- Logging: structlog, drf-extensions; Sentry

**Models (sketch)**
```python
# tickets/models.py
class Ticket(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    draw = models.ForeignKey('draws.Draw', on_delete=models.PROTECT)
    selection = models.PositiveSmallIntegerField()  # 1..99
    stake = models.DecimalField(max_digits=12, decimal_places=2)
    potential_payout = models.DecimalField(max_digits=14, decimal_places=2)
    status = models.CharField(max_length=16, choices=TicketStatus.choices, default=TicketStatus.PENDING)
    placed_at = models.DateTimeField(auto_now_add=True)
    ticket_hash = models.CharField(max_length=64, db_index=True)
```

```python
# draws/models.py
class Draw(models.Model):
    game = models.ForeignKey('games.GameConfig', on_delete=models.PROTECT)
    scheduled_at = models.DateTimeField(db_index=True)
    locked_at = models.DateTimeField()
    status = models.CharField(max_length=16, choices=DrawStatus.choices, default=DrawStatus.PENDING)
    seed_commit_hash = models.CharField(max_length=64)
    seed_reveal = models.CharField(max_length=128, null=True, blank=True)
    winning_number = models.PositiveSmallIntegerField(null=True, blank=True)
```

```python
# wallet/models.py
class Wallet(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    currency = models.CharField(max_length=3, default='NGN')
    available = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    locked = models.DecimalField(max_digits=14, decimal_places=2, default=0)

class LedgerEntry(models.Model):
    wallet = models.ForeignKey(Wallet, on_delete=models.PROTECT)
    type = models.CharField(max_length=32)  # BET_PLACE, BET_REFUND, WIN_PAYOUT, DEPOSIT, WITHDRAWAL, FEE
    amount = models.DecimalField(max_digits=14, decimal_places=2)
    balance_after = models.DecimalField(max_digits=14, decimal_places=2)
    ref = models.CharField(max_length=64, db_index=True)
    meta = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)
```

**Services (examples)**
```python
# draws/services.py
import hmac, hashlib, os

def commit_seed():
    seed = os.urandom(32).hex()
    commit = hashlib.sha256(seed.encode()).hexdigest()
    return seed, commit

def draw_winning(seed: str, nonce: str) -> int:
    digest = hmac.new(seed.encode(), nonce.encode(), hashlib.sha256).hexdigest()
    n = int(digest, 16) % 99 + 1
    return n
```

```python
# tickets/services.py
from django.db import transaction

def place_ticket(user, draw, selection, stake):
    assert 1 <= selection <= 99
    with transaction.atomic():
        wallet = Wallet.objects.select_for_update().get(user=user)
        # lock funds
        if wallet.available < stake:
            raise InsufficientFunds
        wallet.available -= stake
        wallet.locked += stake
        wallet.save()
        # compute potential payout from active odds scheme
        multiplier = get_multiplier(draw.game)
        potential = stake * Decimal(multiplier)
        ticket = Ticket.objects.create(
            user=user, draw=draw, selection=selection, stake=stake,
            potential_payout=potential, ticket_hash=hash_ticket(...)
        )
        LedgerEntry.objects.create(...)
        return ticket
```

**Celery tasks**
- `schedule_draws()` – create upcoming draws & seed commits.
- `lock_draw(draw_id)` – set status=closed; prevent new tickets.
- `execute_draw(draw_id)` – reveal seed, compute winning, result tickets, payouts.
- `payout_winners(draw_id)` – credit wallets, release locks.
- `reconcile_payments()` – pull provider settlements.

**Idempotency**: use unique keys for critical tasks (ticket id, draw id) and **outbox pattern** for webhooks.

---

## 10) Payments (Nigeria-first)
**Providers**: Paystack, Flutterwave, Remita (cards, bank transfer, USSD). Add Mobile Money per region.

**Flow (deposit)**:
1) Client requests `POST /payments/deposit {amount}`.
2) Server creates Payment row (status=pending) and initializes provider session (secret key server-side).
3) Client is redirected or given authorization params (no secrets in browser).
4) Provider completes, fires **webhook** to `/payments/webhook/{provider}`.
5) Verify HMAC signature & event; mark Payment as success; **credit wallet**; emit ledger entries.

**Flow (withdrawal)**:
1) User requests withdrawal; server checks KYC, limits, cooldowns.
2) Create payout via provider (or manual ops queue for large amounts); status=pending.
3) On provider confirmation, mark success; debit wallet; record ledger entries.

**Reconciliation**: daily job to match provider settlements to internal ledger; variance report to Admin.

---

## 11) React frontend architecture
**Stack**: React 18, TypeScript, React Router, Redux Toolkit + RTK Query, Zod (validation), Tailwind CSS, Vite.

**Structure**
```
src/
  app/ (store.ts, api.ts)
  pages/
    Home.tsx
    Play.tsx          # number grid 1–99, stake input, bet slip
    Results.tsx       # recent draws, seed commit/reveal proofs
    Wallet.tsx        # deposits/withdrawals, statements
    Tickets.tsx
    Profile.tsx       # KYC, limits, security
  components/
    NumberGrid.tsx
    StakeInput.tsx
    TicketList.tsx
    DrawCountdown.tsx
    ResultCard.tsx
    Toast.tsx
  features/
    auth/, wallet/, tickets/, draws/
```

**UX notes**
- **NumberGrid**: 10×10 grid (1..99 with one empty/“00” blocked); big hit area; selected highlight; quick-pick.
- Show **countdown** to next draw; lock UI X seconds before `locked_at`.
- Offline support for results history (localStorage / IndexedDB).
- Error states for payment pending, draw locked, insufficient funds.

---

## 12) Security & compliance (Nigeria)
- **Age & KYC**: enforce 18+; NIN/BVN checks via approved aggregators; keep audit of consents.
- **AML/CFT**: monitor deposits/withdrawals, SARs to NFIU as required; PEP/sanctions screening vendor.
- **Data**: NDPR-aligned privacy policy; encrypt PII at rest (PGP or field-level AES); strict RBAC.
- **Payments**: keep card data off-scope (hosted fields/redirects); store only tokens; rotate API keys; IP allow-list webhooks.
- **AppSec**: OWASP Top 10; CSRF protection (for cookie sessions), rate limits, bot defense; secrets in Vault.
- **Fairness**: publish commit–reveal, retain tamper-evident logs (hash-chained log records) and third-party audits.

---

## 13) Observability & ops
- **Metrics**: bets/min, conversion, payout ratio, GGR, DAU/MAU, failed payments, draw latency.
- **Logs**: structured JSON; correlation IDs per request; webhook logs.
- **Tracing**: OpenTelemetry to backend + Celery workers.
- **Alerts**: draw failures, payment variance, error rate spikes, balance mismatch.

---

## 14) Testing strategy
- **Unit**: RNG functions, odds calc, ledger accounting, limits, API validators.
- **Integration**: deposit webhooks, draw life-cycle, payout idempotency, KYC flows (mocked providers).
- **E2E**: Cypress/Playwright for core journeys; mobile viewports.
- **Load/Perf**: k6/Gatling; simulate draw-close spikes; DB tuning.
- **Security**: SAST, DAST, dependency scans; pentest before launch.

---

## 15) Deployment & DevOps
- **Envs**: dev → staging → prod; seeded test data; sandbox keys.
- **Containers**: Docker for API, worker, scheduler, Nginx; docker-compose for local; Helm on Kubernetes post-MVP.
- **CI/CD**: GitHub Actions; run tests, build images, run migrations; feature flags for risky changes.
- **DB**: PostgreSQL HA (managed: RDS/Azure PG); nightly backups; PITR.
- **Cache**: Redis (managed) for sessions, rate-limit, Celery broker.
- **Static**: S3 + CloudFront (or Azure/GCP equivalents); HTTP/2 + gzip/br.

---

## 16) Migration & data integrity patterns
- **Ledger**: only append; never update balances directly; recompute wallet from ledger during audits.
- **Outbox**: publish webhooks/events from DB-committed outbox to avoid lost notifications.
- **Idempotency**: idempotency-key header → request table with status + response cache.

---

## 17) Admin & reporting
- Dashboards: GGR, hold %, ARPU, cohort retention.
- Financial: deposits vs. withdrawals, settlement reconciliation, operator take.
- Compliance: KYC status, SARs exported CSV, self-exclusion list.
- Game: hit frequency, hot/cold numbers (for user curiosity—avoid implying causality).

---

## 18) Example workflows (sequence summaries)
**Place bet** → Auth user → fetch next draw → validate selection + stake → lock funds → create ticket → return ticket + potential payout → UI shows confirmation.

**Run draw** → Celery lock draw → compute winning from seed → mark tickets won/lost → payout winners (credit wallets) → publish results + reveal seed → notify winners.

**Deposit** → init payment → provider checkout → webhook → verify signature → credit wallet → show success.

**Withdrawal** → request → risk/KYC checks → initiate payout → on success debit wallet → notify user.

---

## 19) Backlog (MVP → v1.1)
**MVP (6–8 weeks targetable by a small team)**
- Auth (OTP), KYC basic, wallet + ledger, deposits, pick-1 game, scheduled draws (5min), commit–reveal RNG, payouts, results page, tickets/history, admin basics, logging/metrics, CI/CD, staging.

**v1.1**
- Withdrawals automation, advanced limits/self-exclusion, agents/affiliates, subscriptions, push notifications, comprehensive reporting, external RNG certification, mobile app wrappers (Capacitor/React Native shell).

---

## 20) Acceptance criteria (MVP highlights)
- Can register, pass KYC-l1, deposit NGN via at least one provider.
- Can place pick-1 bet for the next draw; UI prevents betting after lock time.
- Draw runs every 5 minutes; results published with seed reveal matching prior commit hash.
- Winners automatically credited; losers released lock; wallet & ledger always reconcile.
- Webhooks idempotent; reconciliation report has zero unexplained variance for settled day.
- Admin can change odds safely without code redeploy.

---

## 21) Sample configs (env)
```
DJANGO_SECRET_KEY=...
DATABASE_URL=postgres://...
REDIS_URL=redis://...
CELERY_BROKER_URL=redis://...
PAYSTACK_SECRET=...
PAYSTACK_PUBLIC=...
ALLOWED_HOSTS=...
JWT_SIGNING_KEY=...
```

---

## 22) Risk register (selected)
- **Regulatory**: licensing delays → Mitigate: start compliance early; consult NLRC.
- **Payments**: webhook spoofing → Mitigate: HMAC verify + IP allow-list.
- **RNG trust**: user skepticism → Mitigate: commit–reveal + third-party audit badge.
- **Ops**: draw failure → Mitigate: automated retries, runbooks, on-call.

---

## 23) Next steps
1) Confirm game parameters (interval, lock offset, min/max stake, multiplier).
2) Set up repos (backend, frontend), base CI/CD, infrastructure-as-code.
3) Implement ledger/wallet, deposit flow, ticket placement.
4) Add draws (commit–reveal), payouts, results publication.
5) UAT on staging with sandbox payments; run simulated 1,000+ draws; sign off.

---

### Appendix A — Minimal DRF serializers (illustrative)
```python
class TicketCreateSerializer(serializers.Serializer):
    game_id = serializers.UUIDField()
    draw_id = serializers.UUIDField()
    selection = serializers.IntegerField(min_value=1, max_value=99)
    stake = serializers.DecimalField(max_digits=12, decimal_places=2)
```

### Appendix B — RTK Query example slice
```ts
export const api = createApi({
  baseQuery: fetchBaseQuery({ baseUrl: "/api/v1", prepareHeaders(h) { /* add JWT */ return h } }),
  endpoints: (b) => ({
    getNextDraw: b.query<Draw, {gameId: string}>({ query: ({gameId}) => `draws/next?game_id=${gameId}` }),
    createTicket: b.mutation<Ticket, TicketInput>({ query: (body) => ({ url: `tickets`, method: 'POST', body }) }),
    getWallet: b.query<Wallet, void>({ query: () => `wallet` }),
  })
})
```

### Appendix C — Draw scheduler cadence (Celery beat)
- `schedule_draws`: every hour – create 12×5min draws ahead.
- `lock_draw`: run per draw at `locked_at`.
- `execute_draw`: run at `scheduled_at` + small delay.
- `payout_winners`: immediately after execute; retry on failure.

