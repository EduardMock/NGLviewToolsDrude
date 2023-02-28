
import nglview as nv 
import IPython.display as display
import numpy as np
import MDAnalysis as mda




def remove_groups(u, drude=True,prot=True,fluor=True):
    watch = u.atoms
    if drude:
        drudes = u.select_atoms("type DRUD ")
        watch -= drudes
    if prot:
        protons =  u.select_atoms("type H*")
        watch -= protons
    if fluor:
        protons =  u.select_atoms("type F*")
        watch -= protons
    return watch


def rotate_view(view, x=0, y=0, z=0, degrees=True):
    radians = 1
    if degrees: radians = np.pi / 180
    view.control.spin([1, 0, 0], x*radians)
    view.control.spin([0, 1, 0], y*radians)
    view.control.spin([0, 0, 1], z*radians)



def build_hhvecs(u,list):
    vecs=dict()
    for h in list:
        at1=u.select_atoms(f"name {h[0]}")
        at2=u.select_atoms(f"name {h[1]}")
        at1_at2=mvec.get_vecarray(universe=u, agrp=at1, bgrp=at2, pbc=False)
        vecs[f"{h[0]}_{h[1]}"]= at1_at2
    return vecs

def add_axis(view):
    view.shape.add_arrow([-4, -4, -4], [0, -4, -4], [1, 0, 0], 0.5, "x-axis")
    view.shape.add_arrow([-4, -4, -4], [-4, 0, -4], [0, 1, 0], 0.5, "y-axis")
    view.shape.add_arrow([-4, -4, -4], [-4, -4, 0], [0, 0, 1], 0.5, "z-axis")
    # view.update_representation(repr_type='shape', color='black', opacity=0.5)

def bonds_woD(atomlist):
    
    bond_dict=atomlist.atoms.bonds.topDict
    bonds_woD_dict= dict()
    bonds_woD= list()
        
        
    for key in bond_dict.keys():
        if key[1] != 'DRUD' and  'H' in key[1]  or 'F' in key[1] : 
            bonds_woD_dict[key]=[]
            for k in bond_dict[key]:
                bonds_woD_dict[key].append( list(k.atoms.names))
                bonds_woD.append( list(k.atoms.names))

    
    return bonds_woD, bonds_woD_dict


def update_vdw_radii(u):
    for atom in u.atoms:
        if atom.name in vdwradii.keys():
            atom.radius=vdwradii[atom.name]
    return u

# update vdw radii for FY
# vdwradii={ "FY":0.5}

import time
import threading


def save_rep(v, outfilename):
    def generate_images(v, outfilename):
        im = v.render_image()
        while not im.value:
            time.sleep(0.1)
        with open(f'{outfilename}', 'wb') as fh:
            fh.write(im.value)

    thread = threading.Thread(target=generate_images(v=v,outfilename=outfilename))
    thread.daemon = True
    thread.start()





