#!/usr/bin/env python3
import numpy as np
import os
import sys
import struct
import argparse

def r_ascii_w_bcr(infilename, outfilename):
	data=[]
	counter = 0
	with open(infilename,'r', encoding = "ascii") as asci_matrix:
		num_sequence = []
		for line in asci_matrix:
			if line.startswith("# Width"):
				if line.split()[3] == "nm":
					width = line.split()[2]
					units = "nm"
				else: 
					print("Unknown units- units need to be in nm")
					return(1)
					sys.exit()
			if line.startswith("# Height"):
				if line.split()[3] == units:
					height = line.split()[2]
				else: 
					print("x and y  units doesn't match")
					return(1)
					sys.exit()
			if line.startswith("# Value units:"):
				if line.split()[3] == 'm':
					m_to_nm = 1e9
				else:
					print("unknown unit")
					return(1)
					sys.exit()
			if(line[0].isdigit()):
				#print("line startswith #")
				line_seq = line.split()
				#if(counter == 0):
				#print(counter + "\n")
				xpixels = len(line_seq)
				num_sequence.extend([round(m_to_nm*float(i),3) for i in line_seq])
				counter += 1
		ypixels = counter
		bit2nm = 0.01 
		nm2bit = 1/bit2nm
	print(max(num_sequence))
	print(len(num_sequence))
	with open(outfilename,'a+', encoding = 'ascii') as bcr_file_text:
		header = "fileformat = {}\nxlength = {}\nylength = {}\nxpixels = {}\nypixels = {}\nbit2nm = {}\n".format("bcrstm",width,height,xpixels,ypixels,bit2nm)
		#bcr_file_text.write ("fileformat = {}\n".format("bcrstm"))
		#bcr_file_text.write ("xlength = {}\n".format(width))
		#bcr_file_text.write ("ylength = {}\n".format(height))
		#bcr_file_text.write ("xpixels = {}\n".format(xpixels))
		#bcr_file_text.write ("ypixels = {}\n".format(ypixels))
		#bcr_file_text.write ("bit2nm = {}\n".format(bit2nm))
		#size_read = bcr_file_text.read()
		#print("Fuckin size is {}".format(len(size_read)))
		bcr_file_text.write(header)
		header_byte_size=sys.getsizeof(header)
		char_to_fill = (2048 - len(header)) * 'a'
		bcr_file_text.write(char_to_fill)
	#bin_seq = int(nm2bit * num_sequence[0]).to_bytes(2, 'little') # initiate binary sequence
	bin_seq = bytes()
	seq_cnt = 0
	for i in range(0, len(num_sequence)):
		bin_seq = (bin_seq + int(nm2bit * num_sequence[i]).to_bytes(2,'little')) # 16bit integer
		seq_cnt += 1 
	print(seq_cnt)
	print(bin_seq)
	with open(outfilename,'ab+') as bcr_file_bin:
		bcr_file_bin.write(bin_seq)		
	return(0)

#r_ascii_w_bcr('ascii_matrix2bcr.py','input/1hzh_ascii antibody.bcr')
def Main():
	pdb = {}
	parser = argparse.ArgumentParser(description='Bcr from ascii creator')
	parser.add_argument("ascii_file", help = "ascii file to read", type=str)
	parser.add_argument("output_file", help = "bcr file to output", type=str)
	#parser.add_argument("--endianity", help = "Byte order depending on your system, default is 1", type=int, default=1)
	args = parser.parse_args()
	if ((args.output_file is not None) and (args.ascii_file is not None)):
		print(r_ascii_w_bcr(args.ascii_file, args.output_file))
	else: 
		print('\n Input must include input ascii file and output bcr file \n')
		return(0)	
	return()
if __name__  == '__main__' :
	Main()

