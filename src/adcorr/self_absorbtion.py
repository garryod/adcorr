from typing import Tuple, TypeVar, cast

from numpy import cos, dtype, exp, floating, log, ndarray, power
from numpy.ma import MaskedArray, masked_array

from .utils.geometry import scattering_angles

FrameDType = TypeVar("FrameDType", bound=dtype)
NumFrames = TypeVar("NumFrames", bound=int)
FrameWidth = TypeVar("FrameWidth", bound=int)
FrameHeight = TypeVar("FrameHeight", bound=int)


def self_absorbtion_correction_factors(
    frame_shape: Tuple[FrameWidth, FrameHeight],
    beam_center: Tuple[float, float],
    pixel_sizes: Tuple[float, float],
    distance: float,
    absorbtion_coefficient: float,
    thickness: float,
) -> ndarray[Tuple[FrameWidth, FrameHeight], dtype[floating]]:
    """Computes the self absorbtion correction factors given geometry and transmissibility.

    Args:
        frame_shape (Tuple[FrameWidth, FrameHeight]): The shape of a frame.
        beam_center (Tuple[float, float]): The center position of the beam in pixels.
        pixel_sizes (Tuple[float, float]): The real space size of a detector pixel.
        distance (float): The distance between the detector and the sample.
        absorbtion_coefficient (float): The coefficient of absorbtion for a given
            material at a given photon energy.
        thickness (float): The thickness of the detector head material.

    Returns:
        ndarray[Any, dtype[floating]]: An array of correction factors to be applied to
            frames.
    """
    angles = scattering_angles(frame_shape, beam_center, pixel_sizes, distance)
    transmissibility = exp(-absorbtion_coefficient * thickness)
    return (1 - power(transmissibility, 1 / cos(angles) - 1)) / (
        log(transmissibility) * (1 - 1 / cos(angles))
    )


def correct_self_absorbtion(
    frames: MaskedArray[Tuple[NumFrames, FrameWidth, FrameHeight], FrameDType],
    beam_center: Tuple[float, float],
    pixel_sizes: Tuple[float, float],
    distance: float,
    absorbtion_coefficient: float,
    thickness: float,
) -> MaskedArray[Tuple[NumFrames, FrameWidth, FrameHeight], FrameDType]:
    """Correct for transmission loss due to differences in observation angle.

    Correct for transmission loss due to differences in observation angle, as detailed
    in section 3.4.7 of 'Everything SAXS: small-angle scattering pattern collection and
    correction' [https://doi.org/10.1088/0953-8984/25/38/383201].

    Args:
        frames (MaskedArray[Tuple[NumFrames, FrameWidth, FrameHeight], FrameDType]): A
            stack of frames to be corrected.
        beam_center (Tuple[float, float]): The center position of the beam in pixels.
        pixel_sizes (Tuple[float, float]): The real space size of a detector pixel.
        distance (float): The distance between the detector and the sample.
        absorbtion_coefficient (float): The coefficient of absorbtion for a given
            material at a given photon energy.
        thickness (float): The thickness of the detector head material.

    Returns:
        MaskedArray[FramesShape, FrameDType]: The corrected stack of frames.
    """
    correction_factors = self_absorbtion_correction_factors(
        cast(Tuple[FrameWidth, FrameHeight], frames.shape[-2:]),
        beam_center,
        pixel_sizes,
        distance,
        absorbtion_coefficient,
        thickness,
    )
    return masked_array(frames.data * correction_factors, frames.mask)