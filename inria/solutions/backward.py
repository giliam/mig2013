# functional style
def backward (PI, A, E, sequence):
    N = len(A)
    T = len(sequence)
    states = range(N)

    beta = [ [ 0. for t in range(T) ] for i in states ]

    # beta starts with 1's on last time
    for i in states: beta[i][T-1]=1.
    
    # starting with time but last, i.e. T-2
    for t in range (T-2, -1, -1):
        for i in range (N):
            beta[i][t] = \
                reduce (add, [ beta[j][t+1]*A[i][j]*E[j][sequence[t+1]] for j in states ] )
    # resulting proba, summing on time=0
    total = reduce (add, [ PI[i]*E[i][sequence[0]]*beta[i][0] for i in states ] )
    return (total,beta)
        
