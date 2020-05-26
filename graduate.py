import numpy 
import networkx as nx
import matplotlib.pyplot as plt
import random
import math

n = 10000
m = 6
p = 0.01
G = nx.random_graphs.barabasi_albert_graph(n,m)

link = [[] for i in range(n)]#邻接
link2 = [[] for i in range(n)]#邻接
origin_link = [[] for i in range(n)]#邻接

h_index = numpy.zeros(n)#h-index值
ks = numpy.zeros(n)#k-shell值
father = numpy.arange(0,n,1)#并查集 指向的数
number_of_node = numpy.zeros(n)#节点数
level = numpy.zeros(n)#节点层数
number_of_link = numpy.zeros(n)#连边数
number_of_outlink = numpy.zeros((n,n))#骨干结构之间连变数
degree_of_outnode = numpy.zeros(n)

for i in range(n):
    k = iter(nx.all_neighbors(G,i))
    flag = 1
    while flag:
        try:
            q = next(k)
            link[i].append(q)
            origin_link[i].append(q)
            link2[i].append(q)
        except:
            flag = 0
def get_h_index():
    for i in range(n):
        temphindex = []
        for j in range(len(link[i])):
            temphindex.append(len(link[link[i][j]]))
        temphindex.sort()
        for j in range(len(temphindex)):
            if j > temphindex[j]:
                h_index[i] = j
                break
            if j == len(temphindex) - 1:
                h_index[i] = j

def get_ks():
    already_delete = numpy.zeros(n)
    already_deleted = []
    temp_k = 1
    while len(already_deleted) != n:
        for i in range(n):
            need_to_delete = []
            if already_delete[i] == 0 and len(link2[i]) <= temp_k:
                for j in range(len(link2[i])):
                    need_to_delete.append(link2[i][j])
                already_delete[i] = 1
                ks[i] = temp_k
                already_deleted.append(i)
            for j in range(len(need_to_delete)):
                link2[need_to_delete[j]].remove(i)
        temp_k += 1

def find_father(a):
    while(father[a]!=a):
        a = father[a]
    return a

def union(a,b):
    a_father = find_father(a)
    b_father = find_father(b)
    if a_father<b_father:
        father[b_father] = a_father
    if a_father>b_father:
        father[a_father] = b_father

def findclique(root,tempclique2,maxlength):
    tempclique2.append(root)
    ffflag = 0
    for i in range(len(link[root])):
        fflag = 0
        for j in range(len(tempclique2)):
            for k in range(len(link[tempclique2[j]])):
                if link[tempclique2[j]][k] > tempclique2[j] and link[tempclique2[j]][k] == link[root][i]:
                    fflag = fflag + 1
        if fflag == len(tempclique2):
            ffflag = 1
            findclique(link[root][i],tempclique2,max(maxlength,len(tempclique2)))

    if ffflag == 0:
        if maxlength + 1 == len(tempclique2) : 
            tempclique.clear()
            for i in range(len(tempclique2)):
                tempclique.append(tempclique2[i])
        tempclique2.pop()

def find_clique():

    flag = 0
    global maxsize_of_clique
    global can_find_clique
    global result_of_flag
    temp_maxsize_of_clique = 0

    for i in range(n): 
        findclique(i,[],0)
        if len(tempclique)>2:
            #for i in range(len(tempclique)):
             #   if find_father(tempclique[i]) != tempclique[i]:
              #      level[tempclique[i]] = level[find_father(tempclique[i])] + 1
            if len(tempclique)>temp_maxsize_of_clique:
                temp_maxsize_of_clique = len(tempclique)
            print(tempclique)
            for j in tempclique:
                clique[flag].append(j)
            number_of_clique[len(tempclique)] += 1
            size_of_clique[len(tempclique)].append(flag)
            flag += 1
        tempclique.clear()

    for i in reversed(range(3,temp_maxsize_of_clique+1)):
        max_level = 0
        for j in range(len(size_of_clique[i])):
            ind = size_of_clique[i][j]
            is_be_oneself = 0 #是否独占
            for k in range(len(clique[ind])):
                if max_level < level[clique[ind][k]]:
                    max_level = level[clique[ind][k]]
                if visit[clique[ind][k]] == 1:
                    is_be_oneself = 1
            if is_be_oneself == 0:
                number_of_result_clique[i] += 1
                for k in range(len(clique[ind])):
                    level[clique[ind][k]] = max_level + 1
                    visit[clique[ind][k]] = 1
                    result_of_cliques[result_of_flag].append(clique[ind][k])
                    if k != 0:
                        union(clique[ind][k-1],clique[ind][k])
                result_of_flag += 1
    
    maxsize_of_clique = temp_maxsize_of_clique
    if result_of_flag == 0:
        can_find_clique = 2

def simply_clique():
    for i in range(result_of_flag):
        for j in range(len(result_of_cliques[i])):
            ind = result_of_cliques[i][j]
            if find_father(ind) != ind:
                for k in range(n):
                    for l in range(len(link[k])):
                        if link[k][l] == ind:
                            link[k][l] = find_father(ind)
                                                                              
def count_number_of_nodes():
    for i in range(n):
        number_of_node[find_father(i)] += 1

def count_number_of_edges():
    for i in range(n):
        for j in range(len(link[i])):
            if find_father(link[i][j]) == find_father(i):
                number_of_link[find_father(i)] += 0.5
            else:
                number_of_outlink[find_father(link[i][j])][find_father(i)] += 0.5
                number_of_outlink[find_father(i)][find_father(link[i][j])] +=0.5

def SIR(start):
    a = 0.4 #传染率
    b = 0.2 #治愈率

    for i in range(n):
        if i != start:
            susceptible.append(i)
        else:
            infective.append(i)
            status[i] = 1

    flagggg = 0

    while flagggg < 25:
        number_of_S.append(len(susceptible))
        number_of_I.append(len(infective))
        number_of_R.append(len(removal))
        delete_from_infective = []
        for i in range(len(infective)):
            for j in range(len(origin_link[infective[i]])):
                if status[origin_link[infective[i]][j]] == 0:
                    pro1 = random.randint(0,100)
                    if pro1 < 100 * a:
                        susceptible.remove(origin_link[infective[i]][j])
                        infective.append(origin_link[infective[i]][j])
                        status[origin_link[infective[i]][j]] = 1
            if status[infective[i]] == 1:
                pro2 = random.randint(0,100)
                if pro2 < 100 * b:
                    delete_from_infective.append(infective[i])
                    removal.append(infective[i])
                    status[infective[i]] = 2
        for i in range(len(delete_from_infective)):
            infective.remove(delete_from_infective[i])
        flagggg += 1

def pic_first_time():
    exist1 = numpy.zeros(maxsize_of_clique + 1)
    exist_size1 = 0
    exist2 = numpy.zeros(maxsize_of_clique + 1)
    exist_size2 = 0

    for i in range(len(number_of_clique)):
        if number_of_clique[i] != 0 :
            exist_size1 += 1
            exist1[i] = 1
    for i in range(len(number_of_result_clique)):
        if number_of_result_clique[i] != 0:
            exist_size2 += 1
            exist2[i] = 1

    result_exist1 = []
    result_exist2 = []
    for i in reversed(range(3,maxsize_of_clique + 1)):
        if exist1[i] == 1:
            result_exist1.append(i)
        if exist2[i] == 1:
            result_exist2.append(i)

    fig = plt.figure()
    fig1 = fig.add_subplot(2,2,1)
    fig2 = fig.add_subplot(2,2,2)
    fig3 = fig.add_subplot(2,2,3)
    fig4 = fig.add_subplot(2,2,4)
    fig1.scatter(range(3,maxsize_of_clique + 1),number_of_clique[3:maxsize_of_clique + 1])
    fig1.set_xlabel("clique size")
    fig1.set_ylabel("number")
    fig1.set_title("The number of each non-unique clique")
    fig2.scatter(range(1, exist_size1 + 1),result_exist1)
    fig2.set_xlabel("rank")
    fig2.set_ylabel("clique size")
    fig2.set_title("The rank of each non-unique clique")
    fig3.scatter(range(3,maxsize_of_clique + 1),number_of_result_clique[3:maxsize_of_clique + 1])
    fig3.set_xlabel("clique size")
    fig3.set_ylabel("number")
    fig3.set_title("The number of each unique clique")
    fig4.scatter(range(1, exist_size2 + 1),result_exist2)
    fig4.set_xlabel("rank")
    fig4.set_ylabel("clique size")
    fig4.set_title("The rank of each unique clique")
    plt.tight_layout()
    plt.show()

def get_degree():
    for i in range(n):
        if find_father(i) == i:
            result_of_nodes.append(i)
            for j in range(len(link[i])):
                if find_father(link[i][j]) != link[i][j]:
                    link[i][j] = find_father(link[i][j])

    for i in range(len(result_of_nodes)):
        for j in range(i+1,len(result_of_nodes)):
            a = result_of_nodes[i]
            b = result_of_nodes[j]
            if number_of_outlink[a][b] > 1:
                degree_of_outnode[a] += number_of_outlink[a][b]
                degree_of_outnode[b] += number_of_outlink[b][a]

def select_clique_node():
    start_max1 = 0
    start_group1 = []
    clique_degree_flag = 0
    for i in range(len(result_of_nodes)):
        if degree_of_outnode[result_of_nodes[i]] > start_max1:
            start_group1.clear()
            clique_degree_flag = 1
            start_max1 = degree_of_outnode[result_of_nodes[i]]
            start_group1.append(result_of_nodes[i])
        elif degree_of_outnode[result_of_nodes[i]] == start_max1:
            clique_degree_flag += 1
            start_group1.append(result_of_nodes[i])
    start_node1 = start_group1[random.randint(0,clique_degree_flag-1)]
    start_node.append(start_node1)

def select_h_index_node():
    start_max2 = 0
    start_group2 = []
    h_index_flag = 0
    for i in range(n):
        if h_index[i] > start_max2:
            start_group2.clear()
            start_max2 = h_index[i]
            start_group2.append(i)
            h_index_flag = 1
        elif h_index[i] == start_max2:
            h_index_flag += 1
            start_group2.append(i)
    start_node2 = start_group2[random.randint(0,h_index_flag-1)]
    start_node.append(start_node2)

def select_ks_node():
    start_max3 = 0
    start_group3 = []
    ks_flag = 0
    for i in range(n):
        if ks[i] > start_max3:
            ks_flag = 1
            start_group3.clear()
            start_max3 = ks[i]
            start_group3.append(i)
        elif ks[i] == start_max3:
            ks_flag += 1
            start_group3.append(i)
    start_node3 = start_group3[random.randint(0,ks_flag-1)]
    start_node.append(start_node3)
    
def draw_SIR():
    plt.plot(range(len(number_of_S)),number_of_S,color = "red",label = "susceptible")
    plt.plot(range(len(number_of_I)),number_of_I,color = "blue",label = "infective")
    plt.plot(range(len(number_of_R)),number_of_R,color = "black",label = "removal")
    plt.xlabel("time")
    plt.ylabel("number")
    plt.title("SIR model")
    plt.legend(loc = "best")
    plt.show()

def draw_three_curves():
    plt.plot(range(len(rrrrrr[0])),rrrrrr[0],color = "red",label = "removal of clique")
    plt.plot(range(len(rrrrrr[1])),rrrrrr[1],color = "blue",label = "removal of hindex")
    plt.plot(range(len(rrrrrr[2])),rrrrrr[2],color = "black",label = "removal of ks")
    plt.xlabel("time")
    plt.ylabel("number")
    plt.title("SIR model")
    plt.legend(loc = "best")
    plt.show()

def draw_result_pic():
    final_G = nx.Graph()
    result_edges = []
    for i in range(len(result_of_nodes)):
        for j in range(i+1,len(result_of_nodes)):
            if number_of_outlink[result_of_nodes[i]][result_of_nodes[j]] >= 1:
                result_edges.append(number_of_outlink[result_of_nodes[i]][result_of_nodes[j]])
    result_edges.sort(reverse = True)
    for k in range(len(result_of_nodes)-1):
        for i in range(len(result_of_nodes)):
            for j in range(i+1,len(result_of_nodes)):
                if number_of_outlink[result_of_nodes[i]][result_of_nodes[j]] == result_edges[k]:
                    final_G.add_edge(result_of_nodes[i],result_of_nodes[j])
    nx.draw(final_G,with_labels = True)
    plt.show()

if __name__ == '__main__':
    get_h_index()
    get_ks()
    result_of_nodes = []
    can_find_clique = 0
    time = 0
    while can_find_clique != 2:
        result_of_flag = 0
        tempclique = []
        visit = numpy.zeros(n)
        clique = [[] for i in range(n)]#clique包含的点
        result_of_cliques = [[] for i in range(n)]
        size_of_clique = [[] for i in range(n)]
        node_in_clique = numpy.zeros(n)
        number_of_clique = numpy.zeros(n)
        number_of_result_clique = numpy.zeros(n)
        find_clique()
        simply_clique()
        time += 1

        print(number_of_clique,maxsize_of_clique)
        print(number_of_result_clique)
    
        if time == 1:
            pic_first_time()

    count_number_of_nodes()
    count_number_of_edges()
    get_degree()

    start_node = []

    select_clique_node()
    select_h_index_node()
    select_ks_node()
    
    rrrrrr = [[] for i in range(n)]#邻接
    
    for i in range(3):
        status = numpy.zeros(n)# 0 sus 1 in 2 re
        susceptible =[] #S
        infective = [] #I
        removal = [] #R
        number_of_S =[]
        number_of_I = []
        number_of_R = []

        SIR(start_node[i])
        rrrrrr[i] = number_of_R
        
        draw_SIR()
        
    draw_three_curves()
    print(start_node)
    
    draw_result_pic()