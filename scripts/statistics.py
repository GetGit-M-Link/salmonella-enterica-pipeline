#!/usr/bin/env python3
"""
Setup
"""
import os
import sys
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


class Assembly:
    def __init__(self, contigs_fasta_filename, log_filename, k_value, barcode):
        # path to contigs.fasta file
        self.contigs_fasta_filename = contigs_fasta_filename
        # path to spades.log file
        self.log_filename = log_filename
        # list of contig length in contig.fasta
        self.contig_lengths = get_contig_lengths(contigs_fasta_filename)
        # average read length of input files for spades assembly (queried from spades.log)
        self.avg_read_length = read_avg_read_length(log_filename)
        # average contigs length (calculated from contigs.fasta)
        self.avg_contigs_length = calc_avg_contig_length(self.contig_lengths)
         # total number of contigs (counted in contigs.fasta)
        self.totl_nr_contigs = len(self.contig_lengths)
        # Shortest contig in contigs.fasta
        self.shortest_contig = min(self.contig_lengths)
        # Longest contig in contigs.fasta
        self.longest_contig = max (self.contig_lengths)
        # N50 calculated from contig.fasta
        self.N50_all_contigs = calculate_N50(self.contig_lengths)
        # N50 for all contigs longer than 300bp from contigs.fasta
        self.N50_contigs_over_300 = calculate_N50_bigger_300(self.contig_lengths)
        self.barcode = barcode
        self.k_value = k_value
    def __str__(self):
        return f"""# statistics analysis for barcode: {self.barcode} assembled with SPAdes with parameter k = {self.k_value}  
        average contig length: {self.avg_contigs_length}  
        total number of contigs: {self.totl_nr_contigs}  
        shortest contig: {self.shortest_contig}  
        longest contig: {self.longest_contig}  
        N50 of all contigs: {self.N50_all_contigs}  
        N50 of all contigs over 300 bp: {self.N50_contigs_over_300} 
<img src="../plots/{self.barcode}_{self.k_value}.png" width="400"> \n \n """


"""
get files
"""
def get_barcodes(dir_path):
    barcodes = []
    for item in os.scandir(dir_path):
        if item.is_dir() and item.name.startswith("SRR"):
            barcodes.append(item.name)
    return barcodes
    

def get_assemblies(assembly_path):
    assemblies = []
    barcode = assembly_path.split("assembled/")[1].split("/")[0]
    for item in os.scandir(assembly_path):
        if item.is_dir():
            contigs_file = assembly_path + "/" + item.name + "/contigs.fasta"
            log_file = assembly_path + "/" + item.name + "/spades.log"
            if os.path.exists(contigs_file) and os.path.exists(log_file):
                assemblies.append(Assembly(contigs_file, log_file, str(item.name), barcode))
    return assemblies

"""
average read length
->spades.log Average read length
"""
def read_avg_read_length(filepath):
    with open(filepath, 'r') as log_file:
        return float((log_file.read().split("Average read length ")[1].split("\n")[0]))

"""
Read contig.fasta file
"""
def get_contig_lengths(file):
    with open(file, 'r') as fasta:
    #  contigs = fasta.read().split(">NODE")
    # Splits fasta file at _length_ to have lines starting with the length (except the first item in the list, which is the text before)
        dirty_lengths = fasta.read().split("_length_")
    #remove first item in list and split off the rest of the information so only lengths remain
    dirty_lengths.pop(0)
    lengths = []
    for length in dirty_lengths:
        lengths.append(int(length.split("_")[0]))
    return lengths


"""
average contig length

"""
def calc_avg_contig_length(list_of_lengths):
    return sum(list_of_lengths) /len(list_of_lengths)


"""
N50 of all contigs
https://onestopdataanalysis.com/n50-genome/

"""
def calculate_N50(list_of_lengths):
    tmp = []
    for tmp_number in set(list_of_lengths):
            tmp += [tmp_number] * list_of_lengths.count(tmp_number) * tmp_number
    tmp.sort()
    if (len(tmp) % 2) == 0:
        median = (tmp[int(len(tmp) / 2) - 1] + tmp[int(len(tmp) / 2)]) / 2
    else:
        median = tmp[int(len(tmp) / 2)]
    return median

"""
N50 of all contigs longer than 300bp

"""
def calculate_N50_bigger_300(list_of_lengths):
    tmp = []
    filtered_lengths = [x for x in list_of_lengths if x>300]
    for tmp_number in set(filtered_lengths):
            tmp += [tmp_number] * filtered_lengths.count(tmp_number) * tmp_number
    tmp.sort()
    if (len(tmp) % 2) == 0:
        median = (tmp[int(len(tmp) / 2) - 1] + tmp[int(len(tmp) / 2)]) / 2
    else:
        median = tmp[int(len(tmp) / 2)]
    return median

"""
plots

"""
def make_plots(assembly):
    df = pd.DataFrame (assembly.contig_lengths, columns = ['contig_length'])
    sns.histplot(data=df, x="contig_length", log_scale=True)
    plt.savefig("../plots/" + assembly.barcode + "_" + assembly.k_value)
    plot.fig.clf()
    





"""
Load data from assembly directory
and write analysis file

"""

dir_path = sys.argv[1]
#dir_path = snakemake.input[0]
barcodes = get_barcodes(dir_path)
# To save a list of assemblies for each barcode
masterlist_of_assemblies = []
for barcode in barcodes:
    masterlist_of_assemblies.append(get_assemblies(dir_path + barcode))

with open("../data/" + "Analysis.md", 'w') as stats:
    for barcode in masterlist_of_assemblies:
        for assembly in barcode:
            stats.write(str(assembly))
            make_plots(assembly)







"""
Decision for best assembly

"""






