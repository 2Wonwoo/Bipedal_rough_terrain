"""Gravel/rough-terrain generator for the terrain-mix experiment.

Scaled down from Isaac Lab's stock ``ROUGH_TERRAINS_CFG``
(``isaaclab.terrains.config.rough``), which targets ANYmal-class quadrupeds
(~0.7 m standing height, ~30 kg, ~10 cm feet). Open Duck Mini V2 stands
~140-190 mm tall, weighs 2.7 kg, and has 60 mm feet — roughly a 4-5x smaller
robot — so every length below (bump height, obstacle size, patch size) is
divided by about that much. Full-scale ANYmal bump heights (2-10 cm) would be
taller than this robot's whole leg swing; scaled to gravel-pebble size
(4-20 mm) they're still a real footing challenge given the 5 mm leg/torso
self-collision margin this project treats as a hard constraint (see
docs/decisions.md and JoystickEnvCfg's safety_margin_mm).

``curriculum=False`` is deliberate: this is a static 50/50 population mix
(half the parallel envs spawn on flat ground, half on gravel/rocks, for
every iteration), not a progressive difficulty ramp.
"""

import isaaclab.terrains as terrain_gen
from isaaclab.terrains import TerrainGeneratorCfg

GRAVEL_ROUGH_TERRAINS_CFG = TerrainGeneratorCfg(
    size=(3.0, 3.0),
    border_width=1.0,
    num_rows=10,
    num_cols=20,
    horizontal_scale=0.02,
    vertical_scale=0.002,
    slope_threshold=0.75,
    use_cache=False,
    curriculum=False,
    sub_terrains={
        "flat": terrain_gen.MeshPlaneTerrainCfg(proportion=0.5),
        # gravel: shallow random height-field noise, ~4-20 mm bumps.
        "gravel": terrain_gen.HfRandomUniformTerrainCfg(
            proportion=0.25,
            noise_range=(0.004, 0.02),
            noise_step=0.004,
            border_width=0.25,
        ),
        # small rocks: discrete bumps smaller than the 60 mm foot, on a flat
        # 1 m platform at the patch center so RSI/reset spawns stay stable.
        "rocks": terrain_gen.HfDiscreteObstaclesTerrainCfg(
            proportion=0.25,
            obstacle_height_range=(0.005, 0.02),
            obstacle_width_range=(0.02, 0.06),
            num_obstacles=40,
            platform_width=1.0,
        ),
    },
)
"""50% flat / 25% gravel / 25% small-rocks terrain generator, sized for Open Duck Mini V2."""
