"""학습 시점에 쓰는 험지 혼합 지형 (평지/요철/장애물 병렬 분할).

`open_duck_mini_isaaclab/terrains.py`(상위 디렉토리)와는 다른 물건이다 — 그건
"학습은 전부 평면에서 돌았다"는 전제 위에서 **학습이 끝난 정책을 재생/진단**할
때만 지형을 바꿔 끼우는 도구(`apply_terrain()`)다. 이 파일은 반대로 **학습
자체를** 지형이 섞인 환경에서 돌리기 위한 것이다 — `num_rows`/`num_cols`
그리드에 `curriculum=False`로 서브테레인을 배치하면 각 env가 스폰 시점에
평지/요철/장애물 중 하나에 고정 배정되고, 그 비율이 서브테레인 population
분할(병렬)이 된다. 난이도를 점진적으로 올리는 curriculum이 아니라 "전체
env의 절반은 평지, 절반은 험지"로 고정 분할한다.

요철·장애물 파라미터는 `terrains.py`의 `rough_s`/`obstacles_s`(로봇 스케일
보정값 — 로봇 서 있는 높이 125~140mm, 발 들어올림 4cm 기준)를 그대로
채용한다. `vertical_scale`도 그쪽과 같은 이유(요철 최소 단위 2mm보다 작아야
지형이 뭉개지지 않음)로 IsaacLab 기본값(5mm) 대신 2mm를 쓴다.
"""

import isaaclab.sim as sim_utils
import isaaclab.terrains as terrain_gen
from isaaclab.terrains import TerrainGeneratorCfg

GRAVEL_ROUGH_TERRAINS_CFG = TerrainGeneratorCfg(
    size=(3.0, 3.0),
    border_width=0.25,
    num_rows=10,
    num_cols=20,
    horizontal_scale=0.02,
    vertical_scale=0.002,
    slope_threshold=0.75,
    use_cache=False,
    curriculum=False,  # 난이도 점진 상승이 아니라 population 고정 분할
    sub_terrains={
        "flat": terrain_gen.MeshPlaneTerrainCfg(proportion=0.5),
        # terrains.py의 rough_s와 동일 (요철 2~12mm, 로봇 스케일)
        "gravel": terrain_gen.HfRandomUniformTerrainCfg(
            proportion=0.25, noise_range=(0.002, 0.012), noise_step=0.002, border_width=0.25,
        ),
        # terrains.py의 obstacles_s와 동일 (흩뿌린 장애물 5~20mm)
        "rocks": terrain_gen.HfDiscreteObstaclesTerrainCfg(
            proportion=0.25, obstacle_height_mode="choice", obstacle_width_range=(0.05, 0.15),
            obstacle_height_range=(0.005, 0.020), num_obstacles=40,
            platform_width=1.0, border_width=0.25,
        ),
    },
)

GRAVEL_ROUGH_TERRAIN_IMPORTER = dict(
    prim_path="/World/ground",
    terrain_type="generator",
    terrain_generator=GRAVEL_ROUGH_TERRAINS_CFG,
    collision_group=-1,
    physics_material=sim_utils.RigidBodyMaterialCfg(
        friction_combine_mode="multiply",
        restitution_combine_mode="multiply",
        static_friction=1.0,
        dynamic_friction=1.0,
    ),
    debug_vis=False,
)
