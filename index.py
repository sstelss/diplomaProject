import data_formats as df
import simulated_annealing as sim
import ant_thread as ant
import gibrid_al as gb
import new_bee as nb


if __name__ == '__main__':
    # для виндоса изменить `/` на `\\`
    path = "graph/dj38.tsp.txt"
    G, points = df.ReadPointGraph(path)

    result_simul = sim.run(path, paint = 0)
    result_bee = nb.run(path, n=100, amount=1000)
    result_gib = gb.run(path, alpha=0.7, beta=1.3, gamma=0.3, count=38, t_live=100, p=0.7, Q=1)
    result_ant = ant.run(path, alpha=0.7, beta=1.3, count=38, t_live=100, e=10, p=0.7, Q=1)


    print("Bee result                  ", result_bee)
    print("Ant colony algorithm   ", result_ant)
    print("Simulated                   ", result_simul)
    print("Gibrid    ", result_gib)
