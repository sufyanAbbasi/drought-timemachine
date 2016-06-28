import sys, getopt, json
from os import listdir, walk, makedirs
from os.path import isfile, join, isdir, exists
from shutil import copyfile

def main(argv):
	source_root = ''
	dest_root = ''
	try:
		opts, args = getopt.getopt(argv,"hs:d:",["sdir=","ddir="])
	except getopt.GetoptError:
		print 'usage: processMapTiles.py -s <sourcedir> -d <destfile>'
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			print 'usage: processMapTiles.py -s <sourcedir> -d <destfile>'
			sys.exit()
		elif opt in ("-s", "--sdir"):
	 		source_root = arg
		elif opt in ("-d", "--ddir"):
	 		dest_root = arg

	if(source_root == ''):
		print 'No source directory specified. Use -h flag for help.'
		sys.exit(2)
	elif(dest_root == ''):
		print 'No destination directory specified. Use -h flag for help.'	
		sys.exit(2)

	numrows = 0
	numcols = 0
	source_root += '/'
	dest_root += '/'
	type_root = '0100-unstitched/' #'0100-original-images/'
	time_folders = [f for f in listdir(source_root) if not isfile(f)]
	for current_dir in time_folders:
		current_path = source_root + current_dir + '/'
		max_zoom_dir = max(walk(current_path).next()[1])
		current_path += max_zoom_dir + '/'
		dest_dir = '{0}/{2}{1}-000000/'.format(dest_root, current_dir, type_root)
		if not exists(dest_dir):
			makedirs(dest_dir)
		i = 0;
		tile_dirs = sorted([int(f) for f in walk(current_path).next()[1]])
		numcols = len(tile_dirs)
		for tile_dir in tile_dirs:
			current_path_file = current_path + str(tile_dir) + '/'
			file_ext = '.' + listdir(current_path_file)[0].split('.')[1]
			file_dir = sorted([int(f.split('.')[0]) for f in listdir(current_path_file)])
			numrows = len(file_dir)
			for file in file_dir:
				path_to_file = current_path_file + str(file) + file_ext
				copyfile(path_to_file, "{0}IMG-{1}{2:0=2d}{3}".format(dest_dir, current_dir, i, file_ext))
				i += 1

	definitions = {}
	capture_times = walk('{0}{1}'.format(dest_root, type_root)).next()[1]
	definitions["source"] = {};
	definitions["source"]["type"] = "stitch"
	definitions["source"]["align_to"] = "[i-1]"
	definitions["source"]["align_to_comment"] =  "Align each gigapan to the previous one"
	definitions["source"]["cols"] = numcols
	definitions["source"]["rows"] = numrows
	definitions["source"]["width"] = 1
	definitions["source"]["height"] = 1
	definitions["source"]["capture_times"] = capture_times
	videosets = {}
	videosets["label"] = "Drought Timelapse"
	videosets["type"] = "h.264"
	videosets["size"] = "large"
	videosets["quality"] = 26
	videosets["fps"] = len(time_folders)/2
	definitions["videosets"] = [videosets]
	
	with open(dest_root+'definition.tmc', 'w') as outfile:
		json.dump(definitions, outfile)
	
if __name__ == "__main__":
   main(sys.argv[1:])



