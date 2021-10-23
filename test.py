from multiprocessing.dummy import Pool

A = [1,2,1,2,2,3,4,1,1,223,2,1,1,2,1,1,1]

def f(a):
    print('1'*a)


with Pool(processes=len(A)) as p:
    p.map(f, A)

print(A)


