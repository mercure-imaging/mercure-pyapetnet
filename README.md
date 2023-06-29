# **mercure-pyapetnet**
<br>

Mercure module to deploy [pyapetnet](https://github.com/gschramm/pyapetnet) - a convolutional neural network (CNN) to mimick the behavior of anatomy-guided PET reconstruction in image space. This module runs as a docker container in mercure, it can be added to an existing mercure installation using docker tag : *mercureimaging/mercure-pyapetnet*.
<br>

# Installation

## Add module to existing mercure installation
Follow instructions on [mercure website](https://mercure-imaging.org) on how to add a new module. Use the docker tag *mercureimaging/mercure-pyapetnet*.

<br>

## Build module for local testing, modification and development
1. Clone repo.
2. Build Docker container locally by running make (modify makefile with new docker tag as needed).
3. Test container :\
`docker run -it -v /input_data:/input -v /output_data:/output --env MERCURE_IN_DIR=/input  --env MERCURE_OUT_DIR=/output *mercureimaging/mercure-pyapetnet*`

<br>
