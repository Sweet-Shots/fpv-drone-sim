# Acro FPV

A rate-mode FPV quadcopter simulator in one HTML file. Open `index.html` in any
modern browser — no build step, no server, no install. Three.js loads from a CDN
at runtime.

```
open index.html          # macOS
xdg-open index.html      # Linux
```

## Flying it

The sim is **acro (rate) mode**: the sticks command angular *rates*, not angles,
and the quad holds whatever attitude you leave it in. Nothing self-levels.

Keyboard, gamepad and touch are fully interchangeable and none is required. A gamepad
takes over the moment you move a stick or press a button; touching the keyboard
hands control straight back. Only the active device's bindings are ever shown on
screen.

### Keyboard
| Key | Action |
| --- | --- |
| `W` `S` or `↑` `↓` | Pitch |
| `A` `D` or `←` `→` | Roll |
| `Q` `E` | Yaw |
| `Shift` `Ctrl` | Throttle up / down |
| `Space` | Arm / disarm |
| `R` | Reset drone |
| `C` / `V` | Camera / prop-in-view |
| `Backspace` ×2 | Restart run |
| `Esc` | Pause |

### Gamepad (Mode 2, standard mapping — PS4/PS5/Xbox)

Flying a quad takes exactly four axes — two gimbals. Everything else on a real
transmitter is an **AUX switch**, and that is what the shoulder buttons are here.

| Control | Action |
| --- | --- |
| Left stick | Throttle / yaw |
| Right stick | Pitch / roll |
| ✕ / A | Arm / disarm |
| ○ / B | Reset drone |
| □ / X | Prop-in-view |
| △ / Y | Camera |
| **L1** | AUX: flight mode |
| **R1** | AUX: rate profile |
| **L2** | AUX: lost-model beeper (Acro/Angle) |
| **R2** | AUX: turtle mode — flip an upside-down quad back over (Acro/Angle) |
| **L2 / R2** | Gimbal tilt wheel (Camera mode) |
| **Share / View ×2** | Restart run |
| **Options / Start** | Pause |

Pushing the right stick **away from you pitches the nose down and flies you
forward**, as on a real Mode 2 transmitter. If you prefer it the other way, the
Pitch stick row in the menu inverts it.

Arming is blocked above 12% throttle, the same check a real flight controller
does, and every run starts at idle.

## Airframes

Four aircraft, each a complete set of the constants the model already runs on,
so the difference between them is physics rather than a multiplier. Swappable
from the Play page or mid-flight from the pause screen; the loop gains, mixer
geometry and pack are all rebuilt with the airframe.

| | Mass | Thrust/weight | Hover | Pack | Feels like |
| --- | --- | --- | --- | --- | --- |
| 5″ Freestyle | 650 g | 6.5:1 | 25% | 4S 1300 | The default; everything else is measured against it |
| Tinywhoop | 35 g | 3.5:1 | 39% | 2S 450 | Ducted, near-zero inertia, stops instantly, slow |
| Cinewhoop | 550 g | 4.4:1 | 33% | 4S 1100 | Heavy and draggy on purpose; refuses to be twitchy |
| 7″ Long range | 1.15 kg | 4.9:1 | 31% | 6S 3000 | Carries momentum into every corner, flies for ten minutes |

Records and ghosts are kept per airframe, because a whoop lap and a 7″ lap are
not the same race.

## Ghost replay

Time Trial and Line of Sight record each lap — position and attitude at 30 Hz,
with the gate splits alongside — and play the best one back beside you as a
translucent aircraft. The split delta shown after each gate is a real
comparison at a real point on the track, not a guess from elapsed time. Ghosts
are stored per course, airframe and flight mode, capped at six, and are the
first thing dropped if browser storage fills, so they can never cost you your
settings or records.

## Flight modes

Betaflight flies one mode at a time, picked from an AUX switch. All three are here:

| Mode | What it does |
| --- | --- |
| **Acro** | Rate mode. Sticks command rotation, nothing levels you, and the quad holds whatever attitude you leave it in. |
| **Angle** | Self-levelling. Stick deflection is a target lean angle; centre the sticks and it rolls back to level. |
| **Camera** | Angle mode plus altitude hold and braking, like a DJI-style camera drone. Up/down, left/right, yaw to turn — let go and it parks in the air. |

In Angle and Camera the throttle gimbal is a **climb-rate** command about its
spring centre, which is how a camera drone's stick actually works, and the
Recovery Drill disappears from the session list — a quad that levels itself has
nothing to recover from.

### The camera follows the aircraft, not the other way round

An FPV quad's camera is **bolted to the frame** at a fixed uptilt you set with a
screwdriver on the bench. So in Acro and Angle the view rolls with the airframe —
that is the whole FPV look — and the angle can only be changed landed and
disarmed. The front arms and prop tips clip the corners of the frame.

A camera drone hangs its camera on a **3-axis gimbal**, so the horizon stays
level however hard the aircraft banks and only yaw follows the airframe. In
Camera mode the shoulder buttons drive the gimbal wheel in flight (−90° to +20°),
the HUD horizon stops rolling because the lens no longer does, and the props are
never in shot — the gimbal hangs below them.

### Touch

On-screen sticks appear the moment you touch the screen. The right pad is a
self-centring gimbal. The left pad is not: its vertical axis is an absolute
throttle that stays where you lift your thumb off, because a spring-centred
throttle is the one thing no transmitter has — in Camera mode it does spring
back, since there the stick is a climb command about its centre. The OSD moves
out of the pads' way when they are up.

Honestly: acro on a touchscreen is hard. Camera mode is the one that actually
plays well with thumbs.

## Rate profiles

Real freestyle quads run 600–900°/s, which is two rolls a second. That is not a
bug in the feel — it is what acro rates are — but nobody learns on them, and a
keyboard's on/off keys make it worse than a real gimbal. Three profiles are
selectable in the menu and in the pause screen:

| Profile | Roll rate | For |
| --- | --- | --- |
| Cruise | 260°/s | What a trainer quad ships with |
| Sport | 420°/s | Quick but recoverable — start here |
| Acro | 700°/s | Real freestyle rates, unforgiving |

Each profile carries its own expo and stick smoothing.

## Sessions

| Session | What it is |
| --- | --- |
| Free Flight | No clock, no gates |
| Time Trial | Three laps against the clock, gate splits live |
| Gate Rush | 45 seconds; every gate taken adds four more |
| Recovery Drill | Dropped inverted, tumbling and sinking. Air mode will stop the spin, but nothing levels you: read the attitude, roll upright, then power out. Each round starts lower and spins harder |
| Line of Sight | The camera stays on the ground where you are standing, as at a real field |

## Graphics

Low / Medium / High, switchable from the menu or mid-flight from the pause
screen. Each step is a real cost lever, not a label: render resolution, whether
the sun casts shadows at all, how much scenery gets built, how many point lights
each material has to loop over, prop blur, and draw distance. Low turns shadows
off entirely and thins the treeline to a third.

## Locations

**Sunset Field** — open grass, low sun, wind off the treeline.
**Night Circuit** — lit gates and little else; you fly the LEDs, not the ground.
**The Hangar** — indoor, no wind, concrete, tight lines between pillars.

Best lap, most gates and most rounds are kept per location per session in
`localStorage`.

## Flight model

The aircraft is a 650 g 5-inch freestyle quad on a 4S 1300 mAh pack, flown in
Betaflight acro mode. The model is built from that airframe rather than from
feel-good constants, so the numbers below are consequences, not settings.

- **Rates** use Betaflight's own `applyBetaflightRates` — RC Rate, Super Rate and
  RC Expo — so the three profiles are expressed the way you would actually set
  them in the configurator. Real quads have switchable rate profiles; so does this.
- **The rate loop is a PID controller**, not a curve. P and D act on gyro error
  and gyro derivative, I is clamped and reset below `min_check`, output is capped
  at Betaflight's `pidsum_limit`, and the result goes through the real QUADX
  mixer with mix scaling and an idle clip. Roll reaches a commanded 420°/s in
  67 ms with ~5% overshoot.
- **Authority is emergent.** Torque comes from four individual motor thrusts, so
  how much you have depends on where the mixer can put them — which is why the
  **Idle authority** setting matters. It exposes three real Betaflight
  configurations: `Air mode` (default, what a modern freestyle quad flies — full
  authority at zero throttle), `Idle floor` (plain defaults; only the upward half
  of each correction survives at the bottom of the stick), and `Motor stop`
  (props actually stop below `min_check`, so there is no authority at all).
- **Yaw is weak because of physics, not tuning.** Roll torque is differential
  thrust on a 78 mm arm; yaw is only prop drag torque. Measured ratio 15:1.
- **Thrust** follows RPM², with stick mapped onto `[motor_idle, 1]` and a per-motor
  spool. Hover sits at **25%** stick; thrust-to-weight is 6.5:1 on the bench and
  4.9:1 in flight once the pack sags.
- **Props unload with airspeed.** Thrust falls as axial inflow approaches the
  prop's geometric pitch speed, which is what really caps top speed and climb
  rate — not drag.
- **Drag is anisotropic**, in the body frame: a quad is a bluff body belly-on
  (four prop discs) and far cleaner nose-on. A flat belly-down fall terminates at
  13 m/s; a nose-down dive reaches 27 m/s. Level top speed is 32 m/s (115 km/h).
- **The battery is electrical.** Current is drawn against a 7-point Li-Po
  discharge curve through 16 mΩ of pack resistance; sag costs RPM and therefore
  thrust, so a fresh pack punches harder. 6 minutes hovering, 32 seconds flat out.
- **Wind is a velocity field**, not a shove: it acts through drag on airspeed,
  with a 1/7-power boundary layer so it strengthens with altitude.
- Also modelled: gyroscopic cross-coupling (Euler's equations), vortex-ring state
  — which is what propwash actually is — aerodynamic rotational damping, ground
  effect (honestly negligible at 1.1% for a 5" prop), a ±2000°/s gyro clip, and
  Coulomb ground friction.
- Physics runs on a fixed 240 Hz step decoupled from the render loop.

Constants live in `QUAD` (airframe), `FC` (flight controller), `CFG` and
`RATE_PROFILES` at the top of the script, each commented with its units and where
the figure comes from.

Two test suites back this up: `test2.js` covers behaviour and UI, and
`physics-check.js` measures hover throttle, thrust-to-weight, per-axis step
response, dive and flat-fall terminal velocities, top speed, endurance, sag, and
the three idle modes, asserting each lands in a realistic range.

## Main menu

A semicircular dial on the left, and a live showcase flight on the right — the
same renderer and the same airframe, flown along a baked spline through a lit
ring course, with three cinematic camera shots on rotation. It is a scripted
line rather than an autopilot: repeatable, and honest about being a demo.

Four entries, each opening its own page on the same dial:

| | |
| --- | --- |
| **Play** | Mode, Place and Drone, then Launch |
| **Options** | Sound, volume, quality, rates, idle authority, prop view, throttle and pitch stick |
| **Help** | Every control, keyboard and gamepad side by side |
| **Credits** | Made by Douglas Harvey for Drone Club — Made with love |

`Esc` (or ○) steps back a page. The arc is sized from the viewport rather than
from its neighbours, so it stays exactly the same circle on every page and at
every selection — measured in the test suite, because it was not always true.

## HUD

Betaflight-style OSD drawn straight on the video: no panels. Throttle bar with a
tick for actual spooled motor output, pack voltage, speed, altitude, next-gate
range with corner brackets and an off-screen director arrow. In FPV the pitch
ladder is projected by tangent rather than linearly, so the HUD horizon sits
exactly on the rendered one at wide FOV; in chase and line-of-sight views it
becomes a bezelled attitude ball instead.

Audio is synthesised at runtime with WebAudio — four detuned motors whose pitch
follows RPM, airflow noise driven by airspeed, plus gate, crash and arming tones.
No audio assets.

## Publishing

`index.html` is the whole app. The hosted Claude Artifact variant is generated
from it, since that host supplies its own document wrapper:

```
python3 build-artifact.py
```
