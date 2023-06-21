agent = 'A1'
other_agent = 'A2'
service = 'Phone Call'
successful_interactions = int(input("No of successful interactions: "))
unsuccessful_interactions = int(input("No of unsuccessful interactions: "))
prev_history = (successful_interactions, unsuccessful_interactions)
confidence_threshold = 0.95
cooperation_threshold = 0.5
error_threshold = 0.2

# Opinion provider for agent A2 (static)
opinions = [{'A5': (15, 46)}, {'A6': (4, 1)}, {'A7': (3, 0)}]

# Static history
# prev_history = [{'A2': (17, 5)}, {'A3': (2, 15)}, {'A4': (18, 5)}]


NAME = 'TRAVOS Trust Scenario'

AGENTS = ['A', 'B', 'C', 'D']

OBSERVATIONS = [{'authors': ['A'],
                 'before': [],
                 'details': {'uri': 'www.example.com/for-dummies.html'},
                 'message': 'Redecentralization of the Web',
                 'observation_id': 1,
                 'receiver': 'B',
                 'sender': 'A'},
                {'authors': ['A'],
                 'before': [1],
                 'details': {'uri': 'www.example.com/web-of-things-for-dummies.html'},
                 'message': 'Web of Things',
                 'observation_id': 2,
                 'receiver': 'B',
                 'sender': 'A'},
                {'authors': ['A'],
                 'before': [2],
                 'details': {'uri': 'www.example.com/wasm-with-rust.html'},
                 'message': 'Web Assembly',
                 'observation_id': 3,
                 'receiver': 'B',
                 'sender': 'A'},
                {'authors': ['C'],
                 'before': [3],
                 'details': {'uri': 'www.example.com/beginners-guide-semantic-web.pdf'},
                 'message': 'Semantic Web and Linked Open Data',
                 'observation_id': 4,
                 'receiver': 'B',
                 'sender': 'C'},
                {'authors': ['C'],
                 'before': [4],
                 'details': {'uri': 'www.example.com/how-to-decentralize-your-favorite-data-structure.html'},
                 'message': 'Redecentralization of the Web',
                 'observation_id': 5,
                 'receiver': 'B',
                 'sender': 'C'},
                {'authors': ['C'],
                 'before': [5],
                 'details': {'uri': 'www.example.com/interactive-web-tutorial.html'},
                 'message': 'Web-based learning',
                 'observation_id': 6,
                 'receiver': 'B',
                 'sender': 'C'}]

HISTORY = {'A': [['B', 'www.example.com/interactive-web-tutorial.html', (1, 0)],
                 ['C',
                  'www.example.com/how-to-decentralize-your-favorite-data-structure.html',
                  (1, 0)],
                 ['D', 'www.example.com/beginners-guide-semantic-web.pdf', (0, 1)]],
           'B': [['A', 'www.example.com/interactive-web-tutorial.html', (1, 0)],
                 ['C',
                  'www.example.com/how-to-decentralize-your-favorite-data-structure.html',
                  (1, 0)],
                 ['D', 'www.example.com/beginners-guide-semantic-web.pdf', (1, 0)]],
           'C': [['A', 'www.example.com/interactive-web-tutorial.html', (1, 0)],
                 ['B',
                  'www.example.com/how-to-decentralize-your-favorite-data-structure.html',
                  (1, 0)],
                 ['D', 'www.example.com/beginners-guide-semantic-web.pdf', (1, 0)]],
           'D': [['A', 'www.example.com/interactive-web-tutorial.html', (1, 0)],
                 ['B',
                  'www.example.com/how-to-decentralize-your-favorite-data-structure.html',
                  (1, 0)],
                 ['C', 'www.example.com/beginners-guide-semantic-web.pdf', (1, 0)]]}

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

                           'Travos.experience': {},
                           'Travos.opinion': {}},
                     'B': {'__final__': {'name': 'weighted_average', 'weights': {}},

                           'Travos.experience': {},
                           'Travos.opinion': {}},
                     'C': {'__final__': {'name': 'weighted_average', 'weights': {}},

                           'Travos.experience': {},
                           'Travos.opinion': {}},
                     'D': {'__final__': {'name': 'weighted_average', 'weights': {}},

                           'Travos.experience': {},
                           'Travos.opinion': {}}}

DESCRIPTION = 'This is a basic scenario with four agents that contains the necessary ' \
              'metrics for TRAVOS trust evaluation.'
