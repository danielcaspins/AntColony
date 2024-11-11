import turtle
import random
import numpy as np

NUM_OF_CITIES = 10
NUM_OF_ANTS = NUM_OF_CITIES
ALPHA = 1.000
BETA = 4.000


"""
TODO:
remeber that the starting node automatically counted as visited

good luck (: be strong

"""
colors = ["red", "blue", "green", "yellow", "purple", "orange", "pink", "brown", "black", "gray"]




def main():
    cities = create_cities()



    route = []

    for i in range(NUM_OF_CITIES - 1):
        route.append({"pheramone": 0.5, "desire": 0, "proximity": 0, "distance" : 0 , "color" : colors[i + 1], "visited": False}) 

    ant(cities, route)

    turtle.exitonclick()





    
def create_cities():
    list_cities = []
    turtle.speed(1000)
    turtle.hideturtle()
    for i in range(NUM_OF_CITIES):
        x = random.randint(-turtle.window_width() // 2, turtle.window_width() // 2)
        y = random.randint(-turtle.window_height() // 2, turtle.window_height() // 2)
        list_cities.append([x,y, False])
        turtle.pencolor(colors[i])
        turtle.goto(x, y)
        turtle.circle(3)
        turtle.width(2)

    return list_cities





def desires(current_point, locations, route):

    limiter = ((turtle.window_width() // 2)**2 + (turtle.window_height() // 2)**2)**0.5
    bg = 100000000
    bi = 0
    distances = []
    for i in range(NUM_OF_CITIES):
        if(locations[i][2]):
            distances.append(0)
            continue

        
        distance = calc_distance(locations[current_point], locations[i])
        distances.append(distance)


    for i in range(1 , NUM_OF_CITIES):
        if(distances[i] == 0):
            continue

        if(min(bg, distances[i]) != bg):
            bi = i - 1
            bg = min(bg, distances[i])
        cr_line = route[i - 1]
        cr_line["distance"] = distances[i]
        proximity = (limiter / 2) / distances[i]  
        cr_line["proximity"] = proximity
        desire = (cr_line["pheramone"]**ALPHA * proximity**BETA)
        cr_line["desire"] = desire


    print(f"closet to {route[current_point - 1]["color"]} is {route[bi]["color"]}")
    


        


def probability(route):


    probabilities = []
    desire_of_all = 0
    for i in range(len(route)):
        if(route[i]["visited"]):
            continue
        desire_of_all += route[i]["desire"]
    

    for line in route:
        if(line["visited"]):
            probabilities.append(0)
            continue
        probabilities.append(line["desire"] / desire_of_all)

    return probabilities




def ant(locations, route):
    ant_route = []
    chosen_point = 0
    locations[chosen_point][2] = True
    for i in range(NUM_OF_CITIES - 1):
        
        desires(chosen_point, locations, route)
        p = probability(route)
        chosen_point = get_a_prob(p)
        #route.pop(chosen_point)
        route[chosen_point]["visited"] = True

        print(f"max p: {max(p)} the chosen p: {p[chosen_point]}")
        ant_route.append(route[chosen_point])
        print(route[chosen_point]["color"])
        chosen_point += 1
        locations[chosen_point][2] = True


        


def get_a_prob(probabilities):
    cumulative_probabilities = np.cumsum(probabilities)
    random_value = random.random()
    for i, cumulative in enumerate(cumulative_probabilities):
        if random_value <= cumulative:
            chosen_probability = probabilities[i]
            return i








def calc_distance(point1, point2):
    return ((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)**0.5






if(__name__ == "__main__"):
    main()