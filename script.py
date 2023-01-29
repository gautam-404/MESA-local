from MESAcontroller import ProjectOps, MesaAccess
import glob

inlists = sorted(glob.glob("./inlists/*_inlist_*"))

proj = ProjectOps("test")     
proj.create(overwrite=False, clean=True)             
proj.make()

star = MesaAccess("test")
star.load_HistoryColumns("./inlists/history_columns.list")
star.load_ProfileColumns("./inlists/profile_columns.list")

for i in range(5):
    print("Inlist: ", inlists[i], "\n")
    star.load_InlistProject(inlists[i])
    # star.set("pgstar_flag", True)
    proj.run(silent=True)

proj.runGyre(gyre_in="./inlists/gyre_template.in", files='all')
