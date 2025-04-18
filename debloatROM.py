import os
import re
from collections import defaultdict

games_dir = "test" # Set to your top level directory name
dry_run = True  # Set to False to actually delete files

# Priority tiers
region_priority_1 = {"usa", "world"}
region_priority_2 = {"eu", "europe"}

# Keywords that define a variant (case-insensitive)
variant_keywords = ("rev", "v", "beta")

# Regex to match all parenthesis groups in filenames
paren_pattern = re.compile(r"\(([^)]+)\)")

# Dictionary: basename → list of (path, regions, is_variant)
file_groups = defaultdict(list)

# Step 1: Walk the directory and group files by basename
for root, _, files in os.walk(games_dir):
    for file in files:
        if not file.lower().endswith(".zip"):
            continue

        matches = paren_pattern.findall(file)
        if not matches:
            continue  # Skip files with no (something)

        basename_key = file.split('(')[0].strip().lower()
        region_raw = matches[0].strip().lower()
        additional_tags = matches[1:]

        # Check if any other parenthesis contains a variant keyword
        is_variant = any(tag.strip().lower().startswith(variant_keywords) for tag in additional_tags)

        # Support multiple regions like (USA, Europe)
        regions = [r.strip().lower() for r in region_raw.split(",")]

        full_path = os.path.join(root, file)
        file_groups[basename_key].append((full_path, regions, is_variant))

# Step 2: Decide what to keep/delete
for basename_key, file_list in file_groups.items():
    if len(file_list) == 1:
        continue  # Only one file, keep

    keep_paths = []

    # Step 1: Keep all variant files
    for path, regions, is_variant in file_list:
        if is_variant:
            keep_paths.append(path)

    # Step 2: Keep all Tier 1 matches (USA/World)
    for path, regions, is_variant in file_list:
        if path in keep_paths:
            continue
        if any(r in region_priority_1 for r in regions):
            keep_paths.append(path)

    # Step 3: If no Tier 1 or variants kept, keep one Tier 2 (EU/Europe)
    if not keep_paths:
        for path, regions, _ in file_list:
            if any(r in region_priority_2 for r in regions):
                keep_paths.append(path)
                break

    # Step 4: Still nothing? Keep one arbitrary file
    if not keep_paths:
        keep_paths.append(file_list[0][0])

    # Step 5: Delete everything else
    for path, _, _ in file_list:
        if path not in keep_paths:
            if dry_run:
                print(f"[DRY RUN] Would delete: {path}")
            else:
                os.remove(path)
                print(f"Deleted: {path}")
