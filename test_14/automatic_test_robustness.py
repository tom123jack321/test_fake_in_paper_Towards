import os
from yyc import pipeline
from yyc import scheme
from yyc.utils import data_handle
from module_robustness import change_nucleotide

error_rates = [0.0001, 0.0010, 0.0030, 0.0050, 0.0080, 0.0100]
error_types = ["substitution", "deletion", "insertion", "mix"]
original_files = ["mona_lisa.jpg", "united_nations_flag.bmp"]
# the number of tests for each file at every error rate every error type
number_tests = 1
robustness_log = "robustness.txt"

fh_rob = open(robustness_log, "wt")
s_dict = {}
s_dict["substitution"] = "substituted"
s_dict["deletion"] = "deleted"
s_dict["insertion"] = "inserted"
s_dict["mix"] = "substituted, deleted or inserted"
if __name__ == "__main__":
 for f_in in original_files :
   f_name = os.path.splitext(os.path.basename(f_in))[0]
   read_file_path = "./files/" + f_in
   dna_path = "./output/" + f_name + ".dna"
   model_path = "./output/" + f_name + ".pkl"

   # values of [support_base, rule1, rule2] determine whether encode could succeeds. This scheme fails for file "united_nations_flag.bmp"
   # YYC No.1536 scheme
   # [support_base, rule1, rule2] = ["A", [1, 1, 0, 0], [[1, 0, 1, 0], [1, 0, 1, 0], [1, 0, 1, 0], [1, 0, 1, 0]]]
   # YYC No.1 scheme
   # [support_base, rule1, rule2] = ["A", [0, 0, 1, 1], [[0, 1, 0, 1], [0, 1, 0, 1], [0, 1, 0, 1], [0, 1, 0, 1]]]
   # YYC No.888 scheme
   [support_base, rule1, rule2] = ["A", [1, 0, 0, 1], [[0, 1, 0, 1], [1, 1, 0, 0], [1, 0, 1, 0], [0, 0, 1, 1]]]
   # YYC No.496 scheme
   # [support_base, rule1, rule2] = ["A", [0, 1, 0, 1], [[1, 1, 0, 0], [1, 0, 0, 1], [1, 1, 0, 0], [1, 1, 0, 0]]]
   tool = scheme.YYC(support_bases=support_base, base_reference=rule1, current_code_matrix=rule2, search_count=100, max_homopolymer=4, max_content=0.6)
   pipeline.encode( method=tool, input_path=read_file_path, output_path=dna_path, model_path=model_path, need_index=True, need_log=True)
   del tool

   for error_rate in error_rates :
    for error_type in error_types :
      n_test = 0
      n_success = 0
      dna_path_new = dna_path + "_new" + "_" + str(error_rate) +"_"+ str(error_type) +"_"+ "subTest" +"_"+ str(n_test)
      write_file_path = "./output/output_" + f_name + "_" + str(error_rate) +"_"+ str(error_type) +"_"+ "subTest" +"_"+ str(n_test) + ".jpg"
      while( n_test < number_tests ) :
        if(os.path.isfile(dna_path_new)) : os.remove(dna_path_new)
        if(os.path.isfile(write_file_path)) : os.remove(write_file_path)
        n_base, n_err_base = change_nucleotide(dna_path, error_rate, error_type, dna_path_new)

        try :
          pipeline.decode( model_path=model_path, input_path=dna_path_new, output_path=write_file_path, has_index=True, need_log=True)
        except :
          print("Failed to decode! Error : " + str(IOError) )
          pass

        # compare two files 
        if(os.path.isfile(write_file_path)) :
          matrix_1, _ = data_handle.read_binary_from_all(read_file_path, 120, False)
          matrix_2, _ = data_handle.read_binary_from_all(write_file_path, 120, False)
          # print("source digital file == target digital file: " + str(matrix_1 == matrix_2))
          if(matrix_1 == matrix_2) :
              n_success += 1
              print("Successful recovery of original information!")
          else :
              print("Failed to recover original information!")
        else :
            print("Failed to recover original information!")
        n_test += 1
        ###################### end while #################################
      success_rate = n_success/number_tests
      fh_rob.write("Error rate: "+str(error_rate) +"\n")
      fh_rob.write("Error type: "+str(error_type) +"\n")
      fh_rob.write("The number of tests: "+str(number_tests) +"\n")
      fh_rob.write("The number of successful recoveries: "+str(n_success) +"\n")
      fh_rob.write("Success rate: "+str(success_rate) +"\n")
      fh_rob.write("Tested file: "+str(read_file_path) +"\n")
      fh_rob.write("The number of nucleotides in each test: " + str(n_base) +"\n")
      fh_rob.write("The number of nucleotides " + s_dict[error_type] + " in each test: " + str(n_err_base) +"\n")
      fh_rob.write("\n")
