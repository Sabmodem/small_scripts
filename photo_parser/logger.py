import logging
import os

log_dir = os.path.join(os.getcwd(), 'log')

def create_dir_if_not_exists():
  if not os.path.exists(log_dir):
    os.mkdir(log_dir)

def loggerInit(filename):
  create_dir_if_not_exists()
  logging.basicConfig(level=logging.INFO, filename=os.path.join(log_dir, filename),filemode="a", format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
