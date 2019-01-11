"""Main.

This is the main module that runs the neural network according to arguments.
This is also the module that connects to AirSim to actually drive the vehicle.

Authors:
    Maximilian Roth
    Nina Pant
    Yvan Satyawan <ys88@saturn.uni-freiburg.de>
"""
import argparse

from runner import Runner

from os import path

def parse_arguments():
    """Parses arguments from terminal."""
    description = "Trains DriveNet on a dataset or runs it in AirSim."
    parser = argparse.ArgumentParser(description=description)

    # Required:
    parser.add_argument('weights', metavar='W', type=str, nargs=1,
                        help="file that has the weights, or where the weights"
                             "should be stored.")

    # Training and training arguments
    parser.add_argument('-t', type=str, nargs='?',
                        help="sets to training mode and the data directory.")
    parser.add_argument('-c', '--csv-dir', type=str, nargs='?',
                        help="location of the csv file, if it is not in the "
                        "data root directory.")
    parser.add_argument('-b', '--batch-size', type=int, nargs='?', default=120,
                        help="batch size of the training.")
    parser.add_argument("-p", "--epoch", type=int, nargs='?', default=1,
                        help="number of epochs to train for.")

    # Run the model
    parser.add_argument('-e', '--eval', action='store_true',
                        help="set to evaluation mode")

    args = parser.parse_args()

    if args.t and args.eval:
        parser.error("Cannot be in both training and evaluation modes at the "
                     "same time.")

    if not args.t and not args.eval:
        parser.error("What do you want me to do?")

    return args


def main(args):
    """Main function that runs everything"""
    runner = Runner(args.weights[0])

    if args.t:
        # Means run in training mode, parse args
        if args.csv_dir is not None:
            csv_dir = args.csv_dir
        else:
            csv_dir = path.join(args.t, "control_input.csv")

        # Now run the training
        runner.train_model(csv_dir, args.t, args.epoch, args.batch_size)

    elif args.eval:
        # TODO Make this run airsim
        pass

if __name__ == "__main__":
    args = parse_arguments()
    print(args)
    main(args)
