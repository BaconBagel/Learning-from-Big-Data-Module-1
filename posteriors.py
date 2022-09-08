priors = [0.3333, 0.3333, 0.3333]

tech = [0.00518, 0.0038, 0.0398]
car = [0.0052, 0.0731, 0.052]
lab = [0.0104, 0.0038, 0.0459]
probs = [tech, car, lab]


def priors_1(priors_input, list1, list2, list3):
    post_1 = [a*b for a, b in zip(priors_input, list1)] # something is wrong here!
    post_2 = [p * o for p, o in zip(priors_input, list2)]
    post_3 = [a * b for a, b in zip(priors_input, list3)]
    print(post_2)
    post_pre = [a + b + c for a, b, c in zip(post_1, post_2, post_3)]
    post_post = [a / b for a, b in zip(post_1, post_pre)]
    return post_pre


print(priors_1(priors, tech, car, lab))


