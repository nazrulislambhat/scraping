#Simplest Clustering Algo on this planet by Mudasir Ali
import math
list1 = [17999,10000,7000,8500,9000,9500,4199,99,0]
#list2 = [1,5,6,3,2,3,4]
m1 = 17999
m2 = 99
cluster1=[]
cluster2=[]
for i in range(len(list1)):
    val1 = math.sqrt(pow(list1[i]-m1,2))
    val2 = math.sqrt(pow(list1[i]-m2,2))
    if (val1<val2):
        cluster1.append(list1[i])
        #m1 = (m1+list1[i])/len(cluster1)
    else:
        cluster2.append(list1[i])
        #m2 = (m2+list1[i])/len(cluster2)
print(cluster1)
print(cluster2)
