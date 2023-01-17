from MESAmanager import ProjectOps
import glob

inlists = glob.glob("./inlists/*_inlist_*")

dsct = ProjectOps("dsct")       
dsct.create(overwrite=True, clean=True)             
# dsct.make()

# for i in range(5):
#     dsct.loadProjInlist(inlists[i])
#     dsct.run(silent=True)