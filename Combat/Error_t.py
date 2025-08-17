def get_integer(prompt):
    while True:
        try:
            n = int(input(prompt))
            return n
        except ValueError:
            print("Must be an integer")
