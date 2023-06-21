from models import Observation


def extract_resource_data(observation):
    """
    Extract the resource data from the observation.

    :param observation: The observation to extract the resource data from.
    :type observation: Observation
    :return: The resource data.
    :rtype: dict
    """
    # TODO: extract data from observation message not only from observation details
    # adding all resource data based on observation details if existing
    resource_data = {}
    if hasattr(observation, 'authors'):
        resource_data['authors'] = observation.authors # list of authors in string format
    if hasattr(observation, 'details'):
        if 'content_trust.publication_date' in observation.details:
            # utcnow().timestamp() float
            resource_data['publication_date'] = observation.details['content_trust.publication_date']
        if 'content_trust.related_resources' in observation.details:
            # list of related resources
            resource_data['related_resources'] = observation.details['content_trust.related_resources']
        if 'content_trust.topics' in observation.details:
            # list of topics in string format
            resource_data['topics'] = observation.details['content_trust.topics']
    return resource_data
