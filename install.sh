#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
Usage: ./install.sh [--dry-run]

skills/ 配下の各スキルを ~/.agents/skills/<name> へシンボリックリンクする。

  --dry-run   実行せず、予定だけ表示する
  -h, --help  このヘルプを表示する
EOF
}

dry_run=0
for arg in "$@"; do
  case "$arg" in
    --dry-run) dry_run=1 ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "不明な引数: $arg" >&2
      usage >&2
      exit 2
      ;;
  esac
done

run() {
  if [[ "$dry_run" -eq 1 ]]; then
    printf '[dry-run] '
    printf '%q ' "$@"
    printf '\n'
  else
    "$@"
  fi
}

# 都度 y/N で許可を得る（未入力は No）。dry-run では問い合わせず許可扱い。
confirm_yn() {
  local prompt="$1"
  local reply
  if [[ "$dry_run" -eq 1 ]]; then
    return 0
  fi
  if [[ ! -r /dev/tty || ! -w /dev/tty ]]; then
    echo "対話入力できません (/dev/tty)" >&2
    return 1
  fi
  while true; do
    printf '%s [y/N] ' "$prompt" >/dev/tty
    if ! read -r reply </dev/tty; then
      printf '\n' >/dev/tty
      return 1
    fi
    case "$reply" in
      y|Y) return 0 ;;
      n|N|'') return 1 ;;
    esac
  done
}

prune_if_confirmed() {
  local dest="$1"
  local name="$2"
  local current="$3"

  echo "prune $name  (ソースがありません: $current)"
  if confirm_yn "  削除しますか?"; then
    run rm "$dest"
    linked=$((linked + 1))
  else
    echo "skip  $name  (削除をキャンセル)"
    skipped=$((skipped + 1))
  fi
}

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
skills_dir="$repo_root/skills"
dest_dir="${HOME}/.agents/skills"

if [[ ! -d "$skills_dir" ]]; then
  echo "skills ディレクトリが見つかりません: $skills_dir" >&2
  exit 1
fi

run mkdir -p "$dest_dir"

# 相対リンクも含め、リンク先を絶対パスに正規化する
resolve_symlink() {
  local link="$1"
  local target dir resolved
  target="$(readlink "$link")"
  if [[ "$target" == /* ]]; then
    printf '%s\n' "$target"
    return 0
  fi
  dir="$(cd "$(dirname "$link")" && pwd)"
  if resolved="$(cd "$dir" && cd "$(dirname "$target")" && pwd)"; then
    printf '%s\n' "$resolved/$(basename "$target")"
    return 0
  fi
  printf '%s\n' "$dir/$target"
}

is_under_skills_dir() {
  local path="$1"
  [[ "$path" == "$skills_dir"/* ]]
}

linked=0
skipped=0
failed=0

shopt -s nullglob
for src in "$skills_dir"/*/; do
  src="${src%/}"
  name="$(basename "$src")"
  dest="$dest_dir/$name"

  if [[ ! -f "$src/SKILL.md" ]]; then
    echo "skip  $name  (SKILL.md がありません)"
    skipped=$((skipped + 1))
    continue
  fi

  if [[ -e "$dest" || -L "$dest" ]]; then
    if [[ -L "$dest" ]]; then
      current_raw="$(readlink "$dest")"
      # -e はリンクを辿る。ソースが無い壊れたリンクは張り替える
      if [[ ! -e "$dest" ]]; then
        echo "update $name  (ソースなし: $current_raw -> $src)"
        run ln -sfn "$src" "$dest"
        linked=$((linked + 1))
        continue
      fi
      current="$(resolve_symlink "$dest")"
      if [[ "$current_raw" == "$src" ]]; then
        echo "ok    $name  (既にリンク済み)"
        skipped=$((skipped + 1))
        continue
      fi
      if [[ "$current" == "$src" ]] || is_under_skills_dir "$current"; then
        echo "update $name  ($current_raw -> $src)"
        run ln -sfn "$src" "$dest"
        linked=$((linked + 1))
        continue
      fi
      echo "skip  $name  (別のリンク先です: $current_raw)" >&2
      skipped=$((skipped + 1))
      failed=$((failed + 1))
      continue
    fi

    echo "skip  $name  (実体が既に存在します: $dest)" >&2
    skipped=$((skipped + 1))
    failed=$((failed + 1))
    continue
  fi

  echo "link  $name  -> $src"
  if confirm_yn "  作成しますか?"; then
    run ln -sfn "$src" "$dest"
    linked=$((linked + 1))
  else
    echo "skip  $name  (作成をキャンセル)"
    skipped=$((skipped + 1))
  fi
done

# ソースが無い壊れたリンクと、このリポジトリ由来で skills/ から消えたリンクを外す
for dest in "$dest_dir"/*; do
  [[ -L "$dest" ]] || continue
  name="$(basename "$dest")"
  current_raw="$(readlink "$dest")"

  # -e はリンクを辿る。ソースが無いことが確認できたリンクは、許可を得て削除する
  if [[ ! -e "$dest" ]]; then
    prune_if_confirmed "$dest" "$name" "$current_raw"
    continue
  fi

  current="$(resolve_symlink "$dest")"
  is_under_skills_dir "$current" || continue
  src="$skills_dir/$name"
  if [[ -d "$src" && -f "$src/SKILL.md" ]]; then
    continue
  fi
  prune_if_confirmed "$dest" "$name" "$current"
done

echo
echo "done. linked/updated/pruned=${linked} skipped=${skipped} conflicts=${failed}"
if [[ "$failed" -gt 0 ]]; then
  exit 1
fi
