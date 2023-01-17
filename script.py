from MESAmanager import ProjectOps, MesaAccess
import glob

inlists = glob.glob("./inlists/*_inlist_*")

dsct = ProjectOps("tmp")       
dsct.create(overwrite=True, clean=True)             
dsct.make()

for i in range(5):
    dsct.loadProjInlist(inlists[i])
    dsct.run(silent=True)