wildcard_constraints:
  barcodes="SRR\d+",
  long_barcodes="SRR\d+"
#restrains barcodes to only consist of SRR + numbers

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
        expand("plots/{barcodes}_untrimmed_{value_of_k}.png",value_of_k=config["VALUE_OF_K"],barcodes=config["BARCODES"]),
        expand("plots/{barcodes}_trimmed_{value_of_k}.png",value_of_k=config["VALUE_OF_K"],barcodes=config["BARCODES"]),
        expand("plots/{long_barcodes}.png",long_barcodes=config["LONG_BARCODES"]),
        expand("/data/long_read_assembled/{long_barcodes}/contigs.fasta",long_barcodes=config["LONG_BARCODES"]),
        "plots/advanced/N50.png"
rule download_sr_paired:
    output:
        "/data/short-reads/{barcodes}_1.fastq",
        "/data/short-reads/{barcodes}_2.fastq"
    threads: 6
    shell:
        "fasterq-dump {wildcards.barcodes} -O /data/short-reads/ -t /data/sra-tools-temp"
rule download_sr_single:
    output:
        "/data/short-reads_single/{long_barcodes}.fastq"
    threads: 6
    shell:
        "fasterq-dump {wildcards.long_barcodes} -O /data/short-reads_single/ -t /data/sra-tools-temp"
rule long_read_preprocess:
    input:
        "/data/short-reads_single/{long_barcodes}.fastq"
    output:
        "/data/long_read_preprocessed/{long_barcodes}.paf.gz"
    log:
        "logs/minimap2/{long_barcodes}.log"
    shell:
        """
        minimap2 -x ava-ont -t8 {input} {input} | gzip -1 > {output}
        """
rule assemble_long_reads:
    input:
        preprocessed="/data/long_read_preprocessed/{long_barcodes}.paf.gz",
        raw_reads="/data/short-reads_single/{long_barcodes}.fastq"
    output:
        "/data/long_read_assembled/{long_barcodes}/contigs.gfa"
        
    log:
        "logs/miniasm/{long_barcodes}.log"
    shell:
        """
        miniasm -f {input.raw_reads} {input.preprocessed} > {output}
        """
rule gfa_to_fasta:
    input:
        "/data/long_read_assembled/{long_barcodes}/contigs.gfa"
    output:
        "/data/long_read_assembled/{long_barcodes}/contigs.fasta"
    log:
        "logs/awk/{long_barcodes}.log"
    shell:
        """
        awk '/^S/{{print \">\"$2"\\n\"$3}}' {input} | fold > {output}
        """
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
        expand("/data/long_read_assembled/{long_barcodes}/contigs.fasta",long_barcodes=config["LONG_BARCODES"])
    output:
        expand("plots/{barcodes}_untrimmed_{value_of_k}.png",value_of_k=config["VALUE_OF_K"],barcodes=config["BARCODES"]),
        expand("plots/{barcodes}_trimmed_{value_of_k}.png",value_of_k=config["VALUE_OF_K"],barcodes=config["BARCODES"]),
        expand("plots/{long_barcodes}.png",long_barcodes=config["LONG_BARCODES"]),
        "data/best_data.txt"
    shell:
        "python3 scripts/statistics.py /data/assembled/ /data/long_read_assembled/"
rule comparative_analysis:
    input:
        "data/best_data.txt"
    output:
        "plots/advanced/N50.png"
    shell:
        "python3 scripts/advanced_statistics.py"
