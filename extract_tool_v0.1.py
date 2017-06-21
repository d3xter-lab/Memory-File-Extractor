import sys
import mmap
import os
import argparse
import time

# Init progress
def init():
    # Main Title
    print "######################################################"
    print "##            File Format Extractor 1.0.0           ##"
    print "##                                                  ##"
    print "##                                         2016.10  ##"
    print "######################################################"
    #time.sleep(0)
    
# File Signature setting

def Image_Extract(dirname):

    filenames = os.listdir('./'+dirname)

    print "[+] Extract_file_name"
    
    for filename in filenames:
        full_filename = os.path.join('./'+dirname, filename)
        extract_jpg(full_filename)
        extract_png(full_filename)
        extract_gif(full_filename)


def pdf_Extract(dirname):

    filenames = os.listdir('./'+dirname)

    print "[+] Extract_file_name"

    for filename in filenames:
        full_filename = os.path.join('./'+dirname, filename)
        extract_pdf(full_filename)


def extract_jpg(fname):
        header = reduce(lambda x, y: x+y, map(chr, [0xff, 0xd8, 0xff, 0xe0]))
        trailer = reduce(lambda x, y: x+y, map(chr, [0xff, 0xd9]))
        type = 'jpg'
        extract_file(fname, header, trailer, type)

def extract_png(fname):
	header = reduce(lambda x, y: x+y, map(chr, [0x89, 0x50, 0x4E, 0x47, 0x0D, 0x0A, 0x1A, 0x0A]))
	trailer = reduce(lambda x, y: x+y, map(chr, [0x49, 0x45, 0x4E, 0x44, 0xAE, 0x42, 0x60, 0x82]))
	type = 'png'
	extract_file(fname, header, trailer, type)

def extract_gif(fname):
	header = reduce(lambda x, y: x+y, map(chr, [0x47, 0x49, 0x46, 0x38, 0x39, 0x61]))
	trailer = reduce(lambda x, y: x+y, map(chr, [0x00, 0x3B]))
	type = 'gif'
	extract_file(fname, header, trailer, type)
    
def extract_pdf(fname):
	# header
	header = reduce(lambda x, y: x+y, map(chr, [0x25, 0x50, 0x44, 0x46]))
	# trailer
	trailer = reduce(lambda x, y: x+y, map(chr, [0x0A, 0x25, 0x25, 0x45, 0x4F, 0x46]))
	type = 'pdf'
	extract_file(fname, header, trailer, type)

# Extract files from memory dump
def extract_file(fname, header, trailer, type):
	found_idx = 0
	with open(fname, "r+b") as f:
		# memory-map the file, size 0 means whole file
		fmap = mmap.mmap(f.fileno(), 0)
   
		pos = fmap.find(header)
		while pos != -1:
			#print "[*] Found possible %s header at 0x%x" % (type, pos)
			pos_old = pos
					   
			pos_tr = fmap.find(trailer, pos + 4)
			#print "[*] Found possible %s trailer at 0x%x" % (type, pos_tr)
					 
			# Search for other occurences
			pos = fmap.find(header, pos + 2)
            
			# Create output file
			fout = open("./%s_%s.%s" % (type, str(found_idx), type), "wb")
			fmap.seek(pos_old)
			if pos == -1 :
				fout.write(fmap.read(pos_tr - pos_old + 2))
			else :
				fout.write(fmap.read(min(pos,pos_tr) - pos_old + 2))
			fout.close()
			found_idx = found_idx + 1

			print "[-] %s - %s" % (fname, type)
				   
		# close the map
		fmap.close()
                

if __name__=="__main__":
    
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--pdf", action="store_true", help="Extract PDF file")
    parser.add_argument("-i", "--image", action="store_true", help="Extract image file (jpg, gif, png)")
    parser.add_argument("-d", "--directory", action="store_true", help="Select_directory")
    parser.add_argument("filename", type=str, help="filename")
    options = parser.parse_args()

    init()
    
    if options.image :
        if options.directory :
            print "[+] Directory name : %s" % sys.argv[3]
            Image_Extract(sys.argv[3])
            print "[*] Directoty_Extract_Success"
        else :
            print "[+] Filename : %s" % sys.argv[2]
            print "[+] Extract_file_name"
            extract_jpg(sys.argv[2])
            extract_png(sys.argv[2])
            extract_gif(sys.argv[2])
            print "[*] File_Extract_Success"
            
    elif options.pdf :
        if options.directory :
            print "[+] Directory name : %s" % sys.argv[3]
            pdf_Extract(sys.argv[3])
            print "[*] Directoty_Extract_Success"
        else :
            print "[+] Filename : %s" % sys.argv[2]
            print "[+] Extract_file_name"
            extract_pdf(sys.argv[2])
            print "[*] File_Extract_Success"
        
