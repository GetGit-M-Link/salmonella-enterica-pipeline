## A genomics pipeline with snakemake

>Your boss is looking for a motivated student to do some reproducible data analysis on a few
>Salmonella enterica genomes they sequenced recently.

### Task 1: Salmonella: a brief introduction





#### Setup:
```
conda env create -n salmonella -f tools/environment.yml
conda activate salmonella
```
#### Usage Instructions


#### Results



#### Creation Diary
- setup a conda environment from yml file
- created a folder strucutre and README
- Read about sra-tools [here](https://eaton-lab.org/articles/sra-downloads/) -> tool fastq-dump for downloading fastq files
- Read about SPAdes [here] (https://github.com/ablab/spades)
- State of tools and version at this time [here](https://gitlab.rlp.net/bioinformatik-praktikum-sose21/MLink/salmonella-enterica-pipeline/-/blob/main/tools/tools-state-after-first-tools-install)
- ran `fastq-dump --split-files SRR1965341 -O /data/short-reads/` to find out what the output files look like
- wrote first rule in Snakefile:
 ```
 rule download_sr:
    output:
        "/data/short-reads/SRR1965341_1.fastq",
        "/data/short-reads/SRR1965341_2.fastq"
    shell:
        "fastq-dump --split-files SRR1965341 -O /data/short-reads/"
```
- Expand Snakefile to allow for variable barcodes:
```
rule all:
    input:
        expand("/data/short-reads/{barcodes}_{NR}.fastq",NR=["1","2"],barcodes=["SRR1965341"])
rule download_sr:
    output:
        "/data/short-reads/{barcodes}_1.fastq",
        "/data/short-reads/{barcodes}_2.fastq"
    shell:
        "fastq-dump --split-files {wildcards.barcodes} -O /data/short-reads/"
```
- Install Graphviz to generate pretty picture
```
conda install graphviz
```

