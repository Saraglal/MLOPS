#!/usr/bin/env python
"""
Download from W&B the raw dataset and apply some basic data cleaning, exporting the result to a new artifact
"""
import argparse
import logging
import wandb
import pandas as pd


logging.basicConfig(level=logging.INFO, format="%(asctime)-15s %(message)s")
logger = logging.getLogger()


def go(args):

    run = wandb.init(job_type="basic_cleaning1")
    run.config.update(args)

    # Download input artifact. This will also log that this script is using this
    # particular version of the artifact
    # artifact_local_path = run.use_artifact(args.input_artifact).file()

    ######################
    # Setup logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    # Define and parse command-line arguments
    parser = argparse.ArgumentParser(description="Process Airbnb data")
    parser.add_argument('--min_price', type=float, required=True, help='Minimum price to filter outliers')
    parser.add_argument('--max_price', type=float, required=True, help='Maximum price to filter outliers')
    args = parser.parse_args()

    # Initialize a W&B run
    run = wandb.init(project="nyc_airbnb", group="eda", save_code=True)
    logger.info("Initialized W&B run.")

    # Download the artifact and read the data into a DataFrame
    local_path = wandb.use_artifact("sample.csv:latest").file()
    logger.info(f"Downloaded artifact and stored at {local_path}.")
    df = pd.read_csv(local_path)
    logger.info("Data loaded into a DataFrame.")

    # Generate a pandas profiling report
    import pandas_profiling

    profile = pandas_profiling.ProfileReport(df)
    profile.to_widgets()
    logger.info("Generated pandas profiling report.")

    # Drop outliers based on price using args.min_price and args.max_price
    min_price = args.min_price
    max_price = args.max_price
    idx = df['price'].between(min_price, max_price)
    df = df[idx].copy()
    logger.info(f"Dropped outliers outside the range {min_price} to {max_price}.")

    # Convert the 'last_review' column to datetime
    df['last_review'] = pd.to_datetime(df['last_review'])
    logger.info("Converted 'last_review' column to datetime.")

    # Save the cleaned DataFrame to a CSV file
    output_file = "clean_sample.csv"
    df.to_csv(output_file, index=False)
    logger.info(f"Saved the cleaned DataFrame to {output_file}.")

    # Display DataFrame info
    df.info()

    # Finish the W&B run
    run.finish()
    logger.info("W&B run finished.")

    artifact = wandb.Artifact(
     args.output_artifact,
     type=args.output_type,
     description=args.output_description,
    )
    artifact.add_file("clean_sample.csv")
    run.log_artifact(artifact)
    ######################


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="A very basic data cleaning")


    parser.add_argument(
        "--input_artifact", 
        type= str,
        help="Description of input_artifact",
        required=True
    )

    parser.add_argument(
        "--output_artifact", 
        type= str,
        help="Description of output_artifact",
        required=True
    )

    parser.add_argument(
        "--output_type", 
        type= str,
        help="Description of output_type",
        required=True
    )

    parser.add_argument(
        "--output_description", 
        type= str,
        help="Description of output_description",
        required=True
    )

    parser.add_argument(
        "--min_price", 
        type= float,
        help="Description of min_price",
        required=True
    )

    parser.add_argument(
        "--max_price", 
        type= float,
        help="Description of max_price",
        required=True
    )


    args = parser.parse_args()

    go(args)
