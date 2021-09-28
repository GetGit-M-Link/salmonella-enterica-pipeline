 configfile: "config.yaml"
def optional_input(filepath):
   if os.path.exists(filepath):
      return "-s " + filepath
   else:
      return ""
rule all:
    input:
        expand("/data/assembled/{barcodes}/{value_of_k}/contigs.fasta",value_of_k=config["VALUE_OF_K"],barcodes=config["BARCODES"]),
        expand("/data/assembled/{barcodes}_trimmed/{value_of_k}/contigs.fasta",value_of_k=config["VALUE_OF_K"],barcodes=config["BARCODES"]),
        "data/Analysis.md"
rule download_sr:
    output:
        "/data/short-reads/{barcodes}_1.fastq",
        "/data/short-reads/{barcodes}_2.fastq"
    threads: 6
    shell:
        "fasterq-dump {wildcards.barcodes} -O /data/short-reads/ -t /data/sra-tools-temp"
rule adapter_trimming:
    input:
        "/data/short-reads/{barcodes}_1.fastq",
        "/data/short-reads/{barcodes}_2.fastq"

    output:
        "/data/trimmed/{barcodes}_1.fastq",
        "/data/trimmed/{barcodes}_2.fastq"
    shell:
        """
        cutadapt -a file:tools/adapter.fasta -A file:tools/adapter.fasta -o {output} {input} -j 0
        """
rule SPAdes_untrimmed:
    input:
        forward_1 = ["/data/short-reads/{barcodes}_1.fastq".format(barcodes=barcodes) for barcodes in config["BARCODES"]],
        reverse_2 = ["/data/short-reads/{barcodes}_2.fastq".format(barcodes=barcodes) for barcodes in config["BARCODES"]]
    output:
        "/data/assembled/{barcodes}_untrimmed/{value_of_k}/contigs.fasta"
    params:
        optional=optional_input("/data/short-reads/{barcodes}.fastq")    
    shell:
       "spades.py -k {wildcards.value_of_k} -1 {input.forward_1} -2 {input.reverse_2} {params.optional} -o /data/assembled/{wildcards.barcodes}/{wildcards.value_of_k}/"
rule SPAdes_trimmed:
    input:
        forward_1 = "/data/trimmed/{barcodes}_1.fastq",
        reverse_2 = "/data/trimmed/{barcodes}_2.fastq"
    output:
        "/data/assembled/{barcodes}_trimmed/{value_of_k}/contigs.fasta"
    shell:
       "spades.py -k {wildcards.value_of_k} -1 {input.forward_1} -2 {input.reverse_2} -o /data/assembled/{wildcards.barcodes}/{wildcards.value_of_k}/"
rule analysis:
    input:
        "/data/assembled/{barcodes}_trimmed/{value_of_k}/contigs.fasta",
        "/data/assembled/{barcodes}/{value_of_k}/contigs.fasta"
    output:
        "/plots/{barcodes}_{value_of_k}.png"
    shell:
        "python3 scripts/statistics.py /data/assembled/"

