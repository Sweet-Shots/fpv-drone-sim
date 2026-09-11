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
| Recovery Drill | Dropped inverted and tumbling — stop the spin, get upright, hold it before the ground arrives. Each round starts lower and spins harder |
| Line of Sight | The camera stays on the ground where you are standing, as at a real field |

## Locations

**Sunset Field** — open grass, low sun, wind off the treeline.
**Night Circuit** — lit gates and little else; you fly the LEDs, not the ground.
**The Hangar** — indoor, no wind, concrete, tight lines between pillars.

Best lap, most gates and most rounds are kept per location per session in
`localStorage`.

## Flight model

- **Rates** are commanded, never angles. Commanded rates are reached through a
  first-order lag (40–100 ms per axis, yaw heaviest), so the airframe carries
  rotational momentum instead of snapping.
- **Control authority follows the motors.** Torque comes from differential
  thrust, so near zero throttle you have almost none — which is why a tumbling
  quad has to be spooled up before it can be caught. This is the whole point of
  the recovery drill.
- **Thrust** is a single body-up force, ~2.6 g at full throttle, behind a 60 ms
  motor spool. Hover sits near 38%.
- **Battery** is a 4S pack that sags under draw and loses thrust as it drains;
  flat ends the flight.
- **Wind** is a per-location constant plus a gust cycle, stronger with altitude.
  The hangar has none.
- **Translation** adds gravity plus linear and quadratic drag, giving a terminal
  velocity and carrying you wide out of turns.
- **Collisions** with ground, pylons, walls, ceiling and gate rings all push
  back; an impact above 9 m/s disarms you.
- Physics runs on a fixed 240 Hz step decoupled from the render loop, so feel
  does not change with frame rate.

Tuning lives in `CFG` and `RATE_PROFILES` at the top of the script.

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
