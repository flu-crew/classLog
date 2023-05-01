# classLog Benchmarking

## Machine Notes
Benchmarking was run using WSL2 on Widnow 10.

```
OS Name:                   Microsoft Windows 10 Enterprise
OS Version:                10.0.19045 N/A Build 19045
System Manufacturer:       ASUS
System Type:               x64-based PC
Processor(s):              1 Processor(s) Installed.
                           [01]: Intel64 Family 6 Model 167 Stepping 1 GenuineIntel ~3600 Mhz
BIOS Version:              American Megatrends Inc. 1017, 7/13/2021 (11th Gen i7-11700KF @ 3.60GHz)
Total Physical Memory:     65,370 MB
Virtual Memory: Max Size:  75,098 MB
Hyper-V Requirements:      VM Monitor Mode Extensions: Yes
                           Virtualization Enabled In Firmware: No
                           Second Level Address Translation: Yes
                           Data Execution Prevention Available: Yes
```

## Testing Method
All runs were timed and measured using `/usr/bin/time -v`. The testing conditions can be recreated using below.

```bash
#Time the training
/usr/bin/time -v classlog train -d "|" -n 1 -p 0.05 classlog/examples/prrsv/annotated_prrsv2.fasta	
/usr/bin/time -v classlog train -d "|" -n 1 -p 0.05 classlog/examples/prrsv/annotated_prrsv1and2.fasta
/usr/bin/time -v classlog train -d "|" -n 2 -p 0.05 classlog/examples/h1_iav/nt/no2020_train.aln.fasta

#Time the prediction
/usr/bin/time -v classlog predict classlog/examples/prrsv/annotated_prrsv2.fasta.classify.pickle classlog/examples/time_trial/unknown_yoon_prrsv.fasta -t 0.7
/usr/bin/time -v classlog predict classlog/examples/prrsv/annotated_prrsv1and2.fasta.classify.pickle classlog/examples/time_trial/unknown_yoon_prrsv.fasta -t 0.7
/usr/bin/time -v classlog predict classlog/examples/prrsv/annotated_prrsv2.fasta.classify.pickle classlog/examples/time_trial/annotated_prrsv1and2.fasta -t 0.7
/usr/bin/time -v classlog predict classlog/examples/prrsv/annotated_prrsv1and2.fasta.classify.pickle classlog/examples/time_trial/annotated_prrsv1and2.fasta -t 0.7
/usr/bin/time -v classlog predict classlog/examples/h1_iav/nt/no2020_train.aln.fasta.classify.pickle classlog/examples/time_trial/2020_test.fasta -t 0.7
/usr/bin/time -v classlog predict classlog/examples/h1_iav/nt/no2020_train.aln.fasta.classify.pickle classlog/examples/time_trial/BVBRC_genome_sequence.fasta -t 0.7

#pplacer test runs (commands do not represent files in the repository, but show the structure)
pplacer -r subset_prrsv2.fasta -t raxml/RAxML_bestTree.output -s raxml/RAxML_info.output yoon.aln.fasta
pplacer -r 200_subsample.tre -t raxml/RAxML_bestTree.output -s raxml/RAxML_info.output 2020_iav.aln.fasta

#RAPPAS test runs (commands do not represent files in the repository, but show the structure)
java -Xmx16G -jar $(which RAPPAS.jar) -p b -s nucl -w . -r raxml/iav_subset.fasta.reduced.fasta -t raxml/RAxML_bestTree.output --use_unrooted -b $(which raxml-ng)
java -Xmx8G -jar $(which RAPPAS.jar) -p p -d DB_session_k8_o1.5.union -q 2020_test.fasta
java -Xmx16G -jar $(which RAPPAS.jar) -p b -s nucl -w . -r raxml/subset_prrsv2.fasta.reduced.fasta -t raxml/RAxML_bestTree.output --use_unrooted -b $(which raxml-ng)
java -Xmx8G -jar $(which RAPPAS.jar) -p p -d DB_session_k8_o1.5.union -q unknown_yoon_prrsv.fasta
```

## Results
|Dataset   |Training Taxa|Test Taxa|Approx Length (nt)|Training Time (seconds)|Training memory (MB)|Testing Time (seconds)|Testing Memory (MB)|Total Time (seconds)|
|----------|-------------|---------|------------------|-----------------------|--------------------|----------------------|--------------|--------------------|
|PRRSV2    |4053         |77       |603               |4.11                   |222.904             |1.35                  |116.248       |5.46      |
|          |             |4381     |603               |                       |                    |15.34                 |129.092       |19.45     |
|PRRSV1+2  |4381         |77       |603               |4.22                   |239.412             |1.29                  |116.672       |5.51      |
|          |             |4381     |603               |                       |                    |15.41                 |129.104       |19.63     |
|H1_no_2020|3510         |136      |1701              |5.16                   |346.204             |4.7                   |141.016       |9.86      |
|          |             |2188     |1701              |                       |                    |44.86                 |155.412       |50.02     |


## Comparison to pplacer and RAPPAS system usage
Phylogenetic placement (PP) can be used to assign taxonomical designations to new sequences quickly and accurately. To assess the performance of these methods, both pplacer and RAPPAS were used to perform PP on the same test datasets used in the manuscript. This is by not a direct comparison. While classLog relies on a plethora of example sequences for generalizing lineages, PP methods can use much smaller trees to give accurate lineage designations by finding the nearest neighbor. To reflect this, 200 taxa were used for each reference tree, paraphyletically sampled from the original dataset using SMOT (https://joss.theoj.org/papers/10.21105/joss.04193). Realistically, an even smaller dataset between 30-60 taxa could have been used reliably to represent > 90% of the diversity through the use of PARNAS (https://github.com/flu-crew/parnas). While it appears that classLog may be able to solve the lineage faster than common PP programs, the scope and use of these programs in different. Both PPlacer and RAPPAS can assign taxonomical classification for both broad (cross species) and narrow scope (viral lineages) diversity, whereas classLog is only designed to address lineage classifications with narrow windows of diversity. Additionally, I may not have run the programs in the most optimal way possible.

|Dataset   |Test Taxa|Training Taxa|pplacer (seconds)|pplacer (MB)|RAPPAS db build (seconds)|RAPPAS db build (MB)|RAPPAS placement (seconds)|RAPPAS placement (MB)|
|----------|---------|-------------|----------------------|-------------------|-------------------------------|--------------------|--------------------------|---------------------|
|PRRSV2    |77       |200          |71.1                  |105.872            |164.1                          |659.228             |10.4                      |2965.632             |
|H1_no_2020|136      |200          |176.3                 |294.832            |491.3                          |1116.728            |2.3                       |1270.456             |


