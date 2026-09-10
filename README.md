# Acro FPV — browser drone racing simulator

A single-file FPV quadcopter simulator. Open `index.html` in any modern browser —
no build step, no server, no install. Three.js is pulled from a CDN at runtime.

```
open index.html          # macOS
xdg-open index.html      # Linux
```

## Controls

Keyboard and gamepad work interchangeably at all times. A gamepad is used
automatically when one is connected and you move a stick or press a button;
touching the keyboard hands control straight back. The panel in the top-right
always shows which device is currently flying the quad.

### Keyboard
| Key | Action |
| --- | --- |
| `W` / `S` or `↑` / `↓` | Pitch forward / back |
| `A` / `D` or `←` / `→` | Roll left / right |
| `Q` / `E` | Yaw left / right |
| `Shift` / `Ctrl` | Throttle up / down (ramped, holds where you leave it) |
| `Space` | Arm / disarm |
| `R` | Reset drone to the pad |

### Gamepad (Mode 2, standard mapping — PS4/PS5/Xbox all work)
| Control | Action |
| --- | --- |
| Left stick | Throttle (Y) / yaw (X) |
| Right stick | Pitch (Y) / roll (X) |
| ✕ / A | Arm / disarm |
| ○ / B | Reset drone |
| △ / Y | Toggle FPV / chase camera |
| Options / Start | Restart lap timing |

### General
| Key | Action |
| --- | --- |
| `C` | FPV / chase camera |
| `T` | Throttle mode: absolute (stick position) or ramped (stick deflection) |
| `[` / `]` | Camera uptilt |
| `H` | Hide the controls panel |

Arming is blocked above 12% throttle, the same safety check a real flight
controller does.

## Flight model

Rate mode (acro) — the sticks command **angular rates**, not angles, and the
quad holds whatever attitude you leave it in. There is no self-levelling.

- **Rates:** 700°/s roll, 620°/s pitch, 380°/s yaw at full stick, with expo on
  every axis for fine centre resolution.
- **Rotational momentum:** commanded rates are reached through a first-order lag
  (~40–75 ms per axis, yaw heaviest), so the airframe carries rotation rather
  than snapping between rates.
- **Thrust:** a single body-up force, ~2.6 g at full throttle, run through a
  60 ms motor spool so throttle punches are not instant. Hover sits near 38%.
- **Translation:** gravity plus linear and quadratic drag, which gives the quad
  a terminal velocity and makes it drift on momentum out of turns.
- **Collisions:** ground, pylons and gate rings all push back; an impact above
  9 m/s disarms you.
- Physics runs on a fixed 240 Hz step decoupled from the render loop, so the
  feel does not change with frame rate.

Tuning constants live in the `CFG` object near the top of the script.

## Course and HUD

Six gates form a loop around the launch pad; the next gate glows orange and the
HUD shows its range, with an off-screen arrow when it is behind you. Passing
gate 1 starts the clock, and lap and best-lap times appear in the top-right.
Pylons and distant blocks give parallax cues for judging speed and altitude.

The HUD carries a throttle bar (with a tick for actual spooled motor output),
altitude and speed, and an attitude indicator: a full-screen pitch ladder and
horizon locked to the camera in FPV, and a bezelled attitude ball in chase view.
Both cameras are rigidly tied to the airframe — there is no free orbit camera.
