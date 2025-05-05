#!/bin/bash

# Toggle: Set to 1 to download only USA/World region files
usa_only=1

# ====== Main URLs ======
# Define an array of URLs
urls=(
 # "https://myrient.erista.me/files/No-Intro/Sega%20-%20Game%20Gear/"
 # "https://myrient.erista.me/files/No-Intro/Sega%20-%20Master%20System%20-%20Mark%20III/"
 # "https://myrient.erista.me/files/No-Intro/Sega%20-%20Mega%20Drive%20-%20Genesis/"
 # "https://myrient.erista.me/files/Redump/Sega%20-%20Dreamcast/"
 # "https://myrient.erista.me/files/Redump/Sega%20-%20Saturn/"
 # "https://myrient.erista.me/files/Redump/Sony%20-%20PlayStation/"
 # "https://myrient.erista.me/files/Redump/Sony - PlayStation - BIOS Images/"
 "https://myrient.erista.me/files/Redump/Sony%20-%20PlayStation%202/"
 "https://myrient.erista.me/files/Redump/Sony%20-%20PlayStation%202%20-%20BIOS%20Images/"
 )

# Define accept patterns if usa_only is enabled
# if [[ "$usa_only" -eq 1 ]]; then
#   accept_patterns="*USA*.*,*World*.*"
# else
#   accept_patterns=""
# fi
if [[ "$usa_only" -eq 1 ]]; then
  accept_patterns="*USA*.*"
else
  accept_patterns=""
fi

# # ====== Download Main URLs ======
# Loop over the array and download each
for url in "${urls[@]}"; do
  if [[ -n "$accept_patterns" ]]; then
    wget -m -np -c -e robots=off -R "index.html*" -A "$accept_patterns" "$url"
  else
    wget -m -np -c -e robots=off -R "index.html*" "$url"
  fi
done
