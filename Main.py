import numpy as np
import matplotlib.pyplot as plt
import math


class Point:

    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)


class Triangle:

    def __init__(self, Points, Triangles):
        self.Points = list(Points)
        self.Triangles = list(Triangles)


def rotate(a, b, c):
    return (b.x - a.x) * (c.y - b.y) - (b.y - a.y) * (c.x - b.x)


def grahamscan(List_Point):
    n = len(List_Point)  # число точек
    index_point = list(range(n))  # список номеров точек

    for i in range(2, n):
        j = i
        while j > 1 and (
                rotate(List_Point[index_point[0]], List_Point[index_point[j - 1]], List_Point[index_point[j]]) < 0):
            index_point[j], index_point[j - 1] = index_point[j - 1], index_point[j]
            j -= 1
    S = [index_point[0], index_point[1]]
    for i in range(2, n):
        while rotate(List_Point[S[-2]], List_Point[S[-1]], List_Point[index_point[i]]) < 0:
            del S[-1]
        S.append(index_point[i])
    return S


def array_create_for_draw(array_def):
    All_x = list()
    All_y = list()
    for i in range(len(array_def)):
        All_x.append(array_def[i].x)
        All_y.append(array_def[i].y)
    All_x.append(array_def[0].x)
    All_y.append(array_def[0].y)
    return All_x, All_y


list_point = []  # список всех точек
list_triangle = []  # список треугольников в триангуляции

def check_side(T, P):
    p1 = (T.Points[0].x - P.x) * (T.Points[1].y - T.Points[0].y) - (T.Points[1].x - T.Points[0].x) * (T.Points[0].y - P.y)
    p2 = (T.Points[1].x - P.x) * (T.Points[2].y - T.Points[1].y) - (T.Points[2].x - T.Points[1].x) * (T.Points[1].y - P.y)
    p3 = (T.Points[2].x - P.x) * (T.Points[0].y - T.Points[2].y) - (T.Points[0].x - T.Points[2].x) * (T.Points[2].y - P.y)
    if p1 == 0:
        return 0, 2, 1
    if p2 == 0:
        return 1, 0, 2
    if p3 == 0:
        return 0, 1, 2

def check_point_inPolygon(P, T):
    c=0
    for i in range(3):
        if (((T.Points[i].y <= P.y and P.y<T.Points[i-1].y) or (T.Points[i-1].y <= P.y and P.y < T.Points[i].y)) and
                (P.x > (T.Points[i-1].x - T.Points[i].x) * (P.y - T.Points[i].y) / (T.Points[i-1].y - T.Points[i].y) + T.Points[i].x)):
            c = 1 - c
    return c

def check_point_in_triangle (A, tr_A):
    p1 = (tr_A.Points[0].x - A.x) * (tr_A.Points[1].y - tr_A.Points[0].y) - (tr_A.Points[1].x - tr_A.Points[0].x) * (tr_A.Points[0].y - A.y)
    p2 = (tr_A.Points[1].x - A.x) * (tr_A.Points[2].y - tr_A.Points[1].y) - (tr_A.Points[2].x - tr_A.Points[1].x) * (tr_A.Points[1].y - A.y)
    p3 = (tr_A.Points[2].x - A.x) * (tr_A.Points[0].y - tr_A.Points[2].y) - (tr_A.Points[0].x - tr_A.Points[2].x) * (tr_A.Points[2].y - A.y)
    if (p1 > 0 and p2 > 0 and p3 > 0) or (p1 < 0 and p2 < 0 and p3 < 0):
        return 2
    if (p1 == 0 or p2 == 0 or p3 == 0):
        return 1
    return 0

def bulge(A, B, C, D) :
    t1 = ((D.x - A.x)*(B.y - A.y) - (D.y - A.y)*(B.x - A.x))
    t2 = ((D.x - B.x)*(C.y - B.y) - (D.y - B.y)*(C.x - B.x))
    t3 = ((D.x - C.x)*(A.y - C.y) - (D.y - C.y)*(A.x - C.x))
    t4 = ((A.x - C.x)*(B.y - C.y) - (A.y - C.y)*(B.x - C.x))
    return t1 * t2 * t3 * t4 > 0

def swap_line(A_def, B_def, t_0_r, t_1_o, t_2_r, t_3_o):
    A_def.Points[0] = t_0_r
    A_def.Points[1] = t_1_o
    A_def.Points[2] = t_2_r
    B_def.Points[0] = t_0_r
    B_def.Points[1] = t_2_r
    B_def.Points[2] = t_3_o
    array_1, array_1_0 = A_def.Points[0], A_def.Points[1]
    array_3, array_3_0 = A_def.Points[1], A_def.Points[2]

    array_4, array_4_0 = B_def.Points[0], B_def.Points[2]
    array_6, array_6_0 = B_def.Points[1], B_def.Points[2]

    tmp7 = 0
    tmp8 = 0
    for i in range(3):
        if (B_def.Triangles[i] != 0):
            if array_1 in B_def.Triangles[i].Points and array_1_0 in B_def.Triangles[i].Points and B_def.Triangles[i] != A_def:
                tmp7 = B_def.Triangles[i]

            if array_3 in B_def.Triangles[i].Points and array_3_0 in B_def.Triangles[i].Points and B_def.Triangles[i] != A_def:
                tmp7 = B_def.Triangles[i]

        if (A_def.Triangles[i] != 0):
            if array_4 in A_def.Triangles[i].Points and array_4_0 in A_def.Triangles[i].Points and A_def.Triangles[i] != B_def:
                tmp8 = A_def.Triangles[i]

            if array_6 in A_def.Triangles[i].Points and array_6_0 in A_def.Triangles[i].Points and A_def.Triangles[i] != B_def:
                tmp8 = A_def.Triangles[i]

    if tmp7 == 0 and tmp8 != 0:
        B_def.Triangles[B_def.Triangles.index(0)] = tmp8
        A_def.Triangles[A_def.Triangles.index(tmp8)] = 0
        tmp8.Triangles[tmp8.Triangles.index(A_def)] = B_def

    if tmp8 == 0 and tmp7 != 0:
        A_def.Triangles[A_def.Triangles.index(0)] = tmp7
        B_def.Triangles[B_def.Triangles.index(tmp7)] = 0
        tmp7.Triangles[tmp7.Triangles.index(B_def)] = A_def

    if tmp7 != 0 and tmp8 != 0:
        for i in range(3):
            if (B_def.Triangles[i] == tmp7):
                for j in range(3):
                    if (A_def.Triangles[j] == tmp8):
                        B_def.Triangles[i], A_def.Triangles[j] = A_def.Triangles[j], B_def.Triangles[i]
                        tmp8.Triangles[tmp8.Triangles.index(A_def)] = B_def
                        tmp7.Triangles[tmp7.Triangles.index(B_def)] = A_def


def Intersection(A, B, C, D):
    v1 = (D.x-C.x)*(A.y-C.y)-(D.y-C.y)*(A.x-C.x)
    v2 = (D.x-C.x)*(B.y-C.y)-(D.y-C.y)*(B.x-C.x)
    v3 = (B.x-A.x)*(C.y-A.y)-(B.y-A.y)*(C.x-A.x)
    v4 = (B.x-A.x)*(D.y-A.y)-(B.y-A.y)*(D.x-A.x)
    return ((v1*v2<0) and (v3*v4<0))

def judge(a,b,c,d):
    if min(a.x,b.x) <= max(c.x,d.x) and min(c.y,d.y) <= max(a.y,b.y) and min(c.x,d.x) <= max(a.x,b.x) and min(a.y,b.y) <= max(c.y,d.y):
        return True
    return False

def judge2(a,b,c,d):
    denominator = (d.y - c.y)*(a.x - b.x)-(d.x-c.x)*(a.y - b.y);

    if (denominator == 0):
        if  (a.x*b.y - b.x*a.y)*(d.x - c.x) - (c.x*d.y - d.x*c.y)*(b.x-a.x) == 0 and (a.x*b.y - b.x*a.y)*(d.y - c.y) - (c.x*d.y - d.x*c.y)*(b.y-a.y) == 0:
            return True
        else:
            return  False
    else:
        numerator_a = (d.x - b.x)*(d.y - c.y) - (d.x - c.x)*(d.y - b.y);
        numerator_b = (a.x - b.x)*(d.y - b.y) - (d.x - b.x)*(a.y - b.y);
        Ua = numerator_a/denominator;
        Ub = numerator_b/denominator;

    if (Ua >=0 and Ua <=1 and Ub >=0 and Ub <=1):
        return True
    return False



def search_triangle(A_tr2, B1, D1):
    for i in range(3):
        if (A_tr2.Triangles[i] != 0):
            if B1 in A_tr2.Triangles[i].Points and D1 in A_tr2.Triangles[i].Points:
                return i
    return -1

def triangle_center(A):
    return Point((A.Points[0].x + A.Points[1].x + A.Points[2].x) / 3, (A.Points[0].y + A.Points[1].y + A.Points[2].y) / 3)

def add_point_into_triangle(A_tr_, P):
    points_for_1 = [P, A_tr_.Points[0], A_tr_.Points[1]]
    points_for_2 = [P, A_tr_.Points[1], A_tr_.Points[2]]
    points_for_3 = [P, A_tr_.Points[0], A_tr_.Points[2]]

    t1 = search_triangle(A_tr_, A_tr_.Points[0], A_tr_.Points[1])
    triangle_for_1 = [A_tr_.Triangles[t1], 0, 0] if t1 != -1 else [0, 0, 0]

    t2 = search_triangle(A_tr_, A_tr_.Points[1], A_tr_.Points[2])
    triangle_for_2 = [A_tr_.Triangles[t2], 0, 0] if t2 != -1 else [0, 0, 0]

    t3 = search_triangle(A_tr_, A_tr_.Points[0], A_tr_.Points[2])
    triangle_for_3 = [A_tr_.Triangles[t3], 0, 0] if t3 != -1 else [0, 0, 0]

    A1 = Triangle(points_for_1, triangle_for_1)
    A2 = Triangle(points_for_2, triangle_for_2)
    A3 = Triangle(points_for_3, triangle_for_3)

    if t1 != -1:
        S1 = A_tr_.Triangles[t1]
        S1.Triangles[search_triangle(S1, A_tr_.Points[0], A_tr_.Points[1])] = A1

    if t2 != -1:
        S1 = A_tr_.Triangles[t2]
        S1.Triangles[search_triangle(S1, A_tr_.Points[1], A_tr_.Points[2])] = A2

    if t3 != -1:
        S1 = A_tr_.Triangles[t3]
        S1.Triangles[search_triangle(S1, A_tr_.Points[0], A_tr_.Points[2])] = A3

    A1.Triangles[1] = A2
    A1.Triangles[2] = A3
    A2.Triangles[1] = A1
    A2.Triangles[2] = A3
    A3.Triangles[1] = A1
    A3.Triangles[2] = A2

    list_triangle.remove(A_tr_)
    list_triangle.append(A1)
    list_triangle.append(A2)
    list_triangle.append(A3)

    if t1 != -1:
        check_delone(A1, A1.Triangles[0])
    if t2 != -1:
        check_delone(A2, A2.Triangles[0])
    if t3 != -1:
        check_delone(A3, A3.Triangles[0])

    return A1

def add_point_into_side(A_tr_, P):
    first_ind, sec_ind, third_ind = check_side(A_tr_, P)

    points_for_1 = [P, A_tr_.Points[first_ind], A_tr_.Points[sec_ind]]
    points_for_2 = [P, A_tr_.Points[sec_ind], A_tr_.Points[third_ind]]
    ind_3 = search_triangle(A_tr_, A_tr_.Points[first_ind], A_tr_.Points[third_ind])
    ind_1, ind_2, ind_5 = check_side(A_tr_.Triangles[ind_3], P)
    points_for_3 = [P, A_tr_.Triangles[ind_3].Points[ind_1], A_tr_.Triangles[ind_3].Points[ind_2]]
    points_for_4 = [P, A_tr_.Triangles[ind_3].Points[ind_5], A_tr_.Triangles[ind_3].Points[ind_2]]

    t1 = search_triangle(A_tr_, A_tr_.Points[first_ind], A_tr_.Points[sec_ind])
    triangle_for_1 = [A_tr_.Triangles[t1], 0, 0] if t1 != -1 else [0, 0, 0]

    t2 = search_triangle(A_tr_, A_tr_.Points[sec_ind], A_tr_.Points[third_ind])
    triangle_for_2 = [A_tr_.Triangles[t2], 0, 0] if t2 != -1 else [0, 0, 0]

    t3 = search_triangle(A_tr_.Triangles[ind_3], A_tr_.Triangles[ind_3].Points[ind_1], A_tr_.Triangles[ind_3].Points[ind_2])
    triangle_for_3 = [A_tr_.Triangles[ind_3].Triangles[t3], 0, 0] if t3 != -1 else [0, 0, 0]

    t4 = search_triangle(A_tr_.Triangles[ind_3], A_tr_.Triangles[ind_3].Points[ind_5], A_tr_.Triangles[ind_3].Points[ind_2])
    triangle_for_4 = [A_tr_.Triangles[ind_3].Triangles[t4], 0, 0] if t4 != -1 else [0, 0, 0]

    A1 = Triangle(points_for_1, triangle_for_1)
    A2 = Triangle(points_for_2, triangle_for_2)
    A3 = Triangle(points_for_3, triangle_for_3)
    A4 = Triangle(points_for_4, triangle_for_4)

    if t1 != -1:
        S1 = A_tr_.Triangles[t1]
        S1.Triangles[search_triangle(S1, A_tr_.Points[first_ind], A_tr_.Points[sec_ind])] = A1

    if t2 != -1:
        S1 = A_tr_.Triangles[t2]
        S1.Triangles[search_triangle(S1, A_tr_.Points[sec_ind], A_tr_.Points[third_ind])] = A2

    if t3 != -1:
        S1 = A_tr_.Triangles[ind_3].Triangles[t3]
        S1.Triangles[search_triangle(S1, A_tr_.Triangles[ind_3].Points[ind_1], A_tr_.Triangles[ind_3].Points[ind_2])] = A3

    if t4 != -1:
        S1 = A_tr_.Triangles[ind_3].Triangles[t4]
        S1.Triangles[search_triangle(S1, A_tr_.Triangles[ind_3].Points[ind_5], A_tr_.Triangles[ind_3].Points[ind_2])] = A4

    A1.Triangles[1] = A2
    A2.Triangles[1] = A1

    if (A1.Points[0] in A3.Points and A1.Points[2] in A3.Points) or (A1.Points[0] in A3.Points and A1.Points[1] in A3.Points):
        A1.Triangles[2] = A3
        A2.Triangles[2] = A4
    else:
        A1.Triangles[2] = A4
        A2.Triangles[2] = A3

    A3.Triangles[1] = A4
    A4.Triangles[1] = A3

    if (A3.Points[0] in A1.Points and A3.Points[2] in A1.Points) or (A3.Points[0] in A1.Points and A3.Points[1] in A1.Points):
        A3.Triangles[2] = A1
        A4.Triangles[2] = A2
    else:
        A3.Triangles[2] = A2
        A4.Triangles[2] = A1

    list_triangle.remove(A_tr_.Triangles[ind_3])
    list_triangle.remove(A_tr_)
    list_triangle.append(A1)
    list_triangle.append(A2)
    list_triangle.append(A3)
    list_triangle.append(A4)

    if t1 != -1:
        check_delone(A1, A1.Triangles[0])
    if t2 != -1:
        check_delone(A2, A2.Triangles[0])
    if t3 != -1:
        check_delone(A3, A3.Triangles[0])
    if t4 != -1:
        check_delone(A4, A4.Triangles[0])

    return A1


def check_delone(A_def, B_def):
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

    if (t_1.x - t_0.x)*(t_1.y + t_0.y) + (t_2.x - t_1.x)*(t_2.y + t_1.y) + (t_3.x - t_2.x)*(t_3.y + t_2.y) + (t_0.x - t_3.x)*(t_0.y + t_3.y) < 0:
        t_1, t_3 = t_3, t_1


    cos_a = (t_1.x - t_2.x) * (t_3.x - t_2.x) + (t_1.y - t_2.y) * (t_3.y - t_2.y)
    cos_b = (t_3.x - t_0.x) * (t_1.x - t_0.x) + (t_3.y - t_0.y) * (t_1.y - t_0.y)
    if cos_a < 0 and cos_b < 0:
        swap_line(A_def, B_def, t_0, t_1, t_2, t_3)
        return
    if (not (cos_a < 0 and cos_b < 0)) and (not (cos_a >= 0 and cos_b >= 0)) and bulge(t_0, t_1, t_2, t_3):
        check_1 = (t_1.x - t_2.x) * (t_3.y - t_2.y) - (t_3.x - t_2.x) * (t_1.y - t_2.y)
        check_2 = (t_3.x - t_0.x) * (t_1.x - t_0.x) + (t_3.y - t_0.y) * (t_1.y - t_0.y)
        check_3 = (t_3.x - t_0.x) * (t_1.y - t_0.y) - (t_1.x - t_0.x) * (t_3.y - t_0.y)
        check_4 = (t_1.x - t_2.x) * (t_3.x - t_2.x) + (t_1.y - t_2.y) * (t_3.y - t_2.y)
        a = (check_1 * check_2) + (check_3 * check_4)
        if not (a >= 0):
            swap_line(A_def, B_def, t_0, t_1, t_2, t_3)

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

X, Y = array_create_for_draw(MVO)
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


if B != MVO[len(MVO)-2]:
    list_triangle[0].Triangles[0] = list_triangle[len(list_triangle) - 1]


# проверка Делоне по всем построенным треугольникам
for i in range(len(list_triangle)):
    for j in range(3):
        if list_triangle[i].Triangles[j] != 0:
            check_delone(list_triangle[i], list_triangle[i].Triangles[j])


x_min = list_point[0].x
x_max = list_point[len(list_point)-1].x


m = abs(((0.16 * (y_max - y_min)) * len(list_point) / (x_max - x_min))**(1/2))

i = 1
triangle_for_check = list_triangle[0]
bc = (x_max - x_min) / round(m)
for cnt in range(round(m)):
    array_for_y = list()
    while (i < len(Other_point) and Other_point[i].x < x_min + bc * (cnt+1)):
        array_for_y.append(Other_point[i])
        i+=1

    if cnt / 2 != 0 and len(array_for_y) != 0   :
        array_for_y.sort(key=lambda k: [k.y, k.x], reverse=True)

    for j in range(len(array_for_y)):
        result = check_point_inPolygon(array_for_y[j], triangle_for_check)

        while result == 0:
            flag1 = False
            flag2 = False
            flag3 = False
            # проводим прямую от центра треугольника, в котором ищем, до точки
            # проверяем, с какой стороной она пересекается
            # ищем соседний треугольник с той же стороной и идем далее
            centr = triangle_center(triangle_for_check)
            result_intersection = judge2(centr, array_for_y[j], triangle_for_check.Points[0], triangle_for_check.Points[1])
            flag1 = True
            if not result_intersection:
                result_intersection = judge2(centr, array_for_y[j], triangle_for_check.Points[0], triangle_for_check.Points[2])
                flag2 = True
                if not result_intersection:
                    result_intersection = judge2(centr, array_for_y[j], triangle_for_check.Points[1], triangle_for_check.Points[2])
                    flag3 = True

            if flag3:
                number_next_triangle_for_search = search_triangle(triangle_for_check, triangle_for_check.Points[1], triangle_for_check.Points[2])
                triangle_for_check = triangle_for_check.Triangles[number_next_triangle_for_search]
            elif flag2:
                number_next_triangle_for_search = search_triangle(triangle_for_check, triangle_for_check.Points[0], triangle_for_check.Points[2])
                triangle_for_check = triangle_for_check.Triangles[number_next_triangle_for_search]
            elif flag1:
                number_next_triangle_for_search = search_triangle(triangle_for_check, triangle_for_check.Points[0], triangle_for_check.Points[1])
                triangle_for_check = triangle_for_check.Triangles[number_next_triangle_for_search]

            result = check_point_inPolygon(array_for_y[j], triangle_for_check)

        if result == 1 and check_point_in_triangle(array_for_y[j], triangle_for_check) != 1:
            triangle_for_check = add_point_into_triangle(triangle_for_check, array_for_y[j])

        elif result == 1 and check_point_in_triangle(array_for_y[j], triangle_for_check) == 1:
            triangle_for_check = add_point_into_side(triangle_for_check, array_for_y[j])

# проверка Делоне по всем построенным треугольникам
for i in range(len(list_triangle)):
    for j in range(3):
        if list_triangle[i].Triangles[j] != 0:
            check_delone(list_triangle[i], list_triangle[i].Triangles[j])

for i in range(len(list_triangle)):
    X2, Y2 = array_create_for_draw(list_triangle[i].Points)
    plt.plot(X2, Y2)


plt.gca().set_aspect('equal', adjustable='box')
plt.xlim([0, 13])
plt.ylim([0, 13])
plt.show()
