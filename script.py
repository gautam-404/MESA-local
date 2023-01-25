from MESAcontroller import ProjectOps, MesaAccess
import glob

inlists = sorted(glob.glob("./inlists/*_inlist_*"))

proj = ProjectOps("dsct")       
# proj.create(overwrite=True, clean=True)             
# proj.make()

# star = MesaAccess("dsct2", astero=True)

# for i in range(5):
#     print("Running for inlist: ", inlists[i])
#     star.load_InlistProject(inlists[i])
#     proj.run(silent=True)

# profs = sorted(glob.glob("./dsct/LOGS/*profile*.data.FGONG"))

# for i in range():
#     print("Running for inlist: ", inlists[i])
#     proj.load_InlistProject(inlists[i])
#     proj.run(silent=True)
proj.runGyre("./inlists/gyre_template.in", silent=True)
