import argparse
import sys
from distutils.util import strtobool
from models.scenario_ct_random import Scenario
from models.scenario_ct_init import Scenario as ScenarioInit
from models.scenario_ct_random_without_pop_rec import Scenario as ScenarioWithoutPopRec

PARAMS = [
    (2000, 2000, 'rp_2000x2000', 'D:\\aTLAS_scenarios\\rp_2000x2000_scenario.py'),
    (2500, 2500, 'rp_2500x2500', 'D:\\aTLAS_scenarios\\rp_2500x2500_scenario.py'),
]


def gen_scenario(messages, agents, scenario_name, scenario_path, mode):
    if mode == 'random':
        scenario = Scenario(messages, agents, scenario_path, scenario_name)
    elif mode == 'random_init':
        scenario = ScenarioInit(messages, agents, scenario_path, scenario_name)
    elif mode == 'random_without_pop_rec':
        scenario = ScenarioWithoutPopRec(messages, agents, scenario_path, scenario_name)
    else:
        raise ValueError('Unknown mode: {}'.format(mode))
    scenario.generate_and_write_to_file()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-m", "--messages", type=int,
                        help="The amount of messages/observations send in the scenario.")
    parser.add_argument("-a", "--agents", type=int,
                        help="The amount of agents/applications spawned in the scenario.")
    parser.add_argument("-o", "--outfile",
                        help="The pathname of the output scenario file.")
    parser.add_argument("-n", "--name", default=None,
                        help="The Scenario name given to the scenario via variable.")
    parser.add_argument("-s", "--several", type=lambda x: bool(strtobool(x)), nargs='?', const=True, default=False,
                        help="Whether to use the list in gen.py. Alternatively one scenario in parameters.")
    parser.add_argument("-M", "--mode", type=str, default='random', choices=['random', 'random_rp', 'random_init'],)
    args = parser.parse_args()
    if args.several:
        for msgs, apps, s_name, path in PARAMS:
            gen_scenario(msgs, apps, path, s_name, args.mode)
            print(f'Generated scenario {s_name} with {msgs} observations and {apps} agents')
    else:
        gen_scenario(args.messages, args.agents, args.name, args.outfile, args.mode)
