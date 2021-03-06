from typing import cast

from .utils.typing import Frames


def correct_displaced_volume(frames: Frames, displaced_fraction: float) -> Frames:
    """Correct for displaced volume of solvent by multiplying signal by retained fraction.

    Correct for displaced volume of solvent by multiplying signal by the retained
    fraction, as detailed in section 3.xviii and appendix B of 'The modular small-angle
    X-ray scattering data correction sequence'
    [https://doi.org/10.1107/S1600576717015096].

    Args:
        frames:  A stack of frames to be corrected.
        displaced_fraction: The fraction of solvent displaced by the analyte.

    Returns:
        The corrected stack of frames.
    """
    if displaced_fraction < 0.0 or displaced_fraction > 1.0:
        raise ValueError("Displaced Fraction must be in interval [0, 1].")

    return cast(Frames, frames * (1.0 - displaced_fraction))
