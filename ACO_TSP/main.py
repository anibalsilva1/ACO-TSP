import numpy as np
import pandas as pd
import random
#from aux_functions import *
from plot import plot_path
from aux_functions import transition_prob,length,visibility,ant_pheromone,distance




df = pd.read_csv("data/chn31.csv",header=None,delimiter=" ",names=["city","x","y"])
#Reshape city index and convert to numpy array
df["city"] = df["city"] - 1
points = np.array(df)
#print(points)

def main():

    '''
    :param alpha: relative importance of trail
    :param beta:  relative importance of visibility
    :param rho:   trail evaporation
    :param Q:     visibility constant
    :param NMAX:  number of tours over all the cities (AKA ant generations)
    '''

    
    ncity  = points.shape[0]
    n_ants = ncity
    
    shortest_tour = []
    ants          = np.arange(0,n_ants)
    tabu_list     = [[] for _ in range(len(ants))]
    pheromones    = np.full([ncity,ncity],0.0001)
    
    ## Parameters
    Q     = 1
    rho   = 0.2
    alpha = .8
    beta  = 0.7
    max_error = 0.05
    NMAX  = 50
    delta_pheromones = np.zeros([ncity,ncity])
    NC = 0
    
    while NC < NMAX:
        
        print("Going through the cycle: ", NC)
        allowed_cities = []
        cities = points[:,0]
        [tabu.append(random.randint(0,ncity-1)) for tabu in tabu_list]
    

        for ant in ants:

            start_city = tabu_list[ant][0]
            tabu_list_size = len(tabu_list[ant])

            while tabu_list_size < ncity:
                
                '''
                Choose the town to transit to: calculate the transition probability for 
                each pair and select the one where the probability is highest
                '''
                
                current_city = tabu_list[ant][tabu_list_size-1]
                allowed_cities = [city for city in cities if city not in tabu_list[ant]]

                probs = [(transition_prob(pheromones,alpha,beta,current_city,city_j,allowed_cities,points),city_j) for city_j in allowed_cities] # Returns a tuple with all the 
                #print(probs)
                next_city = max(probs,key=lambda item:item[0])[1]
                tabu_list[ant].append(next_city)
                tabu_list_size += 1
            
            tabu_list[ant].append(start_city) # Finally place the ant in the initial city
        tot_dist = [(length(tabu_list[ant],points),ant) for ant in ants]

        best_ant_per_cycle  = min(tot_dist, key = lambda t: t[0])[1]
        best_path_per_cycle = tabu_list[best_ant_per_cycle]
        shortest_tour.append([best_ant_per_cycle,length(best_path_per_cycle,points),best_path_per_cycle])

        print("\t Shortest tour in cycle :", NC ," was done by ant", best_ant_per_cycle, "with a tour of ", shortest_tour[NC][1], "and a path \n\t", shortest_tour[NC][2], "\n")
        error = (shortest_tour[NC][1] - shortest_tour[NC-1][1])/shortest_tour[NC][1]
        print(error)
        if error > max_error:

            '''
            Stagnation behavior: if the last tour is worse than 
            the previous one times an error factor epsilon,
            we stop the search.
            '''
            print("The last run had a tour of length ",shortest_tour[NC][1], "which is higher than the previous one: ",shortest_tour[NC-1][1], "so we are stopping")
            print("Plotting best path...")
            
            plot_path(points,shortest_tour[NC-1][2])
            break
        
        else:

            #### UPDATES BEGIN ####

            for ant in ants:
                cities = tabu_list[ant]
                for city in range(len(cities)-1):
                    delta_pheromones[cities[city],cities[city+1]] = ant_pheromone(Q,cities,points)

            pheromones = rho*pheromones + delta_pheromones

            #### UPDATES END ####
            
            if NC == NMAX - 1:
                print("Plotting best path...")
                plot_path(points,best_path_per_cycle)

        #print(best_path_per_cycle)
            delta_pheromones = np.zeros([ncity,ncity])
            [tabu.clear() for tabu in tabu_list]
            NC +=1
    #print(shortest_tour)
    #print("Plotting best path...")
    #plot_path(points,best_path_per_cycle)


if __name__ == '__main__':
    main()
