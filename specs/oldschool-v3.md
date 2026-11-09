# Spec: old-school profile v3 (review follow-ups)

Source: `reviews/apple.md`, `reviews/emil.md`, `reviews/taste.md`, `reviews/impeccable.md`, plus what v2 left unverified.

## 1. Problem

v2 fixed font sizes and motion timing, but every card is still 860 wide. On a phone GitHub scales it to ~0.4, so 14px text renders at ~5.6px. Half-width cards (`width="49%"`) are worse (~0.2). All four reviewers ranked mobile legibility first. v2 also left light theme, reduced motion and phone width unchecked.

## 2. Requirements

| ID | Requirement | Source |
|---|---|---|
| R1 | Every read text is >= 11px as rendered on a 375px phone. | all 4 |
| R2 | Desktop keeps a compact 2-column layout and the page does not get longer. | user: lean |
| R3 | Every link that exists today still works, and each linked card shows a visible cue (→). | user, Apple |
| R4 | Nothing goes against the user's explicit asks: Daily Tools kept, dynamic motion kept, LVC emphasized, English only, no contribution board. | user |
| R5 | No invented content and no meaningless ornaments (e.g. "No. 01" numbering). | Taste |
| R6 | Cards read well on GitHub dark and light themes. | Impeccable, Taste |
| R7 | Reduced motion shows a complete, static final frame. | Apple, Emil, Impeccable |
| R8 | Total asset size stays <= v2 (520 KB). | Apple, Emil |

## 3. Design

**Responsive pairs (R1, R2).** Every card is redrawn at viewBox width 420 and placed in the README with a fixed `width="410"`, two per `<p align="center">`. GitHub sets `img{max-width:100%}`:
- desktop (column ~830px+): two cards side by side at about 1:1 scale;
- phone: each card wraps to its own line at full width, scale ~0.82, so 14px becomes ~11.5px.

No media queries are needed, and none would survive GitHub's sanitizer anyway. Pairs share one height so rows align.

| Row | Left card (link) | Right card (link) |
|---|---|---|
| Hero | Receipt out of the printer (LinkedIn) | Polaroid and tagline, set larger (LinkedIn) |
| LVC, as an open folder | Cover: title, abstract, stamp, "READ THE PAPER →" (paper site) | Contents: six modules, validation, event store, "SOURCE CODE →" (org) |
| Projects x2 | poc-grpc, Demo-SpringSecurity6-JWT | spring-and-vue, cachyos-setup |
| Desk | Computer with the terminal loop (repos) | Daily Tools slip, "ALL REPOSITORIES →" (repos) |
| Record | 2 days, USD 37k (LinkedIn) | 670k+, 45%, "CV ON LINKEDIN →" (LinkedIn) |
| Contact | Email ticket | LinkedIn ticket |

- **CODE/PAPER tickets removed.** The two LVC cards now carry both links with visible cues (Taste: duplicates; R3 still holds).
- **"No. 01–04" removed** from the project cards (R5). The red → stays (Apple).
- **Light theme (R6).** Card corners go from rx 6 to rx 10. Each card keeps its own dark desk, so both themes render the same.
- **Motion.** v2 timings stay. The hero tagline gets its own card, so it enters at 300ms instead of waiting for the receipt (Taste, Emil).

**Kept on purpose, in conflict with Taste (R4):** Daily Tools, the terminal loop, rows 01–05, the stamps, and the illustrative event log. A plain-text fallback line is also not added: the user asked for no loose markdown.

## 4. Verification

1. Every SVG parses as XML. Total size <= 520 KB.
2. Desktop preview at 930px: pairs sit side by side, heights match, nothing is clipped.
3. Phone preview at 400px: cards stack, and the smallest read text is >= 11px.
4. Light preview (white page): the cards look intentional.
5. Reduced-motion preview (`--force-prefers-reduced-motion`): every card shows its full final frame.
6. On GitHub: the blob page resolves every `/assets/...` image.

## 5. Tasks

- [x] T1 `lib.preview`: add `width`, `column`, `bg` and `reduced_motion` options.
- [x] T2 Theme: 420-wide cards (hero x2, lvc x2, desk x2, record x2), projects without the numbering, rx 10, CODE/PAPER tickets dropped. Only the font faces each card uses are embedded.
- [x] T3 README: six rows of pairs with `width="410"`, alt text matching each card.
- [x] T4 Run verification 1–6, fix what fails, commit, push.

## 6. Results

| Check | Result |
|---|---|
| 1 XML + size | 14 SVGs parse. 379 KB total (v2: 520 KB). |
| 2 Desktop 930px | Pairs sit side by side with matching heights. Two overlaps fixed: the LVC contents cue and the Daily Tools cue. |
| 3 Phone 375px column | Cards stack at full width (scale ~0.82); 14px text renders at ~11.5px. |
| 4 Light page | Each card keeps its own desk, so the render matches dark mode. |
| 5 Reduced motion | Every card shows its complete final frame. |
| 6 GitHub | See the commit message: the blob page resolves `/assets/oldschool/*`. |

Previews: `previews/oldschool.png` (desktop), `previews/oldschool-phone.png`, `previews/oldschool-light.png`.

## 7. Reverted: responsive pairs

The user rejected the left/right split ("pretty ugly"), so the layout is back to v2's full-width cards. Projects and tickets stay as half-width pairs, as in v2.

What stays from v3:
- per-card font faces (338 KB total);
- project cards without "No. 01–04";
- rx 10 corners;
- the `lib.preview` options.

Trade-off accepted: on a phone, full-width cards scale to ~0.4 again (R1 is not met).
