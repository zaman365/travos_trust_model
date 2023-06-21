from experience import experience_value, confidence_value
from opinion import opinion_value
from scenario import prev_history, confidence_threshold, cooperation_threshold, agent, other_agent

interaction_history = (prev_history[0], prev_history[1])
final_trust_value = ""

# Compare confidence value with confidence threshold and experience value with cooperation threshold
if confidence_value >= confidence_threshold and experience_value >= cooperation_threshold:
    interaction_history = (interaction_history[0] + 1, interaction_history[1])
    final_trust_value = experience_value
    print(f"Experience value {experience_value} > Cooperation threshold {cooperation_threshold},the interaction is "
          f"most likely to be successful")
    print("Trustworthy")
    print(
        f"Confidence value {confidence_value} {'=' if confidence_value == confidence_threshold else '>'} Confidence "
        f"threshold value {confidence_threshold}, that's why opinion is not necessary for trust evaluation.")
    print(f"Final Trust Value : {final_trust_value}")
    print(f"Previous history : {prev_history}")
    print(f"Updated interaction history : {interaction_history}")

if confidence_value >= confidence_threshold and experience_value < cooperation_threshold:
    interaction_history = (interaction_history[0], interaction_history[1] + 1)
    final_trust_value = experience_value
    print(f"Experience value {experience_value} < Cooperation threshold {cooperation_threshold},the interaction is "
          f"most likely to be unsuccessful")
    print("Not Trustworthy")
    print(
        f"Confidence value {confidence_value} {'=' if confidence_value == confidence_threshold else '>'} Confidence "
        f"threshold value {confidence_threshold}, that's why opinion is not necessary for trust evaluation.")
    print(f"Final Trust Value : {final_trust_value}")
    print(f"Previous history : {prev_history}")
    print(f"Updated interaction history : {interaction_history}")

# Look for opinions
if confidence_value < confidence_threshold:
    print(f"Opinion value is necessary to evaluate trust between agents {agent} and {other_agent}")

# Compare opinion value with experience value
if confidence_value < confidence_threshold and cooperation_threshold < experience_value <= opinion_value:
    interaction_history = (interaction_history[0] + 1, interaction_history[1])
    final_trust_value = opinion_value
    print(f"Opinion value {opinion_value} {'=' if opinion_value == experience_value else '>'} "
          f"Experience value {experience_value} and Experience value > Cooperation threshold {cooperation_threshold} "
          f"that's why the interaction is most likely to be successful")
    print("Trustworthy")
    print(f"Final Trust Value : {final_trust_value}")
    print(f"Previous history : {prev_history}")
    print(f"Updated interaction history : {interaction_history}")

if confidence_value < confidence_threshold and opinion_value < experience_value:
    interaction_history = (interaction_history[0], interaction_history[1] + 1)
    final_trust_value = opinion_value
    print(f"Opinion value {opinion_value} < Experience value {experience_value} "
          f" that's why the interaction is most likely to be unsuccessful")
    print("Not Trustworthy")
    print(f"Final Trust Value : {final_trust_value}")
    print(f"Previous history : {prev_history}")
    print(f"Updated interaction history : {interaction_history}")
