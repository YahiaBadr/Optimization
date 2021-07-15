import numpy as np
import random

np.random.seed(5)

### parameters for generator ###

number_of_tests = 20

minimum_number_of_branches = 2
maximum_number_of_branches = 5

minimum_number_of_requests = 1
maximum_number_of_requests = 15

minimum_number_of_services = 1
maximum_number_of_services = 3

minimum_maximum_distance = 100
maximum_maximum_distance = 2000

min_no_of_slots_for_one_service = 1
max_no_of_slots_for_one_service = 2

min_no_of_counters_at_branch = 1
max_no_of_counters_at_branch = 3

min_no_of_slots_per_day = 2
max_no_of_slots_per_day = 4

# Assuming the whole area is square in shape, the diagonal is the distance from (0,0) to the farthest possible point,
# The diagonal is calculated as a ration of d for each test
ratio_of_diagonal_of_whole_area_to_d = 2

#########################################


def generate():
    ### Generate all b,r,m,d ###
    list_of_b = np.sort(
        np.random.randint(
            minimum_number_of_branches,
            maximum_number_of_branches,
            [number_of_tests]
        )
    )

    list_of_r = np.sort(
        np.random.randint(
            minimum_number_of_requests,
            maximum_number_of_requests,
            [number_of_tests]
        )
    )

    list_of_m = np.sort(
        np.random.randint(
            minimum_number_of_services,
            maximum_number_of_services,
            [number_of_tests]
        )
    )

    list_of_d = np.sort(
        np.random.randint(
            minimum_maximum_distance,
            maximum_maximum_distance,
            [number_of_tests]
        )
    )
    ##########################################

    ### Generating test by test ###
    for test_num in range(0, number_of_tests):

        path = "./small_dataset/test_" + str(test_num) + ".in"
        f = open(path, "w+")

        b = list_of_b[test_num]
        r = list_of_r[test_num]
        m = list_of_m[test_num]
        d = list_of_d[test_num]

        f.write(str(b) + " " + str(r) + " " + str(m) + " " + str(d) + " \n")

        list_of_services = list(range(0, m))
        diagonal= d * ratio_of_diagonal_of_whole_area_to_d
        # Using Pythagoras to determine the largest possible value of x and y (assuming square shaped area of the city)
        max_x = np.round(
            np.sqrt(np.square(diagonal)/2)
        ) + 1
        max_y = max_x

        for i in range(m):
            to_print = ""
            for j in range(b):
                a = np.random.randint(low=min_no_of_slots_for_one_service, high=max_no_of_slots_for_one_service)
                to_print += str(a) + " "
            f.write(to_print + "\n")

        for i in range(r):
            x = np.random.randint(low=0, high=max_x)
            y = np.random.randint(low=0, high=max_y)
            p = np.random.randint(low=1, high=r+1)
            rs = np.random.randint(low=0, high=m)
            f.write(str(x) + " " + str(y) + " " + str(p) + " " + str(rs) + " \n")


        for i in range(b):
            x = np.random.randint(low=0, high=max_x)
            y = np.random.randint(low=0, high=max_y)
            s = np.random.randint(low=min_no_of_slots_per_day, high=max_no_of_slots_per_day)
            c = np.random.randint(low=min_no_of_counters_at_branch, high=max_no_of_counters_at_branch)
            f.write(str(x) + " " + str(y) + " " + str(s) + " " + str(c) + " \n")
            for j in range(c):
                n = np.random.randint(low=1, high=m+1)
                services = random.sample(list_of_services,n)
                to_print = str(n) + " "

                for s in services:
                    to_print += str(s)+" "
                f.write(to_print+"\n")

        f.close()



if __name__ == '__main__':
    generate()