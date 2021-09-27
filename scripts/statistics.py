```
Setup
```
import os

class Assembly:
    def __init__(self, contigs_fasta_filename, log_filename):
    self.contigs_fasta_filename = contigs_fasta_filename
    self.log_filename = log_filename
    self.contig_lengths = get_contig_lengths(contigs_fasta_filename)
    self.avg_read_length = read_avg_read_length(log_filename)
    self.avg_contigs_length
    self.totl_nr_contigs
    self.shortest_contig
    self.longest_contig
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



```
total number of contigs

```




```
 shortest contig

```





```
longest contig

```




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
