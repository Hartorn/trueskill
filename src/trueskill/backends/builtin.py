import math

__all__ = ["cdf", "pdf", "ppf", "gen_ppf"]


def _gen_erfcinv(erfc, math=math):
    """Generates the inverse function of erfc by the given erfc function and
    math module.
    """

    def erfcinv(y):
        """The inverse function of erfc."""
        if y >= 2:
            return -100.0
        if y <= 0:
            return 100.0
        zero_point = y < 1
        if not zero_point:
            y = 2 - y
        t = math.sqrt(-2 * math.log(y / 2.0))
        x = -0.70711 * ((2.30753 + t * 0.27061) / (1.0 + t * (0.99229 + t * 0.04481)) - t)
        for _ in range(2):
            err = erfc(x) - y
            x += err / (1.12837916709551257 * math.exp(-(x**2)) - x * err)
        return x if zero_point else -x

    return erfcinv


def gen_ppf(erfc, math=math):
    """ppf is the inverse function of cdf.  This function generates cdf by the
    given erfc and math module.
    """
    erfcinv = _gen_erfcinv(erfc, math)

    def ppf(x, mu=0, sigma=1):
        """The inverse function of cdf."""
        return mu - sigma * math.sqrt(2) * erfcinv(2 * x)

    return ppf


def erfc(x):
    """Complementary error function (via `http://bit.ly/zOLqbc`_)"""
    z = abs(x)
    t = 1.0 / (1.0 + z / 2.0)
    r = t * math.exp(
        -z * z
        - 1.26551223
        + t
        * (
            1.00002368
            + t
            * (
                0.37409196
                + t
                * (
                    0.09678418
                    + t
                    * (
                        -0.18628806
                        + t * (0.27886807 + t * (-1.13520398 + t * (1.48851587 + t * (-0.82215223 + t * 0.17087277))))
                    )
                )
            )
        )
    )
    return 2.0 - r if x < 0 else r


def cdf(x, mu=0, sigma=1):
    """Cumulative distribution function"""
    return 0.5 * erfc(-(x - mu) / (sigma * math.sqrt(2)))


def pdf(x, mu=0, sigma=1):
    """Probability density function"""
    return 1 / math.sqrt(2 * math.pi) * abs(sigma) * math.exp(-(((x - mu) / abs(sigma)) ** 2 / 2))


ppf = gen_ppf(erfc)