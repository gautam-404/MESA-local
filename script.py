from MesaHandler.MesaProjHandler import ProjectOps
from MesaHandler import MesaAccess
import glob
from alive_progress import alive_bar

inlists = glob.glob("inlists/*_inlist_*")

dsct = ProjectOps("dsct")       
dsct.create(overwrite=True, clean=True)             
dsct.make()

with alive_bar(unknown="waves2", spinner="dots") as bar:
    for i in range(5):
        dsct.loadProjInlist(inlists[i])
        dsct.run(silent=True)
        file = open("/workspace/MESA/dsct/runlog", "a")  # append mode
        file.write( "\n\n"+("*"*100)+"\n\n" )
        file.close()
        bar()
