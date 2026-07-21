# Strategy Review: Where to Gate the Free Tier of the Ear Training Lab
*2026-07-21*

## The Brief

Where should we draw the free/paid line in the Ear Training Lab so it converts free users into Audio University members, without losing its value as a top-of-funnel lead magnet?

Verified current state:
- Members get the full app (`lab.html`); non-members get a free build (`lab.html?free=1`) embedded on public pages.
- Free users get, unlimited and forever: the EQ module's Custom Practice (build-your-own rounds) and Learn (free-dial explore). No cap, no meter.
- Already members-only: the entire Compression module (hard wall), and the guided EQ Levels curriculum (the 15-week Foundations course, plus Advanced, plus drafted Mastery). Free users hit a "Guided training is for members only" wall at Levels.
- Lead capture today: a soft, dismissible newsletter modal fires once per browser after 6 answered questions and posts to Kit. It is not a hard gate. Users can dismiss and keep training free forever.
- Membership is the paid Mixing program; the Lab and curriculum are a benefit of it.

Kyle's hypothesis: unlimited free Custom Practice may leave money on the table. The real paid value is the curriculum behind the tool, not the tool itself. He wants the Lab to stay at least a strong lead magnet while converting more actively.

Options on the table: (A) keep as-is, (B) meter free Practice, (C) require email to use Practice at all, (D) give a free taste of the curriculum then wall the rest, (E) a staged combination.

---

## Council Deliberation

### Audience Advocate
*Conditional*

The person who needs ear training is usually earlier in the journey than the seasoned pro. A working engineer already has trained ears. So the free Lab's real user is the developing mixer, which is exactly who the Mixing program is built for. That user does not want to be counted and cut off mid-rep, but they very much want an answer to "am I doing this right, and am I getting better?" Unstructured Custom Practice cannot answer that. Hiding the curriculum entirely serves no one: the user cannot tell if they are improving, and Kyle never gets to show his best work.

**Red flag / green light:** Green light on letting them taste the structured path; red flag on metering reps, which punishes the exact habit you want to build.

---

### The Craftsman
*Conditional, leaning to D*

Custom Practice without a path is a metronome with no sheet music. It is a real tool, but it does not teach. The teaching is the sequence. Showing Foundations Week 1 for free is the honest move: it demonstrates that Audio University's value is the pedagogy, not a random-round generator. The condition is that Week 1 has to deliver one genuine "I can hear that now" moment on its own, or the taste undercuts the promise instead of proving it.

**Red flag / green light:** Green light on showcasing the teaching, not the tool; the taste must be excellent enough to stand alone.

---

### Revenue Architect
*Support, with the email gate plus a curriculum taste*

The curriculum is the paid lever, and right now it is invisible to free users, so the funnel sells the tool and hides the product. Two moves have clear return: capture the email properly, since a dismissible modal leaks most of the leads it should catch, and put a curriculum taste in front of free users so the upgrade CTA points at something concrete they already felt. Metering Custom Practice is a weaker lever that trades goodwill for marginal conversion. The email is the asset that lets you convert on your own schedule through Kit, not only in the moment inside the app.

**Red flag / green light:** Green light on email capture and a visible curriculum; the current soft modal is leaving the actual lead-magnet job half done.

---

### The Operator
*Support D plus the email gate; caution on metering*

Cost check. A curriculum taste is nearly free to ship: Week 1 already exists, and it is close to a one-line gate change to let free users into it and wall Week 2. The email gate is also cheap: the modal and the Kit integration already exist, so it is a state change from dismissible to required-to-continue. Metering is the expensive path. It needs per-user counting, daily-reset logic, an analytics loop to tune the number, and ongoing support when users ask why it stopped working. Ship the two cheap, high-value moves now, and do not build metering machinery until data justifies it.

**Red flag / green light:** Green light on the two low-cost moves; red flag on committing to a meter you then have to tune and support.

---

### The Skeptic
*Challenge the metering assumption*

The claim is that unlimited free Practice leaves money on the table. What is the evidence? We do not know how many free users are heavy Practice users who would convert if blocked, versus tire-kickers who bounce at any gate. There is little instrumentation today, so a meter would be guessing at a number, and every wrong guess costs reach or goodwill. The deeper buried assumption is that people fail to convert because Practice is "good enough." The likelier reason is that they never see the curriculum, so they cannot want what they have never seen. Fix visibility before adding friction.

**Red flag / green light:** Red flag on metering blind; the probable failure mode is throttling your most engaged users, who are your best prospects, and losing them with a bad taste instead of an email.

---

### The Long Game
*Support the staged funnel; protect reach*

In five years the assets that compound are the email list and brand trust, not this quarter's conversion rate. The Lab's strategic job is to turn YouTube attention into owned audience and warm those leads toward membership over time. That argues for a gate that reliably captures the email and a taste that builds trust, and against an aggressive meter that trades long-term goodwill for short-term upgrade nudges. The email capture is the asymmetric bet here: cheap now, compounding for years.

**Red flag / green light:** Green light on capturing trusting leads as the compounding asset; set the gate to maximize captured goodwill, not this week's upgrades.

---

## Decision Forks

> **Fork 1 (Reach vs Capture):** A required email gate raises lead capture but lowers how many people ever touch the tool, since some bounce at the form. If YouTube traffic is abundant and conversion is the binding constraint, capture wins and you can gate earlier. If the Lab is still building traffic, reach wins and the gate should sit later. Kyle knows which constraint is actually binding.

> **Fork 2 (Taste converts vs cannibalizes):** Free Week 1 of Foundations either proves the structured path and pulls users toward membership, or gives away enough of an "aha" that some feel finished. Which one happens depends on whether Week 1 is a genuine standalone result or a clear on-ramp that implies the rest.

> **Fork 3 (Meter the habit or not):** Metering Custom Practice could nudge fence-sitters to upgrade, or could kill the daily streak that is the strongest predictor of conversion. These conflict directly, and the resolution depends on data Kyle does not have yet.

---

## Synthesis

### Signal
Five of six advisors converge on the same two moves. First, make the curriculum visible by giving free users a real taste, Week 1 of Foundations in full, because hiding the hero product is the actual funnel leak. Second, capture the email properly by turning the soft, dismissible modal into a value-anchored gate placed after that taste. Both are cheap to build, both are almost certainly right, and neither depends on data you do not have.

### Tension
Whether and how hard to meter Custom Practice. Revenue sees upside; Audience, Skeptic, and Long Game see a habit product where friction on your most engaged users is self-defeating. Also unresolved is exactly where the email gate sits: at the door captures more emails but costs reach, while after a taste protects reach but captures fewer. That placement is Kyle's call based on whether traffic or conversion is the tighter constraint.

### Watchlist
- Instrument free-user behavior before metering anything: rounds per session, return visits, where users hit walls, and form completion rate.
- Watch whether the free Week 1 raises or lowers upgrade-CTA clicks once it ships.
- Watch the Kit opt-in rate before and after the modal becomes required-to-continue.
- Make sure the staging-pathname curriculum split does not accidentally expose more of the curriculum than the intended free taste.

### Recommendation
Proceed with a staged funnel, option E built around D, not a hard meter.

1. Give free users Foundations Week 1 in full, so they experience the structured path that is the real paid value.
2. At the Week 1 to Week 2 boundary, require a free email opt-in to continue and to save streak and progress. This is where the soft modal becomes a real but friendly gate. Frame it as creating a free account, not hitting a paywall.
3. Keep Learn and Custom Practice available as the habit tool, framed as drilling what the lessons teach, and pointing back to membership. Do not meter them yet.
4. Instrument free-user behavior now. Only add a Practice meter later, and only if the data shows a real population of heavy free users who do not convert.
5. Leave the Compression hard wall as is. It is correctly gated.

Do not put a hard email wall at answer zero, which kills reach, and do not aggressively meter Practice before you have data, which kills the streak that drives conversion. The order matters: visibility and email capture first, metering only if the numbers later demand it.
