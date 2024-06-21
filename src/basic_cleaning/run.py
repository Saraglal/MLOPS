#!/usr/bin/env python
"""
An example of a step using MLflow and Weights & Biases
"""
import argparse
import logging
import wandb


logging.basicConfig(level=logging.INFO, format="%(asctime)-15s %(message)s")
logger = logging.getLogger()


def go(args):
    run = wandb.init(job_type="basic_cleaning")
    run.config.update(args)

    logger.info("Starting data cleaning process...")
    logger.info(f"Parameter 1: {args.parameter1}")
    logger.info(f"Parameter 2: {args.parameter2}")
    logger.info(f"Parameter 3: {args.parameter3}")

    cleaned_data = {
        "param1": args.parameter1,
        "param2": args.parameter2,
        "param3": args.parameter3
    }

    logger.info("Data cleaning completed.")
    logger.info("Saving results to Weights & Biases...")

    run.finish()


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="This step cleans the data")


    parser.add_argument(
        "--parameter1",
        type=str,
        help="Description of parameter1",
        required=True
    )

    parser.add_argument(
        "--parameter2",
        type=int,
        help="Description of parameter2",
        required=True
    )

    parser.add_argument(
        "--parameter3",
        type=float,
        help="Description of parameter3",
        required=True
    )


    args = parser.parse_args()

    go(args)
