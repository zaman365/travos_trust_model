import datetime
from datetime import *
from models import Scale


def age_check(agent_behavior, publication_date, scale):
    """
    :param agent_behavior:  Metrics to be used the agent.
    :type agent_behavior: dict
    :param publication_date: Publication date to be used as calculation point as utcnow().timestamp() float.
    :type publication_date: float
    :param scale: The trust scale used by the agent
    :type scale: Scale
    :return: An age punishment value that is equal to the scale maximum value for recent publications and falls within
    [default, max) if it exceeded the allowed lifetime.
    :rtype: float or int
    """
    now = datetime.utcnow().timestamp()
    age = publication_date + \
        agent_behavior['content_trust.max_lifetime_seconds']
    if now < age:  # within allowed lifetime
        return scale.maximum_value()
    else:  # exceeded lifetime
        if 'content_trust.age_grace_period_seconds' in agent_behavior:
            grace_value = (
                now - age) / agent_behavior['content_trust.age_grace_period_seconds']
            if grace_value < 1.0:  # within grace period
                return (1-grace_value) * scale.maximum_value()
        return scale.default_value()  # no grace period or grace period exceeded
