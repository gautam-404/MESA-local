from MESAmanager import ProjectOps
import glob

inlists = sorted(glob.glob("./inlists/*_inlist_*"))

dsct = ProjectOps("dsct")       
dsct.create(overwrite=True, clean=True)             
dsct.make()


for i in range(5):
    print("Running for inlist: ", inlists[i])
    dsct.loadProjInlist(inlists[i])
    dsct.run(silent=True)
