import math

from trueskill.constants import DELTA
from trueskill.trueskill import global_env


def calc_draw_probability(draw_margin, size, env=None):
    """Calculates a draw-probability from the given ``draw_margin``.

    :param draw_margin: the draw-margin.
    :param size: the number of players in two comparing teams.
    :param env: the :class:`TrueSkill` object.  Defaults to the global
                environment.

    """
    if env is None:
        env = global_env()
    return 2 * env.cdf(draw_margin / (math.sqrt(size) * env.beta)) - 1


def rate_1vs1(rating1, rating2, drawn=False, min_delta=DELTA, env=None):
    """A shortcut to rate just 2 players in a head-to-head match::

       alice, bob = Rating(25), Rating(30)
       alice, bob = rate_1vs1(alice, bob)
       alice, bob = rate_1vs1(alice, bob, drawn=True)

    :param rating1: the winner's rating if they didn't draw.
    :param rating2: the loser's rating if they didn't draw.
    :param drawn: if the players drew, set this to ``True``.  Defaults to
                  ``False``.
    :param min_delta: will be passed to :meth:`rate`.
    :param env: the :class:`TrueSkill` object.  Defaults to the global
                environment.
    :returns: a tuple containing recalculated 2 ratings.

    .. versionadded:: 0.2

    """
    if env is None:
        env = global_env()
    ranks = [0, 0 if drawn else 1]
    teams = env.rate([(rating1,), (rating2,)], ranks, min_delta=min_delta)
    return teams[0][0], teams[1][0]


def quality_1vs1(rating1, rating2, env=None):
    """A shortcut to calculate the match quality between just 2 players in
    a head-to-head match::

       if quality_1vs1(alice, bob) < 0.50:
           print('This match seems to be not so fair')

    :param rating1: the rating.
    :param rating2: the another rating.
    :param env: the :class:`TrueSkill` object.  Defaults to the global
                environment.

    .. versionadded:: 0.2

    """
    if env is None:
        env = global_env()
    return env.quality([(rating1,), (rating2,)])


def rate(rating_groups, ranks=None, weights=None, min_delta=DELTA):
    """A proxy function for :meth:`TrueSkill.rate` of the global environment.

    .. versionadded:: 0.2

    """
    return global_env().rate(rating_groups, ranks, weights, min_delta)


def quality(rating_groups, weights=None):
    """A proxy function for :meth:`TrueSkill.quality` of the global
    environment.

    .. versionadded:: 0.2

    """
    return global_env().quality(rating_groups, weights)


def expose(rating):
    """A proxy function for :meth:`TrueSkill.expose` of the global environment.

    .. versionadded:: 0.4

    """
    return global_env().expose(rating)
