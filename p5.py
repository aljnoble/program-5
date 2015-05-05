import json


with open('Crafting.json') as f:
    Crafting = json.load(f)


def inventory_to_tuple(d):
    return tuple(d.get(items, 0) for i, items in enumerate(Items))


def inventory_to_set(d):
    return frozenset(d.items())


def heuristic(state):
    # heuristics needed

    return 0


def make_checker(rule):
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
        return next_state

    return check


def graph(state):
    for r in all_recipes:
        if r.check(state):
            yield (r.name, r.effect(state), r.cost)


t_initial = 'a'
t_limit = 20

edges = {'a': {'b': 1, 'c': 10}, 'b': {'c': 1}}


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


def make_goal_checker(goal):


# this code runs once


def is_goal(state):
    # this code runs millions of times
    return True  # or False

    return is_goal


is_goal = make_goal_checker(Crafting['Goal'])


def make_checker(rule):
    def check(state):
        return True  # or False


def make_effector(rule):
    def effect(state):
        return next_state


def graph(state):
    for r in all_recipes:
        if r.check(state):
            yield (r.name, r.effect(state), r.cost)


def heuristic(state):
    return 0  # or something more accurate


initial_state = make_initial_state(Crafting['Initial'])

__author__ = 'Alec'
