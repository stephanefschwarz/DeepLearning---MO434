import numpy as np
import pandas as pd
import argparse
import re

from glob import glob
from pyopenms import *

def command_line_parsing():
	"""Parse command lines
		Parameters
		----------
		model_path : str
			path to the train dataset
		model : URLPhish
			path to the train dataset
		Returns
		-------
		parser
			The arguments from command line
	"""
	parser = argparse.ArgumentParser(description = __doc__)

	parser.add_argument('--folder', '-f',
						dest='folder',
						required=True,
						help='Path to data folder')

	parser.add_argument('--output_file', '-o',
						dest='output',
						required=True,
						help='Output pickle file')

	return parser.parse_args()


def arrange_data(data_path, output_file):

	list_sample_name = []
	list_mz = []
	list_intensity = []
	list_label = []

	label_folder = glob(data_path+'*')
	for folder in label_folder:

		pattern = r'(N|P)\d+'

		samples = glob(folder+'/*')

		for sample in samples:
		
			sample_name = re.search(pattern, sample)[0]

			experiment = MSExperiment()

			try:

				MzMLFile().load(sample, experiment)

			except Exception as e:
				print('Exception: ', e)
				# add log here

			mz, intensity = experiment[0].get_peaks()
			label = 'negative' if (re.search('Neg', folder) != None) else 'positive'

			list_sample_name.append(sample_name)
			list_mz.append(mz)
			list_intensity.append(intensity)
			list_label.append(label)

	json_dataset = {
					'sample_name': list_sample_name,
					'mz': list_mz,
					'intensity': list_intensity,
					'label': list_label
				   }

	dataset = pd.DataFrame(json_dataset)

	dataset.to_pickle('./')


def main():

	args = command_line_parsing()

	arrange_data(args.folder, args.output)


if __name__ == '__main__':
	main()
