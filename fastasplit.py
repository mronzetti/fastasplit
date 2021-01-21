import os
import sys
import argparse

print('\n*****************************************************************')
print('      Script to split FASTA sequences into individual files')
print('                    Michael Ronzetti 2020')
print('\n*****************************************************************')

parser = argparse.ArgumentParser(description="Split multi fasta file into individual files using sequence ids as their file names.")
parser.add_argument("-m", "--multifasta", metavar = "multifasta", help="Input FASTA file", type = str)
args = parser.parse_args()

in_file = args.multifasta
file_path = os.path.abspath(os.path.dirname(in_file))
os.mkdir(file_path+'/split')
scr = open(file_path+'/itasser.swarm', 'x')
try:
	with open(in_file, "r") as fa:
	    lines=fa.read().split('>')
	    lines = lines[1:]
	    lines=['>'+ seq for seq in lines]
	    for name in lines:
	    	#Extracting sequence Id to use it for file name
	        file_name=name.split('\n')[0][1:]  
	        out_file=open(file_path+"/split/"+file_name+".fasta", "w")
	        out_file.write(name)
	        out_file.close()
	print ("\nSuccessfully split "+os.path.basename(in_file)+" into single files")
except:
	sys.exit("Whoops! Incorrect file passed to script.")

#Rename all files in sequential order
rename_path=file_path+'/split/'
files=os.listdir(rename_path)
for index, file in enumerate(files):
	os.mkdir(os.path.join(rename_path, 'seq'+str(index)))
	os.rename(rename_path+file, rename_path+'seq'+str(index)+'/'+'seq.fasta')
	scr.write('export TMPDIR="/lscratch/$SLURM_JOB_ID"; runI-TASSER.pl -runstyle gnuparallel -LBS true -EC true -GO true -seqname seq'+str(index)+ ' -datadir ./seq'+str(index)+' -light true -outdir ./seq'+str(index)+' && file2html.py ./seq'+str(index)+'\n')
	print('Seq '+str(index) +' successfully split')

