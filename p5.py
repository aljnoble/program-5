import json
from collections import namedtuple
from heapq import heappush, heappop

with open("crafting.json") as f:  # change to Plutonium.json for Plutonium
    Crafting = json.load(f)

Items = Crafting['Items']

minecraft = True  # change to false for Plutonium, modifies max values for heuristic


def inventory_to_tuple(d):
    return tuple((d.get(name, 0)) for i, name in enumerate(Items))


def inventory_to_frozenset(d):
    return frozenset(d.items())


def is_goal(state):
    goal = Crafting['Goal']
    goal_tuple = inventory_to_tuple(goal)
    for i in xrange(len(state)):
        if goal_tuple[i] != 0:
            if state[i] < goal_tuple[i]:
                return False
    return True


def make_checker(rule):
    # this code runs once
    # do something with rule['Consumes'] and rule['Requires']
    def check(state):
        # this code will run millions of times
        checker = True
        if rule.get('Requires') is not None:
            requires = inventory_to_tuple(rule['Requires'])
            for i in xrange(len(state)):
                if requires[i] != 0:
                    if requires[i] > state[i]:
                        # requires more than we have
                        return False
                    else:
                        checker = True
        if rule.get('Consumes') is not None:
            consumes = inventory_to_tuple(rule['Consumes'])
            for i in xrange(len(state)):
                if consumes[i] != 0:
                    if consumes[i] > state[i]:
                        # consumes more than we have
                        return False
                    else:
                        checker = True
        return checker

    return check


def make_effector(rule):
    # this code runs once
    # do something with rule['Produces'] and rule['Consumes']
    def effect(state):
        # this code will run millions of times
        produces = inventory_to_tuple(rule['Produces'])
        if rule.get('Consumes') is not None:
            consumes = inventory_to_tuple(rule['Consumes'])
            # subtract consumes
            temp = tuple(state[i] - consumes[i] for i, amount in enumerate(state))
            # add in produces
            result_state = tuple(temp[i] + produces[i] for i, amount in enumerate(state))
        else:
            # does not consume, add in produces
            result_state = tuple(state[i] + produces[i] for i, amount in enumerate(state))
        return result_state

    return effect


def graph(state):
    for r in all_recipes:
        if r.check(state):
            yield (r.name, r.effect(state), r.cost)


def heuristic(state, next_state):
    new_item = False
    cost = 0
    for i in xrange(len(state)):
        if state[i] == 0 and next_state[i] > 0:
            # new item crafted
            new_item = True
        if next_state[i] > limit:  # over limit
            cost += float('inf')  # infinity
        if next_state[i] > max_items[i]:
            cost += float('inf')  # check max values of all items
    if not new_item:  # else
        cost += 1
    return cost


def search(graph, initial, is_goal, limit, heuristic):
    init_tuple = inventory_to_tuple(initial)
    dist = {}
    prev = {}
    steps = {}
    queue = []
    steps[init_tuple] = (0, 'start', init_tuple)
    dist[init_tuple] = 0.0
    prev[init_tuple] = None
    tentative = 0.0
    priortiy = 0.0
    heappush(queue, (0, 0, init_tuple))
    plan = []

    while queue:
        prio, cost, state = heappop(queue)
        if is_goal(state):
            break
        for next_action, next_state, next_cost in graph(state):
            tentative = dist[state] + next_cost
            if next_state not in dist or tentative < dist[next_state]:
                dist[next_state] = tentative
                total_cost = tentative
                priority = tentative + heuristic(state, next_state)
                prev[next_state] = state
                # add actions to steps to construct path
                steps[next_state] = (next_cost, next_action, next_state)
                heappush(queue, (priority, total_cost, next_state))

    node = state
    length = 0
    while node is not None:
        plan.append(steps[node])
        node = prev[node]
        length += 1
    plan.reverse()
    return cost, plan, length - 1


Recipe = namedtuple('Recipe', ['name', 'check', 'effect', 'cost'])
all_recipes = []
for name, rule in Crafting['Recipes'].items():
    checker = make_checker(rule)
    effector = make_effector(rule)
    recipe = Recipe(name, checker, effector, rule['Time'])
    all_recipes.append(recipe)

limit = 80
initial = Crafting['Initial']
if minecraft:
    max_items = (1, 1, 1, 8, 1, 6, 1, 1, 1, 4, 32, 4, 1, 1, 1, 1, 1)
else:
    max_items = (2, 2, 1, 1)

total_cost, path, length = search(graph, initial, is_goal, limit, heuristic)
print ("\n".join(str(p) for p in path))
print "{'total_cost': " + str(total_cost) + ", 'length': " + str(length) + "}"