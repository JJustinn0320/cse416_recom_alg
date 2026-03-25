from gerrychain import Graph, Partition, MarkovChain, updaters, constraints, accept
from gerrychain.proposals import recom
from gerrychain.constraints import contiguous
from functools import partial
from tqdm import tqdm
import random
random.seed(2024)

# Load the graph in from the provided json file
graph = Graph.from_json("./PA_VTDs_clean.json")

# Set up updaters
my_updater = {
    "population": updaters.Tally("TOT_POP", alias="population"),
    "cut_edges": updaters.cut_edges,
}

# Set up the initial partition object
initial_partition = Partition(
    graph,
    assignment = "2011_PLA_1",
    updaters = my_updater
)

ideal_population = sum(initial_partition["population"].values()) / len(initial_partition)
# print(f"ideal population: {ideal_population}")

# create new function from the recom with our given arguments
proposal = partial(
    recom,
    pop_col="TOT_POP",
    pop_target=ideal_population,
    epsilon=0.01,
    node_repeats=2
)

num_of_ensembles = 10
ensemble_list = []

outer_bar = tqdm(range(num_of_ensembles), desc="Ensembles", position=0)
for run in outer_bar:
    cur_chain = MarkovChain(
        proposal=proposal,
        constraints=[contiguous],
        accept=accept.always_accept,
        initial_state=initial_partition,
        total_steps=50
    )

    final_partition = None
    inner_bar = tqdm(cur_chain, desc=f"  Chain {run+1}", position=1, leave=False)
    for item in inner_bar:
        final_partition = item
    
    inner_bar.close()
    
    ensemble_list.append(final_partition)

print(f"Collected {len(ensemble_list)} district plans")  