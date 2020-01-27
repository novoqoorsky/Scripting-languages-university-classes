from balancing.balancer import Balancer


def run_tests():
    balancer = Balancer(logging=False)
    print_failed = True
    equations_read = 0
    equations_balanced_correctly = 0
    for line in open('test_data.txt', 'r').readlines():
        equation, flag = line.split(";")
        if flag == "True\n":
            can_be_balanced = True
        else:
            can_be_balanced = False
        result = balancer.balance_equation(equation)
        equations_read += 1
        equations_balanced_correctly += int(result == can_be_balanced)
        if result != can_be_balanced and print_failed:
            print("*** Failed: ", equation, " ***")
    print("Equations read: ", equations_read)
    print("Equation balanced correctly: ", equations_balanced_correctly)
    print("Success rate: ", (equations_balanced_correctly / equations_read) * 100, "%")


run_tests()
