# Touché23-Human-Value-Detection
DOI: https://doi.org/10.5281/zenodo.6814563
Version: 2022-07-11

Dataset for [Touché / SemEval 2023 Task 4; ValueEval: Identification of Human Values behind Arguments](https://touche.webis.de/semeval23/touche23-web). Based on the original [Webis-ArgValues-22 dataset](https://doi.org/10.5281/zenodo.5657249) accompanying the paper [Identifying the Human Values behind Arguments](https://webis.de/publications.html#kiesel_2022b), published at ACL'22.

The dataset currently contains 5220 arguments. We are, however, looking for more argument datasets (conclusion + stance + premise) to annotate and incorporate, especially datasets from different cultures and genres. Please send suggestions to our [task](mailto:valueeval@googlegroups.com) or [organizers](mailto:valueeval-organizers@googlegroups.com) mailing lists.


## Argument Corpus
The annotated corpus in tab-separated value format. Future versions of this dataset will contain more arguments and be split into "-training", "-validation", and "-testing" files to represent the corresponding sets for the evaluation.
- `arguments-training.tsv`: Each row corresponds to one argument
    - `Argument ID`: The unique identifier for the argument
    - `Conclusion`: Conclusion text of the argument
    - `Stance`: Stance of the `Premise` towards the `Conclusion`; one of "in favor of", "against"
    - `Premise`: Premise text of the argument
- `labels-training.tsv`: Each row corresponds to one argument
    - `Argument ID`: The unique identifier for the argument
    - Other: Each other column corresponds to one value category, with a 1 meaning that the argument resorts to the value category and a 0 that not
- `level1-labels-training.tsv`: The same as `labels-training.tsv` but for the 54 level 1 values of the taxonomy (used in human annotation). Though not used for the 2023 task (except for the annotation), participants can still use them in their approaches.


## Value Taxonomy
The `value-categories.json` describes the 20 value categories of this task through examples. Format:
```
{
  "<value category>": {
    "<level 1 value>": [
      "<exemplary effect a corresponding argument might target>",
      ...
    ], ...
  }, ...
}
```
The level 1 values are not used for the 2023 task (except for the annotation), but are still listed here for some might find them useful for understanding the value categories. See our paper on [Identifying the Human Values behind Arguments](https://webis.de/publications.html#kiesel_2022b) for the complete taxonomy.


## Email Update
for SemEval we decided to focus on the 20 value categories.
This task will use https://www.tira.io/ for submissions  
In short: you will be able to either submit a run file or a Docker container that runs your system.  


## Version History
- 2022-07-11
  - Exchanged the values.json from original dataset with task-specific value-categories.json

- 2022-07-09
  - Initial


## License
This dataset is distributed under [CC BY-SA 4.0](http://creativecommons.org/licenses/by-sa/4.0/).


# acl22-identifying-the-human-values-behind-arguments
[![license](https://img.shields.io/github/license/webis-de/acl22-identifying-the-human-values-behind-arguments)](https://github.com/webis-de/acl22-identifying-the-human-values-behind-arguments/blob/main/LICENSE)

Code and docker containers employed in the ACL'22 publication "[Identifying the Human Values behind Arguments](https://webis.de/publications.html#kiesel_2022b)". Use this repository to reproduce the experiments of the paper or apply the classifiers to new data.


## Setup
Requirements:
- [Docker](https://docs.docker.com/engine/installation/) for training/using the classifier
- [CUDA](https://developer.nvidia.com/cuda-downloads) and [nvidia-docker](https://github.com/NVIDIA/nvidia-docker) for GPU support
- [R](https://cran.r-project.org/) for evaluation

Download the dataset from [Zenodo](https://doi.org/10.5281/zenodo.5657250) and extract it in the main directory:
```bash
$ wget https://zenodo.org/record/6855004/files/webis-argvalues-22.zip
$ unzip webis-argvalues-22.zip
```

Download the models:
```bash
$ wget https://zenodo.org/record/6855004/files/models.zip
$ unzip models.zip
```
Or [train them yourself](#train-classification-models).


## Predict
Prediction on all arguments from `webis-argvalues-22/arguments.tsv` with `test` in the `Usage` column, or all arguments if no such column exists.
```bash
TAG=0.1.1-nocuda # or 'TAG=0.1.1-cuda11.3' if a GPU is available
GPUS="" # or 'GPUS="--gpus=all"' to use all GPUs

# Select classifiers with --classifier: "b" for BERT, "o" for one-baseline, and "s" for SVM
docker run --rm -it --init $GPUS \
  --volume "$PWD/webis-argvalues-22:/data" \
  --volume "$PWD/models:/models" \
  --volume "$PWD:/output" \
  ghcr.io/webis-de/acl22-value-classification:$TAG \
  python predict.py --classifier bos --levels "1,2,3,4a,4b"
```


## Evaluate
Calculate for each model the label-wise and mean _Precision_, _Recall_, _F1-Score_, and _Accuracy_.
```bash
$ Rscript src/R/Evaluation.R --data-dir webis-argvalues-22/ --predictions predictions.tsv
```

Note that the result does vary for BERT after re-training due to randomness in the training process. We had to re-train our models after the publication, so expect to get slightly different results to the publication even with the models we published. In our retries, however, the conclusions we draw in the publication were still valid.


## Train Classification Models
Training on all arguments from `webis-argvalues-22/arguments.tsv` with `train` in the `Usage` column, or all arguments if no such column exists.
```bash
mkdir models
TAG=0.1.1-nocuda # or 'TAG=0.1.1-cuda11.3' if a GPU is available
GPUS="" # or 'GPUS="--gpus=all"' to use all GPUs

# Select classifiers with --classifier: "b" for BERT and "s" for SVM
docker run --rm -it --init $GPUS \
  --volume "$PWD/webis-argvalues-22:/data" \
  --volume "$PWD/models:/models" \
  ghcr.io/webis-de/acl22-value-classification:$TAG \
  python training.py --classifier bs --levels "1,2,3,4a,4b"
```


## Build Docker Images
The Docker images are hosted at `ghcr.io` and will be pulled automatically by `docker run`.

If you need to change them, you can also build them:
```bash
cd src/python/
docker build -t ghcr.io/webis-de/acl22-value-classification:0.1.1-cuda11.3 --build-arg CUDA=cuda11.3 .
docker build -t ghcr.io/webis-de/acl22-value-classification:0.1.1-nocuda --build-arg CUDA=nocuda .
```


