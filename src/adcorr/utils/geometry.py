from typing import List, Tuple

from numpy import (
    Inf,
    arctan,
    divide,
    dtype,
    floating,
    full_like,
    hypot,
    linspace,
    meshgrid,
    ndarray,
    where,
    zeros_like,
)


def _relative_position_meshgrid(
    frame_shape: Tuple[int, int],
    beam_center: Tuple[float, float],
    pixel_sizes: Tuple[float, float],
) -> List[ndarray]:
    return meshgrid(
        linspace(
            (0.5 - beam_center[1]) * pixel_sizes[1],
            (frame_shape[1] - 0.5 - beam_center[1]) * pixel_sizes[1],
            frame_shape[1],
        ),
        linspace(
            (0.5 - beam_center[0]) * pixel_sizes[0],
            (frame_shape[0] - 0.5 - beam_center[0]) * pixel_sizes[0],
            frame_shape[0],
        ),
    )


def scattering_angles(
    frame_shape: Tuple[int, int],
    beam_center: Tuple[float, float],
    pixel_sizes: Tuple[float, float],
    distance: float,
) -> ndarray[Tuple[int, int], dtype[floating]]:
    """Computes the angles of pixels from the sample for a given geometry.

    Args:
        frame_shape (Tuple[int, int]): The shape of a frame.
        beam_center (Tuple[float, float]): The center position of the beam in pixels.
        pixel_sizes (Tuple[float, float]): The real space size of a detector pixel.
        distance (float): The distance between the detector and the sample.

    Returns:
        ndarray[Tuple[int, int], dtype[floating]]: An array of pixel angles from the
            sample.
    """
    yy, xx = _relative_position_meshgrid(frame_shape, beam_center, pixel_sizes)
    return arctan(hypot(xx, yy) / distance)


def azimuthal_angles(
    frame_shape: Tuple[int, int],
    beam_center: Tuple[float, float],
    pixel_sizes: Tuple[float, float],
) -> ndarray[Tuple[int, int], dtype[floating]]:
    """Computes the azimuthal angles of pixels from the beam center.

    Args:
        frame_shape (Tuple[int, int]): The shape of the frame.
        beam_center (Tuple[float, float]): The center position of the beam in pixels.

    Returns:
        ndarray[Tuple[int, int], dtype[floating]]: An array of pixel azimuthal angles
            from the beam center.
    """
    yy, xx = _relative_position_meshgrid(frame_shape, beam_center, pixel_sizes)
    return arctan(
        where(
            xx == 0,
            zeros_like(xx),
            divide(xx, yy, out=full_like(yy, Inf), where=yy != 0),
        )
    )
