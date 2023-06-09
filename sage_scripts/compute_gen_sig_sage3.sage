# author: Manfred Scheucher (2016-2023)
from sys import *
from itertools import *
from ast import *




def graph_2_ipe(G,filepath,DEBUG=False):
	points = G.get_pos()
	points = {literal_eval(v):points[v] for v in points} # python3 sucks

	ipestyle = 'ipestyle.txt'
	g = open(filepath,'w')
	g.write("""<?xml version="1.0"?>
		<!DOCTYPE ipe SYSTEM "ipe.dtd">
		<ipe version="70005" creator="Ipe 7.1.4">
		<info created="D:20150825115823" modified="D:20150825115852"/>
		""")
	with open(ipestyle) as f:
		for l in f.readlines():
			g.write("\t\t"+l)
	g.write("""<page>
		<layer name="alpha"/>
		<layer name="beta"/>
		<layer name="gamma"/>
		<view layers="alpha beta gamma" active="alpha"/>\n""")
	
	# normalize
	x0 = min(x for (x,y) in points.values())
	y0 = min(y for (x,y) in points.values())
	x1 = max(1,max(x for (x,y) in points.values())-x0,1)
	y1 = max(1,max(y for (x,y) in points.values())-y0,1)
	maxval = max(x1,y1)
	
	#scale 
	M = 300
	M0 = 100
	points = {i:(M0+float((points[i][0]-x0)*M)/maxval,M0+float((points[i][1]-y0)*M)/maxval) for i in points}

	# write edges
	print ("compute_curves")
	curves = compute_curves(G)
	
	if DEBUG:
		print ("curves:")
		for c in curves: print (c,"->",curves[c])
	

	distances = {literal_eval(v):[] for v in G.vertices()}
	for c in curves:
		for i in range(len(curves[c])):
			p0 = x0,y0 = points[curves[c][i-1]]
			p1 = x1,y1 = points[curves[c][i  ]]
			d2 = (x0-x1)^2+(y0-y1)^2
			distances[curves[c][i-1]].append(d2)
			distances[curves[c][i  ]].append(d2)

	IPE_COLORS = ['red','blue','green','orange','pink','lightblue','purple','lightgray','black','darkgray','navy','darkred','darkgreen','brown','gold','lightgreen','turquoise']

	for c in curves:
		for color in c:
			# B-splines
			DASHED = '' if color == c[0] else ' dash="dashed"'
			g.write('<path layer="alpha" stroke="'+IPE_COLORS[color]+'" '+DASHED+'>\n')
			lc = len(curves[c])
			for i in range(lc):
				x0,y0 = points[curves[c][(i-1)%lc]]
				x1,y1 = points[curves[c][ i      ]]
				x2,y2 = points[curves[c][(i+1)%lc]]
				d0 = (x0-x1)^2+(y0-y1)^2
				d2 = (x2-x1)^2+(y2-y1)^2
				lmbd0 = sqrt(min(distances[curves[c][i]])/d0)/3
				lmbd2 = sqrt(min(distances[curves[c][i]])/d2)/3
				xl,yl = x1+lmbd0*(x0-x1),y1+lmbd0*(y0-y1)
				xr,yr = x1+lmbd2*(x2-x1),y1+lmbd2*(y2-y1)
				if i != 0   : g.write(str(xl)+" "+str(yl)+"\n")
				g.write(str(x1)+" "+str(y1)+(" m" if i == 0 else "")+"\n")
				if i != lc-1: g.write(str(xr)+" "+str(yr)+"\n")
			g.write("c\n</path>\n")
		


	proper_vertices = set()
	for a,b in curves: proper_vertices |= {a,b} # proper vertices are endpoints

	for u in proper_vertices:
		x,y = points[u]
		g.write('<use layer="beta" name="mark/fdisk(sfx)" pos="'+str(x)+' '+str(y)+'" size="large" stroke="black" fill="'+IPE_COLORS[u]+'"/>\n')
		g.write('<text layer="gamma" pos="'+str(x+2)+' '+str(y+2)+'" stroke="black" type="label">$'+str(u)+'$</text>\n')

	
	g.write("""</page>\n</ipe>""")
	g.close()
	print ("wrote to ipe-file: ",filepath)




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

	for c_str in G.edge_labels():
		c = literal_eval(c_str)
		curves[c] = []

		v = c[0]
		curves[c].append(v)
		while v != c[1]:
			for (a_str,b_str,cc_str) in G.edges_incident(str(v)):
				cc = literal_eval(cc_str)
				a = literal_eval(a_str)
				b = literal_eval(b_str)
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

example = 0

for lct,line in enumerate(open(fp)):
	rs,drawn_edges = literal_eval(line) 

	drawn_edges_py3 = [(str(a),str(b),str(c)) for (a,b,c) in drawn_edges] # python3
	G = Graph(drawn_edges_py3)
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
		pos_str = tutte_layout(G,f)
		pos = {literal_eval(v):pos_str[v] for v in pos_str}


		s = ''
		for a,b,c in combinations(N,3):
			curve = di_curves[a,b] + di_curves[b,c] + di_curves[c,a]

			X = [pos[i][0] for i in curve]
			Y = [pos[i][1] for i in curve]

			area = sum((Y[i-1]+Y[i])*(X[i-1]-X[i]) for i in range(len(curve)))/2
			
			assert(abs(area) > 10^-6)

			s += '+' if area > 0 else '-'


		if s not in found: 
			print (s)
			found.add(s)

			if 1:
				X = {}
				for i,(a,b,c) in enumerate(combinations(N,3)):
					X[a,b,c] = X[b,c,a] = X[c,a,b] = +1 if s[i] == '+' else -1
					X[b,a,c] = X[c,b,a] = X[a,c,b] = -X[a,b,c]


				if 0:
					k_vec = {k:0 for k in range(n-1)}
					for a,b in permutations(N,int(2)):
						k = len([c for c in set(N)-{a,b} if X[a,b,c] == +1])
						k_vec[k] += 1

					print("k-edges vector:",k_vec)

					if 0 in k_vec.values():
						example += 1
						G.set_pos(pos_str)
						s = '_'.join(str(k_vec[k]) for k in range(n//2))
						G.plot().save(fp+".line"+str(lct)+"_"+str(example)+"_"+s+".png")
						graph_2_ipe(G,fp+".line"+str(lct)+"_"+str(example)+"_"+s+".ipe")
						#exit("found problem!")

					assert(k_vec[n//2-1]>0)

				if 1:
					for a in N:
						k_vec = {k:0 for k in range(n-1)}
						for b in set(N)-{a}:
							k = len([c for c in set(N)-{a,b} if X[a,b,c] == +1])
							k_vec[k] += 1

						if k_vec[n//2-1] == 0:
							print("no halving edge for",a)
							example += 1
							G.set_pos(pos_str)
							s = '_'.join(str(k_vec[k]) for k in range(n//2))
							G.plot().save(fp+".fooline"+str(lct)+"_"+str(example)+"_"+s+".png")
							graph_2_ipe(G,fp+".fooline"+str(lct)+"_"+str(example)+"_"+s+".ipe")
							#exit("found problem!")

							#assert(k_vec[n//2-1]>0)

