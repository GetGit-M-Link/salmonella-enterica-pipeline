rule all:
    input:
        expand("/data/short-reads/{barcodes}_{NR}.fastq",NR=["1","2"],barcodes=["SRR1965341"])
rule download_sr:
    output:
        "/data/short-reads/{barcodes}_{NR}.fastq",
    shell:
        "fastq-dump --split-files {wildcards.barcodes} -O /data/short-reads/"
