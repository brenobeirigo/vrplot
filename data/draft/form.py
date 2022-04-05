current_sol_cost = 20

# Random costs sampled from normal distribution
# mean = current solution and std = 10
candidate_sol_costs = np.random.normal(current_sol_cost, 10, 10000)
candidate_sol_costs = candidate_sol_costs[candidate_sol_costs >=0]

# Temperature params
params = [0.1, 0.2, 0.5, 1]
prob_next_costs = dict()

for p in params:
    prob_next_costs[p] =  [get_prob_acceptance(current_sol_cost, n, p*current_sol_cost) for n in candidate_sol_costs]

for p in params:
    plt.scatter(candidate_sol_costs, prob_next_costs[p], s=1, label=f"$T={p:3.2f}*Z_c$")

plt.axvline(current_sol_cost, color='k', linewidth=1, label="Current solution", linestyle="--")

plt.xlabel("Cost candidate solution")
plt.ylabel("Probabity of acceptance")
plt.title("Probability of acceptance of candidate solutions \naccording to parameter $T$")
plt.yscale("log")
_ = plt.legend(bbox_to_anchor=(1.04, 0.5), loc="center left", frameon=False)