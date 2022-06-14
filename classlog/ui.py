import signal
import os
from classlog.version import __version__
import sys
import click

INT_SENTINEL = 1e9

CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])

@click.command(
    name="train",
    help="Train a logistic regression classifier with a reference set",
    context_settings={'show_default': True}
)
@click.argument("alignment", default=sys.stdin, type=click.File())
@click.option("-d", "--delimiter", default="|")
@click.option("-n", "--column", type=int, default=1)
@click.option("-p", "--percent", type=float, default=0.0)
def train_cmd(alignment, delimiter, column, percent):
    from classlog.classify import trainClassifier
    trainClassifier(alignment.name, delim=delimiter, col=column, percentFeatures=percent)

@click.command(
    name="predict",
    help="Predict clades of a fatsa file based on previosuly trained model",
)
@click.argument("model", default=sys.stdin, type=click.File())
@click.argument("data", default=sys.stdin, type=click.File())
def predict_cmd(model, data):
    from classlog.classify import predictUnknown
    predictUnknown(model, data)


@click.command(
    name="predictmissing",
    help="Process a mixed datatset and fill in missing values",
    context_settings={'show_default': True}
)
@click.argument("alignment", default=sys.stdin, type=click.File())
@click.option("-d", "--delimiter", default="|")
@click.option("-n", "--column", type=int, default=1)
def predictmissing_cmd(alignment, delimiter, column):
    # import this down here so there is not a long lag when just asking for help
    from classlog.classify import predictMissing
    predictMissing(alignment.name, delim=delimiter, col=column)


@click.command(
    name="getclasses",
    help="Pulls classification names from designated position",
    context_settings={'show_default': True}
)
@click.argument("alignment", default=sys.stdin, type=click.File())
@click.option("-d", "--delimiter", default="|", show_default=True)
@click.option("-n", "--column", type=int, default=1)
def getclasses_cmd(alignment, delimiter, column):
    # import this down here so there is not a long lag when just asking for help
    from classlog.classify import getClasses
    getClasses(alignment.name, delim=delimiter, col=column)


@click.command(
    name="getfeatures",
    help="List the features in a trained classifier",
)
@click.argument("model", default=sys.stdin, type=click.File())
def getfeatures_cmd(model):
    from classlog.classify import getFeatures
    getFeatures(model)
    
    
@click.group(help="A tool for using logistic regression for classifying genetic sequences.", context_settings=CONTEXT_SETTINGS)
def cli_grp():
    pass


cli_grp.add_command(train_cmd)
cli_grp.add_command(predict_cmd)
cli_grp.add_command(predictmissing_cmd)
cli_grp.add_command(getclasses_cmd)
cli_grp.add_command(getfeatures_cmd)


def main():
    cli_grp()


if __name__ == "__main__":
    if os.name == "posix":
        signal.signal(signal.SIGPIPE, signal.SIG_DFL)
    main()
