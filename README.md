# PyCaver

`python caver.py -i example/input/5mdl.pdb -o example/output/ -t example/tmp --starting_point_coordinates 0,0,0 --probe_radius 1.0 -G`

# TODOs
[/] custom config!!!
[X] log file option
[ ] verbose option
[X] graph option
[ ] bottleneckdiagram
[ ] multifile
[ ] pdb wise in folder
[ ] create ./install.sh

## Graph Option -G
The resulting Tunnels are merged and saved into a meta-tunnel graph which starts a the root node (the starting point of the calculation). The leaves are therefore the surface connections.


@article{caver-3_0,
    author = "Eva Chovancov\'{a}, Anton\'{i}n Pavelka, Petr Bene\v{s},  Ond\v{r}ej Strnad, Jan Brezovsk\'{y}, Barbora Kozl\'{i}kovÄ‚Ë‡, Artur Gora, Vil\'{e}m \v{S}ustr, Martin Klva\v{n}a, Petr Medek, Lada Biedermannov\'{a}, Ji\v{r}\'{i} Sochor and Ji\v{r}\'{i} Damborsk\'{y}",
    title = "CAVER 3.0: A Tool for the Analysis of Transport Pathways in Dynamic Protein Structures",
    journal = "Pathways in Dynamic Protein Structures, PLoS Computational Biology 8: e1002708",
    year = "2012"
}

