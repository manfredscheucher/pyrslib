# author: Manfred Scheucher (2016-2023)

from pyrslib import BasicScript
from itertools import *
from copy import *
from random import *

from scipy import optimize


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


def graph_2_ipe(G,filepath):
	points = G.get_pos()

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
		<view layers="alpha beta" active="alpha"/>\n""")
	
	# normalize
	x0 = min(x for (x,y) in points.values())
	y0 = min(y for (x,y) in points.values())
	x1 = max(1,max(x for (x,y) in points.values())-x0,1)
	y1 = max(1,max(y for (x,y) in points.values())-y0,1)
	maxval = max(x1,y1)
	
	#scale 
	M = 200
	points = {i:(100+float((points[i][0]-x0)*M)/maxval,100+float((points[i][1]-y0)*M)/maxval) for i in points}

	# write edges
	print "compute_curves"
	curves = compute_curves(G)
	print "curves:"
	for c in curves: print "c","->",curves[c]
	

	distances = {v:[] for v in G.vertices()}
	for c in curves:
		for i in range(len(curves[c])):
			p0 = x0,y0 = points[curves[c][i-1]]
			p1 = x1,y1 = points[curves[c][i  ]]
			d2 = (x0-x1)^2+(y0-y1)^2
			distances[curves[c][i-1]].append(d2)
			distances[curves[c][i  ]].append(d2)

	for c in curves:
		# B-splines
		g.write('<path layer="beta" stroke="'+str(c)+'" pen="heavier">\n')
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
		g.write('<use name="mark/disk(sx)" pos="'+str(x)+' '+str(y)+'" size="large" stroke="black"/>\n')
		g.write('<text pos="'+str(x+8)+' '+str(y+8)+'" stroke="black" type="label">$'+str(u)+'$</text>\n')

	
	g.write("""</page>\n</ipe>""")
	g.close()
	print "wrote to ipe-file: ",filepath



def iterated_tutte_layout(G,outer_face):
	G2 = copy(G)

	weights = dict()
	for u,v in G2.edges(labels=None):
		weights[u,v] = weights[v,u] = 0.000001


	eps = 0.01
	maxit = 100
	mypoly = lambda x: x
	for it in range(1,maxit+1):
		#print "tutte #",it
		if it > 1:
			weights_old = weights
			weights = dict()
			for (u,v) in G.edges(labels=None):
				weights[u,v] = weights[v,u] = (RR(weights_old[u,v]+eps*(mypoly(dist2(u,v))-weights_old[u,v])))


			pos = G2.get_pos()
			for f in G2.faces():
				try:
					vol_f = ConvexHull([pos[v] for u,v in f]).volume
					qf = RR(vol_f)
					for u,v in f:
						weights[u,v] += float(it*qf)
						weights[v,u] += float(it*qf)
				except:
					None

			vw0 = vector([weights_old[e] for e in G.edges(labels=False)]).normalized()
			vw1 = vector([weights[e] for e in G.edges(labels=False)]).normalized()
			dvw = (vw0-vw1).norm()
			#print "weight-diff:",dvw
			if dvw < 10^-10: break
					
		G2.set_pos(tutte_layout(G2,outer_face,weights))
		pos = G2.get_pos()
		dist2 = lambda u,v: (pos[u][0]-pos[v][0])^2+(pos[u][1]-pos[v][1])^2

	return G2.get_pos()




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



def _crossing_vertex(ab,cd): return (ab,cd) if ab < cd else (cd,ab)


def rec_draw(verts0,drawn_edges0,edge_crosses_todo0):
	depth = len(drawn_edges0)

	if not edge_crosses_todo0:
		yield drawn_edges0

	else:
		# FORWARD CHECK
		if True:
			for e in edge_crosses_todo0:
				forward_check_passed = False
				a,b = e
				crossings_on_e = [_crossing_vertex(e,f) for f in edge_crosses_todo0[e]]
				
				edge_crosses_todo1 = {f:edge_crosses_todo0[f] for f in edge_crosses_todo0 if f != e}

				# precompute constraints for permutation
				forbidden_pairs = []
				for x1,x2 in combinations(crossings_on_e,2):
					if not Graph(drawn_edges0+[[x1,x2]]).is_planar():
						forbidden_pairs.append((x1,x2))
						forbidden_pairs.append((x2,x1))


				for x1 in e:
					for x2 in crossings_on_e:
						if not Graph(drawn_edges0+[[x1,x2]]).is_planar():
							forbidden_pairs.append((x1,x2))
							forbidden_pairs.append((x2,x1))

				# check permutations
				forbidden_start = []

				PERMS = list(permutations(crossings_on_e))
				shuffle(PERMS)
				for order in PERMS:

					order_verts = (a,)+order+(b,)

					skip = 0
					for i in range(1,len(order_verts)):
						#if order_verts[:i] in forbidden_start: 
						#	skip = 1
						#	continue

						if (order_verts[i-1],order_verts[i]) in forbidden_pairs:
							skip = 1
							break

					if skip: continue


					# TODO: speedup here by iteratively adding elements to permutation (better than all)
					
					#print depth*" ","order",order

					drawn_edges1 = copy(drawn_edges0)
					for i in range(1,len(order_verts)):
						drawn_edges1.append([order_verts[i-1],order_verts[i],e])

						#if not Graph(drawn_edges1).is_planar():
						#	forbidden_start.append(order_verts[:i])
					
					if len(drawn_edges1) < 3 or Graph(drawn_edges1).is_planar(): 
						forward_check_passed = True
						break
				
				if not forward_check_passed: return # every edge must be drawable!!!

		# END OF FORWARD CHECK





		min_crossings = min(len(edge_crosses_todo0[e]) for e in edge_crosses_todo0)
		for e in edge_crosses_todo0:
			a,b = e
			crossings_on_e = [_crossing_vertex(e,f) for f in edge_crosses_todo0[e]]
			if len(crossings_on_e) != min_crossings: continue
			
			edge_crosses_todo1 = {f:edge_crosses_todo0[f] for f in edge_crosses_todo0 if f != e}


			# precompute constraints for permutation
			forbidden_pairs = []
			for x1,x2 in combinations(crossings_on_e,2):
				if not Graph(drawn_edges0+[[x1,x2]]).is_planar():
					forbidden_pairs.append((x1,x2))
					forbidden_pairs.append((x2,x1))


			for x1 in e:
				for x2 in crossings_on_e:
					if not Graph(drawn_edges0+[[x1,x2]]).is_planar():
						forbidden_pairs.append((x1,x2))
						forbidden_pairs.append((x2,x1))

			# check permutations
			tests = 0
			forbidden_start = []

			PERMS = list(permutations(crossings_on_e))
			shuffle(PERMS)
			for order in PERMS:

				order_verts = (a,)+order+(b,)

				skip = 0
				for i in range(1,len(order_verts)):
					#if order_verts[:i] in forbidden_start: 
					#	skip = 1
					#	continue

					if (order_verts[i-1],order_verts[i]) in forbidden_pairs:
						skip = 1
						break

				if skip: continue

				tests += 1

				# TODO: speedup here by iteratively adding elements to permutation (better than all)
				
				#print depth*" ","order",order

				drawn_edges1 = copy(drawn_edges0)
				for i in range(1,len(order_verts)):
					drawn_edges1.append([order_verts[i-1],order_verts[i],e])

					#if not Graph(drawn_edges1).is_planar():
					#	forbidden_start.append(order_verts[:i])

				if Graph(drawn_edges1).is_planar():
					for G in rec_draw(verts0,drawn_edges1,edge_crosses_todo1): yield G

			#print "tests",tests,"of",factorial(len(crossings_on_e))
			break







class UnifyRSScript(BasicScript.BasicScript): 

	def __init__(self):
		super(UnifyRSScript,self).__init__()

		self.draw_first_only = int(self.arguments.get("draw_first_only",1))
		self.force_outer_vertices = int(self.arguments.get("force_outer_vertices",1))
		

		outpath = self.filepath+".drawings.txt"
		self.drawings_file = open(outpath,"w")

	def _print_usage_info(self,rs):
		print "description:"


	def _action_inner(self,rs):
		n = rs.n
		N = range(n)
		o = rs.orientations

		#print o
		crossing_pairs = list(rs.enumerate_crossing_pairs())
		#print crossing_pairs


		edge_crosses = {ab:[] for ab in combinations(N,2)}
		for ab,cd in crossing_pairs:
			edge_crosses[ab].append(cd)
			edge_crosses[cd].append(ab)

		#print edge_crosses
		possibilities = []
		for ab in edge_crosses:
			possibilities .append( (len(edge_crosses[ab])) )

		print self.count,"->",max(possibilities),"-> possibilities:",factorial(max(possibilities))


		for (ab,cd) in crossing_pairs: assert( (ab,cd) == _crossing_vertex(ab,cd) )
		verts = N+crossing_pairs


		drawn_edges = next(rec_draw(verts,[],edge_crosses))
		self.drawings_file.write(str((rs.orientations,drawn_edges))+"\n")

		G = Graph(drawn_edges)
		assert(G.vertex_connectivity() >= 3)

		G.is_planar(set_embedding=1)

		F = G.faces()
		F = [[u for (u,v) in f] for f in F] # vertex list instead of edge list



		def _quality(f): return 1


		if self.force_outer_vertices: 
			def _quality(f): return -len(set(f) & set(crossing_pairs)) # fewer crossings are better 

		max_q = max(_quality(f) for f in F)

		aldready_drawn_fingerprints = set()

		ct = 0
		for f in F:
			if _quality(f) == max_q:

				H = copy(G)
				for u in f: 
					H.add_edge('virt1'+str(u),u)
					if u in crossing_pairs: 
						H.add_edge('virt2'+str(u),u) # distinguish crossings and vertices

				hstr = H.canonical_label().sparse6_string()
				if hstr in aldready_drawn_fingerprints: continue # already drawn!
				aldready_drawn_fingerprints.add(hstr)

				assert(len(f)>=3)

				ct += 1
				fp = self.filepath+"_rs"+str(self.count)+"_dr"+str(ct)

				# === iterative tutte embedding ===
				G.set_pos(iterated_tutte_layout(G,outer_face=f))


				# === draw IPE ===
				graph_2_ipe(G,fp+".ipe")


				# === draw PNG ===

				# relabel crossings
				vertex_colors = {'white':[]}
				G2 = copy(Graph(G))
#				G2.set_pos(G.get_pos())
				for v in G2:
					if v in crossing_pairs:
						new_name = 'x'+str(crossing_pairs.index(v))
						G2.relabel({v:new_name})
						vertex_colors['white'].append(new_name)
					
				G2.graphplot(edge_labels=0, color_by_label=True, vertex_colors=vertex_colors).plot().save(fp+".png") 
				print fp,"->",f

				if self.draw_first_only: break


	def _progress_text(self): 
		None

	def _action_end(self): 
		None

if __name__ == "__main__": UnifyRSScript().action()
