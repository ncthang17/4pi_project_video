import os
import re

def rename_files_to_strict_format(folder_path):
    files = os.listdir(folder_path)
    pattern = re.compile(r'(\d+)[_\-](\d+).*?_processed_(\d+)\.png', re.IGNORECASE)

    for filename in files:
        if not filename.lower().endswith('.png'):
            continue

        match = pattern.search(filename)
        if match:
            num1, num2, num3 = match.groups()

            # Ensure exactly 2-digit for first, second, and last part
            num1 = num1.zfill(2)
            num2 = num2.zfill(2)
            num3 = num3.zfill(2)

            new_filename = f"{num1}_{num2}_processed_{num3}.png"

            if filename != new_filename:
                src = os.path.join(folder_path, filename)
                dst = os.path.join(folder_path, new_filename)

                # Avoid overwrite
                if not os.path.exists(dst):
                    os.rename(src, dst)
                    print(f"Renamed: {filename} --> {new_filename}")
                else:
                    print(f"Skipped (target exists): {new_filename}")
        else:
            print(f"Skipped (no match): {filename}")

# Usage:
# folder_path = "/Users/yourname/Downloads/folder"
# rename_files_to_strict_format(folder_path)

if __name__ == "__main__":
    folder_path = "processed_frames"
    rename_files_to_strict_format(folder_path)
