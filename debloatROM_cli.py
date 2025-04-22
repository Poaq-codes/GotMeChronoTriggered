import os
import re
import argparse
from collections import defaultdict

# === CONFIG ===
base_dir = "games"
log_file_path = "deletion_log.txt"

region_priority_1 = {"usa", "world"}
region_priority_2 = {"eu", "europe"}
variant_keywords = ("rev", "v", "beta")
paren_pattern = re.compile(r"\(([^)]+)\)")

# === ARGPARSE SETUP ===
parser = argparse.ArgumentParser(description="Deduplicate ZIP files by region priority.")
parser.add_argument("dirs", nargs="*", help="Subdirectories to scan. If none given, all subdirectories in 'games/' will be used.")
group = parser.add_mutually_exclusive_group()
group.add_argument("--usa-only", action="store_true", help="Only keep files with USA or World region (plus variants).")
group.add_argument("--usa-or-eu", action="store_true", help="Only keep files with USA, World, EU, or Europe regions (plus variants).")
parser.add_argument("--delete", action="store_true", help="Actually delete files (default is dry run).")
args = parser.parse_args()

dry_run = not args.delete

# === SAFETY PROMPT IF --delete IS USED ===
if args.delete:
    confirm = input("\nYou are about to permanently delete files from disk.\nAre you sure you want to continue? (yes/no): ").strip().lower()
    if confirm != "yes":
        print("Aborting. No files were deleted.")
        exit(0)

# === RESOLVE TARGET DIRECTORIES ===
if args.dirs:
    target_dirs = args.dirs
else:
    target_dirs = [
        os.path.join(base_dir, d)
        for d in os.listdir(base_dir)
        if os.path.isdir(os.path.join(base_dir, d))
    ]

# === STATS ===
total_files = 0
deleted_files = 0
kept_files_set = set()

# === OPEN LOG FILE ===
log_mode = "w"
with open(log_file_path, log_mode, encoding="utf-8") as log_file:

    # === GROUP FILES BY BASENAME ===
    file_groups = defaultdict(list)

    for dir_path in target_dirs:
        for root, _, files in os.walk(dir_path):
            for file in files:
                if not file.lower().endswith(".zip"):
                    continue

                matches = paren_pattern.findall(file)
                if not matches:
                    continue  # Skip files with no (…)

                basename_key = file.split('(')[0].strip().lower()
                region_raw = matches[0].strip().lower()
                additional_tags = matches[1:]

                is_variant = any(tag.strip().lower().startswith(variant_keywords) for tag in additional_tags)
                regions = [r.strip().lower() for r in region_raw.split(",")]

                full_path = os.path.join(root, file)
                file_groups[basename_key].append((full_path, regions, is_variant))

    # === EVALUATE KEEP/DELETE ===
    for basename_key, file_list in file_groups.items():
        if len(file_list) == 1:
            path, regions, _ = file_list[0]
            total_files += 1

            if args.usa_only:
                if any(r in region_priority_1 for r in regions):
                    kept_files_set.add(path)
                else:
                    deleted_files += 1
                    if dry_run:
                        print(f"[DRY RUN] Would delete: {path}")
                        log_file.write(f"[DRY RUN] Would delete: {path}\n")
                    else:
                        os.remove(path)
                        print(f"Deleted: {path}")
                        log_file.write(f"Deleted: {path}\n")
                continue

            if args.usa_or_eu:
                if any(r in region_priority_1 | region_priority_2 for r in regions):
                    kept_files_set.add(path)
                else:
                    deleted_files += 1
                    if dry_run:
                        print(f"[DRY RUN] Would delete: {path}")
                        log_file.write(f"[DRY RUN] Would delete: {path}\n")
                    else:
                        os.remove(path)
                        print(f"Deleted: {path}")
                        log_file.write(f"Deleted: {path}\n")
                continue

            kept_files_set.add(path)
            continue

        keep_paths = []

        if args.usa_only:
            for path, regions, is_variant in file_list:
                if any(r in region_priority_1 for r in regions):
                    keep_paths.append(path)

        elif args.usa_or_eu:
            for path, regions, is_variant in file_list:
                if any(r in region_priority_1 | region_priority_2 for r in regions):
                    keep_paths.append(path)

        else:
            for path, regions, is_variant in file_list:
                if is_variant:
                    keep_paths.append(path)

            for path, regions, _ in file_list:
                if path in keep_paths:
                    continue
                if any(r in region_priority_1 for r in regions):
                    keep_paths.append(path)

            if not keep_paths:
                for path, regions, _ in file_list:
                    if any(r in region_priority_2 for r in regions):
                        keep_paths.append(path)
                        break

            if not keep_paths:
                keep_paths.append(file_list[0][0])

        for path, _, _ in file_list:
            total_files += 1
            if path in keep_paths:
                kept_files_set.add(path)
            else:
                deleted_files += 1
                if dry_run:
                    print(f"[DRY RUN] Would delete: {path}")
                    log_file.write(f"[DRY RUN] Would delete: {path}\n")
                else:
                    os.remove(path)
                    print(f"Deleted: {path}")
                    log_file.write(f"Deleted: {path}\n")

# === PRINT SUMMARY ===
print("\nSummary:")
print(f"  Total ZIP files scanned: {total_files}")
print(f"  Files kept:              {len(kept_files_set)}")
print(f"  Files {'to delete' if dry_run else 'deleted'}:    {deleted_files}")
print(f"  Log written to:          {log_file_path}")
