from datetime import datetime
from loggers.basic_logger import BasicLogger
from models import Scale
from scipy.stats import beta
from scipy.integrate import quad
from test_scenario import agent, other_agent, service, prev_history, error_threshold


# Calculate experience value from past interaction history
# def experience(agent, other_agent, service, prev_history):
#     m = prev_history[0] + 1
#     n = prev_history[1] + 1
#     direct_xp = m / (m + n)
#     print(f"{agent} trusts {other_agent} for {service} service with trust value: {direct_xp}")
#     return direct_xp


def experience(agent, other_agent, resource_id, scale, logger):
    """
    The values in the history from agent about other agent are combined via median to the direct XP.

    :param agent: The agent which calculates the trust. (start of relationship)
    :type agent: str
    :param resource_id: The URI of the resource which is evaluated.
    :type resource_id: str
    :param scale: The Scale object to be used by the agent.
    :type scale: Scale
    :param logger: The logger object to be used by the agent.
    :type logger: BasicLogger
    :return: Direct experience value from agent about other agent.
    :rtype: float or int
    """

    history_lines = logger.read_lines_from_agent_history_travos(agent)
    # getting all history values of the agent respective to the evaluated resource and filters them based on their age
    # and the recency limit set in the trust preferences of the agent
    history = [tuple(entry['trust_value']) for entry in history_lines if entry['resource_id'] == resource_id and
               datetime.strptime(entry['date_time'], BasicLogger.get_time_format_string()) and
               entry['trust_value'] != 'None']
    print(history)

    m = history[0] + 1
    n = history[1] + 1
    # calculate direct experience
    direct_xp = m / (m + n)
    print(f"{agent} trusts {other_agent} with resource {resource_id} service with trust value: {direct_xp}")
    print(direct_xp)
    return direct_xp


# Store experience value
# experience_value = experience(agent, other_agent, service, prev_history)
# print(experience_value)


# Confidence value calculate using Beta Probability Density Function
def beta_integral(lower_limit, upper_limit, alpha, beta_):
    dist = beta(alpha, beta_)
    pdf = lambda x: dist.pdf(x)
    integral, _ = quad(pdf, lower_limit, upper_limit)
    return integral


# Beta distribution limit
lower_limit = experience_value - error_threshold
# print(lower_limit)
upper_limit = experience_value + error_threshold
# print(upper_limit)

# Shape parameter for beta distribution3
alpha = prev_history[0] + 1
beta_ = prev_history[1] + 1

# Store confidence value
confidence_value = beta_integral(lower_limit, upper_limit, alpha, beta_) / beta_integral(0, 1, alpha, beta_)
print(f"Experience value: {experience_value} and Confidence value: {confidence_value}")
