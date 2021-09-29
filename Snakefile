 configfile: "config.yaml"
def optional_input(filepath):
   if os.path.exists(filepath):
      return "-s " + filepath
   else:
      return ""
rule all:
    input:
        #expand("/data/assembled/{barcodes}_untrimmed/{value_of_k}/contigs.fasta",value_of_k=config["VALUE_OF_K"],barcodes=config["BARCODES"]),
        #expand("/data/assembled/{barcodes}_trimmed/{value_of_k}/contigs.fasta",value_of_k=config["VALUE_OF_K"],barcodes=config["BARCODES"]),
        expand("/plots/{barcodes}_untrimmed_{value_of_k}.png",value_of_k=config["VALUE_OF_K"],barcodes=config["BARCODES"]),
        expand("/plots/{barcodes}_trimmed_{value_of_k}.png",value_of_k=config["VALUE_OF_K"],barcodes=config["BARCODES"])
rule download_sr:
    output:
        "/data/short-reads/{barcodes}_1.fastq",
        "/data/short-reads/{barcodes}_2.fastq"
    threads: 6
    shell:
        "fasterq-dump {wildcards.barcodes} -O /data/short-reads/ -t /data/sra-tools-temp"
rule adapter_trimming:
    input:
        i_1 = "/data/short-reads/{barcodes}_1.fastq",
        i_2 = "/data/short-reads/{barcodes}_2.fastq"

    output:
        o_1 = "/data/trimmed/{barcodes}_1.fastq",
        o_2 = "/data/trimmed/{barcodes}_2.fastq"
    shell:
        """
        cutadapt -a file:tools/adapter.fasta -A file:tools/adapter.fasta -o {output.o_1} -p {output.o_2}  {input.i_1} {input.i_2} -j 0
        """
rule SPAdes_untrimmed:
    input:
        forward_1 = "/data/short-reads/{barcodes}_1.fastq",
        reverse_2 = "/data/short-reads/{barcodes}_2.fastq"
    output:
        "/data/assembled/{barcodes}_untrimmed/{value_of_k}/contigs.fasta"
    params:
        optional=optional_input("/data/short-reads/{barcodes}.fastq")    
    shell:
       "spades.py -k {wildcards.value_of_k} -1 {input.forward_1} -2 {input.reverse_2} {params.optional} -o /data/assembled/{wildcards.barcodes}_untrimmed/{wildcards.value_of_k}/"
rule SPAdes_trimmed:
    input:
        forward_1 = "/data/trimmed/{barcodes}_1.fastq",
        reverse_2 = "/data/trimmed/{barcodes}_2.fastq"
    output:
        "/data/assembled/{barcodes}_trimmed/{value_of_k}/contigs.fasta"
    shell:
       "spades.py -k {wildcards.value_of_k} -1 {input.forward_1} -2 {input.reverse_2} -o /data/assembled/{wildcards.barcodes}_trimmed/{wildcards.value_of_k}/"
rule analysis:
    input:
        expand("/data/assembled/{barcodes}_untrimmed/{value_of_k}/contigs.fasta",value_of_k=config["VALUE_OF_K"],barcodes=config["BARCODES"]),
        expand("/data/assembled/{barcodes}_trimmed/{value_of_k}/contigs.fasta",value_of_k=config["VALUE_OF_K"],barcodes=config["BARCODES"]),
    output:
        expand("/plots/{barcodes}_untrimmed_{value_of_k}.png",value_of_k=config["VALUE_OF_K"],barcodes=config["BARCODES"]),
        expand("/plots/{barcodes}_trimmed_{value_of_k}.png",value_of_k=config["VALUE_OF_K"],barcodes=config["BARCODES"])
    shell:
        "python3 scripts/statistics.py /data/assembled/"

