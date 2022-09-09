#Made by Sven Leidenbach
priors = [0.3333, 0.3333, 0.3333]

tech = [0.00518134, 0.00384615, 0.03975535]
car = [0.00518134, 0.07307692, 0.051987767]
lab = [0.010362694, 0.0038461538, 0.045871559]
probs = [tech, car, lab]


def priors_1(priors_input, list1):
    post_1 = [a*b for a, b in zip(priors_input, list1)] 
    post_1_1 = (post_1[0]) / (post_1[0] + post_1[1] + post_1[2])
    post_1_2 = (post_1[1]) / (post_1[0] + post_1[1] + post_1[2])
    post_1_3 = (post_1[2]) / (post_1[0] + post_1[1] + post_1[2])
    return post_1_1, post_1_2, post_1_3


tech_prior = priors_1(priors, tech)
tech_tech = priors_1(tech_prior, tech)
tech_tech_car = priors_1(tech_tech, car)
tech_tech_car_lab = priors_1(tech_tech_car, lab)
print(tech_tech_car_lab)


