weight = input("Enter the weight of the potatoe in grams: ")
if weight < 100:
    print("The potatoe is small.")
elif weight >= 100 and weight <= 200:
    print("The potatoe is medium.")
elif weight > 200 and weight <= 300:
    print("The potatoe is large.")



blemish_counts = []
for i in range(5):
    count = input("Enter the number of blemishes on the potatoe: ")
    blemish_counts.append(count)
total = sum(blemish_counts)
average = total / len(blemish_counts)
print("Total: ", total)
print("The average number of blemishes on each potatoe is: ", average)

all_potatoes =[0,2,5,1,0,8,3,0]
perfect_potatoes = []
for p in all_potatoes:
    if p == 0:
        perfect_potatoes.append(p)
    else:
        continue
num_total = len(all_potatoes)
num_perfect = len(perfect_potatoes)
percentage = (num_perfect / num_total) * 100
print(f"Batch Quality: {percentage}% perfect potatoes.")