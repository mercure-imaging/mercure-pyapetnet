FROM continuumio/miniconda3
RUN conda update -n base -c defaults conda
ADD docker-entrypoint.sh ./
RUN chmod 777 ./docker-entrypoint.sh

RUN conda create -n env python>=3.10
RUN echo "source activate env" > ~/.bashrc
ENV PATH /opt/conda/envs/env/bin:$PATH
RUN chmod -R 777 /opt/conda/envs
ADD environment.yml ./
RUN conda env create -f ./environment.yml

# Pull the environment name out of the environment.yml
RUN echo "source activate $(head -1 ./environment.yml | cut -d' ' -f2)" > ~/.bashrc
ENV PATH /opt/conda/envs/$(head -1 ./environment.yml | cut -d' ' -f2)/bin:$PATH

RUN chmod -R 777 ./
CMD ["./docker-entrypoint.sh"]