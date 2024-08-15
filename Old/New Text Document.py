# Check each directory in the base path
for dirname in os.listdir(base_path):
    if re.search(regex, dirname):
        base_subdirs.append(os.path.join(base_path, dirname))
        
    full_dir_path = os.path.join(base_path, dirname)
    
    # Check if it's a directory
    if os.path.isdir(full_dir_path):
        zip_folder = os.path.join(full_dir_path, 'zip')

        # Create 'zip' directory if not exists
        if not os.path.exists(zip_folder):
            os.makedirs(zip_folder)

        # Check each file in the directory
        for filename in os.listdir(full_dir_path):
            if filename.lower().endswith('.zip') and not re.search(regex, filename):
                # Move file to 'zip' directory
                shutil.move(os.path.join(full_dir_path, filename), os.path.join(zip_folder, filename))

# Check each directory in the parent path
for dirname in os.listdir(parent_path):
    match = re.search(regex, dirname)
    if match:
        parent_subdirs.append(os.path.join(parent_path, dirname))
        
        # Extract the six-digit number and rearrange the digits
        six_digit_num = match.group()
        original_dates.append(six_digit_num)
        inv_date = six_digit_num[2:] + six_digit_num[:2]
        inv_dates.append(inv_date)