

a = [[]for i in range(2)]

for i in range(2):
        line = input().split(' ')
        for j in range(2):
            a[i].append(int(line[j]))
   
for i in range(2):
        
        for j in range(2):
            print(a[i][j])             