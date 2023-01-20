#!/usr/bin/env python
import os
import yaml
import sys
import glob
import subprocess
from datetime import date


def SMILE_Preprocessor(MOL, SmileCode):
    """
    Process 
    -------------------------
    1. create PDB from smile code
    2. fix PDB file with right labels

    INPUT
    -------------------------
    SmileCode = Code to create all-atom model


    OUTPUT
    -------------------------
    1. Creates SMILES code into PDB and xyz file with the name StructureOutput
    """
    # Create Smilecode file to use later.
    with open("{}smile.txt".format(MOL), 'w') as outfile:
        outfile.write(SmileCode)

    subprocess.run(["obabel", "-:{}".format(SmileCode), "-O", "{}tmp.pdb".format(MOL),
                   "--gen3d", "--ff", "GAFF"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    if os.path.isfile("{}tmp.pdb".format(MOL)):
        print('Obabel Finished successfully')

    AtomsDictionary = {}
    with open('{}tmp.pdb'.format(MOL), 'r') as infile:
        LabelCoordinate = []
        Labels = []
        for line in infile:
            if 'HETATM' in line:
                column = line.split()
                Label = column[2]
                coordinate = line[20:80]
                Labels.append(Label)
                LabelCoordinate.append([Label, coordinate])

        Elements = list(sorted(set(Labels)))

        print('PDB has {} elements'.format(Elements))
        for element in Elements:
            ElementList = []
            for idx in range(0, len(LabelCoordinate)):

                if element in LabelCoordinate[idx]:
                    # print(LabelCoordinate[idx])
                    ElementList.append(LabelCoordinate[idx])
            # print(ElementList)
            for id, info in enumerate(ElementList):
                #print(id, info)
                AtomsDictionary[str(info[1])] = '{}{}'.format(
                    info[0], str(id+1))

    with open('{}.pdb'.format("StructureOutput"), 'w') as outfile:
        Coords = []
        with open('{}tmp.pdb'.format(MOL), 'r') as infile:
            for line in infile:
                if 'HETATM' in line:
                    column = line.split()
                    coordinate = line[20:80]
                    Coords.append(coordinate)

        # Write new PDB file
        outfile.write("REMARK temporal PDB for parameterization \n")
        outfile.write("AUTHOR SMILE2PDB " + str(date.today()) + " \n")
        for ai in range(0, len(Coords)):
            if ai < 9:
                if int(AtomsDictionary.get(Coords[ai])[1:]) < 10:
                    PDBline = "ATOM      " + \
                        str(ai+1) + "  " + \
                        AtomsDictionary.get(
                            Coords[ai]) + "  " + MOL + Coords[ai] + " \n"
                else:
                    PDBline = "ATOM      " + \
                        str(ai+1) + "  " + \
                        AtomsDictionary.get(
                            Coords[ai]) + " " + MOL + Coords[ai] + " \n"

            elif ai >= 99:
                if int(AtomsDictionary.get(Coords[ai])[1:]) < 10:
                    PDBline = "ATOM    " + \
                        str(ai+1) + "  " + \
                        AtomsDictionary.get(
                            Coords[ai]) + "  " + MOL + Coords[ai] + " \n"
                else:
                    PDBline = "ATOM    " + \
                        str(ai+1) + "  " + \
                        AtomsDictionary.get(
                            Coords[ai]) + " " + MOL + Coords[ai] + " \n"

            else:
                if int(AtomsDictionary.get(Coords[ai])[1:]) < 10:
                    PDBline = "ATOM     " + \
                        str(ai+1) + "  " + \
                        AtomsDictionary.get(
                            Coords[ai]) + "  " + MOL + Coords[ai] + " \n"
                else:
                    PDBline = "ATOM     " + \
                        str(ai+1) + "  " + \
                        AtomsDictionary.get(
                            Coords[ai]) + " " + MOL + Coords[ai] + " \n"

            outfile.write(PDBline)
        outfile.write("END")
        subprocess.run(["obabel", "-i", "pdb", "{}tmp.pdb".format(MOL), "-o", "xyz", "-O",
                       "{}.xyz".format("StructureOutput")], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        os.system("rm {}tmp.pdb".format(MOL))

# -------------MAIN-----------


settings = {}

with open('rendered_wano.yml', 'r') as file:
    wano_file = yaml.full_load(file)
    settings['SMILECode'] = wano_file['SMILES-CODE']


SMILE_Preprocessor('MOL', settings.get('SMILECode'))
