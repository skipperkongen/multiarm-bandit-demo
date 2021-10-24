import numpy as np
import pandas as pd

print('Demo')


def visit(choices, n=1):
    means = np.array([10, 8, 5])
    varis = np.array([5, 4, 3])
    return np.random.normal(means[choices], varis[choices])


choices = np.zeros(10).astype(int)
#sns.displot(visit(choices))

def cheat(visit, rounds=300):
    """
    Optimal strategy
    """
    strat = np.zeros(rounds).astype(int)
    return visit(strat)

def explore(visit, rounds=300):
    """
    100% random sample
    """
    strat = np.random.choice([0, 1, 2], size=300)
    return visit(strat)

def exploit(visit, rounds=300):
    """
    Try all options once, repeat best
    """
    head = visit([0, 1, 2], n=3)
    best = np.argmax(head)
    best
    tail_strat = (np.zeros(rounds - len(head)) + best).astype(int)
    tail = visit(tail_strat)
    return np.concatenate([head, tail])

def greedy(visit, rounds=300, eps=0.1):

    visits = np.array([])
    choices = np.array([])
    for _ in range(rounds):
        if np.random.random() < eps:
            # Explore
            choice = np.random.choice([0, 1, 2])
        else:
            # Exploit
            choice_0 = visits[choices == 0]
            choice_1 = visits[choices == 1]
            choice_2 = visits[choices == 2]
            choice = np.argmax([
                np.mean(choice_0) if len(choice_0) else -np.inf,
                np.mean(choice_1) if len(choice_1) else -np.inf,
                np.mean(choice_1) if len(choice_2) else -np.inf,
            ])
        visits = np.append(visits, visit([choice])[0])
        choices = np.append(choices, choice)
    return visits

def sim(visit, strategy, epochs=100):
    return np.concatenate([strategy(visit) for _ in range(epochs)])


print('explore', np.mean(sim(visit, explore)))
print('exploit', np.mean(sim(visit, exploit)))
print('greedy', np.mean(sim(visit, greedy)))
print('cheat', np.mean(sim(visit, cheat)))
