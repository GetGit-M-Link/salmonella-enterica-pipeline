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
```
snakemake -n --dag | dot -Tsvg > dagsra-tools.svg
```
![DAG](https://gitlab.rlp.net/bioinformatik-praktikum-sose21/MLink/salmonella-enterica-pipeline/-/raw/main/dagsra-tools.svg)

About sra-tools:
- fastq-dump is a tool to download fastq files from the short-reads archive
- --split-files is a parameter to save paired-ended reads into two seperate files
- SRR1965341 is the barcode given in the instructions
-  -O is a parameter to specify the output directory, which is: /data/short-reads/
- Output: two files named BARCODE_1.fastq and BARCODE_2.fastq

1 = file contains “forward” reads
2 = file contains “reverse” reads

SPAdes:
```
-1 <filename>               file with forward paired-end reads
-2 <filename>               file with reverse paired-end reads
-s <filename>               file with unpaired reads
-o <output_dir> directory to store all the resulting files (required)

```
Changed from fastq-dump to fasterq-dump. Fasterq-dump is the more recent tools and also separates the unpaired reads automatically (splits into 3: forward, reverse, error)
```
rule all:
    input:
        expand("/data/short-reads/{barcodes}_{NR}.fastq",NR=["1","2"],barcodes=["SRR1965341"])
rule download_sr:
    output:
        "/data/short-reads/{barcodes}_{NR}.fastq",
    shell:
        "fasterq-dump {wildcards.barcodes} -O /data/short-reads/"
```
Upgraded sra-tools to a newer version to get access to fasterq-dump
```
conda install sra-tools=2.11.0
```
```
screen -S Spades
```
![DAG for current pipeline with SPAdes](https://gitlab.rlp.net/bioinformatik-praktikum-sose21/MLink/salmonella-enterica-pipeline/-/blob/main/dag-spades.svg)
