```
Setup
```





```
average read length
->spades.log Average read length
```


```k
Read contig.fasta file
```
def read_fasta(file):
    with open(file, 'r') as fasta:
    #  contigs = fasta.read().split(">NODE")
    # Splits fasta file at _length_ to have lines starting with the length (except the first item in the list, which is the text before)
        dirty_lengths = fasta.read().split("_length_")
    #remove first item in list and split off the rest of the information so only lengths remain
    dirty_lengths.pop(0)
    lengths = []
    for length in dirty_lengths:
        lengths.append(int(length.split("_")[0]))
        
    print(lengths)


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
