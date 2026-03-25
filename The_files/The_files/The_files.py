fname = "output.txt"
file = open(fname, "w")
for i in range(100):
    file.write("This is line " + str(i) + "\n")
file.close()
