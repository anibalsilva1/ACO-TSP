import numpy as np



def transition_prob(pheromones,alpha,beta,city_i,city_j,tabu_list,points):
    allowed_cities = tabu_list

    numerator    = (visibility(city_i,city_j,points))**beta * (pheromones[city_i,city_j]) ** alpha
    denominator  = np.sum([pheromones[city_i,city_k]**alpha * visibility(city_i,city_k,points)**beta for city_k in allowed_cities])
    
    return numerator/denominator




def length(tabu_list,points):
    cities = tabu_list
    n_cities = len(cities)
    if n_cities <= 1:
        return 0
    else:
        i = 0
        dist = 0
        while i < n_cities-1:
            dist += distance(cities[i],cities[i+1],points)
            i +=1
        return dist


def distance(city_i,city_j,points):
    return np.sqrt((points[city_i][1]-points[city_j][1])**2 + (points[city_i][2]-points[city_j][2])**2)

def visibility(city_i,city_j,points):
    return 1/distance(city_i,city_j,points)


def ant_pheromone(Q,tabu_list,points):
    cities = tabu_list
    return Q / length(cities,points)