#!/usr/bin/env python3
"""
Setup
"""
import os
import sys
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from Bio import SeqIO

"""
in the Assembly object all important informations are saved. Each assembly (each k-value of each barcode) is its own Assembly object
"""

class AssemblyShort:
    def __init__(self, contigs_fasta_filename, log_filename, k_value, barcode):
        self.contigs_fasta_filename = contigs_fasta_filename
        self.log_filename = log_filename
        self.contig_lengths = get_contig_lengths_short(contigs_fasta_filename)
        self.avg_read_length = read_avg_read_length_short(log_filename)
        self.avg_contigs_length = calc_avg_contig_length(self.contig_lengths)
        self.totl_nr_contigs = len(self.contig_lengths)
        self.shortest_contig = min(self.contig_lengths)
        self.longest_contig = max (self.contig_lengths)
        self.N50_all_contigs = calculate_N50(self.contig_lengths)
        self.N50_contigs_over_300 = calculate_N50_bigger_300(self.contig_lengths)
        self.barcode = barcode
        self.k_value = k_value
        self.plot = f"""<img src="../plots/{self.barcode}_{self.k_value}.png" width="400">"""
    def __str__(self):
        return f"""- average contig length: {self.avg_contigs_length}                                                   
-total number of contigs: {self.totl_nr_contigs}                                                        
-shortest contig: {self.shortest_contig}                                                               
-longest contig: {self.longest_contig}                                                                  
-<N50 of all contigs: {self.N50_all_contigs}                                                              
-N50 of all contigs over 300 bp: {self.N50_contigs_over_300}"""

class AssemblyLong:
    def __init__(self, contigs_fasta_filename, gfa_filename, barcode):
        self.contigs_fasta_filename = contigs_fasta_filename
        self.gfa_filename = gfa_filename
        self.contig_lengths = get_contig_lengths_long(contigs_fasta_filename)
        self.avg_contigs_length = calc_avg_contig_length(self.contig_lengths)
        self.totl_nr_contigs = len(self.contig_lengths)
        self.shortest_contig = min(self.contig_lengths)
        self.longest_contig = max (self.contig_lengths)
        self.N50_all_contigs = calculate_N50(self.contig_lengths)
        self.N50_contigs_over_300 = calculate_N50_bigger_300(self.contig_lengths)
        self.barcode = barcode
        
    def __str__(self):
        return f"""
|statistics analysis for barcode: {self.barcode} Nanopore long read assembled with miniasm | plot
| ------------------------------------------------------------------------------------------------------| --------------------------------------------
|average contig length: {self.avg_contigs_length}                                                        | <img src="../plots/{self.barcode}.png" width="400">
|total number of contigs: {self.totl_nr_contigs}                                                         | 
|shortest contig: {self.shortest_contig}                                                                 |
|longest contig: {self.longest_contig}                                                                   |
|N50 of all contigs: {self.N50_all_contigs}                                                              |
|N50 of all contigs over 300 bp: {self.N50_contigs_over_300}                                             |
                                              
"""

"""
get files
"""
def get_barcodes(dir_path):
    barcodes = []
    for item in os.scandir(dir_path):
        if item.is_dir() and item.name.startswith("SRR"):
           barcodes.append(item.name)
    return barcodes
    

def parse_short_assemblies(assembly_path, barcode):
    assemblies = []
    for item in os.scandir(assembly_path):
        if item.is_dir():
            contigs_file = assembly_path + "/" + item.name + "/contigs.fasta"
            log_file = assembly_path + "/" + item.name + "/spades.log"
            if os.path.exists(contigs_file) and os.path.exists(log_file):
                assemblies.append(AssemblyShort(contigs_file, log_file, str(item.name), barcode))
    return assemblies

def parse_long_assemblies(assembly_path, barcode):
    assemblies = []
    contigs_file = assembly_path + "/contigs.fasta"
    gfa_file = assembly_path + "/contigs.gfa"
    if os.path.exists(contigs_file) and os.path.exists(gfa_file):
        assemblies.append(AssemblyLong(contigs_file, gfa_file, barcode))
    return assemblies

"""
average read length
->spades.log Average read length
"""
def read_avg_read_length_short(filepath):
    with open(filepath, 'r') as log_file:
        return float((log_file.read().split("Average read length ")[1].split("\n")[0]))

"""
Read contig.fasta file
"""
def get_contig_lengths_short(file):
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

def get_contig_lengths_long(contigs_fasta_filename):
    lengths = []
    for record in SeqIO.parse(contigs_fasta_filename, "fasta"):
        lengths.append(len(record))
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
def make_contig_plots(assembly, path):
    df = pd.DataFrame (assembly.contig_lengths, columns = ['contig_length'])
    sns.histplot(data=df, x="contig_length", log_scale=True)
    plt.savefig(path)
    plt.clf()

def make_N50_plot(barcode):
    k_values = []
    N50s = []
    for assembly in barcode:
        k_values.append(assembly.k_value)
        N50s.append(assembly.N50_all_contigs)
        barcode = assembly.barcode
    data = {
        "k_values": k_values,
        "N50s": N50s,
        "barcode": barcode
    }
    df = pd.DataFrame(data)
    g = sns.catplot(data=df, kind="bar",
    x="barcode", y="N50s", hue="k_values",
    ci="sd", palette="dark", alpha=.6, height=6
    )
    g.despine(left=True)
    g.set_axis_labels("", "N50")
    g.legend.set_title("k")
    plt.savefig("plots/" + assembly.barcode + "_N50")
    plt.clf()

    
    





"""
Load data from assembly directory
and write analysis file

"""

dir_path_short = sys.argv[1]
dir_path_long = sys.argv[2]
#dir_path = snakemake.input[0]
barcodes_short = get_barcodes(dir_path_short)
barcodes_long = get_barcodes(dir_path_long)
# To save a list of assemblies for each barcode
masterlist_of_short_assemblies = []
masterlist_of_long_assemblies = []
for barcode in barcodes_short:
    masterlist_of_short_assemblies.append(parse_short_assemblies(dir_path_short + barcode, barcode))
for barcode in barcodes_long:
    masterlist_of_long_assemblies.append(parse_long_assemblies(dir_path_long + barcode, barcode))

with open("data/" + "Analysis.md", 'w') as stats:
    for barcode in masterlist_of_short_assemblies:
        make_N50_plot(barcode)
        stats.write(f"""<img src="../plots/{barcode[0].barcode}_N50.png" width="400"> \n\n\n\n\n\n\n """)
        stats.write(f"""
#### statistics analysis for barcode: {barcode[0].barcode}           
|k = {barcode[0].k_value} {str(barcode[0])} {barcode[0].plot}
|-------------------------|--------------------------|--------------------------|
|k = {barcode[1].k_value} {str(barcode[1])} {barcode[1].plot}                                    
|-------------------------|--------------------------|--------------------------|   
| k = {barcode[2].k_value} {str(barcode[2])} {barcode[2].plot}                                                                                         
""")
        for assembly in barcode:
            make_contig_plots(assembly, ("plots/" + assembly.barcode + "_" + assembly.k_value))
    for barcode in masterlist_of_long_assemblies:
        for assembly in barcode:
            stats.write(str(assembly))
            make_contig_plots(assembly, ("plots/" + assembly.barcode))
        







"""
Decision for best assembly

"""
best_assemblies = []
for assembly_list in masterlist_of_short_assemblies:
    best_assembly = ""
    sorted_assemblies = assembly_list
    sorted_assemblies.sort(key=lambda x: x.N50_all_contigs, reverse=True)
    if sorted_assemblies[0].N50_all_contigs > sorted_assemblies[1].N50_all_contigs:
        best_assembly = sorted_assemblies[0].contigs_fasta_filename
    else:
        print(str(sorted_assemblies[0].N50_all_contigs) + "vs. " + str(sorted_assemblies[1].N50_all_contigs))
        if sorted_assemblies[0].longest_contig > sorted_assemblies[1].longest_contig:
            best_assembly = sorted_assemblies[0].contigs_fasta_filename
        else:
            best_assembly = sorted_assemblies[1].contigs_fasta_filename
    best_assemblies.append(best_assembly)
with open("data/" + "best_assemblies.txt", 'w') as out_best_assemblies:
    out_best_assemblies.write(str(best_assemblies))






