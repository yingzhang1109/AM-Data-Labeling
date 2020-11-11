# AM-Data-Labeling
## Prepare voxelaztion files
To voxelize the STL files, binvox(https://www.patrickmin.com/binvox/) is recommended here.

## Label the data which is failed (One potential method)

modify the path in file 'from_binvox_to_vxc.py' to your local directory.
Then, run

```
python from_binvox_to_vxc.py
```

to generate vxc file format in order to be opened in VoxCad(https://www.creativemachineslab.com/voxcad.html)
