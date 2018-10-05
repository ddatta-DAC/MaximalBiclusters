import numpy as np
from itertools import combinations
from itertools import chain
from pprint import pprint

DEBUG = True

def debug(msg):
	if DEBUG:
		pprint(msg)

data = [
	[1, 2, 0, 1, 6, 8, 4, 2, 1],
	[2, 1, 1, 0, 6, 8, 4, 1, 2],
	[2, 2, 1, 7, 6, 8, 4, 0, 2],
	[8, 9, 1, 6, 7, 5, 1, 2, 2]
]

data = np.array(data)


# ----------------------------------------------------------------#
# function to determine partial ordering
# input ordered lists
# Return true if
# set1 < set2
# ----------------------------------------------------------------#
def compare_sets(set1, set2):
	for i in range(min(len(set1), len(set2))):
		if set1[i] <= set2[i]:
			continue
		if set1[i] > set2[i]:
			return False
	return True


def disp_bc(coll_bc):
	for bc in coll_bc:
		print(bc[0], '::', bc[1])


# ----------------------------------------------------------------#
#                       Helper functions
# ----------------------------------------------------------------#
def get_max_d_ij(A_r, j, D):
	tmp = [D[i,j] for i in A_r]
	tmp = np.array(tmp)
	# print('>', np.max(tmp))
	return np.max(tmp)


def get_min_d_ij(A_r, j, D):
	tmp = [ D[i][j] for i in A_r ]

	tmp = np.array(tmp)
	# print('>', np.min(tmp))
	return np.min(tmp)


def add_to_set(B, j):
	B = list(B)
	B.append(j)
	B = list(set(sorted(B)))
	return B


def get_possible_extents(A, D, j):
	power_set = powerset(A)
	extents = []
	# check the formal concepts

	for s in power_set:
		# print ('cand_A' ,s , 'Cand_j',j)
		# print(get_max_d_ij(A,j,D),get_min_d_ij(A,j,D))
		if get_max_d_ij(s,j,D) == get_min_d_ij(s,j,D):
			extents.append(s)

	extents = list(sorted(extents))
	return extents

def powerset(set1):
	s = list(set1)
	res = []
	tmp = chain.from_iterable(combinations(s, r) for r in range(len(s) + 1))
	for t in tmp:
		if len(t) < 1:
			continue
		else:
			t = list(sorted(t))
			res.append(t)
	res = list(sorted(res))
	return res


def is_canonical(RW, B, D, j):

	candidate_k_list = list(range(0,j))
	if j == 0 :
		k=j
		diff = get_max_d_ij(RW, k, D) - get_min_d_ij(RW, k, D)
		if diff == 0 :
			return True
		else:
			return False

	# check for k < j
	# attribute k < j that we can add to the bicluster (RW, B) and it remains a valid perfect CVC bicluster
	# Then return False
	for k in candidate_k_list:
		if k not in B:
			diff = get_max_d_ij(RW, k, D) - get_min_d_ij(RW, k, D)
			if diff == 0:
				res = False
				return res

	return True


# ----------------------------------------------------------------#
# Each bicluster is represented as [A,B] = [ ordered_list_extent , ordered_list_intent ]
# -------------------------------------------------------------- #
# D : Data Matrix  n x m
# min_rows :  minimum number of rows in the bi-cluster
# r : Index of bicluster to be closed
# y : Index of the initial attribute y
# coll_bc : collection of bicluster , type list
# -------------------------------------------------------------- #


def in_close_cvc(D, min_rows, r, y, coll_bc):
	global r_new

	# print('---')
	# print(' In in_close ::', 'r=', r, 'y=', y)
	disp_bc(coll_bc)
	# print("Working to close ", coll_bc[r])

	J = []
	R = []
	m = np.array(D).shape[1]
	B_r = coll_bc[r][1]
	# print('current B_r', B_r)

	for j in range(y, m):
		# print('-----')
		# check if j does not belong to B_r
		if j not in B_r:

			A_r = coll_bc[r][0]

			max_i = get_max_d_ij(A_r, j, D)
			min_i = get_min_d_ij(A_r, j, D)
			diff = max_i - min_i
			# current attribute j is added to the current intent Br if all values of attribute j and objects Ar are equal
			if diff == 0:
				B_r = add_to_set(B_r, j)
				coll_bc[r][1] = B_r
				# print('Case diff = 0', ' j =', j, 'Adding j to B_r . Now B_r', B_r)
			else:
				# Compute the possible extents
				possible_extents = get_possible_extents(A_r,D,j)
				# print ('Exploring possible extents', possible_extents)

				for RW in possible_extents:
					if len(RW) >= min_rows:
						canon = is_canonical(RW, B_r, D, j)
						if canon == True :
							r_new = r_new + 1
							R = add_to_set(R, r_new)
							# J = add_to_set(J, j)
							J.append(j)
							# print('J ',J)
							coll_bc.append([None,None])
							# print('r_new ', r_new, 'RW : ', RW)
							coll_bc[r_new][0] = RW  # Arnew ← RW

	print('Current J ', J)
	print('Current R ', R)

	for k in range(len(J)):
		B_Rk = add_to_set(B_r, J[k])
		coll_bc[R[k]][1] = B_Rk
		in_close_cvc(D, min_rows, R[k], J[k] + 1, coll_bc)

	return coll_bc


def call_inclose(data):
	print(data)
	global r_new
	r_new = 0
	coll_bc = [
		[list(range(data.shape[0])), []]
	]
	coll_bc = in_close_cvc(D=data, min_rows=3, r=0, y=0, coll_bc=coll_bc)
	print('---- Results-----')
	disp_bc(coll_bc)

call_inclose(data)