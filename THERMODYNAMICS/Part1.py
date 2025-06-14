# input values
# part1
# p1 = float(input("enter P1:"))
# p2 = float(input("enter P2:"))
# m1 = float(input("enter m1:"))
# m2 = float(input("enter m2:"))
# t = float(input("enter t:"))
# pi = float(input("enter pi:"))
# ai = float(input("enter ai:"))
# af = float(input("enter af:"))

value = []
f = open("inputset_1.txt", "r")
for x in f:
    value.append(float(x))
f.close()
p1 = value[0]
p2 = value[1]
m1 = value[2]
m2 = value[3]
t =value[4]
pi = value[5]
ai = value[6]
af = value[7]


# linear interpolation
def linear_interpolation(x, x0, y0, x1, y1):
    return y0 + (x - x0)*(y1 - y0)/(x1 - x0)


# steam table

vsat_g = [[700, 0.273],[750, 0.255], [800, 0.24], [850, 0.229], [900, 0.215]
         , [950, 0.204], [1000, 0.194]]
Usat_f = [[700, 696.33],[750, 708.475], [800, 720.02], [850, 731.065], [900, 741.61]
         , [950, 751.755], [1000, 761.5]]
Usat_g = [[700, 2570.9],[750, 2573.75], [800, 2576], [850, 2575.35], [900, 2578.5]
         , [950, 2580.2], [1000, 2582]]
Hsat_f = [[700, 697.1],[750, 709.3], [800, 720.9], [850, 732], [900, 742.6]
         , [950, 752.8], [1000, 762.6]]
Hsat_g = [[700, 2762],[750, 2765], [800, 2768], [850, 2770], [900, 2772]
         , [950, 2774], [1000, 2776]]
vsat_f = [[700, 0.0011],[750, 0.0011], [800, 0.0011], [850, 0.0011], [900, 0.0011]
         , [950, 0.0011], [1000, 0.0011]]



# finding value of sat prop at diff p
def find(arr, p):
    for i in range(len(arr)):
        if(arr[i][0] == p):
                return arr[i][1]
        if(p>arr[i][0] and p < arr[i+1][0]):
            x0 = arr[i][0]
            y0 = arr[i][1]
            x1 = arr[i+1][0]
            y1 = arr[i+1][1]
            ans = linear_interpolation(p, x0, y0, x1, y1)
            return ans


        

def g_1(p, a): 
    v_f = find(vsat_f, p)
    v_g = find(vsat_g, p)
    ans = (a/v_f) + ((1 - a)/v_g)
    
    return ans

def g_2(p, a):
    v_f = find(vsat_f, p)
    v_g = find(vsat_g, p)
    U_f = find(Usat_f, p)
    U_g = find(Usat_g, p)
    
    ans = (a * U_f/v_f) + ((1 - a)* U_g/v_g)
    
    return ans

# value of a
def A(m1, m2, t):
    return (m1 - m2) * t
a = A(m1, m2, t)

# value of b
def B(m1, m2, t, p1, p2):
    return (m1 * find(Hsat_g, p1) - m2 * find(Hsat_g, p2)) * t
b = B(m1, m2, t, p1, p2)



# equation to solve
def equation(pf):
    ans = (g_2(pf, af) - g_2(pi, ai))*a - (g_1(pf, af) - g_1(pi, ai))*b
    return ans

# bisection method
def bisection(equation, start, end, MAX_iter):
    count = 0
    while(count <= MAX_iter and start <= end):
        mid = (start + end)/2
        val = equation(mid)
        if(val == 0):
            return mid
        else:
            if(val * equation(start) > 0):
                start = mid
            else:
                end = mid
        count += 1
    if(abs(val) < 1e-6):
        return mid
    else:
        return "no sol"
    
    
# start value, end value and result
start = p2 + 100
end = p1 - 50
MAX_iter = 1000
mid = (start + end)/2


# function to find Vacc
pf = bisection(equation, start, end, MAX_iter)
if pf == 'no sol':
    print('no solution')
else:
    Vacc = A(m1, m2, t)/(g_1(pf, af) - g_1(pi, ai))
    print("Pf = " + str(pf) + " kPa")
    print("Vacc = " + str(abs(Vacc)) + " m^3" )

