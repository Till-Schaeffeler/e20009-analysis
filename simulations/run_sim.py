from attpc_engine.kinematics import (
    KinematicsPipeline,
    KinematicsTargetMaterial,
    ExcitationGaussian,
    ExcitationUniform,
    ExcitationBreitWigner,
    run_kinematics_pipeline,
    Reaction,
    Decay,
    PolarUniform,
)
from attpc_engine.detector import (
    DetectorParams,
    ElectronicsParams,
    PadParams,
    Config,
    run_simulation,
)
from attpc_engine import nuclear_map
from spyral_utils.nuclear.target import load_target 
from sim_utils import SpyralWriter_e20009, max_reaction_excitation_energy

from pathlib import Path
import numpy as np


# Set output file paths for simulated kinematic events and point clouds
# kine_path = Path("C:\\Users\\schaeffe\\Desktop\\B11_sim\\B_9_2_79_MeV_106_MeV_beam\\B_9_2_79_MeV_106_MeV_beam_kine.h5")
# kine_path = Path('c:\\Users\\schaeffe\\Desktop\\B11_sim\\B9_2_79_a_Li5__106_MeV_beam\\B9_2_79_a_Li5__106_MeV_beam_kine.h5')
# kine_path = Path('c:\\Users\\schaeffe\\Desktop\\B11_sim\\B9_2_79_8Be_p__106_MeV_beam\\B9_2_79_8Be_p__106_MeV_beam_kine.h5')
kine_path = Path("c:\\Users\\schaeffe\\Desktop\\B11_sim\\B_11_12_56_t_Be8_MeV_106_MeV_beam_p_cm_restricted\\B_11_12_56_t_Be8_MeV_106_MeV_beam_p_cm_restricted.h5")
# det_path = Path("c:\\Users\\schaeffe\\Desktop\\B11_sim\\B9_2_79_a_Li5__106_MeV_beam")



target_material_path = Path("C:\\Users\\schaeffe\\Desktop\\e20009_analysis-dev_1_18_2025\\e20009_analysis-dev\\e20009_parameters\\e20009_target.json")
target = load_target(target_material_path, nuclear_map)

nevents = 100000


pipeline = KinematicsPipeline(
    [
        Reaction(
            target=nuclear_map.get_data(1, 2),   # deuteron target
            projectile=nuclear_map.get_data(5, 10),  # B10 beam
            ejectile=nuclear_map.get_data(1, 1),      # 
        ), 
        Decay(parent=nuclear_map.get_data(5, 11), residual_1=nuclear_map.get_data(1, 3)), # First decay: 
        Decay(parent=nuclear_map.get_data(4, 8), residual_1=nuclear_map.get_data(2, 4) ) # Second decay: 
    ],
    excitations= [ExcitationGaussian(12.56, 0.0),
                  ExcitationGaussian(0.0, 0.0),
                  ExcitationGaussian(0.0, 0.0)
                      
    ],
       
    polar_dists=[
        PolarUniform(angle_min= 70 * (np.pi/180), angle_max= 80 * (np.pi/180)),     # 
        PolarUniform(angle_min=0, angle_max=np.pi),
        PolarUniform(angle_min=0, angle_max=np.pi)
    ],



    beam_energy=106,  # MeV
    target_material=KinematicsTargetMaterial(
        material=target, z_range=(0.0, 1.0), rho_sigma=0.02 / 3
    ),
)


detector = DetectorParams(
    length=1.0,
    efield=60000.0,
    bfield=3.0,
    mpgd_gain=175000,
    gas_target=target,
    diffusion=0.0,
    fano_factor=0.2,
    w_value=34.0,
)

electronics = ElectronicsParams(
    clock_freq=3.125,
    amp_gain=900,
    shaping_time=1000,
    micromegas_edge=62,
    windows_edge=396,
    adc_threshold=30.0,
)

pads = PadParams()

config = Config(detector, electronics, pads)
# writer = SpyralWriter_e20009(det_path, config, max_events_per_file=50000)


def main():
    run_kinematics_pipeline(pipeline, nevents, kine_path)
    # run_simulation(
    #     config,
    #     kine_path,
    #     writer,
    # )


if __name__ == "__main__":
    main()
