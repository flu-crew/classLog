# classLog: Machine learning tool for classification of genetic sequences
Implementation of logistic regression for classification of sequences based on a reference set. 

## Abstract

Routine sequencing and phylogenetic classification have become a common task in human and animal diagnostic laboratories. It is routine to sequence pathogens to identify genetic variations of diagnostic significance and to use these data in real-time genomic contact tracing and surveillance. Under this paradigm, unprecedented volumes of sequencing data are generated that require rapid analysis to provide meaningful data for inference. We present a machine learning logistic regression pipeline that can to assign classifications to genetic sequence data alongside a visualization of sequence variants. The pipeline implements an intuitive and customizable approach to developing a trained prediction model that runs in linear time complexity generating accurate output more rapidly than phylogenetic methods. Our approach was benchmarked against porcine respiratory and reproductive syndrome virus (PRRSv) and swine H1 influenza A (IAV) datasets. Trained classifiers were tested against sequences, and simulated datasets that artificially degraded sequence quality at 0, 10, 20, 30, and 40%. When applied to a poor quality sequence data, the classifier achieved >85% to 95% accuracy for the PRRSv and the swine H1 IAV HA dataset and this increased to XX% when using the full dataset. The model also identifies amino acid positions used to determine genetic clade identity through a feature selection ranking within the model. These positions can be mapped onto a maximum-likelihood phylogenetic tree, allowing the inference of clade defining mutations. Our approach is implemented as a python package with code available for use at https://github.com/flu-crew/classLog 

## Installation
Navigate to the directory with the setup.py/ 
```bash
#Temporary: install the correct msalign
pip uninstall msalign
git clone https://github.com/arendsee/msalign.git
cd msalign
pip install .

#Install classlog
cd ..
pip install .
```

## Uninstall
```bash
pip uninstall classlog
```

## Future todo
1. Add active support for feature selection
2. Web implementation

## Functions

`classlog` has the following subcommands.

|	subcommands			|	description														|
|	-----------			|	-----------														|
|	`getclasses`		|	Pulls classification names from designated position				|
|	`getfeatures`		|	Lists the features contained in the classifier, unsorted		|
|	`predictmissing`	|	Process a mixed datatset and fill in missing values				|
|	`predict`			|	Predict clades of a fatsa file based on previosuly trianed...	|
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
>classlog getclasses classlog\examples\h3_iav\h3_aa_aln.fasta -n 4
Unique classes: ['cluster_IVF', 'cluster_IV', 'HA-human-to-swine-2016', 'cluster_IVD', 'cluster_IVB', 'cluster_IVA', '2010.2', 'cluster_I', 'HA-human-to-swine-2018', '2010.1', 'HA-human-to-swine-2017']
```

# `getfeatures`
```bash
classlog getclasses h3_aa_aln.fasta -n 5
```

# `predictmissing`

# `predict`
```bash
classlog predict [classifier] [unknown_fasta] 
```

# `train`
```bash
classlog train h3_aa_aln.fasta -n 5
classlog train h1_aa_aln.fasta -n 5
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