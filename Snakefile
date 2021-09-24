 configfile: "config.yaml"
def optional_input(filepath):
   if os.path.exists(filepath):
      return "-s " + filepath
   else:
      return ""
rule all:
    input:
        expand("/data/assembled/{barcodes}/{value_of_k}/contigs.fasta",value_of_k=config["VALUE_OF_K"],barcodes=config["BARCODES"])
rule download_sr:
    output:
        "/data/short-reads/{barcodes}_1.fastq",
        "/data/short-reads/{barcodes}_2.fastq"
    threads: 6
    shell:
        "fasterq-dump {wildcards.barcodes} -O /data/short-reads/ -t /data/sra-tools-temp"
rule SPAdes:
    input:
        forward_1 = "/data/short-reads/{barcodes}_1.fastq",
        reverse_2 = "/data/short-reads/{barcodes}_2.fastq"
    output:
        "/data/assembled/{barcodes}/{value_of_k}/contigs.fasta"
    params:
        optional=optional_input("/data/short-reads/{barcodes}.fastq")    
    shell:
       "spades.py -k {wildcards.value_of_k} -1 {input.forward_1} -2 {input.reverse_2} params.optional -o /data/assembled/{wildcards.barcodes}/{wildcards.value_of_k}/"

