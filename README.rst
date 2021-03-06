adcorr
======

|code_ci| |docs_ci| |coverage| |pypi_version| |license|

This package provides a set of pure python functions for performing corrections on area
detector data.

============== ==============================================
PyPI           ``pip install adcorr``
Source code    https://github.com/garryod/adcorr
Documentation  https://garryod.github.io/adcorr
Releases       https://github.com/garryod/adcorr/releases
============== ==============================================

A brief example of performing corrections using the library is presented below:

.. code:: python

    frames = load_my_frames()
    mask = load_my_mask()
    count_times = load_count_times()

    frames = mask_frames(frames, mask)
    frames = correct_deadtime(
        frames,
        count_times,
        DETECTOR_MINIMUM_PULSE_SEPARATION,
        DETECTOR_MINIMUM_ARRIVAL_SEPARATION,
    )
    frames = correct_dark_current(
        frames,
        count_times,
        BASE_DARK_CURRENT,
        TEMPORAL_DARK_CURRENT,
        FLUX_DEPENDANT_DARK_CURRENT,
    )
    ...

.. |code_ci| image:: https://github.com/garryod/adcorr/workflows/Code%20CI/badge.svg?branch=main
    :target: https://github.com/garryod/adcorr/actions?query=workflow%3A%22Code+CI%22
    :alt: Code CI

.. |docs_ci| image:: https://github.com/garryod/adcorr/workflows/Docs%20CI/badge.svg?branch=main
    :target: https://github.com/garryod/adcorr/actions?query=workflow%3A%22Docs+CI%22
    :alt: Docs CI

.. |coverage| image:: https://codecov.io/gh/garryod/adcorr/branch/main/graph/badge.svg
    :target: https://codecov.io/gh/garryod/adcorr
    :alt: Test Coverage

.. |pypi_version| image:: https://img.shields.io/pypi/v/adcorr.svg
    :target: https://pypi.org/project/adcorr
    :alt: Latest PyPI version

.. |license| image:: https://img.shields.io/badge/License-Apache%202.0-blue.svg
    :target: https://opensource.org/licenses/Apache-2.0
    :alt: Apache License

..
    Anything below this line is used when viewing README.rst and will be replaced
    when included in index.rst

See https://garryod.github.io/adcorr for more detailed documentation.
