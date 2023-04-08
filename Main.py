import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import math


class Point:

    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)


class Triangle:

    def __init__(self, Points, Triangles):
        self.Points = list(Points)
        self.Triangles = list(Triangles)


# def __repr__(self):
# return str((self.Points, self.Trianlgles))

def rotate(a, b, c):
    return (b.x - a.x) * (c.y - b.y) - (b.y - a.y) * (c.x - b.x)


def grahamscan(List_Point):
    n = len(List_Point)  # число точек
    index_point = list(range(n))  # список номеров точек

    for i in range(2, n):  # сортировка вставкой
        j = i
        while j > 1 and (
                rotate(List_Point[index_point[0]], List_Point[index_point[j - 1]], List_Point[index_point[j]]) < 0):
            index_point[j], index_point[j - 1] = index_point[j - 1], index_point[j]
            j -= 1
    S = [index_point[0], index_point[1]]  # создаем стек
    for i in range(2, n):
        while rotate(List_Point[S[-2]], List_Point[S[-1]], List_Point[index_point[i]]) < 0:
            del S[-1]  # pop(S)
        S.append(index_point[i])  # push(S,P[i])
    return S


def array_create_for_draw(array_def):
    All_x = list()
    All_y = list()
    for i in range(len(array_def)):
        All_x.append(array_def[i].x)
        All_y.append(array_def[i].y)
    return All_x, All_y


list_point = []  # список всех точек
list_triangle = []  # список треугольников в триангуляции


def check_point_in_triangle (A, tr_A):
    p1 = (tr_A.Points[0].x - A.x) * (tr_A.Points[1].y - tr_A.Points[0].y) - (tr_A.Points[1].x - tr_A.Points[0].x) * (tr_A.Points[0].y - A.y)
    p2 = (tr_A.Points[1].x - A.x) * (tr_A.Points[2].y - tr_A.Points[1].y) - (tr_A.Points[2].x - tr_A.Points[1].x) * (tr_A.Points[1].y - A.y)
    p3 = (tr_A.Points[2].x - A.x) * (tr_A.Points[0].y - tr_A.Points[2].y) - (tr_A.Points[0].x - tr_A.Points[2].x) * (tr_A.Points[2].y - A.y)
    if (p1 > 0 and p2 > 0 and p3 > 0) or (p1 < 0 and p2 < 0 and p3 < 0):
        return 2
    if (p1 == 0 or p2 == 0 or p3 == 0):
        return 1
    return 0


def swap_line(index_1, index_2, t_0_r, t_1_o, t_2_r, t_3_o):
    list_triangle[index_1].Points[0] = t_0_r
    list_triangle[index_1].Points[1] = t_1_o
    list_triangle[index_1].Points[2] = t_2_r
    list_triangle[index_2].Points[0] = t_0_r
    list_triangle[index_2].Points[1] = t_2_r
    list_triangle[index_2].Points[2] = t_3_o
    array_1, array_1_0 = list_triangle[index_1].Points[0], list_triangle[index_1].Points[1]
    array_3, array_3_0 = list_triangle[index_1].Points[1], list_triangle[index_1].Points[2]

    array_4, array_4_0 = list_triangle[index_2].Points[0], list_triangle[index_2].Points[2]
    array_6, array_6_0 = list_triangle[index_2].Points[1], list_triangle[index_2].Points[2]


    #array_7 = [list_triangle[index_1].Triangles[0], list_triangle[index_1].Triangles[1], list_triangle[index_1].Triangles[2]]
    #array_8 = [list_triangle[index_2].Triangles[0], list_triangle[index_2].Triangles[1], list_triangle[index_2].Triangles[2]]
    tmp7 = 0
    tmp8 = 0
    for i in range(3):
        if (list_triangle[index_2].Triangles[i] != 0):
            if array_1 in list_triangle[index_2].Triangles[i].Points and array_1_0 in list_triangle[index_2].Triangles[i].Points and list_triangle[index_2].Triangles[i] != list_triangle[index_1]:
                tmp7 = list_triangle[index_2].Triangles[i]

            if array_3 in list_triangle[index_2].Triangles[i].Points and array_3_0 in list_triangle[index_2].Triangles[i].Points and list_triangle[index_2].Triangles[i] != list_triangle[index_1]:
                tmp7 = list_triangle[index_2].Triangles[i]

        if (list_triangle[index_1].Triangles[i] != 0):
            if array_4 in list_triangle[index_1].Triangles[i].Points and array_4_0 in list_triangle[index_1].Triangles[i].Points and list_triangle[index_1].Triangles[i] != list_triangle[index_2]:
                tmp8 = list_triangle[index_1].Triangles[i]

            if array_6 in list_triangle[index_1].Triangles[i].Points and array_6_0 in list_triangle[index_1].Triangles[i].Points and list_triangle[index_1].Triangles[i] != list_triangle[index_2]:
                tmp8 = list_triangle[index_1].Triangles[i]

    if tmp7 == 0:
        list_triangle[index_2].Triangles[list_triangle[index_2].Triangles.index(0)] = tmp8
        list_triangle[index_1].Triangles[list_triangle[index_1].Triangles.index(tmp8)] = 0
        tmp8.Triangles[tmp8.Triangles.index(list_triangle[index_1])] = list_triangle[index_2]

    if tmp8 == 0:
        list_triangle[index_1].Triangles[list_triangle[index_1].Triangles.index(0)] = tmp7
        list_triangle[index_2].Triangles[list_triangle[index_2].Triangles.index(tmp7)] = 0
        tmp7.Triangles[tmp7.Triangles.index(list_triangle[index_2])] = list_triangle[index_1]

    if tmp7 != 0 and tmp8 != 0:
        for i in range(3):
            if (list_triangle[index_2].Triangles[i] == tmp7):
                for j in range(3):
                    if (list_triangle[index_1].Triangles[j] == tmp8):
                        list_triangle[index_2].Triangles[i], list_triangle[index_1].Triangles[j] = list_triangle[index_1].Triangles[j], list_triangle[index_2].Triangles[i]
                        tmp8.Triangles[tmp8.Triangles.index(list_triangle[index_1])] = list_triangle[index_2]
                        tmp7.Triangles[tmp7.Triangles.index(list_triangle[index_2])] = list_triangle[index_1]

   # list_triangle[index_1].Triangles[0] = list_triangle[index_2]
   # list_triangle[index_2].Triangles[0] = list_triangle[index_1]

   # list_triangle[index_1].Triangles[0] = list_triangle[index_2]
   # list_triangle[index_2].Triangles[0] = list_triangle[index_1]



def check_delone(A_def, B_def, index_1, index_2):
    t_0 = 0
    t_1 = 0
    t_2 = 0
    t_3 = 0
    for i in range(3):
        if A_def.Points[i] not in B_def.Points:
           t_0 = A_def.Points[i]
        else:
            if t_1 == 0:
                t_1 = A_def.Points[i]
            else:
                t_3 = A_def.Points[i]
        if B_def.Points[i] not in A_def.Points:
            t_2 = B_def.Points[i]

    cos_a = (t_1.x - t_0.x) * (t_3.x - t_0.x) + (t_1.y - t_0.y) * (t_3.y - t_0.y)
    cos_b = (t_1.x - t_2.x) * (t_3.x - t_2.x) + (t_1.y - t_2.y) * (t_3.y - t_2.y)
    if cos_a < 0 and cos_b < 0:
        swap_line(index_1, index_2, t_0, t_1, t_2, t_3)
        return
    # if (cos_a >= 0 and cos_b >= 0):
    # print("Ok")
    if (not (cos_a < 0 and cos_b < 0)) and (not (cos_a >= 0 and cos_b >= 0)):
        check_1 = (t_1.x - t_0.x) * (t_3.y - t_0.y) - (t_3.x - t_0.x) * (t_1.y - t_0.y)
        check_2 = (t_3.x - t_2.x) * (t_1.x - t_2.x) + (t_3.y - t_2.y) * (t_1.y - t_2.y)
        check_3 = (t_1.x - t_0.x) * (t_3.x - t_0.x) + (t_1.y - t_0.y) * (t_3.y - t_0.y)
        check_4 = (t_3.x - t_2.x) * (t_1.y - t_2.y) - (t_1.x - t_2.x) * (t_3.y - t_2.y)
        a = (check_1 * check_2) + (check_3 * check_4)
        if not (a < 0):
            swap_line(index_1, index_2, t_0, t_1, t_2, t_3)

y_min = float('inf')
y_max = float('-inf')

with open("input.txt") as file:
    for line in file.readlines():
        One = Point(line.split()[0], line.split()[1])
        list_point.append(One)
        if list_point[len(list_point)-1].y < y_min:
            y_min = list_point[len(list_point)-1].y
        if list_point[len(list_point)-1].y > y_max:
            y_max = list_point[len(list_point)-1].y


list_point = sorted(list_point, key=lambda k: [k.x, k.y])

x_min = list_point[0].x
x_max = list_point[len(list_point)-1].x


m = abs(((0.16 * (y_max - y_min)) * len(list_point) / (x_max - x_min))**(1/2))

#cnt_m = round(abs(((0.16 * (y_max - y_min)) * len(list_point) / (x_max - x_min))**(1/2)))

index_MVO = grahamscan(list_point)
MVO = list()
Other_point = list()

for i in range(len(index_MVO)):
    MVO.append(list_point[index_MVO[i]])

for i in range(len(list_point)):
    if i not in index_MVO:
        Other_point.append(list_point[i])
    print(list_point[i].x, list_point[i].y)



print("-------------")
for i in range(len(MVO)):
    print(MVO[i].x, MVO[i].y)
MVO.append(MVO[0])

MVO_x = list()
MVO_y = list()

# All_x = list()
# All_y = list()
# for i in range (len(list_point)):
# All_x.append(list_point[i].x)
# All_y.append(list_point[i].y)

X, Y = array_create_for_draw(MVO)
# Y = All_y

# plt.plot(X, Y, 'bo')
# fig = plt.figure()
# figure.clf() # затереть старые графики
# ax = fig.add_subplot(1, 1, 1)
# ax.clear()
# ax.plot(X, Y)
plt.plot(X, Y)

for i in range(len(MVO) - 1):
    if (len(Other_point) != 0):
        A = MVO[i]
        B = Other_point[0]
        C = MVO[i + 1]
    else:
        A = MVO[i]
        B = MVO[len(MVO)-2]
        C = MVO[i+1]
    Points_triangle = [A, B, C]
    Adjacent_triangles = [0] * 3
    if i != 0:
        Adjacent_triangles[0] = list_triangle[i - 1]
    New_triangle = Triangle(Points_triangle, Adjacent_triangles)
    list_triangle.append(New_triangle)
    if i != 0:
        list_triangle[i - 1].Triangles[2] = list_triangle[i]
    if (B == MVO[len(MVO)-2] and i == len(MVO) - 4):
        break
    if (i == len(MVO) - 2 and list_triangle[i].Triangles[0] != list_triangle[0]):
        list_triangle[i].Triangles[2] = list_triangle[0]


    # X2, Y2 = array_create_for_draw(Points_triangle)
    # plt.plot(X2, Y2)
if B != MVO[len(MVO)-2]:
    list_triangle[0].Triangles[0] = list_triangle[len(list_triangle) - 1]
# ax.plot(X, Y)
# anim = animation.FuncAnimation()
# animate = animation.FuncAnimation(fig, anim, interval=1000)


cash = [[0] * 2] * 2
for i in range(2):
    for j in range(2):
        cash[i][j] = list_triangle[0]

# проверка Делоне по всем построенным треугольникам
for i in range(len(list_triangle)):
    for j in range(3):
        if list_triangle[i].Triangles[j] != 0:
            check_delone(list_triangle[i], list_triangle[i].Triangles[j], i, list_triangle.index(list_triangle[i].Triangles[j]))
        #if list_triangle[i].Triangles[1] != 0:
          #  check_delone(list_triangle[i], list_triangle[i].Triangles[1], i, list_triangle.index(list_triangle[i].Triangles[1]))
      #  if list_triangle[i].Triangles[2] != 0:
           # check_delone(list_triangle[i], list_triangle[i].Triangles[2], i, list_triangle.index(list_triangle[i].Triangles[2]))


#check_delone(list_triangle[0], list_triangle[len(list_triangle) - 1], 0, len(list_triangle) - 1)


i = 1
triangle_for_check = list_triangle[0]
a = math.ceil(m)
bc = (x_max - x_min) / math.ceil(m)
if math.ceil(m) == 1:
    m+=1
for cnt in range(math.ceil(m)):
    array_for_y = list()
    while (i < len(Other_point) and Other_point[i].x < x_min + bc * (cnt+1)):
        #cnt_x_m = m*(i+1)

        array_for_y.append(Other_point[i])
        i+=1

    if cnt / 2 != 0 and len(array_for_y) != 0   :
        array_for_y.sort(key=lambda k: [k.y, k.x], reverse=True)

    for j in range(len(array_for_y)):
        result = check_point_in_triangle(array_for_y[j], triangle_for_check)
        k = -1
        while (result != 2):
            k+=1
            if (triangle_for_check.Triangles[k] != 0):
                result = check_point_in_triangle(array_for_y[j], triangle_for_check.Triangles[k])

            if k == 2:
                k = -1
                triangle_for_check = triangle_for_check.Triangles[0]



for i in range(len(list_triangle)):
    X2, Y2 = array_create_for_draw(list_triangle[i].Points)
    plt.plot(X2, Y2)

# проверка Делоне для последнего и первого треугольника
# check_delone(list_triangle[len(list_triangle) - 1], list_triangle[0], len(list_triangle) - 1, 0)

X3, Y3 = array_create_for_draw(list_triangle[len(list_triangle) - 1].Points)
plt.plot(X3, Y3)
X4, Y4 = array_create_for_draw(list_triangle[0].Points)
plt.plot(X4, Y4)

# Triangle_X, Triangle_Y = array_create_for_draw(list_triangle)
# plt.plot(Triangle_X, Triangle_Y)
plt.show()
