#!/usr/bin/env python3
```
Setup
```
import os

class Assembly:
    def __init__(self, contigs_fasta_filename, log_filename):
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
        self.N50_all_contigs
        self.N50_contigs_over_300

```
get files
```
def get_assemblies(assembly_path):
    assemblies = []
    for item in os.scandir(input_path):
        if item.is_dir():
            assemblies.append(Assembly((input_path + "/" item.name + "/contigs.fasta"), (input_path + "/" item.name + "/spades.log"))
    return assemblies




```
average read length
->spades.log Average read length
```
def read_avg_read_length(filepath):
    with open(filepath, 'r') as log_file:
        return int((log_file.read().split("Average read length ")[1].split("\n")[0]))




```
Read contig.fasta file
```
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


```
average contig length

```
def calc_avg_contig_length(list_of_lengths):
    return sum(list_of_lengths) /len(list_of_lengths)








```
N50 of all contigs
https://onestopdataanalysis.com/n50-genome/

```





```
N50 of all contigs longer than 300bp

```







```
Decision for best assembly

```









```
output

```
