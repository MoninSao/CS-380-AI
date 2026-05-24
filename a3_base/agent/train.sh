#!/usr/bin/env bash
# Progressive Q-learning training regimen for Frogger.
# Run from the project root:  bash agent/train.sh
# Optionally override the Python interpreter:  PYTHON=python3 bash agent/train.sh

set -euo pipefail

PYTHON="${PYTHON:-python3}"
SCRIPT="main.py"
PLAYER="agent"
TRAIN="q"
SCREEN="medium"

echo "=== Starting progressive training ==="

# restart=1 — frog restarts from row 1 above start; 500 steps to learn the road
echo "[1/8] restart=1, steps=500"
"$PYTHON" "$SCRIPT" --player="$PLAYER" --train="$TRAIN" --screen="$SCREEN" \
    --restart=1 --steps=500 --output=text

# restart=2 — two rows of freedom; 1000 steps
echo "[2/8] restart=2, steps=1000"
"$PYTHON" "$SCRIPT" --player="$PLAYER" --train="$TRAIN" --screen="$SCREEN" \
    --restart=2 --steps=1000 --output=text

# restart=3
echo "[3/8] restart=3, steps=1500"
"$PYTHON" "$SCRIPT" --player="$PLAYER" --train="$TRAIN" --screen="$SCREEN" \
    --restart=3 --steps=1500 --output=text

# restart=4
echo "[4/8] restart=4, steps=2000"
"$PYTHON" "$SCRIPT" --player="$PLAYER" --train="$TRAIN" --screen="$SCREEN" \
    --restart=4 --steps=2000 --output=text

# restart=5
echo "[5/8] restart=5, steps=2500"
"$PYTHON" "$SCRIPT" --player="$PLAYER" --train="$TRAIN" --screen="$SCREEN" \
    --restart=5 --steps=2500 --output=text

# restart=6
echo "[6/8] restart=6, steps=3000"
"$PYTHON" "$SCRIPT" --player="$PLAYER" --train="$TRAIN" --screen="$SCREEN" \
    --restart=6 --steps=3000 --output=text

# restart=7
echo "[7/8] restart=7, steps=3500"
"$PYTHON" "$SCRIPT" --player="$PLAYER" --train="$TRAIN" --screen="$SCREEN" \
    --restart=7 --steps=3500 --output=text

# restart=8 — full board; 5000 steps to consolidate
echo "[8/8] restart=8 (full board), steps=5000"
"$PYTHON" "$SCRIPT" --player="$PLAYER" --train="$TRAIN" --screen="$SCREEN" \
    --restart=8 --steps=5000 --output=text

echo "=== Training complete. Q-table saved to agent/train/${TRAIN}.json ==="
