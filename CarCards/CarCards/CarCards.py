from ast import For

E2 = ["E2", "Ford Escort WRC", 220, (220, 299), 6250, 5.6, 1993, 4]
H3 = ["H3", "Honda Integra Typ R", 235, (145, 198), 6500, 5.5, 1800, 4]
C2 = ["C2", "Opel Astra GSi", 235, (235, 320), 6200, 5.6, 2962, 4]
D2 = ["D2", "Toyota Celica GT-Four", 245, (220, 299), 5600, 5.3, 1998, 4]
D1 = ["D1", "Mitsubishi Lancer RS", 220, (219, 300), 6200, 5.9, 1997, 4]
E3 = ["E3", "Skoda Octavia WRC", 230, (221, 300), 7500, 5.3, 2000, 4]
B2 = ["B2", "Opel Kadett 4x4", 225, (221, 300), 8600, 6.5, 1980, 4]
B1 = ["B1", "VW Golf Kit-Car", 220, (191, 260), 8000, 6.2, 1998, 4]
C1 = ["C1", "Subaru Impreza WRC", 220, (221, 300), 5500, 5.4, 1994, 4]
A4 = ["A4", "Suzuki Ignis", 180, (153, 206), 7250, 8.0, 1597, 4]

cars = [E2, H3, C2, D2, D1, E3, B2, B1, C1, A4]

def print_car(c):
    print(c[0] + " Car model: " + c[1])
    print("Top Speed: " + str(c[2]) + "km/h" + "   Rpm: " + str(c[4]))
    print("HP: " + str(c[3]) + "     0-60: " + str(c[5]) + "s")
    print("CCs: " + str(c[6]) + "      Cylinders: " + str(c[7]))

num = input("Input car code: ")
found = False
for c in cars:
    if c[0] == num:
        print_car(c)
        found = True
        break

if not found:
    print("Car code not found.")