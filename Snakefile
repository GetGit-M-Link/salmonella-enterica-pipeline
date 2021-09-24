rule all:
    input:
        expand("/data/short-reads/{barcodes}_1.fastq",barcodes=["SRR1965341"]),
        expand("/data/short-reads/{barcodes}_2.fastq",barcodes=["SRR1965341"])
rule download_sr:
    output:
        "/data/short-reads/{barcodes}_1.fastq",
        "/data/short-reads/{barcodes}_2.fastq"
    shell:
        "fasterq-dump {wildcards.barcodes} -O /data/short-reads/"
