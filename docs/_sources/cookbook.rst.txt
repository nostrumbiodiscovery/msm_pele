===============
Getting Started
===============

.. toctree::
   :maxdepth: 2

These MSM Pele cookbook shows how to use basics of the platform and walk you
through your first steps.

Launch your first MSM job
---------------------------

**Previous Requisites**

- Binded ligand-receptor pdb file if using OPLS2005 charges.
- Binded .mae ligand file on the same reference space than the receptor pdb file.

**Launch MSM_Pele with OPLS charges (pdb file)**::

    python2.X main.py PDB ligand_resname ligand_chain --cpus X


**Launch MSM_Pele with QM charges (receptor pdb and ligand as .mae)**::

    python2.X main.py receptor_PDB ligand_resname ligand_chain --mae_lig ligand.mae --cpus X

