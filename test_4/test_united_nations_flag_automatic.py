import os
import shutil
from yyc import pipeline
from yyc import scheme
from yyc.utils import data_handle

out_dir = "./output"
shutil.rmtree(out_dir)
os.mkdir(out_dir)
read_file_path = "./files/United Nations Flag.bmp"
dna_path = "./output/united_nations_flag.dna"
model_path = "./output/united_nations_flag.pkl"
write_file_path = "./output/output_united_nations_flag.jpg"

if __name__ == "__main__":
  n=0
  n_success=0
  while(n<30) :
    if(os.path.isfile(dna_path)) : os.remove(dna_path)
    # YYC No.1536 scheme
    # [support_base, rule1, rule2] = ["A", [1, 1, 0, 0], [[1, 0, 1, 0], [1, 0, 1, 0], [1, 0, 1, 0], [1, 0, 1, 0]]]
    # YYC No.1 scheme
    # [support_base, rule1, rule2] = ["A", [0, 0, 1, 1], [[0, 1, 0, 1], [0, 1, 0, 1], [0, 1, 0, 1], [0, 1, 0, 1]]]
    # YYC No.888 scheme
    [support_base, rule1, rule2] = ["A", [1, 0, 0, 1], [[0, 1, 0, 1], [1, 1, 0, 0], [1, 0, 1, 0], [0, 0, 1, 1]]]
    # YYC No.496 scheme
    # [support_base, rule1, rule2] = ["A", [0, 1, 0, 1], [[1, 1, 0, 0], [1, 0, 0, 1], [1, 1, 0, 0], [1, 1, 0, 0]]]
    tool = scheme.YYC(support_bases=support_base, base_reference=rule1, current_code_matrix=rule2, search_count=100, max_homopolymer=4, max_content=0.6)
    try :
      pipeline.encode( method=tool, input_path=read_file_path, output_path=dna_path, model_path=model_path, need_index=True, need_log=True)
    except :
      pass
    del tool
    if(os.path.isfile(dna_path)) : 
      n_success+=1
      dna_path_new = dna_path + '_' + str(n)
      os.rename(dna_path, dna_path_new)
    # pipeline.decode( model_path=model_path, input_path=dna_path, output_path=write_file_path, has_index=True, need_log=True)

    # # compare two file
    # matrix_1, _ = data_handle.read_binary_from_all(read_file_path, 120, False)
    # matrix_2, _ = data_handle.read_binary_from_all(write_file_path, 120, False)
    # print("source digital file == target digital file: " + str(matrix_1 == matrix_2))
    n+=1
  print( 'n_success   ', n_success)
