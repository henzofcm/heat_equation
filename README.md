# Let's solve the heat equation with Python!

As this is part of my Linear Algebra courses final exam, I try to use most of the techniques learned so far by solving numerically the one and two-dimensional heat equations using python.
Basically we used only the difference matrix and its eigenvalues to resolve the PDE, wich is just the explicit finite element method.

Some different boundary conditions were added so you can also analize the diffusions behaviour in all its aspects.

## Results

![Common 1D solution](./img/heat_1d_animation.gif)

Inside the `.\src\` directory you will find each module. Just run them and the equation with your usual boundary conditions will be solved, generating the images in `.\img\`.
