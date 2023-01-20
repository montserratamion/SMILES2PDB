When publishing results obtained with SMILES2PDB WaNo, please consider to cite

# SMILES2PDB

<img src="SIMONA-DHscan.png"  width="10%">

This WaNo:

1. Generate PDB and xyz molecule coordinates from SMILES code. 


## 1. Software Setup


To get this workflow up running on your available computational resources, make sure to have the below libraries installed on Python 3.6 or newer.

```
1.Open Babel

```

We recomend to use Anaconda env.

### SIMONA set up

If there is an specific python env where Open Babel is running modify the SMILES2PDB.xml file accordingly in the executable section.

``` 
 <WaNoExecCommand>

    <!-- Here add Anconda env and/or modules to excute WaNo -->
        python SMILES2PDB.py

</WaNoExecCommand>

```

## 2. Inputs

After dragging the WaNo in the workflow space, just provide a SMILES code (with no space or quotes).

For example: CCCC

Then save and run the workflow and the outputs will be generated
