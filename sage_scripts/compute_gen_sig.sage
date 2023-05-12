# author: Manfred Scheucher (2016-2023)
from sys import *
from itertools import *
from ast import *




def tutte_layout(G,outer_face,weights=None):
	V = G.vertices()
	pos = dict()
	l = len(outer_face)

	a0 = pi/l+pi/2
	for i in range(l):
		ai = a0+pi*2*i/l
		pos[outer_face[i]] = (cos(ai),sin(ai))
	
	n = len(V)
	M = zero_matrix(RR,n,n)
	b = zero_matrix(RR,n,2)

	for i in range(n):
		v = V[i]
		if v in pos:
			M[i,i] = 1
			b[i,0] = pos[v][0]
			b[i,1] = pos[v][1]
		else:
			nv = G.neighbors(v)
			s = 0
			for u in nv:
				j = V.index(u)
				wu = weights[u,v] if weights else 1
				s += wu
				M[i,j] = -wu
			M[i,i] = s

	sol = M.pseudoinverse()*b
	return {V[i]:sol[i] for i in range(n)}




def compute_curves(G):
	curves = {}

	for c in G.edge_labels():
		curves[c] = []


		v = c[0]
		curves[c].append(v)
		while v != c[1]:
			for (a,b,cc) in G.edges_incident(v):
				if cc == c:
					w = (a if a != v else b)
					if w not in curves[c]:
						curves[c].append(w)
						v = w
						break

	return curves


found = set()

n = int(argv[1])
fp = argv[2]

for line in open(fp):
	rs,drawn_edges = literal_eval(line) 

	G = Graph(drawn_edges)
	N = range(n)


	G.is_planar(set_embedding=1)
	F = [[u for u,v in f] for f in G.faces()]


	curves = compute_curves(G)
	assert(len(curves) == (n*(n-1))/2)

	di_curves = {}
	for c in curves:
		a,b = c
		di_curves[a,b] = curves[c]
		di_curves[b,a] = list(reversed(curves[c]))





	for f in F:
		pos = tutte_layout(G,f)


		s = ''
		for a,b,c in combinations(N,3):
			curve = di_curves[a,b] + di_curves[b,c] + di_curves[c,a]

			X = [pos[i][0] for i in curve]
			Y = [pos[i][1] for i in curve]

			area = sum((Y[i-1]+Y[i])*(X[i-1]-X[i]) for i in range(len(curve)))/2
			
			assert(abs(area) > 10^-6)

			s += '+' if area > 0 else '-'


		if s not in found: print s
		found.add(s)




