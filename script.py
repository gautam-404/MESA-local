from MesaHandler.MesaProjHandler import ProjectOps
from MesaHandler import MesaAccess
from alive_progress import alive_bar

dsct = ProjectOps("dsct")       
dsct.create(overwrite=False, clean=True)    
dsct.clean()            

# with alive_bar(unknown="waves") as bar:
#     for i in range(6):
#         dsct.loadProjInlist( "inlists/%i_test"%(i+1) )
#         dsct.make()
#         dsct.run(silent=True)
#         bar()


# dsct.rerun("x450")
# dsct.clean()              ## Clean the project
