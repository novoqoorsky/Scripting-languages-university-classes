from balancing.balancer import Balancer


def main():
    balancer = Balancer(logging=True)
    print("Hello! Enter a chemical equation in below format and I'll try to balance it for you!")
    print("H2 + O2 -> H2O")
    print("\nIf you wish to end the program, just type: exit")
    while True:
        equation = input("Type the equation here: ")
        if equation == "exit":
            print("Thank you! See you soon!")
            break
        balancer.balance_equation(equation)


main()
