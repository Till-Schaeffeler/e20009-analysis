from dataclasses import dataclass


@dataclass
class ContinuityJoinParameters:
    """Parameters for joining clusters based on continuity

    Attributes
    ----------
    join_radius_fraction: float
        The percent difference allowed for the cylindrical radius. Used as
        radius_threshold = join_radius_fraction * (max_radius - min_radius)
        where max_radius and min_radius are the maximum, minimum radius value over both
        clusters being compared
    join_z_fraction: float
        The percent difference allowed for the cylindrical z. Used as
        z_threshold = join_z_fraction * (max_z - min_z)
        where max_z and min_z are the maximum, minimum z value over both
        clusters being compared

    """

    join_radius_fraction: float
    join_z_fraction: float


@dataclass
class OverlapJoinParameters:
    """Parameters for joining clusters based on area of overlap

    Attributes
    ----------
    min_cluster_size_join: int
        The minimum size of a cluster for it to be included in the joining algorithm
    circle_overlap_ratio: float
        Minimum overlap ratio between two circles in the cluster joining algorithm. Used
        as area_overlap > circle_overlap_ratio * (min_area) where area_overlap is the
        area overlap and min_area is the minimum area of the two clusters being compared
    """

    circle_overlap_ratio: float
    min_cluster_size_join: int

@dataclass
class ClusterParameters:
    """Parameters for clustering, cluster joining, and cluster cleaning

    Attributes
    ----------
    min_cloud_size: int
        The minimum size for a point cloud to be clustered
    min_points: int
        min_samples parameter in scikit-learns' HDBSCAN algorithm
    min_size_scale_factor: int
        Factor which is multiplied by the number of points in a point cloud to set
        the min_cluster_size parameter in scikit-learn's HDBSCAN algorithm
    min_size_lower_cutoff: int
        min_cluster_size parameter in scikit-learn's HDBSCAN algorithm for events where n_points * min_size_scale_factor
        are less than this value.
    cluster_selection_epsilon: float
        cluster_selection_epsilon parameter in scikit-learn's HDBSCAN algorithm. Clusters less than this distance apart
        are merged in the hierarchy
    min_cluster_size_join: int
        The minimum size of a cluster for it to be included in the joining algorithm
    circle_overlap_ratio: float
        minimum overlap ratio between two circles in the cluster joining algorithm
    outlier_scale_factor: float
        Factor which is multiplied by the number of points in a trajectory to set the number of neighbors parameter
        for scikit-learns LocalOutlierFactor test
    """

    min_cloud_size: int
    min_points: int
    min_size_scale_factor: float
    min_size_lower_cutoff: int
    cluster_selection_epsilon: float
    overlap_join: OverlapJoinParameters | None
    continuity_join: ContinuityJoinParameters | None
    outlier_scale_factor: float
