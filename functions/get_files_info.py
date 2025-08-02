import os
def get_files_info(working_directory, directory="."):
    new_directory = os.path.join(working_directory, directory)
    new_directory = os.path.abspath(new_directory)
    new_working_directory = os.path.abspath(working_directory)

    if new_directory.startswith(new_working_directory):
        if os.path.isdir(new_directory):
            try:
                file_list = []
                for i in os.listdir(new_directory):
                    file_path = os.path.join(new_directory, i)
                    info_string = f"- {i}: file_size={os.path.getsize(file_path)} bytes, is_dir={os.path.isdir(file_path)}"
                    file_list.append(info_string)
                return "\n".join(file_list)
            except Exception as e:
                return f"Error: {e}"
        else:
            return(f'Error: "{directory}" is not a directory')
    else:
        return(f'Error: Cannot list "{directory}" as it is outside the permitted working directory')