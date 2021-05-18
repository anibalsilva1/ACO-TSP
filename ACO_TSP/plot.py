import matplotlib.pyplot as plt

def plot_path(points,cities):
    
    city_x = points[:,1]
    city_y = points[:,2]
    # Reshape the coordinates with the repective ordered tour
    city_x = city_x[cities]
    city_y = city_y[cities]

    plt.scatter(city_x,city_y)
    plt.plot(city_x,city_y,"-o")
    for x,y,city in zip(city_x,city_y,cities):
        label = "{}".format(city)
        plt.annotate(label,(x,y), ha="center",textcoords="offset points",xytext=(0,10))
    plt.show()