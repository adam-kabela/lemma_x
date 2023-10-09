# Lemma X

This is a computer proof of a multigraph lemma used in the paper entitled Every 3-connected {K_{1,3}, \Gamma_3}-free graph is Hamilton-connected.
For details, see https://drive.google.com/file/d/1PqqV7z4ZNwXpxpn05da9gLBavgSXLY_v/view?usp=drive_link


## Usage

run main.py

The algorithm generates:
- plaintext full proof of the lemma in computer_generated_proof/proof.txt 
- the list of all multigraphs which satisfy the conditions of the lemma in family_F_and_hamiltonian_connectedness/F.py

run family_F_and_hamiltonian_connectedness/find_hamiltonian_paths.py (it uses F.py)

For each multigraph from F, a line graph is created. In the line graph, Hamiltonian paths between all pairs of vertices are found and listed in hamiltonian_connectedness_certificate.py

run family_F_and_hamiltonian_connectedness/verify_certificate.py (it uses hamiltonian_connectedness_certificate.py)

It verifies the Hamiltonian connectedness by checking all listed paths. Verification is much faster than finding Hamiltonian paths (the related problem is NP-complete). 


## Prerequisites

I use:
- Python 3.10.9 
- SageMath 9.6

The code should work with some older versions as well.
