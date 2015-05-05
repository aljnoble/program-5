import json
from collections import namedtuple
from heapq import heappush, heappop

with open('Crafting.json') as f:
    Crafting = json.load(f)

Recipe = namedtuple('Recipe', ['name', 'check', 'effect', 'cost'])
all_recipes = []
for name, rule in Crafting['Recipes'].items:
    checker = make_checker(rule)
    effector = make_effector(rule)
    recipe = Recipe(name, checker, effector, rule['Time'])
    all_recipes.append(recipe)

# List of items that can be in your inventory:
# print Crafting['Items']
# example: ['bench', 'cart', ..., 'wood', 'wooden_axe', 'wooden_pickaxe']

# List of items in your initial inventory with amounts:
#print Crafting['Initial']
# {'coal': 4, 'plank': 1}

# List of items needed to be in your inventory at the end of the plan:
# (okay to have more than this; some might be satisfied by initial inventory)
#print Crafting['Goal']
# {'stone_pickaxe': 2}

# Dictionary of crafting recipes:
#print Crafting['Recipes']['craft stone_pickaxe at bench']
# example:
# {	'Produces': {'stone_pickaxe': 1},
#	'Requires': {'bench': True},
#	'Consumes': {'cobble': 3, 'stick': 2},
#	'Time': 1
# }

def inventory_to_tuple(d):
    Items = Crafting['Items']
    return tuple(d.get(name, 0) for i, name in enumerate(Items))


def inventory_to_set(d):
    return frozenset(d.items())


def make_cheker(rule):
    # this code runs once
    # do something with rule['Consumes'] and rule['Requires']
    def check(state):
        # this code runs millions of times
        return True  # or False

    return check


def make_effector(rule):
    # this code runs once
    # do something with rule['Produces'] and rule['Consumes']
    def effect(state):
        # this code runs millions of times
        next_state = state
        return next_state

    return check


def graph(state):
    for r in all_recipes:
        if r.check(state):
            yield (r.name, r.effect(state), r.cost)


def t_graph(state):
    for next_state, cost in edges[state].items():
        yield ((state, next_state), next_state, cost)


def t_is_goal(state):
    return state == 'c'


def make_initial_state(inventory):
    state = {}

    for item in Crafting['Items']:
        state[item] = 0

    for item, value in inventory.items():
        state[item] = value

    return state


def heuristic(state):
    return 0


def is_goal(state):
    for item in Crafting['Goal']:
        if item not in state or state[item] < 1:
            return False
    return True


def search(graph, initial, is_goal, limit, heuristic):
    return total_cost, plan
