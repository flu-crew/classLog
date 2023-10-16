# classLog: Machine learning tool for classification of genetic sequences
Implementation of logistic regression for classification of sequences based on a reference set. Classlog 
is designed to train logistic regression classifiers based on genetic information. Trained classifiers 
can then be used to assign classification future clades with linear time complexity. 

Please cite: Zeller, M.A., Arendsee, Z.W., Smith, G.J.D., and Anderson, T.K. classLog: Logistic regression for the classification of genetic sequences. [*bioRxiv*, 2022.08.15.503907; doi: https://doi.org/10.1101/2022.08.15.503907](https://www.biorxiv.org/content/10.1101/2022.08.15.503907v1)

## Installation
Clone and then navigate to the directory with the setup.py/ 
```bash
#Clone the classlog repo
git clone https://github.com/flu-crew/classLog.git
cd classLog

#Install the the rapid aligner - rpalign
git clone https://github.com/arendsee/rpalign.git
cd rpalign
pip install .

#Install classlog
cd ..
pip install .
```

## Uninstall
```bash
pip uninstall classlog
```
## Tutorial

Classlog is designed to leverage the power of machine learning to classify sequences. Once a logistic regression
classifier has been trained on a high-quality multisequence alignment that broadly covers all cases of interest, 
that classifier can be recyled to classify unknown sequences in linear run time. This classification is based on 
the idea that clade defining mutations are linearly seperable where each position in the sequence is a nominal 
axis. 
  
This tutorial will be based on the ORF5 gene of Porcine Respiratory and Reproductive Syndrome virus (PRRSv) lineages classified by Paploski et al<sub>1</sub>.
The first step will be to test that the FASTA containing the sequences have been properly annotated with classifications using 
the getclasses subcommand. 
  
```bash
>classlog getclasses classlog/examples/prrsv/annotated_prrsv2.fasta
Unique classes: ['L7', 'L5', 'L1B', 'L1C', 'L8', 'L1D', 'L9', 'L1A', 'L1E']

>classlog getclasses classlog/examples/prrsv/annotated_prrsv1and2.fasta
Unique classes: ['L1A', 'L8', 'L7', 'L1E', 'L5', 'L1B', 'L1D', 'L9', 'L1C', 'T1']
```
  
> **Note**
>The associated classes are returned for both training datasets, with the second dataset containing a 'T1' designation for PRRSv1 detected primarily in Europe. 
>If `nan` is returned in the classes list, that indicates that some sequences have not been given a designation. The `predictmissing` subcommand can be used to 
>fill in blanks in this situation. If there is a formatting error and not all position are avaible, `Postion *x* does not exist (remember indices start at 0 with 
>delimiter '|')`. 
  
Now that the classes have been confirmed, we can train a classifier based on the data. The gene of concern is the ORF5, which is typically 603 nucleotides in 
length, though variants between 600-606 are regularly detected. There is a relatively high amount of diversity between ORF5 clade designations, so it is  
reasonable to use a small number of nucleotide or amino acid positions, or features in machine learning terms, to make the classification. We will train the
classifier on only 5% (~30nt) of the total genetic data. Classlog uses Gini importance score given by a tree classifier to select the features that contribute to the
largest decrease in node impurity. 

```bash
>classlog train -d "|" -n 1 -p 0.05 classlog/examples/prrsv/annotated_prrsv2.fasta
complete
```

In the above command the delimiter is specified as "|" with the -d flag, and the position containing the clade classification as 1 with the -n flag, or the second column based on the delimiter, using only the top 5% of the features specified with the -p flag. 
The "|" is generally a default delimiter in fasta files and 1 is the default position: if your input alignment deflines has this configuration, you do not need to specify this information. After the training completes,
the selected features can be viewed with the `getfeatures` command being run on the output model. It is important to note that the positions are relative to the 
multisequence alignment used in the training, and not to the actual position in the sequence. If the alignment is ungapped, then these two numbers may be the same. The getfeatures command will output the position, the nucleotide or amino acid, and the Gini importance score.

```bash
>classlog getfeatures classlog/examples/prrsv/annotated_prrsv2.fasta.classify.pickle
394_g 0.01869155333772745
417_t 0.01822700227227926
372_a 0.017839808092326707
351_c 0.015234256820791532
405_t 0.014451694613954742
246_t 0.014337547382473786
292_a 0.014052101632721694
304_a 0.0132394468887522
483_a 0.013113132744322117
531_t 0.013034898670080454
304_g 0.012815338614154716
292_g 0.012612763478247833
264_c 0.012527218278322882
273_c 0.012309470109328622
531_c 0.01220547709578351
393_a 0.01205958599333764
471_t 0.011568213409032954
545_a 0.011385100565281914
273_t 0.010750671384477628
201_g 0.01063361417906652
417_c 0.010316582237905516
303_t 0.010267967380961016
...
```

Checking the features can indicate which positions are critical for clade classification, and tend to be more helpful when looking 
at amino acids. Now that the the classifier is trained, it can be used to predict unclassified sequences. Using the general usage of classlog predict path_to_model.classify.pickle path_to_unknown.fasta 

```bash
>classlog predict classlog/examples/prrsv/annotated_prrsv2.fasta.classify.pickle classlog/examples/prrsv/unknown_small_prrsv.fasta -t 0.7
KT902873.1 Porcine reproductive and respiratory syndrome virus isolate PRRSV2/USA/AP516/2010 glycoprotein 5 gene_ complete cds  L8      0.7001194494119555
KT903031.1 Porcine reproductive and respiratory syndrome virus isolate PRRSV2/USA/AP613/2011 glycoprotein 5 gene_ complete cds  L1C     0.9982481556278681
MT629042.1 Porcine reproductive and respiratory syndrome virus isolate 1515_NEBIH_2016_HU surface glycoprotein (ORF5) gene_ complete cds        L8      0.8153941261693686
KT904846.1 Porcine reproductive and respiratory syndrome virus isolate PRRSV2/USA/AP2359/2014 glycoprotein 5 gene_ complete cds L1A     0.99856049904447
KT903797.1 Porcine reproductive and respiratory syndrome virus isolate PRRSV2/USA/AP1354/2012 glycoprotein 5 gene_ complete cds L1C     0.9679526698603171
KU501963.1 Porcine reproductive and respiratory syndrome virus isolate PRRSV2/USA/CB395/2009 glycoprotein 5 gene_ complete cds  L1B     0.9953258025325801
KU503167.1 Porcine reproductive and respiratory syndrome virus isolate PRRSV2/USA/LS1723/2012 glycoprotein 5 gene_ complete cds unknown 0.47979021332687843
KT902650.1 Porcine reproductive and respiratory syndrome virus isolate PRRSV2/USA/AP290/2010 glycoprotein 5 gene_ complete cds  L9      0.9913452955484331
KU666369.1 Porcine reproductive and respiratory syndrome virus strain K15-3-E48_HA envelope glycoprotein GP5 gene_ complete cds unknown 0.6993205230396002
KT904147.1 Porcine reproductive and respiratory syndrome virus isolate PRRSV2/USA/AP1545/2013 glycoprotein 5 gene_ complete cds L1C     0.9970249467946908
KU503709.1 Porcine reproductive and respiratory syndrome virus isolate PRRSV2/USA/LS77/2007 glycoprotein 5 gene_ complete cds   L1B     0.9609593452215996
KU502406.1 Porcine reproductive and respiratory syndrome virus isolate PRRSV2/USA/CB908/2013 glycoprotein 5 gene_ complete cds  L8      0.9548719142323132
KU502369.1 Porcine reproductive and respiratory syndrome virus isolate PRRSV2/USA/CB870/2008 glycoprotein 5 gene_ complete cds  unknown 0.5314173386655152
KF183956.1 Porcine reproductive and respiratory syndrome virus isolate DK-2011-88005-A5 glycoprotein 5 gene_ complete cds       L5      0.9499130907828587
KU503136.1 Porcine reproductive and respiratory syndrome virus isolate PRRSV2/USA/LS1692/2010 glycoprotein 5 gene_ complete cds unknown 0.5658924275798167
KU501762.1 Porcine reproductive and respiratory syndrome virus isolate PRRSV2/USA/LS70/2006 glycoprotein 5 gene_ complete cds   L1B     0.9905717881896017
KU501570.1 Porcine reproductive and respiratory syndrome virus isolate PRRSV2/USA/LS767/2013 glycoprotein 5 gene_ complete cds  L1B     0.975135320020058
KU503836.1 Porcine reproductive and respiratory syndrome virus isolate PRRSV2/USA/LS911/2014 glycoprotein 5 gene_ complete cds  L1B     0.9925646140262852
KT903695.1 Porcine reproductive and respiratory syndrome virus isolate PRRSV2/USA/AP1251/2012 glycoprotein 5 gene_ complete cds L1C     0.7963816353795009
KP317085.1 Porcine reproductive and respiratory syndrome virus strain CP296-3/P508 glycoprotein (ORF5) gene_ complete cds       L5      0.978690514785044
```
  
The threshold for classification rejection was manually set in this run using `-t 0.7`. By default, the threshold is 0.85, where
classifications >= 0.95% likelihood are accepted and reported, and less than this value are rejected and an unknown is returned. 
The results can be piped out to a tab delimited file for use.
  
1. Paploski, I. A. D., Corzo, C., Rovira, A., Murtaugh, M. P., Sanhueza, J. M., Vilalta, C., ... & VanderWaal, K. (2019). Temporal dynamics of co-circulating lineages of porcine reproductive and respiratory syndrome virus. Frontiers in microbiology, 10, 2486.
## Future todo
1. Web implementation

## Functions

`classlog` has the following subcommands.

|	subcommands			|	description														|
|	-----------			|	-----------														|
|	`getclasses`		|	Pulls classification names from designated position				|
|	`getfeatures`		|	Lists the features contained in the classifier, unsorted		|
|	`predictmissing`	|	Process a mixed datatset and fill in missing values				|
|	`predict`			|	Predict clades of a fasta file based on previosuly trianed...	|
|	`train`				|	Train a logistic regression classifier with a reference...		|

More details for each command is available using the '-h' option.

To list subcommands

``` bash
classlog -h
```

## Commands

# getclasses
Usage: classlog getclasses [OPTIONS] [ALIGNMENT]  
  
  Pulls classification names from designated position  
  
Options:
  -d, --delimiter TEXT  [default: |]  
  -n, --column INTEGER  [default: 1]  
  -h, --help            Show this message and exit.  [default: False]  
  
```
>classlog getclasses classlog/examples/h3_iav/h3_aa_aln.fasta -n 4
Unique classes: ['cluster_IVF', 'cluster_IV', 'HA-human-to-swine-2016', 'cluster_IVD', 'cluster_IVB', 'cluster_IVA', '2010.2', 'cluster_I', 'HA-human-to-swine-2018', '2010.1', 'HA-human-to-swine-2017']
```

# getfeatures
Usage: classlog getfeatures [OPTIONS] [MODEL]  
  
  List the features and Gini importance in a trained classifier  
  
```bash
>classlog getfeatures classlog/examples/prrsv/annotated_prrsv1.fasta.classify.pickle
0_-
0_a
100_-
100_a
100_c
100_g
100_r
100_t
101_-
101_a
101_c
...
```

# predictmissing
Usage: classlog predictmissing [OPTIONS] [ALIGNMENT]  
  
  Process a mixed datatset and fill in missing values  
  
Options:  
  -d, --delimiter TEXT  [default: |]  
  -n, --column INTEGER  [default: 1]  
  -h, --help            Show this message and exit.  [default: False]  
  
*Note: The delimiters still need to match in this case to work correctly.*
```bash
>classlog predictmissing classlog/examples/h3_missing/h3_aa_aln.fasta -n 4

                                                 taxa       clade     prob
        A/swine/Indiana/3254/2016|H3N2|IN|2016-01-19| cluster_IVB 0.996091
 A/swine/South_Carolina/7315/2016|H3N2|SC|2016-02-09| cluster_IVA 0.998934
A/swine/North_Carolina/16388/2016|H3N2|NC|2016-03-23| cluster_IVA 0.998211
          A/swine/Iowa/26848/2016|H3N2|IA|2016-05-12| cluster_IVA 0.996451
          A/swine/Iowa/32247/2016|H3N2|IA|2016-06-09|      2010.1 0.999284
          A/swine/USA/42280/2016|H3N2|USA|2016-08-04| cluster_IVA 0.997884
          A/swine/Iowa/55336/2016|H3N2|IA|2016-10-18|      2010.1 0.999336
          A/swine/USA/56618/2016|H3N2|USA|2016-10-25|      2010.1 0.999418
      A/swine/Illinois/65263/2016|H3N2|IL|2016-12-12|      2010.1 0.999412
      A/swine/Missouri/12222/2017|H3N2|MO|2017-02-17|      2010.1 0.999376
```

# predict
Usage: classlog predict [OPTIONS] [MODEL] [DATA]  
  
  Predict clades of a fasta file based on previosuly trained model  
  
```bash
>classlog predict classlog/examples/prrsv/annotated_prrsv1.fasta.classify.pickle classlog/examples/prrsv/unknown_small_prrsv.fasta
KT902873.1 Porcine reproductive and respiratory syndrome virus isolate PRRSV2/USA/AP516/2010 glycoprotein 5 gene_ complete cds  unknown 0.7545282643457021
KT903031.1 Porcine reproductive and respiratory syndrome virus isolate PRRSV2/USA/AP613/2011 glycoprotein 5 gene_ complete cds  L1C     0.9996264323806708
...
```

# train
Usage: classlog train [OPTIONS] [ALIGNMENT]  
  
  Train a logistic regression classifier with a reference set  
  
Options:  
  -d, --delimiter TEXT  [default: |]  
  -n, --column INTEGER  [default: 1]  
  -p, --percent FLOAT   [default: 0.0]  
  -h, --help            Show this message and exit.  [default: False]  
  
```bash
>classlog getclasses classlog/examples/h1_iav/aa/h1_complete_aa.aln.fasta -n 2
Unique classes: ['gamma2_beta_like', 'delta2', 'beta', 'gamma2', 'npdm', 'delta1', 'gamma', 'alpha']

>classlog train classlog/examples/h1_iav/aa/h1_complete_aa.aln.fasta -n 2
complete
```

## Example
# Training and classifying unknown PRRSv ORF5 sequences
```
>classlog getclasses classlog/examples/prrsv/annotated_prrsv1.fasta
Unique classes: ['L9', 'L7', 'L1C', 'L1A', 'L1D', 'L8', 'L1B', 'L5', 'L1E']

>classlog train classlog/examples/prrsv/annotated_prrsv1.fasta
complete

>classlog predict classlog/examples/prrsv/annotated_prrsv1.fasta.classify.pickle classlog/examples/prrsv/unknown_small_prrsv.fasta
KT902873.1 Porcine reproductive and respiratory syndrome virus isolate PRRSV2/USA/AP516/2010 glycoprotein 5 gene_ complete cds  unknown 0.7545282643457021
KT903031.1 Porcine reproductive and respiratory syndrome virus isolate PRRSV2/USA/AP613/2011 glycoprotein 5 gene_ complete cds  L1C     0.9996264323806708
MT629042.1 Porcine reproductive and respiratory syndrome virus isolate 1515_NEBIH_2016_HU surface glycoprotein (ORF5) gene_ complete cds        L9      0.9657072415607401
KT904846.1 Porcine reproductive and respiratory syndrome virus isolate PRRSV2/USA/AP2359/2014 glycoprotein 5 gene_ complete cds L1A     0.999585055147609
KT903797.1 Porcine reproductive and respiratory syndrome virus isolate PRRSV2/USA/AP1354/2012 glycoprotein 5 gene_ complete cds L1C     0.9993476234505754
KU501963.1 Porcine reproductive and respiratory syndrome virus isolate PRRSV2/USA/CB395/2009 glycoprotein 5 gene_ complete cds  L1B     0.9989539667532236
KU503167.1 Porcine reproductive and respiratory syndrome virus isolate PRRSV2/USA/LS1723/2012 glycoprotein 5 gene_ complete cds unknown 0.6937897523426487
KT902650.1 Porcine reproductive and respiratory syndrome virus isolate PRRSV2/USA/AP290/2010 glycoprotein 5 gene_ complete cds  L9      0.9988491970224741
KU666369.1 Porcine reproductive and respiratory syndrome virus strain K15-3-E48_HA envelope glycoprotein GP5 gene_ complete cds L9      0.9206152492542578
KT904147.1 Porcine reproductive and respiratory syndrome virus isolate PRRSV2/USA/AP1545/2013 glycoprotein 5 gene_ complete cds L1C     0.9994452619014953
KU503709.1 Porcine reproductive and respiratory syndrome virus isolate PRRSV2/USA/LS77/2007 glycoprotein 5 gene_ complete cds   L1B     0.9911318788866544
KU502406.1 Porcine reproductive and respiratory syndrome virus isolate PRRSV2/USA/CB908/2013 glycoprotein 5 gene_ complete cds  L8      0.9978457292987061
KU502369.1 Porcine reproductive and respiratory syndrome virus isolate PRRSV2/USA/CB870/2008 glycoprotein 5 gene_ complete cds  unknown 0.39934880429709146
KF183956.1 Porcine reproductive and respiratory syndrome virus isolate DK-2011-88005-A5 glycoprotein 5 gene_ complete cds       L5      0.9982566940576959
KU503136.1 Porcine reproductive and respiratory syndrome virus isolate PRRSV2/USA/LS1692/2010 glycoprotein 5 gene_ complete cds L8      0.9794004098195661
KU501762.1 Porcine reproductive and respiratory syndrome virus isolate PRRSV2/USA/LS70/2006 glycoprotein 5 gene_ complete cds   L1B     0.9968439317070785
KU501570.1 Porcine reproductive and respiratory syndrome virus isolate PRRSV2/USA/LS767/2013 glycoprotein 5 gene_ complete cds  L1B     0.9945967202771347
KU503836.1 Porcine reproductive and respiratory syndrome virus isolate PRRSV2/USA/LS911/2014 glycoprotein 5 gene_ complete cds  L1B     0.9983881245933621
KT903695.1 Porcine reproductive and respiratory syndrome virus isolate PRRSV2/USA/AP1251/2012 glycoprotein 5 gene_ complete cds unknown 0.6638393549798826
KP317085.1 Porcine reproductive and respiratory syndrome virus strain CP296-3/P508 glycoprotein (ORF5) gene_ complete cds       L5      0.9987939638914471
```

# Troubleshooting
## ValueError: Illegal character
This error can occur in nucleotide FASTAs where non-standard characters are used. One potential way to quickly fix this error is to standardize the FASTA. This can be done using SMOF (`pip install smof`), using the following command.

```python
smof clean -t n -r -d -x [PROBLEM.FASTA]> [CLEAN.FASTA]
```

This command 
* Converts irregular letters to unknown
* Converts 'X' in to 'N' in DNA
* Removes all non-letter characters (gaps, stops, etc.)

This should take care of the majority of irregular cases within a FASTA.
