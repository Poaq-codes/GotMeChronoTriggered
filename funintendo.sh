#!/bin/bash

# Define an array of URLs
urls=(
  "https://myrient.erista.me/files/No-Intro/Nintendo%20-%20Nintendo%20Entertainment%20System%20%28Headered%29/"
  "https://myrient.erista.me/files/No-Intro/Nintendo%20-%20Super%20Nintendo%20Entertainment%20System/"
  "https://myrient.erista.me/files/No-Intro/Nintendo%20-%20Nintendo%20DS%20%28Decrypted%29/"
  "https://myrient.erista.me/files/No-Intro/Nintendo%20-%20Nintendo%2064%20(BigEndian)/"
  "https://myrient.erista.me/files/No-Intro/Nintendo%20-%20Nintendo%203DS%20%28Decrypted%29/"
  "https://myrient.erista.me/files/No-Intro/Nintendo%20-%20New%20Nintendo%203DS%20%28Decrypted%29/"
  "https://myrient.erista.me/files/No-Intro/Nintendo%20-%20Game%20Boy%20Advance/"
  "https://myrient.erista.me/files/No-Intro/Nintendo%20-%20Game%20Boy%20Color/"
  "https://myrient.erista.me/files/Redump/Nintendo%20-%20GameCube%20-%20NKit%20RVZ%20%5Bzstd-19-128k%5D/"
  #"https://myrient.erista.me/files/No-Intro/Nintendo%20-%20Wii%20%28Digital%29%20%28CDN%29/" # this only contain Wiiware files and virtual console in chunks
  "https://myrient.erista.me/files/Redump/Nintendo%20-%20Wii%20-%20NKit%20RVZ%20%5Bzstd-19-128k%5D/" # actual Wii games
  #"https://myrient.erista.me/files/No-Intro/Nintendo%20-%20Wii%20U%20%28Digital%29%20%28CDN%29/" # odd, virtual console things
  "https://myrient.erista.me/files/Redump/Nintendo%20-%20Wii%20U%20-%20WUX/" # better one from redump
  "https://myrient.erista.me/files/Redump/Nintendo%20-%20Wii%20U%20-%20Disc%20Keys/" # disc keys for Wii U WUX files
)

# Loop over the array and download each
for url in "${urls[@]}"; do
  wget -m -np -c -e robots=off -R "index.html*" "$url"
done

# Get Wiiware and virtual console
# exclude _Clean/ and _Dangerous/
wget -m -c -np -nH -R "index.html*" \
     --reject-regex "/_[^/]+/" \
     -e robots=off \
     "https://repo.mariocube.com/WADs/_WiiWare,%20VC,%20DLC,%20Channels%20&%20IOS/"
