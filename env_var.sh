# export MESASDK_ROOT=/workspace/MESA-local/software/mesasdk
# source $MESASDK_ROOT/bin/mesasdk_init.sh
# export MESA_DIR=/workspace/MESA-local/software/mesa-r15140
# export OMP_NUM_THREADS=8      ## max should be 2 times the cores on your machine
# export GYRE_DIR=$MESA_DIR/gyre/gyre

echo "export MESASDK_ROOT=/workspace/MESA-local/software/mesasdk" >> ~/.bashrc
echo "source \$MESASDK_ROOT/bin/mesasdk_init.sh" >> ~/.bashrc
echo "export MESA_DIR=/workspace/MESA-local/software/mesa-r15140" >> ~/.bashrc
echo "export OMP_NUM_THREADS=8" >> ~/.bashrc
echo "export GYRE_DIR=\$MESA_DIR/gyre/gyre" >> ~/.bashrc
