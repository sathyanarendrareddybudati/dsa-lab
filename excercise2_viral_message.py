import random

def is_within_budget(selection, costs, budget):
    return sum(costs[i] for i in selection) <= budget


def maximize_reach_exact(budget, costs, reaches):
    n  = len(costs)
    dp = [[0] * (budget + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        for b in range(budget + 1):
            dp[i][b] = dp[i-1][b]
            if costs[i-1] <= b:
                with_i = dp[i-1][b - costs[i-1]] + reaches[i-1]
                if with_i > dp[i][b]:
                    dp[i][b] = with_i

    selected = []
    b = budget
    for i in range(n, 0, -1):
        if dp[i][b] != dp[i-1][b]:
            selected.append(i - 1)
            b -= costs[i - 1]

    return (dp[n][budget], list(reversed(selected)))


def maximize_reach_greedy(budget, costs, reaches):
    n      = len(costs)
    ratios = sorted(
        [(reaches[i] / costs[i], i) for i in range(n) if costs[i] > 0],
        reverse=True
    )

    total_cost  = 0
    total_reach = 0
    selected    = []

    for _, i in ratios:
        if total_cost + costs[i] <= budget:
            selected.append(i)
            total_cost  += costs[i]
            total_reach += reaches[i]

    return (total_reach, selected)


if __name__ == "__main__":

    print("=" * 55)
    print("BASIC EXAMPLE")
    print("=" * 55)
    costs   = [3, 4, 2, 5, 1]
    reaches = [4, 5, 3, 7, 2]
    budget  = 8

    dp_reach,  dp_sel  = maximize_reach_exact(budget, costs, reaches)
    gr_reach,  gr_sel  = maximize_reach_greedy(budget, costs, reaches)

    print(f"  Budget          : {budget}")
    print(f"  DP   → reach={dp_reach}, users={dp_sel}, cost={sum(costs[i] for i in dp_sel)}")
    print(f"  Greedy → reach={gr_reach}, users={gr_sel}, cost={sum(costs[i] for i in gr_sel)}")
    print(f"  DP valid    : {is_within_budget(dp_sel, costs, budget)}")
    print(f"  Greedy valid: {is_within_budget(gr_sel, costs, budget)}")


    print()
    print("=" * 55)
    print("GREEDY COUNTEREXAMPLE")
    print("=" * 55)
    c_costs   = [6, 5, 5]
    c_reaches = [8, 5, 5]
    c_budget  = 10

    dp_r,  dp_s  = maximize_reach_exact(c_budget, c_costs, c_reaches)
    gr_r,  gr_s  = maximize_reach_greedy(c_budget, c_costs, c_reaches)

    print(f"  Users: A(cost=6,reach=8), B(cost=5,reach=5), C(cost=5,reach=5)")
    print(f"  Budget = {c_budget}")
    print(f"  DP     → reach={dp_r}, users={dp_s}")
    print(f"  Greedy → reach={gr_r}, users={gr_s}")
    print(f"  {'Greedy is suboptimal here ✓' if gr_r < dp_r else 'Same result'}")

    print()
    print("=" * 55)
    print("EDGE CASES")
    print("=" * 55)

    r0, s0 = maximize_reach_exact(0, costs, reaches)
    print(f"  Budget=0       → reach={r0}, users={s0}")

    r_all, s_all = maximize_reach_exact(999, costs, reaches)
    print(f"  Budget=999     → reach={r_all}, users={s_all}")

    r1, s1 = maximize_reach_exact(3, [3], [10])
    print(f"  Single user cost=3 reach=10, budget=3 → reach={r1}")  # 10

    r2, s2 = maximize_reach_exact(2, [3], [10])
    print(f"  Single user cost=3 reach=10, budget=2 → reach={r2}")  # 0

    print()
    print("=" * 55)
    print("SIMULATION: 20 users, budget=50")
    print("=" * 55)
    random.seed(42)
    n          = 20
    sim_costs  = [random.randint(1, 15) for _ in range(n)]
    sim_reaches = [random.randint(5, 50) for _ in range(n)]
    sim_budget = 50

    dp_r,  dp_s  = maximize_reach_exact(sim_budget, sim_costs, sim_reaches)
    gr_r,  gr_s  = maximize_reach_greedy(sim_budget, sim_costs, sim_reaches)

    print(f"  DP     → reach={dp_r}, {len(dp_s)} users, cost={sum(sim_costs[i] for i in dp_s)}/{sim_budget}")
    print(f"  Greedy → reach={gr_r}, {len(gr_s)} users, cost={sum(sim_costs[i] for i in gr_s)}/{sim_budget}")
    print(f"  DP improvement over greedy: +{dp_r - gr_r}")