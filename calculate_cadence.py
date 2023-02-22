STRIDE_LENGTH = 61.42
speed = float(input("How fast would you like to go [mph]: "))
cadence = float((speed / (STRIDE_LENGTH/12))*100)
print(cadence)
