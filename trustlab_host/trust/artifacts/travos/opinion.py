from test_scenario import opinions


def opinion():
    # Calculate m and n (for static opinions from scenario)
    m = sum(value[0] for opinion in opinions for value in opinion.values())
    n = sum(value[1] for opinion in opinions for value in opinion.values())

    # Calculate alpha and beta
    alpha = m + 1
    beta = n + 1
    # print(f"Shape parameter : ({alpha}, {beta})")

    # Calculate new trust  value for A2
    new_trust_value = alpha / (alpha + beta)
    print(f"The new trust value for A2 is: {new_trust_value}")
    return new_trust_value


opinion_value = opinion()
