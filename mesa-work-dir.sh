#! /bin/zsh

## Make new MESA work directory
echo "Enter a name for your MESA work directory..." 
read DIR

create_dir()
{
    echo "Creating..."
    inp=$1
    ## Existig directory is removed while creating a
    ## new directory with the same name
    if [ -d "$inp" ]
    then 
        rm -rf $inp
    fi

    cp -R $MESA_DIR/star/work $inp
    # cp -R $MESA_DIR/star/defaults/*.list $inp
    cd $inp
    # run make in silence
    ./mk >/dev/null 2>&1
    echo "Done!"
}


if [ ! -d "$DIR" ]
then
    create_dir $DIR
else
    echo "A work directory for MESA with the same name already exists!"
    echo "Do you wish to overwrite this directory? [y/n]"
    read response
    if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]
    then
        create_dir $DIR
    else
        echo "Clean the existing work directory for re-use? [y/n]"
        read response
        if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]
        then
            ## ./clean + ./mk
            echo "Cleaning and remaking..."
            cd $DIR
            ./clean
            # run make in silence
            ./mk >/dev/null 2>&1
            echo "Done!"
        else
            echo "Skipping...Done!"
        fi
    fi
fi