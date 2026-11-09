# Review: oldschool README (persona: Emil Kowalski)

**Verdict:** Cohesive paper-and-printer motion with a strong ease-out curve and a correct reduced-motion fallback. It is too slow and too busy at load (hero 3.1s, project cards 900ms), the hero animates two things at once, and the event log creeps instead of arriving.
**Decision:** Approve after the Animations table below is applied. No block-level violation (no `scale(0)`, no `ease-in`, no `transition: all`, no layout properties).

## Content
1. **The hero quote arrives last.** `hero()` starts the 4 quote lines at 1700 ms and the photo dev ends at 3100 ms. The thesis ("If it can be deterministic...") is the payload, so it should not wait behind the receipt. Principle: motion order follows importance, and stagger stays 30-80 ms. Change: quote lines `D(900 + i*60)`.
2. **Link tickets animate copy that is a nav control.** `ticket()` wipes stub, label and value at 100/220/320 ms (940 ms total) for a link seen at most once. Principle: purpose test. Change: one `.f` fade on the whole ticket group, 240 ms, no delay (see Animations).

## Animations
| Before | After | Why |
| --- | --- | --- |
| Hero: receipt slide `1500ms` plus every line `.w` wipe `620ms`, `st=85` (hero `print` + `.w`) | Slide `1100ms`, delay 150 ms. Lines `.w` override in hero: `360ms`, `st=55`, first at `t=350` (last line ends ~1315 ms). | Text wiping while its paper is moving is two motions on one object. Shorter, tighter, still custom ease-out. |
| Stamps use `.f` (`translateY(8px)` + fade, 560 ms) in `stamp()` | New `.st` class: `from{opacity:0;transform:scale(1.15)} to{opacity:1;transform:none}`, `180ms`, same `EASE_OUT`; set `transform-box:fill-box;transform-origin:center`. Hero stamp delay 1350 ms; LVC stamp unchanged at 1600 ms. | A stamp is struck, not floated. Scale-down onto the paper is physical (starts at 1.15, never 0), and 180 ms matches the feedback range. |
| `.w` 620 ms, `.f` 560 ms, `.up` 900 ms | `.w` 360 ms, `.f` 380 ms, `.up` 520 ms with `translateY(32px)` | UI-adjacent motion should land under ~400 ms. A 900 ms rise on a link card delays the moment the viewer is looking at it. |
| Stagger 85 / 90 / 120 / 140 ms (hero `st`, `project()` `i*90`, `record()` `i*120`, desk slip `i*140`, lvc `i*90`) | 60 / 60 / 70 / 70 / 60 ms | Stagger window is 30-80 ms; beyond it the layout feels slow. |
| Link `ticket()`: three `.w` wipes | One `.f` on the content group, `240ms`, `D(0)` | Frequency and purpose: navigation chrome gets the least motion. |
| Event store: `translateY` 0 to -88px, `9s linear infinite` | Step per row: keyframes `0%,20%{ty:0} 25%,45%{ty:-22px} 50%,70%{ty:-44px} 75%,95%{ty:-66px} 100%{ty:-88px}`, each step with `animation-timing-function:cubic-bezier(0.77,0,0.175,1)`, `9s` total | Constant 10 px/s drift makes text unreadable and is perpetual peripheral motion. Linear is for marquees; an "event arrives" needs ease-in-out on a hold-and-move cadence (each move ~450 ms). |
| Desk terminal types, holds, clears, retypes forever (`cyc=11s`, opacity 0 at 95%) | Type once, hold the final frame (`animation-iteration-count:1;animation-fill-mode:forwards`, remove the 95-100% clear) | Re-typing the same 7 lines forever has no purpose after the first read. Cursor blink keeps the card alive. |
| Hero cursor `.cur` blinks from t=0 while `@Raphonzius` is not yet printed | `.cur{animation-delay:1.2s;opacity:0}` with `fill-mode:backwards`, or put cursor in the same `.w` group as the text | An orphan cursor before its line exists is the kind of unseen detail that breaks the illusion. |
| Photo dev overlay `2.4s` and unaffected by reduced motion | `1.6s`, delay 500 ms; under `prefers-reduced-motion` set it to `300ms` | Rare delight can be slower, but 2.4 s outlasts the rest of the scene. |
| Reduced motion: `300ms linear` fade, delays kept | `300ms cubic-bezier(0.23,1,0.32,1)`; cap delays: `animation-delay:calc(var(--d,0ms)*0.4)` or hero stagger max 40 ms | Gentler, not zero, is right; linear is the wrong easing for an entrance and long delays defeat "reduced". |
| `sheet()` (feTurbulence grain + Gaussian blur shadow) is inside animated `.f`/`.up` groups (project cards, receipt, tickets) | Move grain to a static layer under the animated content, or replace `feTurbulence` with a 96px data-URI PNG `<pattern>` at ~0.08 opacity; shadow as two offset rects (opacity .25 and .15) instead of `stdDeviation=7` | Animating a group that holds filters re-rasterizes them each frame, risking dropped frames and Camo lag. Transform/opacity only, and keep filters off the moving layer. |

## GitHub integration
1. **Entrances on below-the-fold cards run while no one is looking.** `lvc`, `desk`, `record`, tickets all start at image load. I could not verify whether browsers pause offscreen SVG-in-`img` animations, so assume they finish early. Change: keep below-fold entrance total under 900 ms, let the loops (event log, cursor) carry the "alive" feeling, and make sure end states are the static state (they are: `fill-mode: both`).
2. **Text collapses on mobile.** Cards are 860 px wide; at about 360 px they scale to ~0.42, so 12.5-13 px becomes ~5.4 px (`record()` body 13 px, `project()` 12.5 px). Change: `record()` into a 2x2 (two `<a><img width="49%">` of 420x? tickets, body 15 px, wrap 24), `project()` body 14 px, labels never under 12 px in source units.
3. **Weight.** Each SVG embeds the 4 fonts (~90 KB base) so 12 requests are ~1.1 MB total. Acceptable. Keep, but do not add more filters or images (the avatar is embedded in `hero.svg`, which is already the largest at 111 KB).

## Do not change
- `lib.EASE_OUT = cubic-bezier(0.23, 1, 0.32, 1)` and its use everywhere (no ease-in).
- Animating only `transform`, `opacity`, `clip-path`; wipes via `clip-path: inset`.
- Entrance start states `translateY(8px)` plus opacity, no `scale(0)`.
- `fill-mode: both` so the static frame equals the final frame.
- Reduced-motion block existence, and `.cur`/`.loop` stopping.
- "One live signal per card at most" rule; "illustrative" label on the event log.
- Drawer slide-up for project cards (purposeful: card comes out of its drawer), clipped at the lip.
- Light/dark independence via the opaque `DESK` backdrop.
