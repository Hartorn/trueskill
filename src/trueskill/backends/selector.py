from trueskill.backends.builtin import cdf, gen_ppf, pdf, ppf

__all__ = ["available_backends", "choose_backend"]


def choose_backend(backend):
    """Returns a tuple containing cdf, pdf, ppf from the chosen backend.

    >>> cdf, pdf, ppf = choose_backend(None)
    >>> cdf(-10)
    7.619853263532764e-24
    >>> cdf, pdf, ppf = choose_backend('mpmath')
    >>> cdf(-10)
    mpf('7.6198530241605255e-24')

    .. versionadded:: 0.3

    """
    if backend is None:  # fallback
        return cdf, pdf, ppf
    if backend == "mpmath":
        try:
            import mpmath
        except ImportError as e:
            raise ImportError('Install "mpmath" to use this backend') from e
        return mpmath.ncdf, mpmath.npdf, gen_ppf(mpmath.erfc, math=mpmath)
    if backend == "scipy":
        try:
            from scipy.stats import norm
        except ImportError as e:
            raise ImportError('Install "scipy" to use this backend') from e
        return norm.cdf, norm.pdf, norm.ppf
    raise ValueError(f"{backend} backend is not defined")


def available_backends():
    """Detects list of available backends.  All of defined backends are
    ``None`` -- internal implementation, "mpmath", "scipy".

    You can check if the backend is available in the current environment with
    this function::

       if 'mpmath' in available_backends():
           # mpmath can be used in the current environment
           setup(backend='mpmath')

    .. versionadded:: 0.3

    """
    backends = [None]
    for backend in ["mpmath", "scipy"]:
        try:
            __import__(backend)
        except ImportError:
            continue
        backends.append(backend)
    return backends
