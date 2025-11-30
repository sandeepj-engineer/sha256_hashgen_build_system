import os
import shutil
import subprocess
import sys
import multiprocessing
import re

# --- Paths ---
root = os.path.dirname(os.path.abspath(__file__))
build_root = os.path.join(root, "_builds")
build_dir = os.path.join(build_root, "_cmake")
bin_dir = os.path.join(build_root, "_bin")
log_dir = os.path.join(build_root, "_logs")
out_dir = os.path.join(build_root, "_out")
log_file = os.path.join(log_dir, "build.log")

# --- Default cores (all available) ---
num_cores = multiprocessing.cpu_count()
clean_requested = False
only_clean_requested = False

# --- Parse CLI arguments ---
for arg in sys.argv[1:]:
    arg_lower = arg.lower()
    if arg_lower == "clean":
        clean_requested = True
    elif arg_lower == "--only-clean":
        only_clean_requested = True
    elif re.match(r"-j\d+", arg):
        num_cores = int(arg[2:])

# --- Clean function ---
def clean_builds():
    print("******************************Cleaning _builds folder except _out******************************")
    for folder in [build_dir, bin_dir, log_dir]:
        if os.path.exists(folder):
            shutil.rmtree(folder)
            print(f"Removed: {folder}")
        else:
            print(f"Folder does not exist: {folder}")

# --- Only clean requested ---
if only_clean_requested:
    clean_builds()
    print("Only clean requested. Exiting.")
    sys.exit(0)

# --- Clean + build if clean requested ---
if clean_requested:
    clean_builds()

print(f"Using {num_cores} cores for parallel build\n")

# --- Create necessary folders ---
for path in [build_dir, bin_dir, log_dir]:
    os.makedirs(path, exist_ok=True)

# --- Commands ---
cmake_cmd = f'cmake -G "MinGW Makefiles" -S "{root}" -B "{build_dir}" -DCMAKE_RUNTIME_OUTPUT_DIRECTORY="{bin_dir}"'
make_cmd = f'mingw32-make -C "{build_dir}" -j {num_cores}'

# --- Run command and log ---
def run_and_log(cmd):
    with open(log_file, "a") as log:
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, shell=True)
        for line in proc.stdout:
            print(line, end="")
            log.write(line)
        proc.wait()
        if proc.returncode != 0:
            print(f"Command failed: {cmd}")
            sys.exit(proc.returncode)

# --- Build Flow ---
print("******************************Configuring CMake******************************")
run_and_log(cmake_cmd)

print("\n******************************Building project******************************\n")
run_and_log(make_cmd)

print("\nBuild complete!")
print(f"Binaries in: {bin_dir}")
print(f"Logs in: {log_file}")
print(f"CMake artifacts in: {build_dir}")
print(f"Source folder remains: {out_dir}")
