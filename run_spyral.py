from spyral import (
    Pipeline,
    start_pipeline,
    GetParameters,
    EstimateParameters,
    PadParameters,
)

from e20009_phases.PointcloudLegacyPhase import PointcloudLegacyPhase
from e20009_phases.ClusterPhase import ClusterPhase
from e20009_phases.EstimationPhase import EstimationPhase
from e20009_phases.InterpSolverPhase import InterpSolverPhase
# from e20009_phases.InterpLeastSqSolverPhase import InterpLeastSqSolverPhase
from e20009_phases.config import (
    ICParameters,
    DetectorParameters,
    SolverParameters,
    ClusterParameters,   
    ContinuityJoinParameters,
)


from pathlib import Path
import multiprocessing

#########################################################################################################
# Set up workspace and trace paths
workspace_path = Path("C:\\Users\\schaeffe\\Desktop\\e20009_B11_output_with_joining")
trace_path = Path("e:\\e2009\\traces")   # fake trace path for simulation

# Make directory to store beam events
if not workspace_path.exists():
    workspace_path.mkdir()
beam_events_folder = workspace_path / "beam_events"
if not beam_events_folder.exists():
    beam_events_folder.mkdir()

run_min = 108
run_max = 110
n_processes = 2

#########################################################################################################
# Define configuration
pad_params = PadParameters(
    pad_geometry_path=Path("C:\\Users\\schaeffe\\Desktop\\e20009_analysis-dev_1_18_2025\\e20009_analysis-dev\\e20009_parameters\\pad_geometry_legacy.csv"),
    pad_time_path=Path("C:\\Users\\schaeffe\\Desktop\\e20009_analysis-dev_1_18_2025\\e20009_analysis-dev\\e20009_parameters\\pad_time_correction.csv"),
    pad_electronics_path=Path("C:\\Users\\schaeffe\\Desktop\\e20009_analysis-dev_1_18_2025\\e20009_analysis-dev\\e20009_parameters\\pad_electronics_legacy.csv"),
    pad_scale_path=Path("C:\\Users\\schaeffe\\Desktop\\e20009_analysis-dev_1_18_2025\\e20009_analysis-dev\\e20009_parameters\\pad_scale.csv"),
)

get_params = GetParameters(
    baseline_window_scale=20.0,
    peak_separation=5.0,
    peak_prominence=20.0,
    peak_max_width=100.0,
    peak_threshold=30.0,
)

ic_params = ICParameters(
    baseline_window_scale=100.0,
    peak_separation=5.0,
    peak_prominence=30.0,
    peak_max_width=20.0,
    peak_threshold=300.0,
    low_accept=60,
    high_accept=411,
)

det_params = DetectorParameters(
    magnetic_field=3.0,
    electric_field=60000.0,
    detector_length=1000.0,
    beam_region_radius=20.0,
    drift_velocity_path=Path("C:\\Users\\schaeffe\\Desktop\\e20009_analysis-dev_1_18_2025\\e20009_analysis-dev\\e20009_parameters\\drift_velocity.csv"),
    get_frequency=3.125,
    garfield_file_path=Path("C:\\Users\\zachs\\Desktop\\e20009_analysis\\e20009_analysis\\e20009_parameters\\e20009_efield_correction.txt"),
    do_garfield_correction=False,
)

cluster_params = ClusterParameters(
    min_cloud_size=50,
    min_points=5,
    min_size_scale_factor=0.0,
    min_size_lower_cutoff=10,
    cluster_selection_epsilon=13.0,
    overlap_join = None,
    continuity_join = ContinuityJoinParameters(
        join_radius_fraction = 0.3,
        join_z_fraction = 0.2
    ),
    outlier_scale_factor=0.05,
)

estimate_params = EstimateParameters(
    min_total_trajectory_points=20, smoothing_factor=100.0
)

# Protons
solver_params = SolverParameters(
    gas_data_path=Path(
        "C:\\Users\\schaeffe\\Desktop\\e20009_analysis-dev_1_18_2025\\e20009_analysis-dev\\e20009_parameters\\e20009_target.json"
    ),
    gain_match_factors_path=Path(
        "C:\\Users\\schaeffe\\Desktop\\e20009_analysis-dev_1_18_2025\\e20009_analysis-dev\\e20009_parameters\\gain_match_factors.csv"
    ),
    particle_id_filename=Path("C:\\Users\\schaeffe\\Desktop\\B11_sim\\B_11_12_56_MeV_106_MeV_beam\\proton_sim.json"),
    ic_min_val=900,
    ic_max_val=1300,
    n_time_steps=500,
    interp_ke_min=0.01,
    interp_ke_max=60.0,
    interp_ke_bins=500,
    interp_polar_min=0.1,
    interp_polar_max=179.9,
    interp_polar_bins=360,
)

# # Tritons B10(d,t)B9
# solver_params = SolverParameters(
#     gas_data_path=Path(
#         "C:\\Users\\schaeffe\\Desktop\\e20009_analysis-dev_1_18_2025\\e20009_analysis-dev\\e20009_parameters\\e20009_target.json"
#     ),
#     gain_match_factors_path=Path(
#         "C:\\Users\\schaeffe\\Desktop\\e20009_analysis-dev_1_18_2025\\e20009_analysis-dev\\e20009_parameters\\gain_match_factors.csv"
#     ),
#     particle_id_filename=Path("C:\\Users\\schaeffe\\Desktop\\e20009_analysis-dev_1_18_2025\\e20009_analysis-dev\\notebooks\\B10(d,p)\\triton_particle_id_subset_bigger.json"),
#     ic_min_val=900,
#     ic_max_val=1300,
#     n_time_steps=500,
#     interp_ke_min=0.01,
#     interp_ke_max=70.0,
#     interp_ke_bins=500,
#     interp_polar_min=0.1,
#     interp_polar_max=90,
#     interp_polar_bins=180,
# )

# # Deuterons
# solver_params = SolverParameters(
#     gas_data_path=Path(
#         "C:\\Users\\schaeffe\\Desktop\\e20009_analysis-dev_1_18_2025\\e20009_analysis-dev\\e20009_parameters\\e20009_target.json"
#     ),
#     gain_match_factors_path=Path(
#         "C:\\Users\\schaeffe\\Desktop\\e20009_analysis-dev_1_18_2025\\e20009_analysis-dev\\e20009_parameters\\gain_match_factors.csv"
#     ),
#     particle_id_filename=Path("C:\\Users\\schaeffe\\Desktop\\e20009_analysis-dev_1_18_2025\\e20009_analysis-dev\\notebooks\\B10(d,p)\\proton_particle_id.json"),
#     ic_min_val=900,
#     ic_max_val=1300,
#     n_time_steps=750,
#     interp_ke_min=0.01,
#     interp_ke_max=80.0,
#     interp_ke_bins=350,
#     interp_polar_min=0.1,
#     interp_polar_max=89.9,
#     interp_polar_bins=250,
# )

#########################################################################################################
# Construct pipeline
pipe = Pipeline(
    [
        PointcloudLegacyPhase(
            get_params,
            ic_params,
            det_params,
            pad_params,
        ),
        ClusterPhase(
            cluster_params,
            det_params,
        ),
        EstimationPhase(estimate_params, det_params),
        InterpSolverPhase(solver_params, det_params),
     ],
    [False, True, False, 
     False
     ],
    workspace_path,
    trace_path,
)


def main():
    start_pipeline(pipe, run_min, run_max, n_processes)


if __name__ == "__main__":
    multiprocessing.set_start_method("spawn")
    main()
