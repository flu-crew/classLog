# -*- coding: utf-8 -*-
"""
Created on Fri Feb 19 11:43:15 2021

@author: mazeller
"""

# Input files
import sys
import re
import pandas as pd
import numpy as np

# import textwrap
import pickle
import sklearn

from io import StringIO

import joblib
from sklearn.metrics import (
    confusion_matrix,
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report,
)
from sklearn import model_selection  # cross_validation removed in 0.20 version
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import OneHotEncoder

from sklearn.linear_model import LogisticRegression

from msalign import *
# TODO add cutoff


def formatFasta(filename, delim="|", col=1):
    """
    Converts a fastafile into a machine learning ready dataframe

    Parameters
    ----------
    filename : String
            Location of aligned fasta file.
    delim : String, optional
            Value to split the defline by to retrieve the clade. The default is "|". Delimiter cannot be ",".
    col : Int, optional
            Index position of the clade name. The default is "1".

    Returns
    -------
    df : Dataframe
            Dataframe ready for subsequent machine learning analysis. index zero contains defline, index one contains the class, proceeding index contains machine learning features.

    """
    # Read in entire fasta
    with open(filename, "r") as content_file:
        content = content_file.read()

    # Cut and process
    content = content.replace(",", "_")  # Remove commas from thefile
    content = re.sub(r"(>.*)", r"\1,", content)  # Add comma at the end of the def line
    content = content.replace("\r", "")  # Remove windows \r
    content = content.replace("\n", "")  # Remove all new lines
    content = content.replace(">", "\n")  # Add new lines before strain names
    try:
        content = content[1:]  # Remove starting \n
    except IndexError:
        sys.exit("Empty fasta sequence")

    sequences = content.split("\n")  # Split content into sequence data
    content = ""
    for seq in sequences:
        sub = seq.split(",")  # Split the data into groups using comma delimeter

        # Split title to find the clade
        if (delim != None):
            defLine = sub[0].split(delim)
            try:
                clade = defLine[col]
            except IndexError:
                sys.exit("Postion " + str(col) + " does not exist (remember indexes start at 0 with delimiter '" + delim + "')")
        else:
            clade = ""
        sub.insert(1, clade)

        # Handle sequences
        sub[-1] = ",".join(
            sub[-1].lower()
        )  # HA/NA Aligned Sequence is the last value in the list, make lowercase and separate characters by comma
        content += "\n" + ",".join(sub)
    content = content[1:]  # Remove starting \n

    # Push string into dataframe
    df = pd.read_csv(StringIO(content), header=None)
    return df


def loadFasta(filename):
    """
    Loads a fasta format into a two column dataframe: defline, sequence. This
    function is more conducive for alignments than formatFasta.

    Parameters
    ----------
    filename : String
            Location of aligned fasta file.

    Returns
    -------
    df : Dataframe
            Dataframe of fasta data. index zero contains defline, index one contains the sequence.

    """
    # Read in entire fasta
    with open(filename, "r") as content_file:
        content = content_file.read()

    # Cut and process
    content = content.replace(",", "_")  # Remove commas from thefile
    content = re.sub(r"(>.*)", r"\1,", content)  # Add comma at the end of the def line
    content = content.replace("\r", "")  # Remove windows \r
    content = content.replace("\n", "")  # Remove all new lines
    content = content.replace(">", "\n")  # Add new lines before strain names
    content = content[1:]  # Remove starting \n

    # Push string into dataframe
    df = pd.read_csv(StringIO(content), header=None)
    return df


def getClasses(inputFile, delim="|", col=1):
    """
    Gathers the unique classes at designated delimited position.

    Parameters
    ----------
    inputFile : STRING
        Path to aligned fasta file to train on.
    delim : STRING, optional
        Delimiter to split the fasta def line by. The default is "|".
    col : INT, optional
        Index position of the clade class. Indexes start at 0. The default is 1.

    Returns
    -------
    None.

    """
    # Pull in entire dataframe and turn delimited column into set. Slower/more memory than it should be, be workable.
    # Process aligned fasta into useable dataframe
    df = formatFasta(inputFile, delim, col)
    pd.set_option("display.max_rows", None)
    pd.set_option("display.max_columns", None)
    print("Unique classes:", list(set(df[1])))
    return


def predictMissing(inputFile, delim="|", col=1, threshold=0.85):
    """
    Currently breaks if test set size = 0. Add a useful exception.

    Parameters
    ----------
    inputFile : STRING
        Path to aligned fasta file to train on.
    delim : STRING, optional
        Delimiter to split the fasta def line by. The default is "|".
    col : INT, optional
        Index position of the clade class. Indexes start at 0. The default is 1.
        
    Returns
    -------
    None.

    """
    # Process aligned fasta into useable dataframe
    df = formatFasta(inputFile, delim, col)

    # Split data into labelled/unlabeled sets
    x_train = df[df[1].isna() == False].loc[:, 2:]
    x_test = df[df[1].isna() == True].loc[:, 2:]

    #Abort if there are no test cases
    if(x_test.shape[0] == 0):
        raise SystemExit('No unlabelled sequences in the dataset, aborting.')
    
    # Map class labels to numbers from the train set
    class_le = LabelEncoder()
    y_train = class_le.fit_transform(df[df[1].isna() == False].loc[:, 1].values)

    # One-hot encode all features
    seqDf = df.loc[:, 2:]  # Fix indexing
    seqDf.columns = range(seqDf.shape[1])
    x = pd.get_dummies(seqDf)
    x_train = x[df[1].isna() == False]
    x_test = x[df[1].isna() == True]

    # Try to fit logistic model, 100% data
    # Add solver as liblinear otherwise LR will not work in the future release
    lr = LogisticRegression(
        multi_class="ovr", 
        random_state=0, 
        max_iter=1000, 
        n_jobs=-1
    )  # solver='liblinear'
    lr.fit(x_train, y_train)

    # Predict new classes
    pred_set = lr.predict(x_test)
    pred_prob = lr.predict_proba(x_test)

    #Predict characters and probs
    clade = class_le.inverse_transform(pred_set)
    cladeProbs = np.array([[x] for x in np.max(pred_prob, axis=1)])

    #Arrange dataframe
    results = pd.DataFrame()
    results["taxa"] = df[df[1].isna() == True].loc[:, 0]
    results["clade"] = clade
    results["prob"] = cladeProbs

    #Trim threshold
    results.loc[results['prob'] < threshold, "clade"] = "unknown"
     
    # Print to screen
    pd.set_option("expand_frame_repr", False)
    pd.set_option("display.max_rows", None)
    pd.set_option("display.max_columns", None)
    print(results.to_string(index=False))
    
    return


def trainClassifier(inputFile, delim="|", col=1, percentFeatures = 0):
    """
    Trains a classifier based on input sequences. Outputs a pickle file containing
    the classifier, a base sequences from index 0 to align on, features as amino
    acids, and the labels of the clades.
    
    Parameters
    ----------
    inputFile : STRING
        Path to aligned fasta file to train on.
    delim : STRING, optional
        Delimiter to split the fasta def line by. The default is "|".
    col : INT, optional
        Index position of the clade class. Indexes start at 0. The default is 1.

    Returns
    -------
    None.

    """
    
    # Process aligned fasta into useable dataframe
    df = formatFasta(inputFile, delim, col)

    # Split data into labelled/unlabeled sets
    x_train = df[df[1].isna() == False].loc[:, 2:]
    x_test = df[df[1].isna() == True].loc[:, 2:]    #Strip out unlabelled 

    #Alert if there is unlabbelled data
    if(x_test.shape[0] != 0):
        print("Unlabelled data was found in the dataset, proceeding.")
    
    # Map class labels to numbers from the train set
    class_le = LabelEncoder()
    y_train = class_le.fit_transform(df[df[1].isna() == False].loc[:, 1].values)

    # isolate a base sequence
    baseString = x_train.iloc[0, ].str.cat(sep="")
    
    # One-hot encode all features
    seqDf = df.loc[:, 2:]  # Fix indexing
    seqDf.columns = range(seqDf.shape[1])
    x = pd.get_dummies(seqDf)
    x_train = x[df[1].isna() == False]

    #Feature selection if > 0
    if(percentFeatures > 0 and percentFeatures <= 1):
        from sklearn.ensemble import ExtraTreesClassifier
        import math
        model = ExtraTreesClassifier()
        model.fit(x_train, y_train)
        importances = model.feature_importances_
        sortedImportances = sorted(range(len(importances)), key=lambda k: importances[k], reverse = True)
        
        #Widdle down features further, could try SelectPercentile w/ ANOVA scoring
        numberFeatures = math.floor(percentFeatures * len(importances))
        sortedImportances = sortedImportances[0:numberFeatures]
        x_train = x.iloc[:,sortedImportances]  
    
    # Add solver as liblinear otherwise LR will not work in the future release
    lr = LogisticRegression(
        multi_class="ovr", random_state=0, max_iter=1000, n_jobs=-1
    )  # solver='liblinear'
    lr.fit(x_train, y_train)

    #Pack the pickle
    exportClassifier = {"classifier":lr,
                        "base_seq":baseString,
                        "features":x_train.columns,
                        "labels":class_le}
    
    pickle.dump( exportClassifier, open( inputFile + ".classify.pickle", "wb" ))
    print("complete")
    return

def predictUnknown(classifierPickle, inputFile, threshold = 0.85 ):
    """
    Predict the clades for a set of unknown sequences

    Parameters
    ----------
    classifierPickle : STRING
        Path to an output pickle file, generated by the trainClassifier function.
    inputFile : STRING
        Path to a list of sequences to be classified, fasta format.
    threshold : Float32 (I hope, no point in double precision), optional
        An arbitrary probability cut-off at which to reject classification. The default is 0.85.

    Returns
    -------
    None.

    """
    #Load in alignment methods
    ###from zellerify.align import needlemanWunsch, dropInsertions
    
    
    #test lines
    """
    classifierPickle = "zellerify/data/h1/aa/p10_aa_no2020_train.fasta.classify.pickle"
    classifierPickle = "C:/Users/mazeller.NUSSTF/Desktop/Lab/sequence_classifier/prrsv_orf5/not1/p100train.na.fasta.classify.pickle"
    importClassifier = pickle.load(open( classifierPickle, "rb" ))     #489us
    inputFile = "zellerify/data/h1/aa/aa_2020_test.fasta"
    df = loadFasta(inputFile)              
    """
    
    # Load in the pickle. This section has a security vunerabiltiy that should be looked into
    importClassifier = pickle.load(open( classifierPickle.name, "rb" ))

    #Load in and align sequences via CPU
    df = loadFasta(inputFile.name)                                              #17.8ms slow
    
    #Create blank feature list via numpy, number of undef x number of features
    features = list(importClassifier["features"])                               #89.3us
    featureTable = np.zeros(shape=(df.shape[0],len(features)))                  #7.9us
    
    # Do alignments
    for i,row in enumerate(df.values):
        x = NeedlemanWunsch(row[1].replace("-",""), importClassifier["base_seq"])  #Arendsee align 1.95 ms +- 13.2us
        cleanedSeq = x.get_alignment()

        #Fill out onehot encoded array, very slow method with double loops O(n^2)
        for j, context in enumerate(features):                                  #1.48 ms
            context = context.split("_")
            pos = int(context[0])
            res = context[1].lower()
            
            #Skip if out of bounds
            if (pos > len(cleanedSeq) - 1):
                continue
            
            if (cleanedSeq[pos].upper() == res.upper()):
                featureTable[i, j] = 1
    
    #Predict characters and probs
    clade = importClassifier["classifier"].predict(featureTable)                #53.6us
    clade = importClassifier["labels"].inverse_transform(clade)     
    cladeProbs = importClassifier["classifier"].predict_proba(featureTable)     #68.2us
    cladeProbs = np.array([[x] for x in np.max(cladeProbs, axis=1)])

    #Arrange dataframe
    results = pd.DataFrame()                                                    #125us
    results["taxa"] = df[0]                                                     #33.1us
    results["clade"] = clade                                                    #38us
    results["prob"] = cladeProbs                                                #31.8us

    #Trim threshold
    results.loc[results['prob'] < threshold, "clade"] = "unknown"               #317us
    
    # Print to screen
    for row in results.values:
        print('{0}\t{1}\t{2}'.format(row[0], row[1], row[2]))
    
    return


def getFeatures(classifierPickle):
    """
    List the features relevant to a specific classification. Features are 
    returned in the format of [Position][Acid]. The position is relative to the
    provided alignment, and are not absolute. This feature is meant primarily 
    for debugging.

    Parameters
    ----------
    classifierPickle : STRING
        Path to an output pickle file, generated by the trainClassifier function.

    Returns
    -------
    None.

    """
    #Load in alignment methods
    ###from zellerify.align import needlemanWunsch, dropInsertions
    
    
    #test lines
    """
    classifierPickle = "zellerify/data/h1/aa/p1_aa_no2020_train.fasta.classify.pickle"
    importClassifier = pickle.load(open( classifierPickle, "rb" ))     #489us      
    """
    
    # Load in the pickle. This section has a security vunerabiltiy that should be looked into
    importClassifier = pickle.load(open( classifierPickle.name, "rb" ))

    #Create blank feature list via numpy, number of undef x number of features
    features = list(importClassifier["features"])                               #89.3us
    print("\n".join(sorted(features)))
    
    return