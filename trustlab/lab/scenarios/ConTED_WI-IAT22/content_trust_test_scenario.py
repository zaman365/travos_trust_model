NAME = 'Full Content Trust'

AGENTS = ['A', 'B', 'C', 'D']

OBSERVATIONS = [{'authors': ['A'],
                 'before': [],
                 'details': {'content_trust.bias': 1.0,
                             'content_trust.context_level': 'relaxed',
                             'content_trust.deception': 1.0,
                             'content_trust.incentive': 0.97,
                             'content_trust.likelihood': 1.0,
                             'content_trust.publication_date': 1625783748,
                             'content_trust.related_resources': ['www.example.com/beginners-guide-semantic-web.pdf'],
                             'content_trust.specificity': 0.89,
                             'content_trust.topics': ['Web Engineering', 'Things'],
                             'content_trust.trusted_topics': ['Web Engineering'],
                             'uri': 'www.example.com/for-dummies.html'},
                 'message': 'Redecentralization of the Web',
                 'observation_id': 1,
                 'receiver': 'B',
                 'sender': 'A'},
                {'authors': ['A'],
                 'before': [1],
                 'details': {'content_trust.bias': 1.0,
                             'content_trust.context_level': 'relaxed',
                             'content_trust.deception': 1.0,
                             'content_trust.incentive': 0.97,
                             'content_trust.likelihood': 1.0,
                             'content_trust.publication_date': 1625783748,
                             'content_trust.related_resources': ['www.example.com/beginners-guide-semantic-web.pdf'],
                             'content_trust.specificity': 0.89,
                             'content_trust.topics': ['Web Engineering', 'Things'],
                             'content_trust.trusted_topics': ['Web Engineering'],
                             'uri': 'www.example.com/web-of-things-for-dummies.html'},
                 'message': 'Web of Things',
                 'observation_id': 2,
                 'receiver': 'B',
                 'sender': 'A'},
                {'authors': ['A'],
                 'before': [2],
                 'details': {'content_trust.bias': 1.0,
                             'content_trust.context_level': 'relaxed',
                             'content_trust.deception': 1.0,
                             'content_trust.incentive': 0.97,
                             'content_trust.likelihood': 1.0,
                             'content_trust.publication_date': 1625783748,
                             'content_trust.related_resources': ['www.example.com/beginners-guide-semantic-web.pdf',
                                                                 'www.example.com/web-of-things-for-dummies.html'],
                             'content_trust.specificity': 0.89,
                             'content_trust.topics': ['Web Engineering', 'Rust', 'C++'],
                             'content_trust.trusted_topics': ['Web Engineering', 'Rust'],
                             'uri': 'www.example.com/wasm-with-rust.html'},
                 'message': 'Web Assembly',
                 'observation_id': 3,
                 'receiver': 'B',
                 'sender': 'A'},
                {'authors': ['C'],
                 'before': [3],
                 'details': {'content_trust.bias': 1.0,
                             'content_trust.context_level': 'relaxed',
                             'content_trust.deception': -1.0,
                             'content_trust.incentive': 0.97,
                             'content_trust.likelihood': 1.0,
                             'content_trust.publication_date': 1625783748,
                             'content_trust.related_resources': [
                                 'www.example.com/how-to-decentralize-your-favorite-data-structure.html'],
                             'content_trust.specificity': 0.89,
                             'content_trust.topics': ['Web Engineering'],
                             'content_trust.trusted_topics': ['Semantic Web', 'Linked Data'],
                             'uri': 'www.example.com/beginners-guide-semantic-web.pdf'},
                 'message': 'Semantic Web and Linked Open Data',
                 'observation_id': 4,
                 'receiver': 'B',
                 'sender': 'C'},
                {'authors': ['C'],
                 'before': [4],
                 'details': {'content_trust.bias': 1.0,
                             'content_trust.context_level': 'relaxed',
                             'content_trust.deception': 1.0,
                             'content_trust.incentive': 0.97,
                             'content_trust.likelihood': 1.0,
                             'content_trust.publication_date': 1625783748,
                             'content_trust.related_resources': ['www.example.com/beginners-guide-semantic-web.pdf'],
                             'content_trust.specificity': 0.89,
                             'content_trust.topics': ['Web Engineering',
                                                      'Distributed Data Structures'],
                             'content_trust.trusted_topics': ['Distributed Data Structures'],
                             'uri': 'www.example.com/how-to-decentralize-your-favorite-data-structure.html'},
                 'message': 'Redecentralization of the Web',
                 'observation_id': 5,
                 'receiver': 'B',
                 'sender': 'C'},
                {'authors': ['C'],
                 'before': [5],
                 'details': {'content_trust.bias': 1.0,
                             'content_trust.context_level': 'relaxed',
                             'content_trust.deception': 1.0,
                             'content_trust.incentive': 0.97,
                             'content_trust.likelihood': 1.0,
                             'content_trust.publication_date': 1625783748,
                             'content_trust.related_resources': ['www.example.com/beginners-guide-semantic-web.pdf'],
                             'content_trust.specificity': 0.89,
                             'content_trust.topics': ['Web Engineering', 'Web-based learning'],
                             'content_trust.trusted_topics': ['Web-based learning',
                                                              'Web Engineering',
                                                              'Web'],
                             'uri': 'www.example.com/interactive-web-tutorial.html'},
                 'message': 'Web-based learning',
                 'observation_id': 6,
                 'receiver': 'B',
                 'sender': 'C'}]

HISTORY = {'A': [['B', 'www.example.com/interactive-web-tutorial.html', 1.0],
                 ['C',
                  'www.example.com/how-to-decentralize-your-favorite-data-structure.html',
                  1.0],
                 ['D', 'www.example.com/beginners-guide-semantic-web.pdf', 0.0]],
           'B': [['A', 'www.example.com/interactive-web-tutorial.html', 1.0],
                 ['C',
                  'www.example.com/how-to-decentralize-your-favorite-data-structure.html',
                  1.0],
                 ['D', 'www.example.com/beginners-guide-semantic-web.pdf', 1.0]],
           'C': [['A', 'www.example.com/interactive-web-tutorial.html', 1.0],
                 ['B',
                  'www.example.com/how-to-decentralize-your-favorite-data-structure.html',
                  1.0],
                 ['D', 'www.example.com/beginners-guide-semantic-web.pdf', 1.0]],
           'D': [['A', 'www.example.com/interactive-web-tutorial.html', 1.0],
                 ['B',
                  'www.example.com/how-to-decentralize-your-favorite-data-structure.html',
                  1.0],
                 ['C', 'www.example.com/beginners-guide-semantic-web.pdf', 1.0]]}



SCALES_PER_AGENT = {'A': {'cooperation': 0.5,
                          'default': 0.0,
                          'forgivability': -0.5,
                          'maximum': 1.0,
                          'minimum': -1.0,
                          'name': 'Trust Scale by Marsh and Briggs (2009)',
                          'package': 'marsh_briggs_scale'},
                    'B': {'cooperation': 0.5,
                          'default': 0.0,
                          'forgivability': -0.5,
                          'maximum': 1.0,
                          'minimum': -1.0,
                          'name': 'Trust Scale by Marsh and Briggs (2009)',
                          'package': 'marsh_briggs_scale'},
                    'C': {'cooperation': 0.5,
                          'default': 0.0,
                          'forgivability': -0.5,
                          'maximum': 1.0,
                          'minimum': -1.0,
                          'name': 'Trust Scale by Marsh and Briggs (2009)',
                          'package': 'marsh_briggs_scale'},
                    'D': {'cooperation': 0.5,
                          'default': 0.0,
                          'forgivability': -0.5,
                          'maximum': 1.0,
                          'minimum': -1.0,
                          'name': 'Trust Scale by Marsh and Briggs (2009)',
                          'package': 'marsh_briggs_scale'}}

METRICS_PER_AGENT = {'A': {'__final__': {'name': 'weighted_average', 'weights': {}},
                           'content_trust.age_grace_period_seconds': 2592000,
                           'content_trust.authority': ['C'],
                           'content_trust.context_values': {'critical': 0.75,
                                                            'important': 0.5,
                                                            'relaxed': 0.2},
                           'content_trust.deception': -0.2,
                           'content_trust.direct_experience': {},
                           'content_trust.max_lifetime_seconds': 31536000,
                           'content_trust.popularity': {'peers': ['B', 'C', 'D']},
                           'content_trust.provenance': ['A', 'D'],
                           'content_trust.recency_age_limit': 31536000,
                           'content_trust.recommendation': {},
                           'content_trust.related_resources': {},
                           'content_trust.topic': {'B': {'Web Engineering': 1.0},
                                                   'C': {'Web Engineering': 1.0},
                                                   'D': {'Web Engineering': 1.0}},
                           'content_trust.user_expertise': {}},
                     'B': {'__final__': {'name': 'weighted_average', 'weights': {}},
                           'content_trust.age_grace_period_seconds': 2592000,
                           'content_trust.authority': ['C'],
                           'content_trust.context_values': {'critical': 0.7,
                                                            'important': 0.4,
                                                            'relaxed': 0.2},
                           'content_trust.deception': -0.2,
                           'content_trust.direct_experience': {},
                           'content_trust.max_lifetime_seconds': 31536000,
                           'content_trust.popularity': {'peers': ['B', 'C', 'D']},
                           'content_trust.provenance': ['A', 'D'],
                           'content_trust.recency_age_limit': 31536000,
                           'content_trust.recommendation': {},
                           'content_trust.related_resources': {},
                           'content_trust.topic': {'A': {'Web Engineering': 0.5},
                                                   'C': {'Web Engineering': 0.5},
                                                   'D': {'Web Engineering': 1.0}},
                           'content_trust.user_expertise': {}},
                     'C': {'__final__': {'name': 'weighted_average', 'weights': {}},
                           'content_trust.age_grace_period_seconds': 2592000,
                           'content_trust.authority': [],
                           'content_trust.context_values': {'critical': 0.95,
                                                            'important': 0.7,
                                                            'relaxed': 0.3},
                           'content_trust.deception': -0.2,
                           'content_trust.direct_experience': {},
                           'content_trust.max_lifetime_seconds': 31536000,
                           'content_trust.popularity': {'peers': ['B', 'C', 'D']},
                           'content_trust.provenance': ['A', 'D'],
                           'content_trust.recency_age_limit': 31536000,
                           'content_trust.recommendation': {},
                           'content_trust.related_resources': {},
                           'content_trust.topic': {'A': {'Web Engineering': 1.0},
                                                   'B': {'Web Engineering': 1.0},
                                                   'D': {'Web Engineering': 1.0}},
                           'content_trust.user_expertise': {}},
                     'D': {'__final__': {'name': 'weighted_average', 'weights': {}},
                           'content_trust.age_grace_period_seconds': 2592000,
                           'content_trust.authority': ['C'],
                           'content_trust.context_values': {'critical': 0.5,
                                                            'important': 0.2,
                                                            'relaxed': -0.2},
                           'content_trust.deception': -0.2,
                           'content_trust.direct_experience': {},
                           'content_trust.max_lifetime_seconds': 31536000,
                           'content_trust.popularity': {'peers': ['B', 'C', 'D']},
                           'content_trust.provenance': [],
                           'content_trust.recency_age_limit': 31536000,
                           'content_trust.recommendation': {},
                           'content_trust.related_resources': {},
                           'content_trust.topic': {'A': {'Web Engineering': 1.0},
                                                   'B': {'Web Engineering': 1.0},
                                                   'C': {'Web Engineering': 1.0}},
                           'content_trust.user_expertise': {}}}

DESCRIPTION = 'This is a basic scenario with four agents that contains the necessary ' \
              'metrics for a full content trust-based trust evaluation.'