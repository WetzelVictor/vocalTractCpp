N_tube = 6
N_lambda = N_tube-1

FN_old_core_h = "01_original/core.h"
FN_old_core_cpp = "01_original/core.cpp"

FN_new_core_h = "02_generated/core.h"
FN_new_core_cpp = "02_generated/core.cpp"


####################################
############# core.h ###############

# Protoypes à rentrer dans le core.h 
str_prototypes = '''
    //==========================================================================
    // New functions for the LDL.T solve update
    SpMat A;
    void ud_o_init();
    void A_update();
    void A_init();
    void RHS_update();
    Matrix<double, 5, 1> delta;
    Matrix<double, 5, 1> RHS_vec;

    Eigen::SimplicialCholesky <SpMat> solver;'''

# Includes à entrer au début du fichier
str_includes = '''
// new include ++++
#include <Eigen/SparseCholesky>
#include <Eigen/Sparse>
typedef Eigen::SparseMatrix<double> SpMat; '''

# Insertions
with open(FN_old_core_h, 'r') as old_f:
    with open(FN_new_core_h, 'w') as new_f:
        for line in old_f:
            new_f.write(line)
            if "parameters.h" in line:
                new_f.write(str_includes)
            if "void init()" in line:
                new_f.write(str_prototypes)


####################################
############ core.cpp ##############
# void VOCAL_TRACT::A_update()
str_A_update = '''void VOCAL_TRACT::A_update(){
    // Update method for matrice A (AKA matrix Q22 in doc 28)\n'''

for i in range(N_lambda):
    for j in range(N_lambda):
        if i == j:
            str_A_update += f"\t\tA.coeffRef({i},{j}) = (*mu_{i+1}_add_mu_{i+2});\n"
        if j == i-1:
            str_A_update += f"\t\tA.coeffRef({i},{j}) = 0.5*(*mu_{i+1});\n"
        if j == i+1:
            str_A_update += f"\t\tA.coeffRef({i},{j}) = 0.5*(*mu_{i+2});\n"
str_A_update += "}\n"

# void VOCAL_TRACT::A_init()
str_A_init = r'''void VOCAL_TRACT::A_init(){{
    // Init method for matrice A (AKA matrix Q22 in doc 28)
    A.resize({0}, {0}); // giving matrix the right size 
    A.reserve(3*{0} -2); // allocating memory for sparse mat
'''.format(N_lambda)

for i in range(N_lambda):
    for j in range(N_lambda):
        if i == j:
            str_A_init += f"\t\tA.insert({i},{j}) = (*mu_{i+1}_add_mu_{i+2});\n"
        if j == i-1:
            str_A_init += f"\t\tA.insert({i},{j}) = 0.5*(*mu_{i+1});\n"
        if j == i+1:
            str_A_init += f"\t\tA.insert({i},{j}) = 0.5*(*mu_{i+2});\n"
str_A_init += "}\n"

# void VOCAL_TRACT::RHS_update()
str_RHS_update ='''\tvoid VOCAL_TRACT::RHS_update(){
    // Update method for matrice B (AKA matrix Q12 in doc 28), in the RHS of
    // the auxiliary variable set of linear equations
'''

for i in range(N_lambda):
    str_RHS_update += f"\tRHS_vec({i}, 0) = (*RHS_{i+1});\n"
str_RHS_update += "}\n"

# -------------------------------------------
# void VOCAL_TRACT::ud_o_init()
# First we need to read ud_o_update()
header_ud_o = "void VOCAL_TRACT::ud_o_update()"
str_ud_o_update = "" 
to_add = '''
    // Solving implicit system of linear equations
    A_update();
    RHS_update();
    solver.compute(A);

    if(solver.info()!=Success) {
      cout << "Decomposition failed" << endl;
    }

    delta = solver.solve(RHS_vec);

    if(solver.info()!=Success) {
      cout << "Solving failed" << endl;
    }
'''

# Parsing the file for the method's implementation
B_SAVE_LINE = False
INSERT_INDEX = 4*N_tube-3

with open(FN_old_core_cpp, 'r') as FID:
    for line in FID:
        if header_ud_o in line:
            B_SAVE_LINE = True
        if f'_ud_o({INSERT_INDEX}, 0) =' in line:
            str_ud_o_update += to_add
        if B_SAVE_LINE and not '};' in line:
            str_ud_o_update += line
        if '};' in line:
            B_SAVE_LINE = False

for i in range(N_lambda):
    str_ud_o_update = str_ud_o_update.replace(f'(*RHS_{i+1})', f'delta({i}, 0)')

str_ud_o_update += '}\n'
str_ud_o_init = str_ud_o_update
replace_list = [
                ('ud_o_update', 'ud_o_init'),
                ('A_update', 'A_init'),
               ]
for key, val in replace_list:
    str_ud_o_init = str_ud_o_init.replace(key, val)

print(str_ud_o_update)

#####################
#### Writing the final file
STOP_WRITING = False
IN_INIT_METH = False

# Insertions
with open(FN_old_core_cpp, 'r') as old_f:
    with open(FN_new_core_cpp, 'w') as new_f:
        for line in old_f:
            if "void VOCAL_TRACT::ud_o_update()" in line:
                STOP_WRITING = True
                new_f.write(str_ud_o_update)
                new_f.write(str_ud_o_init)
                new_f.write(str_A_update)
                new_f.write(str_A_init)
                new_f.write(str_RHS_update)
            if 'VOCAL_TRACT::Gnl_update()' in line:
                STOP_WRITING = False
            if "void VOCAL_TRACT::init()" in line:
                IN_INIT_METH = True
            if IN_INIT_METH and 'ud_o_update()' in line:
                new_f.write(line.replace('ud_o_update()','ud_o_init()'))
            elif not STOP_WRITING:
                new_f.write(line)



