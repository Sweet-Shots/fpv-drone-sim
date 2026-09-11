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

Keyboard and gamepad are fully interchangeable and neither is required. A gamepad
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
| Control | Action |
| --- | --- |
| Left stick | Throttle / yaw |
| Right stick | Pitch / roll |
| ✕ / A | Arm / disarm |
| ○ / B | Reset drone |
| □ / X | Prop-in-view |
| △ / Y | Camera |
| **Share / View ×2** | Restart run |
| **Options / Start** | Pause |

Arming is blocked above 12% throttle, the same check a real flight controller
does, and every run starts at idle.

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
