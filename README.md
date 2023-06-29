# **mercure-pyapetnet**
<br>

Mercure module to deploy [pyapetnet](https://github.com/gschramm/pyapetnet) - a convolutional neural network (CNN) to mimick the behavior of anatomy-guided PET reconstruction in image space. This module runs as a docker container in mercure, it can be added to an existing mercure installation using docker tag : *mercureimaging/mercure-pyapetnet*. The module will run with the pyapetnet **S2_osem_b10_fdg_pe2i** trained model by default.

<br>

## **Installation**

### Add module to existing mercure installation
Follow instructions on [mercure website](https://mercure-imaging.org) on how to add a new module. Use the docker tag mercureimaging/mercure-pyapetnet.

<br>

### Build module for local testing, modification and development
1. Clone repo.
2. Build Docker container locally by running make (modify makefile with new docker tag as needed).
3. Test container :\
`docker run -it -v /input_data:/input -v /output_data:/output --env MERCURE_IN_DIR=/input  --env MERCURE_OUT_DIR=/output mercureimaging/mercure-pyapetnet`

<br>

## **Configuration**

### Enforce MRI and PET series filtering
The mercure-pyapetnet module requires that mercure provides a single MRI series and a single PET series for processing. Therefore, it is important that the processing rules are configured to filter out any surplus data received by mercure, an example is shown in the screenshot below where the rule will select series containing 'MPRAGE' or 'PET_AC' in the series description, and processing will be triggered when both series have been received. More information on mercure rule configuration can be found [here.](https://mercure-imaging.org/docs/usage.html)

<br>
<br>

![image](https://github.com/mercure-imaging/mercure-pyapetnet/assets/61509531/96f2c5c4-05ff-482f-811c-c91d8466632c)


<br>
<br>

### Selecting different trained models
By default the module will select the pyapetnet **S2_osem_b10_fdg_pe2i** trained model. Other models can be selected easily in the processing module 'Settings' tab as show in the screenshot below.

<br>
<br>

![image](https://github.com/mercure-imaging/mercure-pyapetnet/assets/61509531/6c1fa463-d563-47dc-a252-b9f5f4a196a5)

<br>
<br>


