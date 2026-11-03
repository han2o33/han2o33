#!/usr/bin/env bash
# 나눔명조/나눔고딕 폰트를 tools/fonts/ 에 내려받는다 (google/fonts 저장소, OFL).
set -e
cd "$(dirname "$0")" && mkdir -p fonts && cd fonts
for p in nanummyeongjo/NanumMyeongjo-Regular nanummyeongjo/NanumMyeongjo-Bold nanummyeongjo/NanumMyeongjo-ExtraBold nanumgothic/NanumGothic-Regular nanumgothic/NanumGothic-Bold; do
  curl -sSfL -o "$(basename $p).ttf" "https://raw.githubusercontent.com/google/fonts/main/ofl/$p.ttf"
done
ls
