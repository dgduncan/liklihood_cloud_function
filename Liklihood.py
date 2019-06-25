import itertools
import math
import numpy


def liklihood (alleles, prob, x1, x2, u1, u2):
    # Begin input error checking

    n_u1 = len(u1)

    n_u2 = len(u2)

    G = len(x1)


    ind1 = None
    ind2 = None

    if (n_u1 > 0):
        ind1 = numpy.repeat(None, n_u1)
        for k in range(0, n_u1):
            ind1[k] = numpy.min(numpy.where(numpy.array(alleles) == u1[k]))

    if (n_u2 > 0):
        ind2 = numpy.repeat(None, n_u2)
        for k in range(0, n_u2):
            ind2[k] = numpy.min(numpy.where(numpy.array(alleles) == u2[k]))

    p1 = p_evid(p = prob, x = x1, ind = ind1, g = G)
    p2 = p_evid(p = prob, x = x2, ind = ind2, g = G)
    LR = p1 / p2
    return LR


def p_evid (p, x, ind, g):
    if ind is None:
        n_u = 0
    else:
        n_u = len(ind)
        
    
    T = numpy.float32(numpy.repeat(0, n_u + 1))
    T[0] = numpy.prod(math.pow(sum(p), 2 * x[0]))

    if(n_u > 1):
        for skip in range(1, n_u):
            K = list(itertools.combinations(ind, skip))
            Kcol = len(K)
            t = numpy.float32(numpy.repeat(0, Kcol))
            for j in range(0, Kcol):
                # print("j = ", j)
                # print("p[int(j)+1:]", numpy.delete(p, K[j]))
                t[j] = numpy.prod(math.pow(sum(numpy.delete(p, K[j])), (2 * x[0])))
                # print("SUM = ", math.pow(sum(numpy.delete(p, K[j])), 2 * x[0]))
            T[skip] = math.pow(-1, skip) * sum(t)
    if(n_u > 0):
        T[n_u] = math.pow(-1, n_u) * numpy.prod(math.pow(sum(numpy.delete(p, ind)), 2 * x[0]))
    return(sum(T))




    # if (n_u1 > 0):
    #     if not u1.intersection(alleles) == u1:
    #         exit("'u1' must contain only elements from 'alleles'")
    # if (n_u2 > 0):
    #     if not u2.intersection(alleles) == u2:
    #         exit("'u2' must contain only elements from 'alleles'")

    # if (alleles == u1):
    #     exit("under the null hypothesis there must be at least one known contributor")
    # G = len(x1)