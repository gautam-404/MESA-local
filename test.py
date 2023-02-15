from MESAcontroller import MesaAccess, ProjectOps

proj = ProjectOps("test")
proj.create(overwrite=True)
star = MesaAccess("test")
star.load_InlistProject("inlists/inlist_12M_sch_rot03_prems")
star.load_HistoryColumns("inlists/history_columns.list")
proj.make()
proj.run()