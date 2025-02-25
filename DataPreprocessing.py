import os
import re
import glob
import shutil

class DataPreprocessor:
    def __init__(self, input_base_dir, output_base_dir):
        self.input_base_dir = input_base_dir
        self.output_base_dir = output_base_dir

        

    def clean_rfc_file(self, input_path, output_path):
        with open(input_path, 'r', encoding='utf-8', errors='replace') as f:
            content = f.read()

        #  split into lines
        lines = content.split('\n')

        # define patterns for headers and footers
        header_pattern = re.compile(r'.*Expires \w* \d*.*\[Page \d*]')
        footer_pattern = re.compile(r'^Internet-Draft.*\d{4}$')

        # process lines
        cleaned_lines = []
        
        for line in lines:
            # Skip header and footer lines
            if header_pattern.match(line) or footer_pattern.match(line):
                continue
            
            # Keep the content
            cleaned_lines.append(line)
        
        # make output directory if it doesn't exist
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        # write cleaned lines to output file
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(cleaned_lines))
        return output_path
    
    def process_greenai_data(self):
        """
        Process all RFC files in the GreenAI Data directory structure.
        
        Args:
            input_base_dir: Path to the GreenAI Data directory
            output_base_dir: Path to the output directory for cleaned files
        """
        # Create output base directory if it doesn't exist
        if not os.path.exists(self.output_base_dir):
            os.makedirs(self.output_base_dir)
        
        # Get all subdirectories in the GreenAI Data folder
        subdirs = [d for d in os.listdir(self.input_base_dir) 
                if os.path.isdir(os.path.join(self.input_base_dir, d))]
        
        for subdir in subdirs:
            input_subdir_path = os.path.join(self.input_base_dir, subdir)
            output_subdir_path = os.path.join(self.output_base_dir, subdir)
            
            # Create output subdirectory if it doesn't exist
            if not os.path.exists(output_subdir_path):
                os.makedirs(output_subdir_path)
            
            # Find all .txt files in the subdirectory
            file_paths = glob.glob(os.path.join(input_subdir_path, "*.txt"))

            
            # Process each file
            for file_path in file_paths:
                filename = os.path.basename(file_path)
                output_path = os.path.join(output_subdir_path, filename)
                
                # If it's an RFC file (most recent), just copy it
                if filename.startswith('rfc'):
                    print(f"Copying most recent RFC file: {filename}")
                    shutil.copy2(file_path, output_path)
                # If it's a draft file, clean it
                else:
                    print(f"Processing draft file: {filename}")
                    self.clean_rfc_file(file_path, output_path)
                
                print(f"Completed {filename}")
            
            print(f"Processed all files in {subdir}")

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Clean RFC-Style text files by removing headers and footers")
    parser.add_argument("--input_dir", default="GreenAI Data", help="Path to the GreenAI Data directory")
    parser.add_argument("--output_dir", default="GreenAI Data Cleaned", help="Path to the output directory for cleaned files")

    args = parser.parse_args()
    
    # Initialize the DataPreprocessor
    preprocessor = DataPreprocessor(args.input_dir, args.output_dir)

    # Process the GreenAI Data
    preprocessor.process_greenai_data()


    # examples
    # python DataPreprocessing.py --input_dir "GreenAI Data" --output_dir "GreenAI Data Cleaned
