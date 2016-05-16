import h5py
import numpy as np


def create_level(res, n_resolutions, parent_cell):
    if res >= n_resolutions:
        return
    parent_name = parent_cell.name
    cell_name_prefix = (parent_name.split('/'))[-1]
    for i in range(10):
        cell = parent_name + '/'+ cell_name_prefix + str(i)
        new_cell  = parent_cell.create_group(cell)
        create_level(res+1, n_resolutions, new_cell)

def create_dggs_hierarchy(n_resolutions):
    cur_res = 0
    f_dggs = h5py.File("/short/ir5/yxs659/data/dggs_hierarchy.hdf5", "w")
    l_0 = ['N','O','P','Q','R','S']
    for cell in l_0:
        #create_cell_groups(f_dggs, cell)
        new_cell  = f_dggs.create_group(cell)
        create_level(cur_res+1, n_resolutions, new_cell)
    return f_dggs


f_dggs = create_dggs_hierarchy(3)
#new_cell=f_dggs.create_group('/abc/cdf/e') 
#new1=new_cell.create_group('q')
#print(new1.name)
