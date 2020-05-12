str_include = '''
// new include ++++
#include <Eigen/SparseCholesky>
typedef Eigen::SparseMatrix<double> SpMat; // declares a column-major sparse matrix type of double
'''

str_comment_prototypes = '''\t\t//==========================================================================
    // Added objects for implicit constrained variables solving
    '''

str_method_prototypes = ''' \t\tvoid update_A();
\t\tSpMat<N_lambda, N_lambda> A;
'''


with open('core.h', 'r') as old_f:
    with open('new_core.h', 'w') as new_f:
        for line in old_f:
            new_f.write(line)
            if "parameters.h" in line:
                new_f.write(str_include)
            if "void init()" in line:
                new_f.write(str_comment_prototypes + str_method_prototypes)
