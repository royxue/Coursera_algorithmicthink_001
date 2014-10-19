"""
Algorithmic Thinking
Week 4
Dynamic Programming
"""

def build_scoring_matrix(alphabet, diag_score, off_diag_score, dash_score):
	"""
	Computing Scoring Matrix
	"""
	all_char = list(alphabet).append('-')
	matrix = {idx_x: {idx_y: 0 for idx_y in all_char} for idx_x in all_char}
	for char in all_char:
		matrix[char][char] = diag_score
		matrix['-'][char] = dash_score
		matrix[char]['-'] = dash_score

	return matrix

def compute_alignment_matrix(seq_x, seq_y, scoring_matrix, global_flag):
	"""
	Computing Alignment Matrix
	"""
	num_x = len(seq_x) + 1
	num_y = len(seq_y) + 1
	matrix = [[0 for _ in range(num_y)] for _ in range(num_x)]

	for idx_x in range(1, num_x):
	    matrix[idx_x][0] = matrix[idx_x-1][0] + scoring_matrix[ seq_x[idx_x-1] ]['-']
	    if not global_flag:
	        matrix[idx_x][0] = max(matrix[idx_x][0], 0)

	for idx_y in range(1, num_y):
	    matrix[0][idx_y] = matrix[0][idx_y-1] + scoring_matrix['-'][ seq_y[idx_y-1] ]
	    if not global_flag:
	        matrix[0][idx_y] = max(matrix[0][idx_y], 0)

	for idx_x in range(1, num_x):
	    for idx_y in range(1, num_y):
	        vert = matrix[idx_x-1][idx_y] + scoring_matrix[ seq_x[idx_x-1] ]['-']
	        horiz = matrix[idx_x][idx_y-1] + scoring_matrix['-'][ seq_y[idx_y-1] ]
	        diag = matrix[idx_x-1][idx_y-1] + scoring_matrix[ seq_x[idx_x-1] ][ seq_y[idx_y-1] ]
	        matrix[idx_x][idx_y] = max(vert, horiz, diag)
	        if not global_flag:
	            matrix[idx_x][idx_y] = max(matrix[idx_x][idx_y], 0)

	return matrix

def compute_global_alignment(seq_x, seq_y, scoring_matrix, alignment_matrix):
    '''
    Computing global alignment
    '''
	idx_x = len(seq_x)
	idx_y = len(seq_y)
	score = alignment_matrix[idx_x][idx_y]

	alignment_x = ''
	alignment_y = ''

	while idx_x != 0 and idx_y != 0:
	    current_score = alignment_matrix[idx_x][idx_y]
	    if current_score == alignment_matrix[idx_x-1][idx_y-1] +\
	                        scoring_matrix[ seq_x[idx_x-1] ][ seq_y[idx_y-1] ]:
	        alignment_x = seq_x[idx_x-1] + alignment_x
	        alignment_y = seq_y[idx_y-1] + alignment_y

	        idx_x -= 1
	        idx_y -= 1

	    elif current_score == alignment_matrix[idx_x-1][idx_y] +\
	                          scoring_matrix[ seq_x[idx_x-1] ]['-']:
	        alignment_x = seq_x[idx_x-1] + alignment_x
	        alignment_y = '-' + alignment_y

	        idx_x -= 1

	    else:
	        alignment_x = '-' + alignment_x
	        alignment_y = seq_y[idx_y-1] + alignment_y

	        idx_y -= 1

	while idx_x != 0:
	    alignment_x = seq_x[idx_x-1] + alignment_x
	    alignment_y = '-' + alignment_y
	    idx_x -= 1

	while idx_y != 0:
	    alignment_x = '-' + alignment_x
	    alignment_y = seq_y[idx_y-1] + alignment_y
	    idx_y -= 1

	return (score, alignment_x, alignment_y)


def compute_local_alignment(seq_x, seq_y, scoring_matrix, alignment_matrix):
    '''
    Computing local alignment
    '''
	max_score = [-float('Inf'), 0, 0]

	for idx_x in range(len(alignment_matrix)):
	    for idx_y in range(len(alignment_matrix[0])):
	        if alignment_matrix[idx_x][idx_y] > max_score[0]:
	            max_score = [alignment_matrix[idx_x][idx_y], idx_x, idx_y]

	score, idx_x, idx_y = max_score
	alignment_x = ''
	alignment_y = ''

	while idx_x != 0 and idx_y != 0:
	    current_score = alignment_matrix[idx_x][idx_y]

	    if current_score <= 0:
	        break

	    if current_score == alignment_matrix[idx_x-1][idx_y-1] +\
	                        scoring_matrix[ seq_x[idx_x-1] ][ seq_y[idx_y-1] ]:
	        alignment_x = seq_x[idx_x-1] + alignment_x
	        alignment_y = seq_y[idx_y-1] + alignment_y
	        idx_x -= 1
	        idx_y -= 1
	    elif current_score == alignment_matrix[idx_x-1][idx_y] +\
	                          scoring_matrix[ seq_x[idx_x-1] ]['-']:
	        alignment_x = seq_x[idx_x-1] + alignment_x
	        alignment_y = '-' + alignment_y
	        idx_x -= 1
	    else:
	        alignment_x = '-' + alignment_x
	        alignment_y = seq_y[idx_y-1] + alignment_y
	        idx_y -= 1

	return (score, alignment_x, alignment_y)
