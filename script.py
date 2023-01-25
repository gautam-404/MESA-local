from MESAcontroller import ProjectOps, MesaAccess
import glob

inlists = sorted(glob.glob("./inlists/*_inlist_*"))

proj = ProjectOps("dsct")       
proj.create(overwrite=False, clean=True)             
proj.make()

star = MesaAccess("dsct", astero=True)
star.load_HistoryColumns("./inlists/history_columns.list")
star.load_ProfileColumns("./inlists/profile_columns.list")

for i in range(5):
    print("Running for inlist: ", inlists[i])
    star.load_InlistProject(inlists[i])
    proj.run(silent=True)


proj.runGyre("./inlists/gyre_template.in", silent=True)
